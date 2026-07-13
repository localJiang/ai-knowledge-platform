# Data Model

> V1 数据库 Entity、表结构、字段、关系。

---

## ER 概览

```
Document (1) ────── (N) Chunk
    │
    └── status: PENDING | PROCESSING | READY | FAILED

ChatSession (1) ── (N) ChatMessage

InterviewSession (1) ── (N) InterviewQA
```

---

## Document

知识文档，对应一个上传的原始文件。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| filename | VARCHAR(512) | 原始文件名 |
| file_type | VARCHAR(32) | PDF / MARKDOWN / TXT / DOCX |
| file_size | BIGINT | 字节数 |
| storage_path | VARCHAR(1024) | MinIO/本地存储路径 |
| status | VARCHAR(32) | PENDING / PROCESSING / READY / FAILED |
| error_message | TEXT | 失败原因（status=FAILED 时） |
| chunk_count | INTEGER | Chunk 数量（处理完成后填充） |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

**索引：** `idx_document_status ON (status)`

---

## Chunk

文档切片，每个 Chunk 对应一个 Embedding 向量。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| document_id | UUID | FK → Document.id |
| chunk_index | INTEGER | 在文档中的顺序位置 |
| content | TEXT | Chunk 文本内容 |
| token_count | INTEGER | Token 数量 |
| metadata | JSONB | 结构化元数据 |
| embedding | vector(1536) | PgVector 向量（维度取决于 Embedding 模型） |
| created_at | TIMESTAMP | 创建时间 |

**metadata JSONB 结构：**

```json
{
  "title": "章节标题",
  "source": "document.pdf",
  "page": 1,
  "heading_path": ["Chapter 1", "Section 1.1"]
}
```

**索引：**
- `idx_chunk_document_id ON (document_id)`
- PgVector 向量索引（IVFFlat 或 HNSW）

---

## ChatSession

Knowledge Chat 会话。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| title | VARCHAR(256) | 会话标题（取第一个问题摘要） |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 最后活跃时间 |

---

## ChatMessage

Chat 会话中的一条消息。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| session_id | UUID | FK → ChatSession.id |
| role | VARCHAR(16) | user / assistant |
| content | TEXT | 消息内容 |
| references | JSONB | 引用的 Chunk 来源 |
| created_at | TIMESTAMP | 消息时间 |

**references JSONB 结构：**

```json
[
  {
    "chunk_id": "uuid",
    "document_id": "uuid",
    "filename": "doc.pdf",
    "content_snippet": "引用的片段...",
    "page": 1
  }
]
```

---

## InterviewSession

AI Interview 会话。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| title | VARCHAR(256) | 会话标题 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 最后更新时间 |

---

## InterviewQA

Interview 中的一轮问答。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| session_id | UUID | FK → InterviewSession.id |
| question | TEXT | AI 出的题 |
| answer | TEXT | 用户回答 |
| evaluation | TEXT | AI 评价 |
| references | JSONB | 评价引用的 Chunk 来源 |
| created_at | TIMESTAMP | 创建时间 |

---

## V1 不实现的表

以下模型 V3 才需要，V1 不创建：

- **User** — V1 无多用户
- **Project / Workspace** — V1 只有一个知识库
- **Permission / Role** — V1 无权限
- **Memory** — V3

---

## Migration 策略

- 使用 Alembic 管理 migration
- 初始 migration 包含以上所有表的创建 + PgVector 扩展启用
- 后续 schema 变更使用增量 migration
