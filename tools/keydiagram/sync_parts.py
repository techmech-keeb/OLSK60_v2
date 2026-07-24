#!/usr/bin/env python3
"""図の共通部品（parts/*.svg）を各図へ複製・検証する。

GitHub 上で表示される SVG は外部ファイルを参照できない（`<use href="other.svg#id">`
が効かない）ため、共通部品は各図にインラインで複製する必要がある。
このスクリプトはマスター（parts/）を正として複製し、ズレを防ぐ。

    python3 sync_parts.py           # マスターの内容を各図へ反映
    python3 sync_parts.py --check   # ズレがないか検証のみ（CI・レビュー用）

複製先の図は、対応する部品を次のマーカーで囲んでおく:

    <!-- parts:<部品名>:begin -->
    ...（マスターからコピーされる。手で編集しない）...
    <!-- parts:<部品名>:end -->
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.normpath(os.path.join(HERE, '..', '..', 'docs', 'images'))

# 部品名 -> (マスターファイル, 複製先の図)
PARTS = {
    'mx-switch-front': (
        os.path.join(HERE, 'parts', 'mx-switch.svg'),
        ['switch-pins.svg', 'switch-mount.svg', 'build-exploded.svg'],
    ),
}


def block_re(name):
    return re.compile(
        r'(?P<begin><!-- parts:%s:begin -->)(?P<body>.*?)(?P<end><!-- parts:%s:end -->)'
        % (re.escape(name), re.escape(name)),
        re.S)


def read_master(name, path):
    m = block_re(name).search(open(path).read())
    if not m:
        raise SystemExit(f'マスターに {name} のマーカーがありません: {path}')
    return m.group('body')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true', help='書き換えず、ズレの有無だけ報告する')
    args = ap.parse_args()

    stale, synced = [], []
    for name, (master_path, targets) in PARTS.items():
        body = read_master(name, master_path)
        pattern = block_re(name)
        for target in targets:
            path = os.path.join(IMAGES, target)
            text = open(path).read()
            m = pattern.search(text)
            if not m:
                raise SystemExit(f'{target} に {name} のマーカーがありません')
            if m.group('body') == body:
                continue
            if args.check:
                stale.append(f'{target} ({name})')
                continue
            open(path, 'w').write(
                text[:m.start()] + m.group('begin') + body + m.group('end') + text[m.end():])
            synced.append(f'{target} ({name})')

    if args.check:
        if stale:
            print('NG: マスターと内容が異なる図があります:', file=sys.stderr)
            for s in stale:
                print(f'  - {s}', file=sys.stderr)
            print('  `python3 sync_parts.py` を実行して同期してください。', file=sys.stderr)
            return 1
        print('OK: すべての図がマスターと一致しています')
        return 0

    if synced:
        for s in synced:
            print('updated', s)
    else:
        print('変更なし（すべて最新）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
