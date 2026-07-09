# OLSK60 v2
60% OrthoLinear Keyboard w/ TrackPoint – Designed for Standard Keycap Compatibility

![OLSK60 v2 キーボード外観写真](https://github.com/user-attachments/assets/2aa9d79e-fb0d-4367-8551-9987699a8846)

## 概要
OLSK60 v2は、標準的なキーキャップセットに対応した、60%サイズの格子配列キーボードです。  
トラックポイントを搭載しているため、マウス操作もこの一台で完結します。  
また、GH60互換ケースに対応しており、お好みのキーキャップやケースと自由に組み合わせて、自分だけのカスタマイズを楽しめます。  
見た目も使い心地も、あなた好みに仕上げてください。

> **モデルについて:** 現在販売中のモデルは **v2.1** です。出荷時は **5-Split Space** レイアウトで、同梱のトッププレートに付け替えることで 3-Split Space／6.25U Space にも変更できます。旧モデル **v2** は 3-Split Space および 6.25U Space のみに対応しています。

### 主な特徴
- 格子配列60キー
- トラックポイント搭載
- GH60互換ケース対応
- Remap / VIA / Vial（Pipette）対応
- 5-Split Space レイアウトで出荷（VIA/Vialで他レイアウトに変更可能）
- ホットスワップスイッチソケット採用
- スタビライザー実装済み

### 仕様

| 項目 | 内容 |
|------|------|
| 配列 | 直交（格子）配列 60キー、60%サイズ |
| 接続 | USB Type-C |
| MCU | RP2040（UF2 形式でファームウェア書き込み） |
| キーマップ | 4レイヤー、設定ツール（Remap / VIA / Vial）で編集可能 |
| ポインティングデバイス | トラックポイント（押し下げクリック対応、オートマウスレイヤー機能） |
| ロータリーエンコーダ | オプション（右上に取り付け可能） |
| LED インジケーター | 1個（レイヤー・設定状態を色で表示） |
| スイッチ | ホットスワップソケット（MX互換） |
| ケース | GH60 互換 |
| キーキャップ | 標準的なキーキャップセットに対応 |

### 出荷時のキー配列（レイヤー0）

![OLSK60 レイヤー0（基本レイヤー）のキー配列図](docs/images/layer0-base.svg)

レイヤー構成の詳細は[キーボード操作ガイド](docs/OLSK60_user_guide.md)をご参照ください。

## ドキュメント

> **初めての方へ:** キットを購入された方は、ビルドガイド → キーボード操作ガイド の順にお読みください。

- [ビルドガイド](docs/buildguide.md) — キットの組み立て手順
- [キーボード操作ガイド](docs/OLSK60_user_guide.md) — レイヤー構成・各機能の使い方
- [マウス機能操作マニュアル](docs/OLSK60_mouse_manual.md) — トラックポイントの速度を自分好みに調整する方法
- [FAQ（よくある質問）](docs/faq.md) — モデルの見分け方・設定ツールの選び方など
- [3Dデータ](cad/)
  - [トラックポイントカバー](cad/trackpoint-cover/) - カスタマイズ用のSTEP/STLファイル

## ファームウェア
コンパイル済みファームウェアおよび更新手順は [`firmware/README.md`](firmware/README.md) にて公開しています。

- **2026年6月までにご購入の個体**には旧版ファームウェアが入っています。そのまま使う場合は **Remap** をご利用ください（更新不要）。
- **最新版に更新する場合**は、**VIA 用ファームウェア**＋VIA、または **Vial 用ファームウェア**＋Vial（**Pipette 推奨**）をご利用ください。

## 購入

[![BOOTH](https://img.shields.io/badge/BOOTH-FC4D50?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTMgM2gxOHYxOEgzVjN6bTIgMnYxNGgxNFY1SDV6bTIgMmgxMHYySDdWN3ptMCA0aDEwdjJIN3YtMnptMCA0aDEwdjJIN3YtMnoiLz48L3N2Zz4=&logoColor=white)](https://techmech.booth.pm/items/5896343)
[![遊舎工房](https://img.shields.io/badge/遊舎工房-Shop-181717?style=for-the-badge)](https://shop.yushakobo.jp/products/11324)

| 販売先 | 販売形態 | リンク |
|--------|----------|--------|
| BOOTH | Techmech keys 直営オンラインショップ | [商品ページ](https://techmech.booth.pm/items/5896343) |
| 遊舎工房 | 委託販売（店頭 & オンライン） | [商品ページ](https://shop.yushakobo.jp/products/11324) |

商品に関するお問い合わせは、ご購入先を問わず **Techmech keys** までお願いいたします。

## ライセンス
このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。
