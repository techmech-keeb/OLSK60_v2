<!-- from ai-agent-playbook@72f3d44 (2026-10-22): tools/claude-code/CLAUDE.md 雛形（ポインタと重大な注意だけ） -->
<!-- 確認環境: Claude Code クラウド版（パターンA）/ 2026-10-22 時点。ローカル・Codex は未確認 -->

# CLAUDE.md (OLSK60_v2)

OLSK60 v2 の**公開**リポジトリ（利用者向けの説明・ビルドガイド・ファームウェアの案内・3D データ）。
開発の正本は非公開リポジトリにある（ファームウェア: `qmk-config` / `rmk-config`、ハードウェア:
`keyboard-hardware`）。ここには利用者に見せる情報だけを置く。

## 守ること

- **公開文書の秘匿ルール**に従う: GPIO ピン番号・部品の型番・内部実装の詳細・未公開の仕様を書かない。
  正本は `qmk-config/docs/olsk60v2_docs_policy.md`（非公開リポジトリ）。本リポジトリしか無いセッションで
  迷ったら、書く前にユーザーに確認する。
- 利用者向けの日本語で書く。現行（ファームウェア v3 以降）と旧版（v2.x）の案内を混ぜない
  （`README.md` 冒頭の注記の形に合わせる）。
- 実機で確かめていない手順・動作を「確認済み」と書かない。
- ファームウェアの配布は Releases。`.uf2` をリポジトリにコミットしない。
- キー配置図（`docs/images/layer*.svg`）は `tools/keydiagram` で生成する（手で描き直さない。
  手順は `tools/keydiagram/README.md`）。
