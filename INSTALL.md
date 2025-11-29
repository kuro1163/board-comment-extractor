# インストールガイド

## 📋 必要な環境

- Python 3.8以上
- pip（Pythonパッケージマネージャー）

## 🚀 インストール方法

### 1. プロジェクトディレクトリに移動

```bash
cd board-comment-extractor
```

### 2. 仮想環境の作成（推奨）

```bash
# 仮想環境を作成
python3 -m venv .venv

# 仮想環境をアクティベート
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

## ✅ インストール確認

インストールが完了したら、以下のコマンドで動作確認できます：

```bash
python extract_comments.py --help
```

ヘルプが表示されれば、インストールは成功です！

## 🔧 トラブルシューティング

### ModuleNotFoundError が発生する場合

依存関係が正しくインストールされていない可能性があります。以下を試してください：

```bash
# 仮想環境がアクティブになっているか確認
which python  # macOS/Linux
# または
where python  # Windows

# 依存関係を再インストール
pip install --upgrade -r requirements.txt
```

### 権限エラーが発生する場合

```bash
# 実行権限を付与（macOS/Linux）
chmod +x extract_comments.py
```

