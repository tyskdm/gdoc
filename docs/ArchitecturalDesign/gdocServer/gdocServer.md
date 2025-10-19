# gdoc Server

1. gdoc Language Server
2. gdoc Object Server

## Use Cases

### User types

1. gdoc Language Server
2. gdoc Object Viewer
3. gdoc CLI

### Usage Patterns

1. 'gdoc Language Server' only

2. 'gdoc Object Viewer' only

3. 'gdoc CLI' only

4. 'gdoc Language Server' + 'gdoc Object Viewer'

5. 'gdoc Language Server' + 'gdoc CLI'

6. 'gdoc Object Viewer' + 'gdoc CLI'

7. 'gdoc Language Server' + 'gdoc Object Viewer' + 'gdoc CLI'

## Architecture

### Basic design

#### Overall Architecture Diagram

![gdoc Server Architecture](./gdocServerArchitecture.drawio.png)

#### Key points

1. gdoc Server includes two servers:
   - gdoc Language Server
   - gdoc Object Server

2. gdoc Language Server and gdoc Object Server are implemented as separate threads within the same process.
   - gdoc Objects are shared between gdoc Language Server and gdoc Object Server.

3. gdoc Server will be implemented in pure Python with minimal dependencies to `pandoc`.
   - For this, Model viewer application will be implemented as a separate application.

4. gdoc Objects will be protected by a read-write lock mechanism to avoid data corruption.

#### Other design considerations

1. gdoc Object Server will provide APIs to access and manipulate gdoc Objects like a graph database.

2. gdoc Language Server and gdoc Object Server will be implemented with asynchronous processing.

3. gdoc Language Server will be implemented with Language Server Protocol (LSP) and JSON-RPC over standard input/output streams. (For debugging, UDS may be used as an option.)

4. gdoc Object Server will be implemented with JSON-RPC over Unix Domain Socket (UDS).

### Technical contexts

#### Python GIL

- GIL (Global Interpreter Lock) free theads will be usable in Pyhon 3.13 and later.
- Until then, we need to consider the GIL limitation when designing the architecture.

#### Graph Database

- gdoc Object Server will wrap gdoc Objects and provide APIs like a graph database.
  - gdoc Object Server API example:

    ```py
    get_node(id)
    get_edges(from_id, to_id)
    query_nodes(filter)
    query_edges(filter)
    ```

- We will provide an API similar to a general graph access API.

- APIs will provide Pub/Sub mechanism to notify changes in gdoc Objects.

##### Graph構造アクセス・操作のAPI群（分類別）

###### 🟦 1. ノード（Node）操作系

| API名 | 説明 |
| --- | --- |
| `GET /nodes` | 全ノード一覧を取得 |
| `GET /nodes/{id}` | 特定ノードの詳細を取得 |
| `POST /nodes` | 新しいノードを追加 |
| `PUT /nodes/{id}` | ノードの属性を更新 |
| `DELETE /nodes/{id}` | ノードを削除 |
| `PATCH /nodes/{id}/position` | UI上の位置情報などを更新（Graphビュー用） |

###### 🟩 2. エッジ（Edge）操作系

| API名 | 説明 |
| --- | --- |
| `GET /edges` | 全エッジ一覧を取得 |
| `GET /edges/{id}` | 特定エッジの詳細を取得 |
| `POST /edges` | ノード間のリンク（関係）を追加 |
| `DELETE /edges/{id}` | エッジを削除 |
| `GET /nodes/{id}/edges` | 特定ノードに関連するエッジ一覧 |

###### 🟨 3. Graph構造探索・分析系

| API名 | 説明 |
| --- | --- |
| `GET /nodes/{id}/neighbors` | 隣接ノード（直接リンク）を取得 |
| `GET /nodes/{id}/trace` | トレースパス（依存・参照）を取得 |
| `GET /graph/subgraph?root={id}` | 特定ノードを起点とした部分グラフを取得 |
| `GET /graph/search?q=...` | ノード属性や関係性に基づく検索 |
| `GET /graph/paths?from=A&to=B` | A→B間のパス探索（最短経路など） |

###### 🟥 4. Graph更新・イベント通知系（Pub/Sub）

| API名 / チャンネル | 説明 |
| --- | --- |
| `POST /events` | Graph操作イベントを発行（REST経由） |
| `Redis channel: graph_update` | ノード/エッジ追加・削除などの通知 |
| `WebSocket: /ws/graph` | クライアントへのリアルタイム通知 |
| `Event: add_node`, `add_edge`, `select_node` | イベントタイプ（type）によるルーティング |
| `GET /events/history` | 過去のイベントログ（履歴管理がある場合） |

###### 🟪 5. メタ・ユーティリティ系

| API名 | 説明 |
| --- | --- |
| `GET /schema` | ノード・エッジの型定義（Pydanticモデルなど） |
| `GET /stats` | ノード数、エッジ数、密度などの統計情報 |
| `GET /graph/export` | Graph構造のエクスポート（JSON, DOTなど） |
| `POST /graph/import` | Graph構造のインポート |

#### Asynchronous Processing and Concurrent Threads

- To share gdoc Objects among Language Server and Object Server, we will implement them in the same process.

- To separate their responsibilities, improve maintainability and performance isues, we will implement them as separate threads.

- We will use asynchronous processing to handle multiple requests concurrently in each of the Language Server and Object Server.

#### Read-Write Lock

- To avoid data corruption when multiple threads access gdoc Objects, we will implement a read-write lock mechanism.
  - Multiple threads can read gdoc Objects simultaneously.
  - Only one thread can write to gdoc Objects at a time, and no other threads can read or write during that time.

#### Graph探索・理解のための代表的なUIパターン

##### 🔹 1. **ノードリンク図（Force-directed Graph）**

- ノード（点）とエッジ（線）を物理的にレイアウト
- 力学モデルで自動配置（D3.js, Cytoscape.js  など）
- **用途**：構造全体の俯瞰、関係性の把握

##### 🔹 2. **ツリー構造ビュー（Tree View）**

- 階層的な依存関係や包含関係を表現
- 折りたたみ可能なノードで探索性向上
- **用途**：Block → Method → Signal のような階層モデル

##### 🔹 3. **マトリクスビュー（Adjacency Matrix）**

- ノード間の関係を行列形式で表示
- 大規模Graphでも密度や関係性が把握しやすい
- **用途**：トレースマトリクス、要件とテストの対応表

##### 🔹 4. **フィルタ付きリストビュー + 詳細パネル**

- ノード一覧 + 検索・フィルタ → 選択 → 詳細表示
- 属性ベースの探索に強い
- **用途**：Requirement一覧 → 関連Block表示 → 編集

##### 🔹 5. **ミニマップ + メインビュー**

- 全体構造をミニマップで表示し、メインビューで詳細操作
- **用途**：大規模Graphのナビゲーション補助

##### 🧰 UIに組み込まれる機能群（Graph操作支援）

| 機能 | 説明 |
| --- | --- |
| 🔍 ノード検索 | IDや属性でノードを検索 |
| 🧭 意味的サブグラフ抽出 | 依存関係やトレースパスを辿って部分表示 |
| 🖱 ノード選択 → 詳細表示 | 属性・履歴・関連ノードを表示 |
| ➕ ノード・エッジ追加 | GUI上で構造を編集（ドラッグ・フォーム） |
| 🔄 Graph更新通知 | WebSocketやRedisでリアルタイム反映 |
| 🎨 属性による色分け | ノードタイプやステータスで視覚的区別 |
| 🧩 プラグイン式ビュー切替 | Graph / Tree / Matrix を切り替え可能に |

#### Cursor position Tracking and Context Awareness

- To provide accurate Language Server features, we will track the cursor position and context in the document being edited.

- And we will track the context objects related to the cursor position, such as the current block, method, signal, and their relationships.

#### UDS: Unix Domain Socket

- To enable efficient inter-process communication between gdoc Language Server and gdoc Object Server, we will use Unix Domain Sockets (UDS).

> - ポート番号不要。ファイルパスで接続
> - LSPやVS Code拡張ではUDSがよく使われる
> - 衝突の心配がなく、セキュリティ的にも安全

##### UDSのOS対応状況

| OS | 利用可否 | 備考 |
| --- | --- | --- |
| **Linux** | ✅ 利用可能 | 最も一般的。`/tmp/xxx.sock` などのパスで使用 |
| **macOS** | ✅ 利用可能 | Linuxとほぼ同様のAPIで動作。開発環境に適している |
| **Windows** | ✅ 利用可能（制限あり） | Windows 10以降で `AF_UNIX` がサポートされている（Python 3.9+ など） |

##### UDSのパス指定に関する基本ルール

| 項目 | 説明 |
| --- | --- |
| ✅ 任意のパス指定 | `/tmp/myservice.sock`, `/var/run/myapp.sock`, `/home/user/.cache/my.sock` など自由に指定可能 |
| ✅ ディレクトリ階層 | `/tmp/path/to/somewhere.sock` のように**階層構造も使用可能**（ただし事前にディレクトリが存在している必要あり） |
| ❌ `~`（チルダ）記法 | `~/tmp/myservice.sock` のような**チルダ展開は自動では行われない**ため、**明示的に展開が必要** |
| ✅ ファイル拡張子 | `.sock`, `.ipc`, `.socket` などは慣習的に使われるが、**拡張子は任意**（なくてもOK） |
| ❌ パス長制限 | Linuxでは**最大108バイト**（`sun_path` の制限） → 長すぎると `OSError: AF_UNIX path too long` になる可能性あり |

##### UDSの一時ファイルの破棄タイミング

| 状況 | ファイル削除されるか | 説明 |
| --- | --- | --- |
| ✅ 正常終了（`close()` + `unlink()`） | ✔️ 削除される | サーバー側が明示的に `os.unlink(path)` を呼ぶ必要あり |
| ❌ 異常終了（クラッシュ、強制終了） | ❌ 残る | OSはソケットファイルを自動削除しないため、**ゴミが残る** |
| ✅ 再起動時に `bind()` 失敗 | ✔️ or ❌ | 既存ファイルがあると `OSError: Address already in use` になる可能性あり |

