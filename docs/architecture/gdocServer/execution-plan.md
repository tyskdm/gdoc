# gdoc Server — 設計文書 実行計画（Execution Plan）

> この文書は、gdoc Server の設計文書群（要件割当て・API仕様・Task/Job管理ルール）を
> **再現可能・再開可能**に作るための実行計画である。
> チャットが途切れたりコンテキストが変わっても、このファイルを読むだけで
> 「どこまで進めたか／次は何をするか／誰が判断すべきか」が復元できること、が目的。

## この文書の使い方（Resume Protocol）

新しい作業セッションを開始したら、次の順で進めること。

1. 本ファイルの **STATUS** を読んで現在地を確認する。
2. **未解決質問レジスタ** で `open` の質問があるか確認し、あれば先にユーザーへ確認する（勝手に仮定しない）。
3. **現在のフェーズ** の「作業内容・手順」をそのまま実行する。
4. 「検証観点 — セルフチェック」を自分で実施し、結果を記録する。
5. 「検証観点 — ユーザーレビュー」の項目をユーザーへ提示し、承認を得る。
6. 承認後、**STATUS** と **判断ログ** を更新し、次のフェーズへ進む。

**原則:** 各フェーズは「成果物ファイル」を必ず産出する。産出物がないフェーズは未完了とみなす。
**原則:** 後続フェーズで前フェーズの成果物を変更する場合、変更内容と理由を **判断ログ** に載せ、該当するトレーサビリティを再実行する。

---

## STATUS（現在地）

| 項目 | 値 |
|---|---|
| 現在のフェーズ | Phase 0（着手前） |
| 直近の状態 | 実行計画のみ作成。成果物文書はまだ無い。 |
| 次のアクション | Phase 0 の「作業内容・手順」を実行し、`subcomponents/README.md` を作成する。 |
| ブロック要因 | 全解決（Q-001〜005 回答、D-003〜D-007 確定、D-005 の v1 スコープも確認済み）。**ブロッカーなし → Phase 0 着手可能。** |
| 最終更新 | 2026-09-11（Q-001〜005 回答、D-003〜D-007 確定、D-005 スコープ確認済み） |

### フェーズ一覧

| Phase | 目的 | 成果物 | 状態 |
|---|---|---|---|
| 0 | 接地：コンポーネント/責任インベントリ＋用語 | `subcomponents/README.md` | ⬜ 未着手 |
| 1a | goal #3：Task/Job 管理ルール | `contracts/task-job-management.md` | ⬜ 未着手 |
| 1b | goal #2：Frontend↔ODB API | `contracts/frontend-odb-api.md` | ⬜ 未着手 |
| 2 | ユースケース分析の統一（挙動の証拠） | `usecases/UC_*.md` | ⬜ 未着手 |
| 3 | goal #1：コンポーネント要求割当て | `subcomponents/*.md` | ⬜ 未着手 |
| 4 | 最終検証：トレーサビリティ＋リスククロージャ | `traceability.md` | ⬜ 未着手 |

---

## ソース・正（Sources of Truth）

設計判断がぶれる場合、**この順の上位**を正とする。

| 優先 | 文書 | 役割 |
|---|---|---|
| 1 | `requirements/requirements.md` | 上位要件（FR-1.x / FR-2.x / FR-3.x / FR-4.x / NFR）。ID の正。 |
| 2 | `adr/*.md`（001〜009）＋`adr/README.md`（リスクレジスター） | 戦略的決定＋リスク（R-00x）。契約の根拠。 |
| 3 | `architecture.md` | 構造・振る舞い・抽象（Workspace/Project/Package）。 |
| 4 | `usecases/UC_*.md` | 挙動分析（テンプレート準拠、IF/ST/DR/EH/SCR ID）。 |
| 5 | 本計画が産出する `contracts/`, `subcomponents/`, `traceability.md` | 上記から導出した実行可能仕様。 |

### 再利用できるエージェント資産

- スキル: `.agents/skills/usecase-analysis/SKILL.md`（Phase 2 の分析方法）
- チェックリスト: `.agents/checklists/Traceability Check Strategy.md`（Phase 3/4 の検証）
- チェックリスト: `.agents/checklists/Architecture Design Checklist.md`
- テンプレート: `.agents/templates/use-case-analysis-template.md`（Phase 2 の形式）

---

## 最終成果物のマップ（Target File Tree）

本計画が完成した時点でできるファイル構成（`docs/architecture/gdocServer/` 以下）:

```
docs/architecture/gdocServer/
├─ requirements/requirements.md      # 既存（上位要件、ID の正）
├─ architecture.md                   # 既存
├─ adr/                              # 既存（001〜009 + リスクレジスター）
├─ execution-plan.md                 # 本ファイル（計画 + STATUS + 判断ログ + 質問レジスタ）
├─ contracts/                        # 新規（Phase 1）
│  ├─ task-job-management.md         #   Phase 1a = goal #3
│  └─ frontend-odb-api.md            #   Phase 1b = goal #2
├─ usecases/                         # Phase 2 で統一（usecase_analysis/ を吸収）
│  ├─ UC_OpenText.md                 #   既存（要統一）
│  ├─ UC_EditText.md                 #   既存（要統一）
│  ├─ UC_GoToDefinition.md           #   既存（要統一）
│  └─ UC_*.md                        #   追加: Hover/References/Symbols/Completion/Rename/Diagnostics/SemanticTokens/CloseText/UpdateDocument/EditConfig
├─ subcomponents/                    # Phase 0(README) + Phase 3
│  ├─ README.md                      #   Phase 0 = 責任インベントリ
│  ├─ language-server.md             #   Phase 3 = goal #1
│  ├─ object-database.md             #   Phase 3 = goal #1
│  ├─ object-datastore.md            #   Phase 3 = goal #1
│  └─ object-builders.md             #   Phase 3 = goal #1
├─ traceability.md                   # Phase 4 = 全方向トレース行列 + リスククロージャ
└─ usecase_analysis/                 # Phase 2 で統合先へ移動 or 明示的に別位置づけ（判断ログで確定）
```

---

## 共通規約（全成果物に適用）

### ID スキーム

| 種別 | 形式 | 例 | 所属 |
|---|---|---|---|
| 上位要件 | `FR-n.m` / `NFR-n.m` | `FR-1.2`, `NFR-2.2` | `requirements.md`（既存） |
| 決定 | `ADR-NNN` | `ADR-008` | `adr/`（既存） |
| リスク | `R-NNN-M` | `R-006-3` | `adr/README.md`（既存） |
| ユースケース | `UC-nnn` | `UC-002` | `usecases/` |
| 派生要求 | `IF-` / `ST-` / `DR-` / `EH-` / `SCR-<COMP>-` | `SCR-DB-001` | `usecases/` |
| コンポーネント要求 | `LSP-nnn` / `ODB-nnn` / `DS-nnn` / `BLD-nnn` | `ODB-001` | `subcomponents/` |
| API 操作 | `API-nnn` | `API-001` | `contracts/frontend-odb-api.md` |
| Task/Job 規則 | `TJ-nnn` | `TJ-001` | `contracts/task-job-management.md` |

### 「Derived From」の書式

下位の各要求は、必ず上位への連鎖を 1 行で記す。例:

```
[ODB-007] ...
  Derived From: FR-3.2 → ADR-006 → R-006-3 → TJ-003 / UC-002
```

### トレーサビリティの機械チェック方針

- **形式チェック（機械的）:** 全要求に ID が存在すること／ID の重複がないこと／トレース行列に孤立項目がないこと。→ 表形式で維持し、grep・集計で確認。
- **意味チェック（LLM レビュー）:** 充足性・意味的包含・一貫性・粒度・検証可能性。→ `.agents/checklists/Traceability Check Strategy.md` を指示書として用い、下表形式で出力:

| 要求ID | 状態(OK/Partial/NG) | 不足要素・理由 | 推奨対策 |
| :--- | :--- | :--- | :--- |

---

## Phase 0 — 接地：コンポーネント/責任インベントリ＋用語

- **目的:** 「誰が何を所有するか」を文字起こしし、後のフェーズで「2箇所所有」「所有者なし」を防ぐ土台を作る。全ステップの前提。
- **成果物:** `subcomponents/README.md`
- **依存:** 無（最初にやる）。

### 作業内容・手順

1. `architecture.md` の「Structure」「Key Abstractions」から、コンポーネントを列挙する。
   - **LSP Frontend** / **Object Database (ODB)** / **Object Datastore** / **Object Builder(s)** /（将来）**Object Server**。
2. ADR-001（frontend/core 分離）と ADR-008（Request/Task 境界）から、各コンポーネントの **所有する責任** と **所有しないこと** を明文化する。
3. **境界を確定する:**
   - Datastore は **ODB の内部**（ADR-004: single writer、外部からアクセス不可）。→ **公開 API を持つのは Frontend↔ODB のみ**。Datastore には公開 API を置かない。
   - Builder は **ODB の下流**（ADR-005: プラグイン、subprocess 実行可）。
   - Object Server は **将来・同一 core の別 frontend**。書き込みは同じ mutate API 経由（単一 writer を維持）。
4. **用語の不変条件を 1 セクションに固定する:** Request / Task / Subtask / Job / Document / Package / Project / **dedup key** / **priority** の各 1 定義。
   - 特に **subtask（task-local 管理単位） vs Job（共有実行単位）** の区別（ADR-002 注記）をここで一度だけ定義し、以降の文書は参照させる。

### 検証観点

- **セルフチェック（自分が実施）:**
  - [ ] 全責任が **ちょうど 1** コンポーネントで所有される（重複なし・なしなし）— ADR-008 の「各意思決定に所有者がちょうど 1」で自己点検。
  - [ ] 用語の定義が ADR の記述と矛盾しない（一貫性チェック）。
  - [ ] 「公開 API を持つのは Frontend↔ODB のみ」が明示されている。
  - [ ] Object Server が「将来・read-only / 同じ mutate API 経由」で明記されている（ADR-001）。
- **ユーザーレビュー（あなたに確認）:**
  - [ ] 4コンポーネントの切り分けが想定通りか（Builder を独立コンポーネントとする見解）。
  - [ ] Datastore を「内部扱い（公開 API なし）」とする見解に同意か。
  - [ ] **v1 のスコープ**（Object Server は除外）を確認 → 質問レジスタ `Q-001`。

- **DoD:** 全責任に所有者が 1 つ・用語が矛盾なく 1 定義・境界が明文化。ユーザーが切り分けを承認。

### 判断待ち

- **解決済み:** `Q-003`（Object Server v1 除外）→ D-006、v1 スコープ（D-005）確認済み。**ブロッカーなし → Phase 0 着手可能。**

---

## Phase 1a — goal #3：Task/Job 管理ルール

- **目的:** ADR-002/006/007/009 を「実行可能な仕様（規則）」に結晶化する。全コンポーネント要求のレールになるため**先に行う**。
- **成果物:** `contracts/task-job-management.md`
- **依存:** Phase 0。

### 作業内容・手順

1. **3 階層モデル**（ADR-002）を状態機械として記述する。Task の状態（Active / Cancelled / Completed …）、Job の状態、Subtask との関係。**状態遷移表を 1 枚**作る。
2. **共有と dedup**（ADR-006）:
   - **dedup key = (file, version, inputs)** を規則 `TJ-` に固定。inputs の中身（content type / dependency state / options）を列挙（R-006-2）。
   - **単一 in-flight 不変条件**（R-002-2）: 同一 dedup key の Job は同時に 1 つのみ。
   - **参照カウントキャンセル**（R-006-3）: waiter ≥1 間で active、最後の離脱で cancel。キャンセルは **ODB 側で集中管理**し、フロントエンドは「自分の task のみ」cancel する。
   - **コミットは成功時のみ原子的**（R-006-1）。
3. **優先度**（ADR-007/006/008）:
   - 2 段: **フロントエンド**＝どのリクエストが重要か・順序（ADR-008）。**ODB**＝どの共有ワークが先か（ADR-007 の 3 状態 + reference-depth）。
   - **合成規則**（R-007-3）: 境界を明文化。
   - **優先度継承**（ADR-006）と **starvation 対策**: state-1 の pin bound（R-007-1）、unbounded の defer/cancel policy（R-007-2）、priority inversion の bound（R-006-4）。
4. **設定保存＝再ビルドイベント**（ADR-009）: state-3（package membership）と依存グラフの更新タイミング、config 更新時に無効化されるキャッシュ。
5. **ドキュメント同一性・新旧判定の方式**を確定する（質問レジスタ `Q-002`）:
   - 候補: buffer の **version / revision / ETag / content-hash** のいずれか。
   - 採用方式を dedup key と Datastore 不変条件に反映し、「新旧比較不能」問題（`usecase_analysis/3. Open Text.md` の質問）を解決する。

### 検証観点

- **セルフチェック:**
  - [ ] ADR-002/006/007/009 の **全 `Verify` 項目**が「規則（TJ-）＋テスト」にマッピングされている。
  - [ ] リスク **R-002-1/2、R-006-1..4、R-007-1..3** が全て規則として現れる。
  - [ ] 「subtask vs job」の境界が全パスで一貫（Phase 0 の定義を参照している）。
  - [ ] 「ODB は client type で分岐しない」（R-008-2）が規則化されている。
- **ユーザーレビュー:**
  - [ ] 優先度 2 段の境界（frontend＝which、ODB＝which）が意図通りか。
  - [ ] starvation / unbounded への policy（pin bound、defer/cancel）を許容するか。
  - [ ] **ドキュメント新旧判定方式（Q-002）** を決定（content-hash / revision / ETag のどれか）。
  - [ ] Job 実行の bound / timeout の許容（R-005-1 / R-003-3 と関連）。

- **DoD:** 全 Verify/リスクが規則化・状態遷移表あり・dedup key と priority 規則が明確・`Q-002` が解決済み。

### 判断待ち

- **解決済み:** `Q-002`（新旧判定方式）→ D-004（LSP `version`＝単調増加 revision）、`Q-004`（starvation/unbounded）→ D-007（詳細設計へ defer、v1 では機構クラスのみ固定）。

---

## Phase 1b — goal #2：Frontend↔ODB API

- **目的:** Phase 1a の Task/Job ルールの「表面（API）」を定義する。ODB が内部処理するためだけの公開 API。
- **成果物:** `contracts/frontend-odb-api.md`
- **依存:** Phase 1a（API は Task/Job ルールの表面）。

### 作業内容・手順

1. **操作一覧**（各 `API-nnn`）:
   - `submit(request) → { inline result | request id }`（ADR-002: 1 request : 1 task）
   - `getResult(id)` / 完了は **push-back（事前登録コールバック）** による（ADR-003）
   - `cancel(id | scope)`（ADR-008: フロントエンドは自分の task のみ cancel 可能）
   - `registerCompletion(callback)`（ADR-003）
2. **Request モデル**（プロトコル非依存フィールド、ADR-002/008）:
   - 触るドキュメント / reference depth / priority hint / source（frontend 識別用のみ、semantics なし）/ 必要コンテキスト。
   - **R-008-2:** ODB が要る文脈を **全て**表現できること（表現できなければ escape valve として Request モデルを拡張する——これは API に追記する正当な口）。
3. **結果型**: diagnostics / semantic tokens / symbols / completion items / definition / references / rename edits 等（FR-1.2 由来）。
4. **同期 facade のセマンティクス**（ADR-003）:
   - コールバックは軽量、`loop.call_soon_threadsafe` / `run_coroutine_threadsafe` 必須（R-003-2）。**polling 禁止**。
   - コールバック内で重い処理禁止（R-003-1）。
5. **エラー / キャンセルモデル**: task が cancel された場合の API 挙動（R-008-1 のキャンセル翻訳）。
6. 各 API 操作 → Phase 1a の `TJ-` 規則や ADR にトレーサブルに紐付ける。

### 検証観点

- **セルフチェック:**
  - [ ] 全 API 操作が `TJ-` 規則 / ADR に trace 可能。
  - [ ] Request モデルが ODB の要る文脈を全て表現（R-008-2）。
  - [ ] コールバック制約が明記（R-003-1/2/3）。
  - [ ] FR-1.2 の各機能が「結果型 or API 操作」で表現できる。
  - [ ] cancel が「自分の task のみ」に翻訳される（R-006-3 / R-008-1）。
- **ユーザーレビュー:**
  - [ ] API の粒度（submit / getResult / cancel の分割）が実装しやすく妥当か。
  - [ ] 結果型の範囲が v1 で十分か（Q-001 と連携）。
  - [ ] request id の意味（request と 1:1）の確認。

- **DoD:** 操作・型・facade・エラーが揃い、全て ADR / `TJ-` に trace 可能。FR-1.2 全機能が表現可能。

### 判断待ち

- **解決済み:** `Q-001`（v1 の機能スコープ＝結果型の範囲）→ D-005。

---

## Phase 2 — ユースケース分析の統一（挙動の証拠）

- **目的:** 挙動の根拠（証拠）を揃え、Phase 1 の契約が「挙動に対して十分か」を逆検証する。
- **成果物:** `usecases/UC_*.md` に統一（`usecase_analysis/` は吸収 or 明示的に別位置づけ——判断ログで確定）。
- **依存:** Phase 1a / 1b（逆チェックの相手）。
- **方法:** `.agents/skills/usecase-analysis/SKILL.md` と `.agents/templates/use-case-analysis-template.md` を使う。

### 作業内容・手順

1. **2 フォルダの関係を 1 つに決める:**
   - 案A: `usecases/` を正とし、`usecase_analysis/` の良い部分（LSP 公式リンク・シーケンス図・`6. Update Document` の Task Queue 注記）を `UC_` 形式に吸収、`usecase_analysis/` を削除 or アーカイブ。
   - 案B: `usecase_analysis/` を「プロトコル参照」に、`usecases/` を「正式分析」に位置づけ、両者の関係を README で明記。
   - **どちらか 1 つ**を判断ログに載せる（混在したままだとトレースが二重化する）。
2. **FR-1.2 の全機能＋系** を UC でカバーする。不足分を追加:
   - Find References / Symbols / Completion / Rename / **Diagnostics の公開** / Semantic Tokens。
   - 同期系: `didOpen` / `didChange` / `didClose`。設定系: `didChangeWatchedFiles` / config 保存（ADR-009）。
3. 各 UC を**テンプレート準拠**（Analysis Focus / Main / Alternative / **Sequence Diagram** / **Derived Requirements: IF / ST / DR / EH / SCR** / **Traceability Matrix**）で記述し、**4 コンポーネント全てに「アクターごとの要求」を落とす**（空にしない）。
4. 各 UC が Phase 1a/1b の契約（`TJ-` 規則・API）を「満たすか / 不足か」を逆チェックし、**不足は Phase 1a/1b にフィードバック**（= escape valve）。

### 検証観点

- **セルフチェック:**
  - [ ] FR-1.2 全機能＋同期系＋設定系が UC でカバー（充足性）。
  - [ ] 各 UC が 4 コンポーネント全てに要求を落としている（空なし）。
  - [ ] IF/ST/DR/EH/SCR ID が揃い、FR/ADR に trace 可能。
  - [ ] シーケンス図が ADR-008 の hand-off（inline vs request-id+push）と矛盾しない。
  - [ ] `3. Open Text` の versioning 質問が Phase 1a（Q-002）で解決済みと整合。
  - [ ] シークエンスで**同一操作の二重呼び出し**が無い（例: hover で `get_hover_info` を 2 回呼ぶ、のような重複）。
- **ユーザーレビュー:**
  - [ ] UC の網羅範囲が v1 想定と一致（例: rename は実装対象か）→ `Q-001`。
  - [ ] 各 UC の main / alternative シナリオが現実のクライアント挙動と合うか。
  - [ ] まず実装すべき UC の優先度を特定。

- **DoD:** FR-1.2 全機能が UC 化・4 コンポーネントへの要求分解が揃う・Phase 1 契約との整合が確認済み。

### 判断待ち

- **解決済み:** `Q-001`（v1 スコープ）→ D-005、`Q-005`（統合方針）→ D-003（案A）。
- **将来:** v2 の機能スコープ（Completion/Rename/Symbols/SemanticTokens）は暫定（D-005）。再検証時に必要なら再提案。

---

## Phase 3 — goal #1：コンポーネント要求割当て（統合）

- **目的:** 契約義務（Phase 1）と挙動義務（Phase 2）を統合し、4 コンポーネントごとに要求セットを作る。**「検証」の本命フェーズ。**
- **成果物:** `subcomponents/language-server.md` / `object-database.md` / `object-datastore.md` / `object-builders.md`
- **依存:** Phase 0 / 1a / 1b / 2。

### 作業内容・手順

1. 各コンポーネント要求 ＝ **（Phase 1 の契約義務）∪（Phase 2 の挙動義務）**。
2. 各要求に安定 ID（`LSP-nnn` / `ODB-nnn` / `DS-nnn` / `BLD-nnn`）＋ **「Derived From」**（FR/NFR → ADR → UC → API操作/Task規則）を付与する。
3. **Datastore は「公開 API」ではなく「データモデル＋一貫性・単一 writer 不変条件」**（ADR-004）で記述する。
4. **NFR（NFR-1.1..3.1）** を該当コンポーネントに割当て:
   - LSP: asyncio / 軽量メッセージ処理 / 最小実行時間（NFR-1.1）。
   - ODB: 別スレッド / 内部 event loop / 動的スケジューリング / 共有・キャンセル（NFR-2.1/2.2/2.3）。
   - Datastore: in-memory / thread-safe / single writer（NFR-3.1）。
5. **全 FR/NFR が ≥1 のコンポーネント要求でカバーされる**ことを確認（漏れゼロ）。

### 検証観点

- **セルフチェック:**
  - [ ] `.agents/checklists/Traceability Check Strategy.md` の **5 項目**（充足性・意味的包含・一貫性・粒度・検証可能性）をコンポーネント毎に適用し、表で出力。
  - [ ] 全 FR/NFR が ≥1 要求でカバー（充足性）。
  - [ ] 全要求が trace 可能（ Derived From が切れていない）。
  - [ ] 0 所有 / 2 所有なし（一貫性）。
  - [ ] 用語が Phase 0 の定義と一致（一貫性）。
  - [ ] 各要求が検証可能（DoD/テスト観点がある）。
- **ユーザーレビュー:**
  - [ ] 各コンポーネントの要求が「実装に渡せる粒度」か（過剰/不足）。
  - [ ] NFR の割り当てが妥当か。
  - [ ] まず実装すべきコアが特定できるか。

- **DoD:** 4 コンポーネントの要求セット完成・全 FR/NFR/ADR/UC が trace 可能・充足性・一貫性チェック合格。

### 判断待ち

- 粒度の妥当性（ユーザー判断）。

---

## Phase 4 — 最終検証：トレーサビリティ＋リスククロージャ

- **目的:** 全体として「設計完了」を宣言できるかを検証する。孤立ゼロ＋全リスクが規則とテストに到達したことを機械的に確認する。
- **成果物:** `traceability.md`（全方向トレース行列）＋ リスクレジスタークロージャ表。
- **依存:** Phase 0〜3。

### 作業内容・手順

1. **全方向トレース行列**を作る: `FR/NFR ↔ ADR ↔ UC ↔ (API 操作 / Task 規則) ↔ コンポーネント要求`。
   - **上位→下位**（要件が要求に落ちているか）と **下位→上位**（要求が要件に起因しているか）の**両方向**で孤立ゼロを確認。
2. **リスクレジスターのクロージャ**: 全 `R-00x` が「規則化済み（Phase 1/3）」**かつ**「テスト計画に到達（Phase 3/4）」であることを表で明記する。
3. **未解決質問レジスタ**を全 close、または明示的に **deferral（v2 へ）**にする。
4. 用語が全ドキュメント横断で一致するか最終確認。

### 検証観点

- **セルフチェック:**
  - [ ] トレース行列に**孤立項目ゼロ**（機械的に行列で確認）。
  - [ ] 全 `R-00x` が規則＋テストに到達（下表で確認）。
  - [ ] 未解決質問が全て close / deferral。
  - [ ] 用語が全ドキュメント横断で一致。
- **ユーザーレビュー:**
  - [ ] 全体として「設計完了」の判定。
  - [ ] deferral した項目の許容。
  - [ ] 次の工程（detailed-design / implementation）への手渡しが十分か。

- **DoD:** 孤立ゼロ・リスク全項目が規則＋テストに到達・未解決質問全解決/deferral・ユーザーが「設計完了」を承認。

### リスククロージャ表（テンプレート）

| リスク | 規則化 | 規則ID | テスト観点 | 到達フェーズ | 状態 |
|---|---|---|---|---|---|
| R-002-1 | 要確認 | | | | |
| R-006-1..4 | 要確認 | | | | |
| R-007-1..3 | 要確認 | | | | |
| R-008-1..3 | 要確認 | | | | |
| R-003-1..3 | 要確認 | | | | |

---

## 判断ログ（Decisions Log）

> ユーザーが判断した事項、または計画上で確定させた事項を記録する。
> **新セッションで再議論を防ぐために、ここに載っている限りは変更しない。**

| ID | 日付 | 決定内容 | 理由 | 状態 |
|---|---|---|---|---|
| D-001 | 2026-09-11 | 実行順序を **goal #3 → goal #2 →（挙動統合）→ goal #1** とする（= Phase 1a/1b を goal #1 より前に置く） | 割当て（goal #1）は検証対象であり、基準（API+Task/Job）が先にあると初めて検証できる。ADR が 80% 決めているため安く済む。 | ✅ 確定 |
| D-002 | 2026-09-11 | Datastore は公開 API なし（ODB の内部）。公開 API は Frontend↔ODB のみ | ADR-004（single writer・外部アクセス不可）。 | ✅ 確定 |
| D-003 | 2026-09-11 | 2 フォルダ統合は **案A**（`usecases/` を正、`usecase_analysis/` の良い部分を `UC_*` に吸収し削除/アーカイブ） | トレースが二重化しない（Q-005 の解消）。 | ✅ 確定 |
| D-004 | 2026-09-11 | ドキュメント新旧判定は **LSP の `version` フィールド（per-document の単調増加 revision カウンタ）** を dedup key / freshness / Datastore 同一性のキーに用いる。「安定したら version 付与」は任意の上位層（v1 不要、将来拡張） | dedup/freshness に必要なのは毎変更で変わる単調カウンターであり、LSP が既に `version` で提供。ラベル版 version はキーを複雑にするだけで利益が薄い（Q-002 の解消）。 | ✅ 確定 |
| D-005 | 2026-09-11 | **v1 スコープ** = didOpen/didChange/didClose（sync）、didChangeWatchedFiles+save（config）、**Hover**（depth0）、**Go-to-Definition**（depth1）、**Find References**（unbounded）、**Diagnostics**（server→client）。**v2（暫定・後で再提案）** = Completion / Rename / Document Symbols / Semantic Tokens（同一 parse/link コアの別結果型、メカニズム新要素が少ない） | 「サブコンポーネント要求が概ね抽出できる+多すぎない」を満たし、全負荷機構（request→task→job、dedup、priority、cancel、push-back、config-rebuild、unbounded policy、server→client）を網羅（Q-001 の解消）。v1 はユーザー確認済み。v2 は暫定で、再検証時に必要なら再提案する（ユーザーは現時点で希望なし）。 | ✅ 確定 |
| D-006 | 2026-09-11 | **Object Server は v1 から除外**（将来、同一 core の別 frontend） | ユーザー確認済み（Q-003 の解消）。 | ✅ 確定 |
| D-007 | 2026-09-11 | **starvation/unbounded/priority-inversion の policy は詳細設計へ defer**。v1 では「機構クラス」のみ名前を固定（R-007-1=age-demotion、R-007-2=size/time-bound、R-006-4=cancel-and-rerun）し、具体的な閾値/タイムアウトは後回し | これらは正解性ではなく生存性（liveness）であり、ADR 自身も「detailed-design input」と明記（Q-004 の解消）。 | ✅ 確定（deferred-by-design） |

---

## 未解決質問レジスタ（Open Questions）

> 私が勝手に仮定してよいものではない質問。`open` は**先にユーザーへ確認**すること。

| ID | 質問 | 関係フェーズ | 状態 | 回答 |
|---|---|---|---|---|
| Q-001 | v1 の機能スコープ | Phase 1b / 2 | ✅ answered（確認済み） | **D-005**: v1=sync+config+Hover+GoToDefinition+FindReferences+Diagnostics；v2=Completion/Rename/Symbols/SemanticTokens（暫定、再検証時に再提案） |
| Q-002 | ドキュメント新旧判定方式 | Phase 1a | ✅ answered | **D-004**: LSP `version`（単調増加 revision）をキーに用いる |
| Q-003 | Object Server は v1 除外でよいか | Phase 0 | ✅ answered | **D-006**: v1 除外 |
| Q-004 | starvation/unbounded の policy | Phase 1a | ✅ answered | **D-007**: 詳細設計へ defer、v1 では機構クラスのみ固定 |
| Q-005 | 2 フォルダ統合方針 | Phase 2 | ✅ answered | **D-003**: 案A |

---

## 運用方針（進め方の補足）

### セルフチェックの実施方針

1. **形式チェック（機械的）** — 全要求に ID が存在するか・重複がないか・トレース行列に孤立がないか。表形式で維持し、grep・集計で確認する。
2. **意味チェック（LLM レビュー）** — 充足性・意味的包含・一貫性・粒度・検証可能性。`.agents/checklists/Traceability Check Strategy.md` を指示書として用いる。
3. **各フェーズ末**に「Phase N 検証レポート」を短く出す（＝ユーザーレビューの入口）。

### 報告形式（各フェーズ完了時に毎回）

ユーザーへの報告は、次の 3 点セットにする:

1. **DoD 達成か**（達成/未達成＋理由）。
2. **見つけたギャップ**（不足・矛盾・矛盾しそうな点）。
3. **判断待ち**（ユーザーに決めてほしい質問）。

### 変更の取り扱い

- 後続フェーズで前フェーズの成果物を変更する場合は、**変更内容＋理由を判断ログに載せ**、該当するトレーサビリティを再実行する。
- ADR を修正する必要がある場合は、まずユーザーへ確認する（ADR は「戦略的決定」であり、勝手に書き換えない）。

### 進め方の補足アイデア（採用判断はユーザー）

- **Phase 1 の成果物（契約）を先に「スモーク検証」する** — 既解析 UC（open / hover / edit）で API と Task/Job ルールが足りるか確認してから確定する。過剰制約のリスクを下げる。
- **検証レポートを別ファイルに**（`verification/phase-<n>.md`）— 文書本体を汚さず、レビューの痕跡を残せる。
- **traceability.md を表（機械可読）で** — 孤立項目チェックを grep/集計で自動化できる形にする。
- **各コンポーネント要求に「テスト観点」列を** — Phase 4 のリスククロージャと直接繋がる。
