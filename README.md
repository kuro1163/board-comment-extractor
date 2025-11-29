# 📝 掲示板コメント抽出ツール

掲示板まとめサイトからコメントを抽出して、YouTube台本形式のスプレッドシートに変換するPythonツールです。

## ✨ 特徴

- 🚀 **簡単操作**: URLを入力するだけでコメント抽出完了
- 📊 **スプレッドシート出力**: タブ区切り形式（TSV）で出力、Googleスプレッドシートに直接貼り付け可能
- 🎬 **YouTube台本形式**: 発言者とセリフの2列形式で出力
- 🔍 **自動コメント抽出**: 主要な掲示板まとめサイトの構造に対応
- 📏 **自動テキスト分割**: 長いコメントを適切な長さ（20-30字程度）に自動分割

## 🚀 クイックスタート

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/kuro1163/board-comment-extractor.git
cd board-comment-extractor

# 仮想環境を作成（推奨）
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 依存関係をインストール
pip install -r requirements.txt
```

### 使い方

#### 基本的な使い方

```bash
python extract_comments.py "https://example.com/board-summary"
```

#### 出力ファイルを指定

```bash
python extract_comments.py "https://example.com/board-summary" --output output/my_script.tsv
```

#### CSV形式で出力

```bash
python extract_comments.py "https://example.com/board-summary" --format csv
```

## 📊 出力形式

出力されるスプレッドシートは以下の形式です：

| 発言者 | セリフ |
|--------|--------|
| 匿名 | コメント内容1 |
| 匿名 | コメント内容2 |
| ID:user123 | コメント内容3 |

この形式は、既存の「スプレッドシート貼り付けプロンプト」で使用されている形式と互換性があります。

### 出力形式の特徴

- **タブ区切り形式（TSV）**: Googleスプレッドシートに直接コピー&ペースト可能
- **自動テキスト分割**: 50字以上の長いコメントは自動的に複数行に分割
- **発言者名の自動抽出**: IDや名前が含まれている場合は自動的に抽出

## 🔧 オプション

- `--output`, `-o`: 出力ファイルパスを指定（デフォルト: `output/comments_YYYYMMDD_HHMMSS.tsv`）
- `--format`: 出力形式を指定（`tsv` または `csv`、デフォルト: `tsv`）

## 📝 使用例

### 例1: 基本的な使用

```bash
python extract_comments.py "https://example.com/5ch-summary"
```

### 例2: カスタム出力パス

```bash
python extract_comments.py "https://example.com/board-summary" -o my_script.tsv
```

### 例3: CSV形式で出力

```bash
python extract_comments.py "https://example.com/board-summary" --format csv -o output.csv
```

## 🎯 対応サイト

以下のような掲示板まとめサイトに対応しています：

- 5chまとめサイト
- その他の掲示板まとめサイト（コメント番号（>>1, >>2など）を含むサイト）

## ⚠️ 注意事項

- サイトによってはHTML構造が異なるため、コメントが正しく抽出されない場合があります
- サイトの利用規約を確認し、適切に使用してください
- 大量のリクエストを送信する場合は、サーバーに負荷をかけないよう注意してください

## 🔄 今後の改善予定

- [ ] より多くのサイト構造への対応
- [ ] コメントのフィルタリング機能
- [ ] 発言者名の自動推測機能の強化
- [ ] 複数ページの自動取得
- [ ] コメントの時系列ソート

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

