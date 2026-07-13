# V1 Task Breakdown

> V1 有序任务清单。每个 Task 有明确的依赖、规格引用和完成标准。

---

## Task 状态说明

- `[ ]` Pending — 未开始
- `[~]` In Progress — 进行中
- `[x]` Done — 已完成

---

## Phase 1: Monorepo 初始化

### Task 1.1: Monorepo 骨架

**依赖：** 无
**规格：** `context/tech-stack.md`
**产出：**

- [ ] `turbo.json` — Turborepo 任务编排
- [ ] `pnpm-workspace.yaml` — pnpm workspace
- [ ] `pyproject.toml` — uv Python 依赖
- [ ] `Makefile` — 统一开发命令（`make dev` / `make build` / `make test` / `make lint`）
- [ ] `apps/web/` — Next.js 项目初始化
- [ ] `apps/api/` — FastAPI 项目骨架
- [ ] `packages/knowledge/` — Python package 骨架
- [ ] `packages/ai-engine/` — Python package 骨架
- [ ] `packages/shared/` — Python package 骨架
- [ ] `.gitignore` — 已有

**完成标准：** `make dev` 可同时启动 web + api（空项目）

---

## Phase 2: Backend 骨架

### Task 2.1: FastAPI 应用骨架

**依赖：** Task 1.1
**规格：** `specs/current/architecture.md`

**产出：**

- [ ] FastAPI app 创建
- [ ] CORS 配置
- [ ] Router 注册结构
- [ ] 健康检查端点 `GET /health`
- [ ] 错误处理中间件

**完成标准：** `GET /health` 返回 200

### Task 2.2: Shared Package

**依赖：** Task 1.1
**规格：** `specs/current/architecture.md`

**产出：**

- [ ] Config（环境变量读取）
- [ ] Logger（统一格式，禁止 print）
- [ ] Exception（统一异常类）
- [ ] Common Types

**完成标准：** packages/shared 可被其他包 import

---

## Phase 3: Database

### Task 3.1: PostgreSQL + PgVector 环境

**依赖：** Task 1.1
**规格：** `context/tech-stack.md`

**产出：**

- [ ] `docker/compose.yaml` — postgres 服务
- [ ] `docker/postgres/init.sql` — 启用 PgVector 扩展
- [ ] 数据库连接配置（环境变量）

**完成标准：** `make dev` 启动 postgres，PgVector 扩展可用

### Task 3.2: ORM + Migration

**依赖：** Task 2.1, 3.1
**规格：** `specs/current/data-model.md`

**产出：**

- [ ] SQLAlchemy Base + async engine
- [ ] Document Model
- [ ] Chunk Model（含 PgVector 列）
- [ ] ChatSession / ChatMessage Model
- [ ] InterviewSession / InterviewQA Model
- [ ] Alembic 初始 migration
- [ ] Repository 层（document_repo / chunk_repo）

**完成标准：** migration 执行成功，所有表创建

---

## Phase 4: Knowledge Core

### Task 4.1: File Storage

**依赖：** Task 2.1
**规格：** `specs/current/knowledge-core.md`

**产出：**

- [ ] `FileStorage` 抽象接口
- [ ] `LocalFileStorage` 实现
- [ ] `MinioFileStorage` 实现（Docker Compose 加 MinIO 服务）
- [ ] 文件保存/读取/删除

**完成标准：** 可上传文件到本地/MinIO 并读取回来

### Task 4.2: Parser + Normalizer

**依赖：** Task 2.1
**规格：** `specs/current/knowledge-core.md`

**产出：**

- [ ] `Parser` 类（封装 Docling）
- [ ] `Normalizer` 类（Unicode/空格/换行/编码）
- [ ] 支持 PDF/Markdown/TXT/DOCX 四种格式

**完成标准：** 上传 PDF → 输出规范化纯文本

### Task 4.3: Chunker

**依赖：** Task 4.2
**规格：** `specs/current/knowledge-core.md`

**产出：**

- [ ] `Chunker` 类（Sliding Window）
- [ ] `chunk_size` / `chunk_overlap` 可配置
- [ ] Token Count 计算

**完成标准：** 纯文本 → Chunk 列表（含 token count）

### Task 4.4: Embedder + VectorStore

**依赖：** Task 3.2, 4.3
**规格：** `specs/current/knowledge-core.md`

**产出：**

- [ ] `Embedder` 类（调用 Embedding API）
- [ ] `VectorStore` 类（PgVector 操作封装）
- [ ] insert / search / delete_by_document

**完成标准：** 文本 → Embedding → 存入 PgVector → Similarity Search 返回结果

### Task 4.5: Indexer

**依赖：** Task 4.1, 4.2, 4.3, 4.4
**规格：** `specs/current/knowledge-core.md`

**产出：**

- [ ] `Indexer` 类（编排 ingest 流程）
- [ ] Document Status 更新
- [ ] 错误处理（失败 → FAILED + error_message）

**完成标准：** 上传文件 → BackgroundTask → PENDING → PROCESSING → READY（或 FAILED）

### Task 4.6: Retriever + Knowledge API

**依赖：** Task 4.4, 4.5
**规格：** `specs/current/knowledge-core.md`

**产出：**

- [ ] `Retriever` 类（query → embedding → search → Top K）
- [ ] `KnowledgeAPI` 类（对外统一接口）
- [ ] `import_document` / `get_document` / `list_documents` / `delete_document` / `search`

**完成标准：** 通过 KnowledgeAPI 完整走通 import → search 流程

---

## Phase 5: AI Engine

### Task 5.1: LLM Gateway

**依赖：** Task 2.1
**规格：** `specs/current/ai-engine.md`

**产出：**

- [ ] `LLMProvider` 抽象接口
- [ ] `DeepSeekProvider` 实现
- [ ] `LLMGateway`（chat + stream）
- [ ] 错误处理（Timeout / Retry / Rate Limit）

**完成标准：** 调用 DeepSeek API 返回回答

### Task 5.2: Prompt Builder + Context Builder

**依赖：** Task 4.6, 5.1
**规格：** `specs/current/ai-engine.md`

**产出：**

- [ ] `QueryProcessor`（V1 简单预处理）
- [ ] `ContextBuilder`（拼接 Chunk 为 LLM 上下文）
- [ ] `PromptBuilder`（chat / interview_question / interview_evaluate 三套模板）
- [ ] `StreamHandler`（流式输出处理）

**完成标准：** 输入 query → 返回组装好的 Prompt + Context

### Task 5.3: AI Engine API

**依赖：** Task 5.2
**规格：** `specs/current/ai-engine.md`

**产出：**

- [ ] `AIEngineAPI` 类
- [ ] `chat()` — 非流式 Chat
- [ ] `chat_stream()` — 流式 Chat
- [ ] `generate_question()` — Interview 出题
- [ ] `evaluate_answer()` — Interview 评价

**完成标准：** 通过 AIEngineAPI 走通 Chat 和 Interview 流程

---

## Phase 6: API Routes

### Task 6.1: Knowledge Routes

**依赖：** Task 4.6
**规格：** `specs/current/api-spec.md`

**产出：**

- [ ] `POST /knowledge/upload` — 上传 + 启动 BackgroundTask
- [ ] `GET /knowledge` — 列表
- [ ] `GET /knowledge/{id}` — 详情 + 状态
- [ ] `DELETE /knowledge/{id}` — 删除
- [ ] `POST /knowledge/search` — 搜索

**完成标准：** 所有 Knowledge 端点可用

### Task 6.2: Chat Routes

**依赖：** Task 5.3
**规格：** `specs/current/api-spec.md`

**产出：**

- [ ] `POST /chat` — 非流式 Chat
- [ ] `WebSocket /ws/chat` — 流式 Chat
- [ ] Session 管理（新建/继续）

**完成标准：** Chat 端点可用，流式返回正常

### Task 6.3: Interview Routes

**依赖：** Task 5.3
**规格：** `specs/current/api-spec.md`

**产出：**

- [ ] `POST /interview/next-question` — 获取题目
- [ ] `POST /interview/evaluate` — 提交评价
- [ ] `WebSocket /ws/interview` — 流式评价

**完成标准：** Interview 端点可用

---

## Phase 7: Frontend

### Task 7.1: Upload Page

**依赖：** Task 6.1
**规格：** `specs/current/frontend.md`

**产出：**

- [ ] 文件拖拽上传组件
- [ ] 文档列表展示（表格/卡片）
- [ ] 状态轮询（PENDING → PROCESSING → READY）
- [ ] 删除功能
- [ ] TanStack Query 集成

**完成标准：** 可上传文件并看到处理状态变化

### Task 7.2: Interview Page

**依赖：** Task 6.2, 6.3
**规格：** `specs/current/frontend.md`

**产出：**

- [ ] Chat 模式（消息列表 + 输入 + Streaming 显示 + 引用来源）
- [ ] Interview 模式（AI 出题 + 回答输入 + 流式评价 + 来源引用）
- [ ] 模式切换
- [ ] 新建会话
- [ ] WebSocket 连接管理

**完成标准：** Chat 和 Interview 完整流程可用

---

## Phase 8: Docker Compose

### Task 8.1: 完整 Docker Compose

**依赖：** Task 7.2
**规格：** `context/tech-stack.md`

**产出：**

- [ ] `docker/compose.yaml` — api + web + postgres + minio
- [ ] 各服务 Dockerfile（如需要）
- [ ] `.env.example`

**完成标准：** `docker compose up` 一键启动全栈

---

## Phase 9: Integration & Testing

### Task 9.1: 端到端集成测试

**依赖：** Task 8.1

**产出：**

- [ ] 上传文档 → 等待 READY → Chat 提问 → 验证引用来源
- [ ] 上传文档 → 等待 READY → Interview 出题 → 回答 → 验证评价
- [ ] 错误场景测试（上传不支持格式、删除文档、LLM 错误处理）

**完成标准：** V1 DOD 全部满足

---

## 依赖关系图

```
1.1 Monorepo
    ├── 2.1 FastAPI ── 2.2 Shared
    │       └── 6.1 Knowledge Routes ── 6.2 Chat Routes ── 6.3 Interview Routes
    │               ↑                        ↑                    ↑
    ├── 3.1 PostgreSQL ── 3.2 ORM           │                    │
    │       └── 4.4 Embedder+Vector         │                    │
    │               └── 4.5 Indexer ── 4.6 Retriever+API ───────┘
    │                       ↑                                       
    ├── 4.1 FileStorage ────┤                                       
    ├── 4.2 Parser+Normalizer ── 4.3 Chunker ─┘                                       
    │                                                       
    └── 5.1 LLM Gateway ── 5.2 Prompt+Context ── 5.3 AI Engine API
                                                                    ↓
    7.1 Upload Page ←──────────────────────────────────────────────┘
    7.2 Interview Page ←────────────────────────────────────────────┘
        └── 8.1 Docker Compose ── 9.1 Integration Testing
```

---

## 开发规则

1. **严格按 Phase 顺序** — Knowledge Core 完成之前不开发 Interview
2. **每完成一个 Task 勾选 `[x]`**
3. **遇到问题在 Task 下方加备注**
4. **不要跨 Task 开发**
