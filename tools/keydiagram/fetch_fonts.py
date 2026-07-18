#!/usr/bin/env python3
"""PNG 描画用の Noto Sans JP ウェブフォントを Google Fonts から取得する。

fonts/ 配下（gitignore 済み）に CSS と woff2 サブセットを保存する。
SVG の生成だけならフォントは不要。PNG (--png) を描画するときに一度だけ実行する。
"""
import hashlib
import os
import re
import ssl
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, 'fonts')
CSS_URL = ('https://fonts.googleapis.com/css2'
           '?family=Noto+Sans+JP:wght@400;600;700&display=swap')
# woff2 を返させるためブラウザの User-Agent を名乗る
UA = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0 Safari/537.36')


def opener():
    handlers = []
    proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    if proxy:
        handlers.append(urllib.request.ProxyHandler({'https': proxy, 'http': proxy}))
    ca = os.environ.get('SSL_CERT_FILE') or '/root/.ccr/ca-bundle.crt'
    ctx = ssl.create_default_context(cafile=ca if os.path.exists(ca) else None)
    handlers.append(urllib.request.HTTPSHandler(context=ctx))
    return urllib.request.build_opener(*handlers)


def main():
    os.makedirs(os.path.join(FONT_DIR, 'woff2'), exist_ok=True)
    op = opener()
    req = urllib.request.Request(CSS_URL, headers={'User-Agent': UA})
    css = op.open(req, timeout=60).read().decode()
    urls = sorted(set(re.findall(r'url\((https://[^)]+)\)', css)))
    print(f'{len(urls)} woff2 subsets')
    for url in urls:
        name = hashlib.md5(url.encode()).hexdigest()[:12] + '.woff2'
        path = os.path.join(FONT_DIR, 'woff2', name)
        if not os.path.exists(path):
            with open(path, 'wb') as fh:
                fh.write(op.open(url, timeout=60).read())
        css = css.replace(url, 'woff2/' + name)
    with open(os.path.join(FONT_DIR, 'notosansjp.local.css'), 'w') as fh:
        fh.write(css)
    print('wrote', os.path.join(FONT_DIR, 'notosansjp.local.css'))


if __name__ == '__main__':
    main()
