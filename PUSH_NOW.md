# 🚀 GitHubへのプッシュ手順（kuro1163用）

リモートリポジトリは既に設定済みです。以下のいずれかの方法でプッシュしてください。

## 方法1: Personal Access Tokenを使用（推奨）

### 1. Personal Access Tokenを作成

1. GitHubにログイン
2. 右上のアイコン → **Settings**
3. 左メニューの一番下 → **Developer settings**
4. **Personal access tokens** → **Tokens (classic)**
5. **Generate new token** → **Generate new token (classic)**
6. Note: `board-comment-extractor` など適当な名前を入力
7. Expiration: 有効期限を設定（または無期限）
8. Scopes: **`repo`** にチェック
9. **Generate token** をクリック
10. **トークンをコピー**（この画面を閉じると二度と見れません！）

### 2. プッシュ

```bash
cd board-comment-extractor

# プッシュ（ユーザー名: kuro1163、パスワード: トークンを貼り付け）
git push -u origin main
```

ユーザー名を聞かれたら: `kuro1163`  
パスワードを聞かれたら: **コピーしたトークンを貼り付け**

## 方法2: SSH鍵を使用

### 1. SSH鍵を設定（まだの場合）

```bash
# SSH鍵を生成（既にある場合はスキップ）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 公開鍵をコピー
cat ~/.ssh/id_ed25519.pub
```

### 2. GitHubにSSH鍵を登録

1. コピーした公開鍵をGitHubに登録
   - Settings → SSH and GPG keys → New SSH key

### 3. リモートURLをSSHに変更してプッシュ

```bash
cd board-comment-extractor

# リモートURLをSSHに変更
git remote set-url origin git@github.com:kuro1163/board-comment-extractor.git

# プッシュ
git push -u origin main
```

## 方法3: GitHub CLIを使用

```bash
# GitHub CLIをインストール（未インストールの場合）
brew install gh  # macOS

# ログイン
gh auth login

# プッシュ
git push -u origin main
```

## ✅ 確認

プッシュが成功したら、以下のURLで確認できます：

🔗 https://github.com/kuro1163/board-comment-extractor

## 💡 トラブルシューティング

### "fatal: could not read Username" エラー

→ Personal Access Tokenを使用してください（方法1）

### "Permission denied" エラー

→ SSH鍵が正しく設定されているか確認してください（方法2）

### リポジトリが存在しないエラー

→ 先にGitHubでリポジトリを作成してください：
   https://github.com/new
   リポジトリ名: `board-comment-extractor`

