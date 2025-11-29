#!/bin/bash
# GitHubへのプッシュスクリプト
# 使用方法: ./PUSH_TO_GITHUB.sh your-username

if [ -z "$1" ]; then
    echo "❌ エラー: GitHubユーザー名を指定してください"
    echo "使用方法: ./PUSH_TO_GITHUB.sh your-username"
    echo ""
    echo "例: ./PUSH_TO_GITHUB.sh kuwabara"
    exit 1
fi

USERNAME=$1
REPO_NAME="board-comment-extractor"

echo "🚀 GitHubへのアップロードを開始します..."
echo ""

# リモートリポジトリが既に設定されているか確認
if git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  既にリモートリポジトリが設定されています:"
    git remote -v
    echo ""
    read -p "上書きしますか？ (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ キャンセルしました"
        exit 1
    fi
    git remote remove origin
fi

# リモートリポジトリを追加
echo "📡 リモートリポジトリを追加中..."
git remote add origin "https://github.com/${USERNAME}/${REPO_NAME}.git"

# GitHubにREADMEがあるか確認（オプション）
echo "🔍 GitHubリポジトリの状態を確認中..."
if git ls-remote --heads origin main > /dev/null 2>&1; then
    echo "⚠️  GitHubに既にコンテンツがあるようです"
    echo "💡 GitHubでREADMEを作成した場合は、以下のコマンドでマージできます:"
    echo "   git pull origin main --allow-unrelated-histories"
    echo ""
    read -p "続行してプッシュしますか？ (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ キャンセルしました"
        exit 1
    fi
fi

# プッシュ
echo "⬆️  GitHubにプッシュ中..."
if git push -u origin main 2>&1 | grep -q "rejected"; then
    echo ""
    echo "⚠️  プッシュが拒否されました。GitHubに既にコンテンツがある可能性があります"
    echo ""
    echo "💡 以下のコマンドでマージしてから再試行してください:"
    echo "   git pull origin main --allow-unrelated-histories"
    echo "   git push -u origin main"
    exit 1
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 成功！GitHubにアップロードされました！"
    echo "🔗 https://github.com/${USERNAME}/${REPO_NAME}"
else
    echo ""
    echo "❌ プッシュに失敗しました"
    echo ""
    echo "💡 ヒント:"
    echo "1. GitHubでリポジトリを作成しているか確認してください"
    echo "2. リポジトリ名が '${REPO_NAME}' であることを確認してください"
    echo "3. 認証情報を確認してください（Personal Access Tokenが必要な場合があります）"
    echo "4. GitHubでREADMEを作成した場合は、先にマージしてください:"
    echo "   git pull origin main --allow-unrelated-histories"
    exit 1
fi
