# System Architecture

> V1 系统架构：分层、依赖、数据流、模块职责。

---

## 分层架构

```
Presentation (apps/web)      → Next.js，纯 UI 渲染
    ↓
Application (apps/api)       → FastAPI，HTTP/WebSocket，业务协调
    ↓
AI Engine (packages/ai-engine) → Prompt / Context / LLM Gateway / Streaming
    ↓
Knowledge Core (packages/knowledge) → Parser / Chunk / Embedding / Retrieval
    ↓
Storage (PostgreSQL + PgVector + MinIO)
```

**规则：任何模块不能跨层访问。**

---

## 依赖关系

```
apps/web
    ↓  HTTP/WebSocket (CORS)
apps/api
    ↓  Python import
packages/ai-engine
    ↓  Python import
packages/knowledge
    ↓  SQLAlchemy
PostgreSQL + PgVector
```

```
apps/api → MinIO (原始文件读写)
```

**禁止：**
- `packages/knowledge` → `packages/ai-engine`（反向依赖）
- `apps/web` → Database（必须经过 API）
- `apps/api` → 直接操作数据库（必须经过 packages/knowledge）
- Application → 直接调用 LLM（必须经过 packages/ai-engine）

---

## Package 职责

### packages/knowledge（Knowledge Core）

```
Import → Parser → Normalization → Chunk → Embedding → Metadata → Storage → Index
                                                                          ↓
                                                                     Retrieval
```

**输入：** 文件（PDF/Markdown/TXT/DOCX）
**输出：** Chunk + Metadata + Source + Reference

**包含：**
- Document Import（接收、校验、存储原始文件到 MinIO，创建异步任务）
- Parser（Docling 统一解析为 Plain Text）
- Normalization（Unicode/空格/换行/编码规范化）
- Chunk（Sliding Window，chunk_size + chunk_overlap）
- Embedding（调用 Embedding Provider 生成向量）
- Metadata（Chunk ID / Document ID / Position / Title / Source / Page / Token Count）
- Storage（PostgreSQL 存 Metadata + PgVector 存向量）
- Retrieval（Question → Embedding → Similarity Search → Top K Chunk）
- Knowledge API（对外暴露的知识操作接口）

### packages/ai-engine（AI Engine）

```
Question → Query Preprocess → 调用 Knowledge.search() → Context Assemble → Prompt → LLM Gateway → Streaming
```

**输入：** 用户问题
**输出：** Streaming Response

**包含：**
- Query Preprocess（Trim / Normalize / Language Detect）
- Context Assemble（拼接 Knowledge 返回的 Chunk + Reference）
- Prompt Builder（System Prompt + Context + User Question + Output Format）
- LLM Gateway（Chat() / Stream()，V1 仅 DeepSeek Provider）
- Streaming（WebSocket / SSE）
- Error Handling（Provider Error / Timeout / Retry / Rate Limit）

### packages/shared

公共能力：Config / Logger / Exception / Utils / Common Types。

**不放业务逻辑。**

---

## 数据流

### Knowledge Flow（文档入库）

```
Upload → MinIO（存原始文件）
    ↓
返回 document_id（立即，状态 PENDING）
    ↓
BackgroundTask:
    Parser（Docling）→ Normalization → Chunk（Sliding Window）
    → Embedding（调用 Provider）→ 存入 PgVector
    → Metadata 存入 PostgreSQL
    → 状态更新 READY
```

### Search Flow（Knowledge Chat）

```
Question → AI Engine → Knowledge.search()
    ↓
Retriever: Question Embedding → PgVector Similarity Search → Top K Chunk
    ↓
AI Engine: Context Assemble → Prompt → DeepSeek → Streaming → Frontend
```

### Interview Flow

```
AI 根据知识库出题 → 用户回答 → Knowledge Retrieval → LLM 评价
```
