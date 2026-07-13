# V1 Overview

> V1 总览：目标、范围、完成标准。所有开发以此为准。

---

## V1 目标

完成一个可以真正使用的 AI Knowledge Platform MVP。

## V1 范围

### 做什么

| 模块 | 内容 |
|------|------|
| Knowledge Core | Document Import、Parser（Docling）、Chunk（Sliding Window）、Embedding、Metadata、Retrieval、Vector Search |
| AI Engine | Query Preprocess、Context Assemble、Prompt Builder、LLM Gateway（DeepSeek）、Streaming |
| Knowledge Chat | 用户提问 → 知识检索 → AI 基于知识库回答 → Streaming 返回 + 引用来源 |
| AI Interview | AI 根据知识库出题 → 用户回答 → AI 评价 |
| Infrastructure | PostgreSQL + PgVector、MinIO、FastAPI BackgroundTasks、Docker Compose |

### 不做什么

- Agent / Workflow / Memory / Planner / Tool Calling / Multi Agent / MCP
- LangChain / LangGraph / GraphRAG / AutoGen
- 企业权限 / 多租户 / 多知识库
- Celery / Redis / GraphQL
- Dashboard / Settings 页面
- 多 LLM Provider 切换（V1 只用 DeepSeek）
- Semantic Chunk / Heading Aware Chunk
- 自动评分 / 学习计划 / 错题本

---

## V1 完成标准（Definition of Done）

用户可以完成以下完整流程：

```
上传文档（PDF/Markdown/TXT/DOCX）
    ↓
系统异步解析（状态轮询 PENDING → PROCESSING → READY）
    ↓
建立索引（知识可搜索）
    ↓
Knowledge Chat：用户提问 → AI 基于知识库回答 → Streaming 返回 → 显示引用来源
    ↓
AI Interview：AI 根据知识库出题 → 用户回答 → AI 评价
```

整个流程无需人工介入，即可完成。

---

## 前端页面（V1 只有两个）

| 页面 | 功能 |
|------|------|
| Upload | 文件上传 + 知识列表 + 状态查看（PENDING/PROCESSING/READY/FAILED） |
| Interview | Knowledge Chat 对话 + AI Interview 问答（同一页面切换模式） |

---

## API 端点（V1 总计 7 个）

| 方法 | 路径 | 用途 |
|------|------|------|
| POST | `/knowledge/upload` | 上传文档 |
| GET | `/knowledge` | 知识列表 |
| GET | `/knowledge/{id}` | 文档详情 + 状态 |
| DELETE | `/knowledge/{id}` | 删除文档 |
| POST | `/knowledge/search` | 知识搜索 |
| POST | `/chat` | Knowledge Chat |
| WS | `/ws/chat` | Chat Streaming |
| POST | `/interview/next-question` | 获取下一题 |
| POST | `/interview/evaluate` | 提交回答并评价 |
| WS | `/ws/interview` | Interview Streaming |

---

## 开发顺序

1. Monorepo 初始化 → 2. Backend 骨架 → 3. Database → 4. Knowledge Core → 5. AI Engine → 6. Frontend → 7. Chat + Interview → 8. Docker Compose → 9. Integration → 10. Testing

**Knowledge Core 完成之前，不开发 Interview。**
