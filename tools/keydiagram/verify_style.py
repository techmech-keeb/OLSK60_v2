#!/usr/bin/env python3
"""様式回帰テスト: diagrams/layer0-base.yaml から SVG を再生成し、
docs/images/layer0-base.svg とバイト一致することを確認する。

ジェネレータや layouts/olsk60.yaml を変更したら必ず実行すること。
一致しなくなった場合は、既存図の様式から乖離した変更をしていないか確認する。
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REFERENCE = os.path.normpath(os.path.join(HERE, '..', '..', 'docs', 'images', 'layer0-base.svg'))


def main():
    with tempfile.TemporaryDirectory() as td:
        subprocess.run([sys.executable, os.path.join(HERE, 'generate.py'),
                        os.path.join(HERE, 'diagrams', 'layer0-base.yaml'), '-o', td],
                       check=True, stdout=subprocess.DEVNULL)
        new = open(os.path.join(td, 'layer0-base.svg'), 'rb').read()
    ref = open(REFERENCE, 'rb').read()
    if new == ref:
        print('OK: layer0-base.svg を既存図とバイト一致で再現できています')
        return 0
    print('NG: 生成結果が docs/images/layer0-base.svg と一致しません', file=sys.stderr)
    n = min(len(ref), len(new))
    for i in range(n):
        if ref[i] != new[i]:
            print(f'first diff at byte {i}:', file=sys.stderr)
            print(f'  reference: ...{ref[max(0, i - 60):i + 80]!r}...', file=sys.stderr)
            print(f'  generated: ...{new[max(0, i - 60):i + 80]!r}...', file=sys.stderr)
            break
    else:
        print(f'length differs: reference={len(ref)} generated={len(new)}', file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
