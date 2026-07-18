#!/usr/bin/env python3
"""OLSK60 操作マニュアル用キー配置図ジェネレータ。

layouts/*.yaml（表示レイアウト＋ハードウェア注記）と diagrams/*.yaml（図スペック）
から、docs/images/ の既存図と同一様式の SVG を生成する。

使い方:
    python3 generate.py diagrams/piano-mode.yaml            # SVG を標準の出力先へ
    python3 generate.py diagrams/piano-mode.yaml --png      # PNG (2x) も描画
    python3 generate.py diagrams/piano-mode.yaml -o /tmp/x  # 出力先を指定

PNG 描画には Playwright(Node) と Chromium、および fetch_fonts.py で取得した
Noto Sans JP ウェブフォントが必要（詳細は README.md）。
"""
import argparse
import os
import subprocess
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.normpath(os.path.join(HERE, '..', '..', 'docs', 'images'))

UNIT = 60          # 1u = 60px
KEY_INSET = 3      # セル内オフセット
KEY_SIZE = 54      # 1u キーの矩形辺長
FONT_STACK = "'Noto Sans CJK JP','Noto Sans JP','Hiragino Sans','Yu Gothic UI',sans-serif"

# 既存図から抽出した配色・寸法の定数
STYLES = {
    'normal':   {'fill': '#ffffff', 'stroke': '#c3c9cf', 'label': '#212529', 'sub': '#868e96'},
    'mod':      {'fill': '#e9ecef', 'stroke': '#b4bbc2', 'label': '#212529', 'sub': '#868e96'},
    'disabled': {'fill': '#fbfcfc', 'stroke': '#e3e7ea', 'label': '#b6bcc2', 'sub': '#ccd1d6'},
}

CANVAS_W, CANVAS_H = 968, 500
BOARD_TX, BOARD_TY = 34, 70
FRAME = {'x': -14, 'y': -14, 'w': 928.0, 'h': 328}

DEFS = ('<defs><marker id="arr" markerWidth="7" markerHeight="7" refX="5" refY="3.5" '
        'orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#868e96"/></marker></defs>')


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def num(v):
    """既存図の数値表記を踏襲: 計算値の float はそのまま str()、int は整数表記。"""
    if isinstance(v, float) and v == int(v):
        return f'{v:.1f}'
    return str(v)


def baseline_offset(font_size):
    """フォントサイズ→中央揃えのベースライン補正（既存図の実測則）。"""
    return round(font_size * 4 / 11, 1)


def cjk_count(s):
    return sum(1 for ch in s if ord(ch) > 0x2E7F)


class Renderer:
    def __init__(self):
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, rx, fill, stroke, sw):
        rx_attr = f' rx="{num(rx)}"' if rx else ''
        self.add(f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}"'
                 f'{rx_attr} fill="{fill}" stroke="{stroke}" stroke-width="{num(sw)}"/>')

    def text(self, x, y, size, fill, s, weight=None, anchor=None):
        w = f' font-weight="{weight}"' if weight else ''
        a = f' text-anchor="{anchor}"' if anchor else ''
        self.add(f'<text x="{num(x)}" y="{num(y)}" font-size="{num(size)}" fill="{fill}"{w}{a}>{esc(s)}</text>')


def key_style(layout_key, override, diagram):
    """キーの描画スタイル（fill/stroke/文字色）を決める。"""
    styles = dict(STYLES)
    styles.update(diagram.get('styles', {}) or {})
    if override and 'style' in override:
        st = styles[override['style']]
        return {'fill': st['fill'], 'stroke': st['stroke'],
                'label': st.get('label', '#212529'), 'sub': st.get('sub', '#868e96')}
    default = diagram.get('defaults', 'base')
    if default == 'disabled' and not override:
        return dict(STYLES['disabled'])
    # base: レイアウト定義の配色（機能キー色 > mod > normal）
    if layout_key.get('fill'):
        return {'fill': layout_key['fill'], 'stroke': layout_key['stroke'],
                'label': '#212529', 'sub': '#868e96'}
    base = STYLES['mod'] if layout_key.get('mod') else STYLES['normal']
    return dict(base)


def render_key(r, lk, override, diagram):
    px = float(round(KEY_INSET + UNIT * lk['x'], 1))
    py = float(round(KEY_INSET + UNIT * lk['y'], 1))
    pw = float(round(UNIT * lk.get('w', 1) - 2 * KEY_INSET, 1))
    st = key_style(lk, override, diagram)
    r.rect(px, py, pw, float(KEY_SIZE), 7, st['fill'], st['stroke'], 1.5)

    ov = override or {}
    label = ov.get('label', lk.get('label'))
    lines = ov.get('lines')
    if 'sub' in ov:
        sub = ov['sub']
    elif 'label' in ov or 'lines' in ov:
        sub = None  # キーの意味を差し替えたら元のシフト刻印は出さない
    else:
        sub = lk.get('sub')
    size = ov.get('size', lk.get('size', 13))
    cx = round(px + pw / 2, 1)

    if sub is not None:
        r.text(cx, round(py + 13, 1), 9.5, st['sub'], sub, anchor='middle')
    if lines:
        off = baseline_offset(11)
        r.text(cx, round(py + 20.5 + off, 1), 11.0, st['label'], lines[0], weight=600, anchor='middle')
        r.text(cx, round(py + 33.5 + off, 1), 11.0, st['label'], lines[1], weight=600, anchor='middle')
    elif label is not None:
        base = 30 if sub is not None else 27
        r.text(cx, round(py + base + baseline_offset(size), 1), float(size), st['label'], label,
               weight=600, anchor='middle')


def render(layout, diagram):
    r = Renderer()
    r.add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
          f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="{FONT_STACK}">')
    r.add(DEFS)
    r.add(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" fill="#ffffff"/>')

    # ヘッダ: バッジ・タイトル・右上注記・LED
    badge = diagram['badge']
    r.add(f'<rect x="20" y="14" width="86" height="26" rx="13" fill="{badge["color"]}"/>')
    r.text(63, 32, 13, '#ffffff', badge['text'], weight=700, anchor='middle')
    r.text(118, 33, 18, '#212529', diagram['title'], weight=700)
    if diagram.get('note'):
        r.text(948, 24, 11.5, '#495057', diagram['note'], anchor='end')
    led = diagram.get('led')
    if led:
        led_text = 'LED: ' + led['text']
        cx = round(902.12 - 11 * cjk_count(led['text']), 2)
        r.add(f'<circle cx="{cx}" cy="36" r="5" fill="{led.get("color", badge["color"])}" stroke="#adb5bd"/>')
        r.text(948, 40, 11.5, '#495057', led_text, anchor='end')

    # キー盤面
    r.add(f'<g transform="translate({BOARD_TX},{BOARD_TY})">')
    r.rect(FRAME['x'], FRAME['y'], FRAME['w'], FRAME['h'], 12, '#f1f3f5', '#dee2e6', 1.5)
    overrides = diagram.get('keys', {}) or {}
    unknown = set(overrides) - {k['id'] for k in layout['keys']}
    if unknown:
        raise SystemExit(f'diagram references unknown key ids: {sorted(unknown)}')
    for lk in layout['keys']:
        render_key(r, lk, overrides.get(lk['id']), diagram)

    tp = (layout.get('hardware') or {}).get('trackpoint')
    if tp and not diagram.get('hide_trackpoint'):
        r.add(f'<circle cx="{num(tp["cx"])}" cy="{num(tp["cy"])}" r="18.0" fill="#d64545" '
              f'stroke="#a02828" stroke-width="2"/>')
        r.add(f'<circle cx="{num(tp["cx"])}" cy="{num(tp["cy"])}" r="9.9" fill="none" '
              f'stroke="#e88f8f" stroke-width="1.5" stroke-dasharray="2,3"/>')
        r.add(f'<text x="{num(tp["cx"])}" y="{num(round(tp["cy"] + 32, 1))}" font-size="9.5" '
              f'fill="#a02828" text-anchor="middle" font-weight="600">{esc(tp["label"])}</text>')
    r.add('</g>')

    # ロータリーエンコーダブロック
    enc = diagram.get('encoder')
    if enc and (layout.get('hardware') or {}).get('encoder'):
        r.text(20, 406, 11, '#868e96', 'ロータリーエンコーダ（オプション）', weight=700)
        r.add('<circle cx="44" cy="440" r="15" fill="#e9ecef" stroke="#868e96" stroke-width="2"/>')
        r.add('<circle cx="44" cy="440" r="4.5" fill="#adb5bd"/>')
        r.add('<line x1="44" y1="425" x2="44" y2="431" stroke="#868e96" stroke-width="2"/>')
        r.add('<path d="M 23 444 a 21 21 0 0 1 6 -14" fill="none" stroke="#868e96" '
              'stroke-width="1.6" marker-end="url(#arr)"/>')
        for i, line in enumerate(enc['lines'][:3]):
            r.text(71, 428 + 15 * i, 10.5, '#495057', line)
        if enc.get('footnote'):
            r.text(20, 474, 9.5, '#adb5bd', enc['footnote'])

    # 凡例
    styles = dict(STYLES)
    styles.update(diagram.get('styles', {}) or {})
    for item in diagram.get('legend', []) or []:
        y = 438 if item.get('row', 1) == 2 else 416
        x = item['x']
        tx = x
        if 'style' in item:
            st = styles[item['style']]
            r.rect(x, y, 14, 13, 3, st['fill'], st['stroke'], 1.2)
            tx = x + 19
        r.text(tx, y + 11, 10.5, '#495057', item['text'])

    r.add('</svg>')
    return ''.join(r.parts)


def render_png(svg_path, png_path):
    subprocess.run(['node', os.path.join(HERE, 'render_png.mjs'), svg_path, png_path],
                   check=True)
    rgba_to_rgb(png_path)


def rgba_to_rgb(path):
    """PNG を既存画像と同じ 8-bit RGB 非インターレースに正規化する（標準ライブラリのみ）。"""
    import struct
    import zlib
    data = open(path, 'rb').read()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    pos, ihdr, idat = 8, None, b''
    while pos < len(data):
        ln = struct.unpack('>I', data[pos:pos + 4])[0]
        typ = data[pos + 4:pos + 8]
        if typ == b'IHDR':
            ihdr = data[pos + 8:pos + 8 + ln]
        elif typ == b'IDAT':
            idat += data[pos + 8:pos + 8 + ln]
        pos += 12 + ln
    w, h, depth, ctype, _, _, inter = struct.unpack('>IIBBBBB', ihdr)
    if ctype == 2:
        return
    assert (depth, ctype, inter) == (8, 6, 0), f'unexpected PNG format {depth}/{ctype}/{inter}'
    raw = zlib.decompress(idat)
    stride, prev, out = w * 4 + 1, bytearray(w * 4), bytearray()
    for yrow in range(h):
        f = raw[yrow * stride]
        line = bytearray(raw[yrow * stride + 1:(yrow + 1) * stride])
        for i in range(len(line)):
            a = line[i - 4] if i >= 4 else 0
            b = prev[i]
            c = prev[i - 4] if i >= 4 else 0
            if f == 1:
                line[i] = (line[i] + a) & 255
            elif f == 2:
                line[i] = (line[i] + b) & 255
            elif f == 3:
                line[i] = (line[i] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[i] = (line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        prev = line
        out.append(0)
        for xcol in range(w):
            out += line[xcol * 4:xcol * 4 + 3]

    def chunk(t, b):
        return struct.pack('>I', len(b)) + t + b + struct.pack('>I', zlib.crc32(t + b) & 0xffffffff)

    new = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(bytes(out), 9))
           + chunk(b'IEND', b''))
    open(path, 'wb').write(new)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('diagram', help='diagrams/*.yaml')
    ap.add_argument('-o', '--outdir', default=DEFAULT_OUT)
    ap.add_argument('--png', action='store_true', help='PNG (2x) も描画する')
    args = ap.parse_args()

    diagram = yaml.safe_load(open(args.diagram))
    layout_path = os.path.join(HERE, 'layouts', diagram['layout'] + '.yaml')
    layout = yaml.safe_load(open(layout_path))

    name = diagram.get('output', os.path.splitext(os.path.basename(args.diagram))[0])
    svg_path = os.path.join(args.outdir, name + '.svg')
    svg = render(layout, diagram)
    with open(svg_path, 'w') as fh:
        fh.write(svg)
    print('wrote', svg_path)

    if args.png:
        png_path = os.path.join(args.outdir, name + '.png')
        render_png(svg_path, png_path)
        print('wrote', png_path)


if __name__ == '__main__':
    main()
