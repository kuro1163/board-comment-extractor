# GitHub Actionsワークフローの追加方法

ワークフローファイル（`.github/workflows/python-check.yml`）を後で追加する方法です。

## 方法1: トークンに`workflow`スコープを追加（推奨）

### 1. GitHubでトークンを更新

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 作成したトークンをクリック（または新規作成）
3. **Select scopes** で **`workflow`** にチェックを追加
4. **Update token** をクリック

### 2. ワークフローファイルを追加

```bash
cd board-comment-extractor

# ワークフローファイルを復元
git checkout HEAD -- .github/workflows/python-check.yml

# コミット
git add .github/workflows/python-check.yml
git commit -m "Add GitHub Actions workflow"

# プッシュ（トークンにworkflowスコープが必要）
git push
```

## 方法2: GitHubのWebインターフェースで追加

1. https://github.com/kuro1163/board-comment-extractor にアクセス
2. 「Add file」→「Create new file」をクリック
3. ファイル名: `.github/workflows/python-check.yml`
4. 以下の内容を貼り付け：

```yaml
name: Python Check

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Check syntax
      run: |
        python -m py_compile extract_comments.py
```

5. 「Commit new file」をクリック

## 注意事項

- ワークフローファイルは必須ではありません（オプション機能）
- プッシュは既に成功しているので、ワークフローファイルは後で追加できます
- ワークフローファイルがない場合でも、プロジェクトは正常に動作します

