"""Check website resources and cross-links against a locally built public documentation site."""
from argparse import ArgumentParser
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

ROOT=Path(__file__).resolve().parents[1]
ORIGIN='https://hyloai.github.io'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.links=[];self.ids=set();self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.add(a['id'])
        for key in ['href','src','poster']:
            if a.get(key):self.links.append(a[key])

def main():
    parser=ArgumentParser();parser.add_argument('--docs',required=True,type=Path);args=parser.parse_args()
    docs=args.docs.resolve();errors=[];cache={};count=0
    def read(p):
        if p not in cache:cache[p]=Page(p.read_text())
        return cache[p]
    def resolve(path):
        decoded=unquote(path)
        root,rel=(docs,decoded.removeprefix('/hylo-docs/')) if decoded.startswith('/hylo-docs/') else (ROOT,decoded.lstrip('/'))
        p=root/rel
        if p.is_dir():p=p/'index.html'
        return p
    pages=[ROOT/'index.html',*(ROOT/'research').rglob('*.html'),*docs.rglob('*.html')]
    for p in pages:
        is_doc=p.is_relative_to(docs)
        path='/hylo-docs/'+p.relative_to(docs).as_posix() if is_doc else '/'+p.relative_to(ROOT).as_posix()
        url=ORIGIN+path.removesuffix('index.html')
        for link in read(p).links:
            parsed=urlsplit(urljoin(url,link))
            if parsed.scheme not in ('https','http') or parsed.netloc!='hyloai.github.io':continue
            # The docs checker handles doc-local links and generated redirect pages.
            if is_doc and parsed.path.startswith('/hylo-docs/'):continue
            target=resolve(parsed.path);count+=1
            if not target.is_file():errors.append(f'{path}: missing {link}');continue
            if parsed.fragment and target.suffix=='.html' and unquote(parsed.fragment) not in read(target).ids:
                errors.append(f'{path}: missing fragment {link}')
    if errors:raise SystemExit('\n'.join(sorted(set(errors))))
    print(f'Checked {count} website/resource and cross-site links across {len(pages)} pages.')
if __name__=='__main__':main()
