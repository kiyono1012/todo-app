# ToDo管理アプリ

Python（Flask）と SQLite で作成したシンプルな ToDo 管理 Web アプリケーションです。

## 機能

- タスク登録（タスク名未入力時はエラーを表示。100文字以内）
- タスク一覧表示（完了・未完了をバッジ・色・取り消し線で表示、件数サマリ付き）
- タスク更新（丸いチェックボタンで完了・未完了を切り替え）
- タスク削除（確認ダイアログ付き）

## 動作環境

- Python 3.12
- Flask 3.0
- SQLite（Python 標準ライブラリの `sqlite3` を使用。別途インストール不要）
- PC のブラウザ（Chrome / Edge / Firefox など）

## ディレクトリ構成

```
todo-app/
├── app.py              # Flask アプリ本体（ルーティング・DB 処理）
├── requirements.txt    # 依存パッケージ
├── README.md
├── templates/
│   └── index.html      # 画面テンプレート
├── static/
│   ├── style.css       # スタイル
│   └── script.js       # 未入力チェック・削除確認
├── tests/
│   └── test_app.py     # 自動テスト（pytest）
└── todo.db             # 初回起動時に自動作成される SQLite DB
```

## 環境構築手順

```bash
cd todo-app

# 仮想環境の作成と有効化
python3.12 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

## 起動方法

```bash
python app.py
```

ブラウザで http://127.0.0.1:5000 を開きます。
データベース（`todo.db`）は初回起動時に自動で作成されます。停止は `Ctrl + C` です。

環境変数 `TODO_DATABASE` で DB ファイルの保存先を変更できます。

## テスト

```bash
python -m pytest -v
```
