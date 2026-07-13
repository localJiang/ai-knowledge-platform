# Project Overview

> AI Knowledge Platform V1 — 浓缩版项目背景。5 分钟恢复认知。

---

## 项目定位

AI Knowledge Platform 是一个围绕 **知识管理、知识检索和 AI 应用** 构建的平台。

**核心公式：**

```
Document → Knowledge → Retrieval → AI Application
```

本项目**不是**：

- AI Agent 平台
- 通用 AI 项目模板
- 聊天机器人

---

## 核心模块（三大件）

```
Knowledge Core  →  负责知识（Parser / Chunk / Embedding / Retrieval）
     ↓
AI Engine       →  负责 AI（Prompt / LLM Gateway / Streaming）
     ↓
Application     →  负责业务（Knowledge Chat / AI Interview）
```

---

## V1 目标

完成一个可以真正使用的 Knowledge Platform MVP。

**包含：**

- Knowledge Core（知识生命周期管理）
- AI Engine（Prompt + LLM Gateway + Streaming）
- Knowledge Chat（用户提问 → 知识检索 → AI 回答）
- AI Interview（AI 出题 → 用户回答 → AI 评价）

**完整闭环：**

```
上传文档 → 解析 → Chunk → Embedding → 索引 → AI 检索 → AI 回答（流式输出 + 引用来源）
```

---

## V1 原则

1. **Knowledge First** — 知识库是核心，Application 只是使用者
2. **Thin First** — 最小可运行版本，不为未来设计
3. **Evolution** — 在上一版本基础上演进，不推翻架构
4. **Reuse** — 所有知识处理能力属于 Knowledge Core，可复用
5. **Single Responsibility** — 每个模块只做一件事

---

## V1 边界

**允许：**
- Knowledge Core、AI Engine、Knowledge Chat、AI Interview
- PostgreSQL + PgVector、MinIO、FastAPI BackgroundTasks
- REST API + WebSocket Streaming

**不允许：**
- Agent、Workflow、Memory、Planner、Tool Calling、MCP
- LangChain、LangGraph、GraphRAG、AutoGen
- 企业权限、多租户、多知识库
- Celery、Redis、GraphQL
- Dashboard、Settings 页面
- 多 LLM Provider 切换（V1 只用 DeepSeek）

---

## 依赖关系

```
apps/web (Next.js) → apps/api (FastAPI) → ai-engine → knowledge → database
```

- Knowledge Core 不依赖 AI Engine
- Application 不直接访问数据库
- AI Engine 是唯一允许调用 LLM 的模块
