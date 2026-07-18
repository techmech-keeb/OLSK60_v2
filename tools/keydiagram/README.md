# keydiagram — 操作マニュアル用キー配置図ジェネレータ

`docs/images/` のキー配置図（layer0-base.svg 等）と**完全に同一の様式**で
新しい図を生成するツール。データとスタイルを分離して管理する。

```text
tools/keydiagram/
├─ generate.py        # SVG ジェネレータ（要 python3 + PyYAML）
├─ render_png.mjs     # SVG → PNG(2x) レンダラ（要 Node + Playwright + Chromium）
├─ fetch_fonts.py     # PNG 描画用 Noto Sans JP ウェブフォント取得（初回のみ）
├─ verify_style.py    # 様式回帰テスト（layer0 図をバイト一致で再現できるか）
├─ layouts/
│  └─ olsk60.yaml     # 表示レイアウト（キー座標・出荷時刻印）＋ハードウェア注記
└─ diagrams/
   ├─ layer0-base.yaml   # 既存図の再現スペック（回帰テスト基準）
   └─ piano-mode.yaml    # サウンド機能・ピアノモード音階配置図
```

## 使い方

```bash
cd tools/keydiagram
python3 generate.py diagrams/piano-mode.yaml          # SVG を docs/images/ へ
python3 fetch_fonts.py                                # 初回のみ（PNG 用フォント）
python3 generate.py diagrams/piano-mode.yaml --png    # PNG (1936x1000) も生成
python3 verify_style.py                               # 様式回帰テスト
```

## データモデル

3種類の情報を分けて管理する。

1. **表示レイアウト**（`layouts/olsk60.yaml` の `keys:`）
   キーの座標（1u = 60px）・幅・出荷時の刻印。既存図から抽出し、
   `qmk-config` の `techmechkeys/olsk60/keyboard.json` と突合済み。
   分割位置（スペース分割・下段オプション）は出荷時キーキャップ構成に統合した
   「表示用」であり、物理マトリクスと 1:1 ではない点に注意。
2. **ハードウェア注記**（同ファイルの `hardware:`）
   TrackPoint マーカーやロータリーエンコーダ凡例など、
   キーマトリクスに現れない要素。
3. **図スペック**（`diagrams/*.yaml`）
   バッジ・タイトル・LED 表示・キーごとの強調/ラベル差し替え・凡例・脚注。
   キーは表示レイアウトの `id` で参照する。

### 図スペックの主な書式

```yaml
layout: olsk60                      # layouts/<name>.yaml を参照
badge: {text: サウンド, color: "#2f66c4"}
title: ピアノモード（音階配置）
note: 右上の補足テキスト
led: {text: 青}                     # 「LED: 」+ 全角テキスト（ドット位置は自動計算）
defaults: base                      # base=出荷時配色 / disabled=全キー薄灰
styles:                             # 図ローカルのキースタイル定義
  white-key: {fill: "#ffffff", stroke: "#2f66c4", label: "#212529", sub: "#868e96"}
keys:                               # id ごとの上書き
  a: {style: white-key, lines: [C4, ド], sub: A}   # lines=2行表示, sub=上部小ラベル
  enter: {style: fx-key, label: Enter, size: 11}   # label=1行表示
encoder:                            # エンコーダ凡例（最大3行＋脚注）
  lines: ["時計回り: ...", "反時計回り: ...", "..."]
  footnote: ※ ...
legend:                             # 下部凡例（row: 2 で2段目、style 省略で文字のみ）
  - {x: 340, style: white-key, text: 白鍵に相当（音階）}
```

## 様式を変えないためのルール

- ジェネレータや `layouts/olsk60.yaml` を変更したら `verify_style.py` を実行し、
  既存の `docs/images/layer0-base.svg` をバイト一致で再現できることを確認する。
- 新しい配色を増やすときは、既存図のパレット（`generate.py` の `STYLES` と
  既存 diagram の `styles:`）に馴染む色を選ぶ。

## PNG 描画の前提

- Node.js + Playwright（`npm i -g playwright` 済み環境か `npx playwright`）と
  Chromium が必要。ヘッドレス Chromium の `--screenshot` を直接使うと
  ウィンドウ枠ぶんビューポートが欠けるため、Playwright で正確な
  ビューポート（968x500, deviceScaleFactor=2）を指定している。
- 文字は Noto Sans JP。システムに無い環境向けに `fetch_fonts.py` が
  Google Fonts から woff2 を `fonts/`（gitignore 済み）へ取得し、
  レンダラが @font-face で適用する。
- 生成 PNG は既存図と同じ 1936x1000 / 8-bit RGB に正規化される。

## 将来の汎用化メモ

- 他キーボードは `layouts/<name>.yaml` を追加すれば同じ図スペック書式で使える。
  QMK の `keyboard.json`（`layouts[].layout` の x/y/w）から座標を起こし、
  1u=60px・セル内 3px オフセットで px 化する（`x_px = 3 + 60 * x_u`）。
- 既存の他の図（layer1/2/3 等）も diagram スペック化すれば再生成可能になる。
