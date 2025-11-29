# GitHubへのアップロード手順

このプロジェクトをGitHubにアップロードする手順です。

## 📋 事前準備

1. GitHubアカウントを持っていること
2. Gitがインストールされていること（通常は既にインストール済み）

## 🚀 手順

### 1. GitHubでリポジトリを作成

1. [GitHub](https://github.com)にログイン
2. 右上の「+」ボタンから「New repository」を選択
3. リポジトリ名を入力（例: `board-comment-extractor`）
4. 説明を入力（例: "掲示板まとめサイトからコメントを抽出してYouTube台本形式のスプレッドシートに変換するツール"）
5. PublicまたはPrivateを選択
6. **「Initialize this repository with a README」のオプションについて**：
   - オプションが表示されない場合：そのまま「Create repository」をクリック（問題ありません）
   - オプションが表示される場合：チェックを外す（既にREADMEがあるため）
7. 「Create repository」をクリック

**注意**: もしGitHubでREADMEを作成してしまった場合でも、後でマージできます（手順3で説明）

### 2. ローカルリポジトリを準備

既にGitリポジトリは初期化済みです。初回コミットを作成します：

```bash
cd board-comment-extractor

# 初回コミット
git commit -m "Initial commit: 掲示板コメント抽出ツール"
```

### 3. GitHubリポジトリと接続

GitHubで作成したリポジトリのURLをコピーして、以下のコマンドを実行：

```bash
# リモートリポジトリを追加（your-usernameを自分のユーザー名に置き換え）
git remote add origin https://github.com/your-username/board-comment-extractor.git

# またはSSHを使用する場合
# git remote add origin git@github.com:your-username/board-comment-extractor.git
```

**GitHubでREADMEを作成してしまった場合**：
GitHubでREADMEを作成してしまった場合は、以下のコマンドでマージしてからプッシュします：

```bash
# GitHubのREADMEを取得
git pull origin main --allow-unrelated-histories

# コンフリクトが発生した場合は、ローカルのREADMEを優先
# または手動でマージ

# その後、プッシュ
git push -u origin main
```

### 4. ブランチ名を確認・変更

```bash
# 現在のブランチ名を確認
git branch

# もしmasterブランチの場合は、mainに変更（GitHubのデフォルトに合わせる）
git branch -M main
```

### 5. GitHubにプッシュ

```bash
# 初回プッシュ
git push -u origin main

# またはmasterブランチの場合
# git push -u origin master
```

### 6. READMEの更新

GitHubにアップロード後、README.mdの以下の部分を自分のリポジトリURLに更新してください：

```markdown
git clone https://github.com/your-username/board-comment-extractor.git
```

## ✅ 確認

GitHubのリポジトリページにアクセスして、ファイルが正しくアップロードされているか確認してください。

## 🔄 今後の更新方法

コードを変更した後は、以下のコマンドで更新できます：

```bash
# 変更をステージング
git add .

# コミット
git commit -m "変更内容の説明"

# GitHubにプッシュ
git push
```

## 📝 トラブルシューティング

### 認証エラーが発生する場合

GitHubの認証方法が変更されました。以下のいずれかの方法で認証してください：

1. **Personal Access Token（推奨）**
   - GitHub Settings > Developer settings > Personal access tokens
   - 新しいトークンを作成
   - プッシュ時にパスワードの代わりにトークンを使用

2. **SSH鍵を使用**
   - SSH鍵を設定して、SSH URLを使用

### リモートリポジトリのURLを変更する場合

```bash
# 現在のリモートURLを確認
git remote -v

# URLを変更
git remote set-url origin https://github.com/your-username/board-comment-extractor.git
```

