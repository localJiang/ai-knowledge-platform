# AI Knowledge Platform

## Project Position

AI Knowledge Platform 是一个围绕知识管理、知识检索和 AI 应用构建的平台。

本项目不是 AI Agent 平台，不是通用 AI 项目模板。

整个项目的核心始终围绕：

Document → Knowledge → Retrieval → AI Application

所有未来功能都建立在 Knowledge Core 之上。

---

# Vision

建立一个可持续扩展的 AI 知识平台。

平台负责：

- 获取知识
- 解析知识
- 管理知识
- 检索知识
- 基于知识构建 AI 应用

Knowledge Core 是整个系统最核心的模块。

未来新增任何应用，都应该复用 Knowledge Core，而不是重新实现知识处理流程。

---

# Project Scope

项目仅围绕 AI Knowledge Platform。

不要为了未来其它 AI 项目做抽象。

不要设计 AI Project Template。

不要增加与知识平台无关的模块。

整个项目始终保持职责单一。

---

# Product Evolution

## V1

目标：

完成一个可以真正使用的 Knowledge Platform MVP。

包含：

- Knowledge Core
- Thin AI Engine
- Knowledge Chat（用户问 AI 答）
- AI Interview（AI 问用户答再评价）

形成完整闭环：

上传文档

↓

解析文档

↓

建立知识库

↓

AI 检索知识

↓

Knowledge Chat：AI 回答

↓

AI Interview：AI 出题 + 评价

V1 不考虑企业能力。

不考虑 Agent。

不考虑复杂 Workflow。

只保证整个知识平台流程跑通。

---

## V2

目标：

从一个 AI 应用扩展到多个学习应用。

新增：

- AI Tutor
- AI Notes
- URL Import
- Hybrid Search
- Redis Cache
- Docker Production

Knowledge Core 保持不变。

AI Engine 小幅增强。

Application 增加。

---

## V3

目标：

升级为企业级 AI Knowledge Platform。

新增：

- 企业知识库
- 多知识库管理
- 权限系统
- Workflow
- Memory
- 更完善的 AI Engine

Knowledge Core 继续作为唯一知识来源。

所有企业能力都建立在现有架构之上。

---

# Product Principles

整个项目遵循以下原则。

## Knowledge First

知识库永远是核心。

Application 只是 Knowledge 的使用者。

不要让业务直接操作数据库。

不要绕过 Knowledge Core。

---

## Thin First

先实现最小可运行版本。

不要提前实现未来能力。

不要因为 V3 而增加 V1 的复杂度。

---

## Evolution Instead Of Rewrite

每个版本都在上一版本基础上演进。

不要推翻已有架构。

不要为了新功能重新设计整个系统。

---

## Reuse

所有知识处理能力必须可复用。

Parser、Chunk、Embedding、Retriever 等能力不能属于某一个 Application。

这些能力属于 Knowledge Core。

---

## Single Responsibility

Knowledge Core：

只负责知识。

AI Engine：

只负责 AI 调用。

Application：

只负责业务。

保持职责清晰。

---

# V1 Boundary

V1 只允许实现：

- Knowledge Core
- Thin AI Engine
- Knowledge Chat
- AI Interview

V1 不允许实现：

- Workflow
- Planner
- Memory
- Tool Calling
- Multi Agent
- MCP
- GraphRAG
- LangGraph
- 企业权限
- 多租户

这些全部属于后续版本。

---

# Current Goal

当前唯一目标：

完成 V1。

不要设计未来。

不要优化未来。

不要提前实现未来。

所有设计均以：

"帮助 Claude Code 高质量完成 V1"

作为唯一标准。

# System Architecture

## Overall Architecture

整个项目采用 Monorepo。

```
ai-knowledge-platform/

apps/
packages/
docker/
scripts/
.ai/
```

各目录职责：

apps

负责运行程序。

包括：

- Web
- API

packages

负责所有可复用业务能力。

任何业务逻辑都应该优先放入 packages。

apps 仅作为运行入口。

docker

部署配置。

scripts

初始化、迁移、工具脚本。

.ai

Claude Code 开发规范。

不是业务代码。

---

# Package Architecture

V1 包含三个 Package。

```
packages/

knowledge/

ai-engine/

shared/
```

## knowledge

负责整个知识库。

包括：

- 文档解析
- Chunk
- Embedding
- Metadata
- 检索
- Knowledge API

它是整个系统最重要的 Package。

以后所有 AI 应用都依赖它。

---

## ai-engine

负责：

AI 调用能力。

包括：

- Prompt
- Context Assemble
- LLM Gateway
- Streaming

不负责知识管理。

不负责数据库。

不负责业务。

---

## shared

公共能力。

例如：

- Config
- Logger
- Utils
- Common Types
- Exception

只允许放真正公共内容。

---

# Apps

## apps/web

Next.js。

职责：

用户界面。

两个核心页面：

- Upload（上传 + 知识管理）
- Interview（Knowledge Chat + AI Interview）

它不包含任何业务逻辑。

所有业务全部调用 API。

## apps/api

FastAPI。

职责：

HTTP API。

WebSocket。

鉴权。

调用 Packages。

Router 不允许写业务逻辑。

## 为什么是 Next.js + FastAPI

V1：

Browser 直接调用 FastAPI。

开启 CORS。

不增加 BFF 层。

原因：

Knowledge Core 基于 Python AI 生态：

- Docling（文档解析）
- Embedding 模型
- OCR 等

这些能力只有 Python 侧能提供。

Next.js 负责纯 UI 渲染。FastAPI 负责所有后端能力。

V2 如有需要再考虑 BFF。

---

# Dependency

依赖关系固定。

```
apps/web

↓

apps/api

↓

packages/ai-engine

↓

packages/knowledge

↓

database
```

禁止反向依赖。

---

Knowledge Core

不能依赖

AI Engine。

---

AI Engine

可以依赖

Knowledge。

---

Application

只能依赖

AI Engine。

不能直接访问

Knowledge Database。

---

# Layer

整个系统分四层。

```
Presentation

↓

Application

↓

AI Engine

↓

Knowledge Core

↓

Storage
```

---

Presentation

负责：

UI。

Application

负责：

业务。

AI Engine

负责：

AI。

Knowledge Core

负责：

知识。

Storage

负责：

存储。

任何模块都不能跨层访问。

---

# Knowledge Flow

知识进入系统：

```
Upload

↓

Parser

↓

Chunk

↓

Embedding

↓

Metadata

↓

Storage

↓

Index Finished
```

Knowledge Core 完成整个流程。

AI Engine 不参与。

---

# Search Flow (Knowledge Chat)

用户搜索：

```
Question

↓

Retriever

↓

Top K

↓

Context Assemble

↓

Prompt

↓

LLM

↓

Streaming

↓

Frontend
```

Retriever 属于 Knowledge。

Prompt 属于 AI Engine。

LLM 属于 AI Engine。

---

# Knowledge Core

Knowledge Core 是整个系统唯一负责知识管理的模块。

它负责：

- Document
- Chunk
- Embedding
- Metadata
- Retrieval
- Search

以后任何 Application：

都不能重新实现这些能力。

---

# Thin AI Engine

AI Engine 是一层很薄的中间层。

作用：

连接：

Knowledge

与

LLM。

它不是 Agent。

它没有：

Workflow。

没有：

Planner。

没有：

Memory。

没有：

Tool Calling。

它只负责：

```
Knowledge

↓

Context

↓

Prompt

↓

LLM

↓

Response
```

未来升级：

只增强这一层。

Knowledge Core 不需要修改。

---

# Applications

V1 包含两个：

```
Knowledge Chat

AI Interview
```

以后增加：

```
AI Tutor

AI Notes

Enterprise Search

Learning Assistant
```

这些全部属于：

Application。

它们共享：

Knowledge Core。

共享：

AI Engine。

不要复制知识处理流程。

---

# Storage

V1：

使用：

PostgreSQL

+

PgVector

对象文件：

MinIO

Storage 不直接提供业务能力。

所有访问：

经过 Knowledge Core。

---

# Future Evolution

未来新增任何应用。

必须满足：

```
Application

↓

AI Engine

↓

Knowledge Core
```

不能绕过。

Knowledge Core 永远保持唯一知识来源。

整个系统始终围绕这一架构演进。

禁止为了新应用破坏现有层级。

# Tech Stack

## Design Principles

技术选型遵循以下原则：

1. 优先成熟稳定。
2. 优先本地可部署。
3. 尽量减少框架耦合。
4. 可逐步升级，不推翻重构。
5. Knowledge Core 与 AI Provider 解耦。

整个项目尽量避免"大而全"框架。

例如：

- LangChain
- LangGraph
- AutoGen

V1 均不作为核心依赖。

它们可以作为未来可选能力，而不是架构基础。

---

# Frontend

V1 使用：

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- TanStack Query
- Zustand

职责：

两个核心页面：

- Upload
- Interview

Frontend 不负责：

Embedding。

Chunk。

Prompt。

Retriever。

这些全部属于 Backend。

---

# Backend

V1 使用：

FastAPI。

职责：

HTTP API。

WebSocket。

业务协调。

调用：

Knowledge Core

AI Engine

Backend 不保存业务状态。

业务能力全部放入 packages。

---

# Database

V1：

PostgreSQL。

作用：

保存：

Document。

Chunk Metadata。

Knowledge。

History。

Configuration。

Project。

User。

以后如果增加业务。

仍然继续使用 PostgreSQL。

它始终是唯一关系数据库。

---

# Vector Database

V1：

PgVector。

作用：

保存：

Embedding。

Similarity Search。

Top K Retrieval。

选择 PgVector 原因：

- 与 PostgreSQL 集成。
- 部署简单。
- 数据一致性高。
- V1 数据量足够。

未来如果数据规模扩大。

允许升级：

Qdrant。

升级时：

Knowledge Core 对外接口保持一致。

Application 不需要修改。

---

# Object Storage

V1：

MinIO。

作用：

保存原始文件。

例如：

PDF。

Word。

Markdown。

Image。

Audio。

Knowledge Core 保存：

Metadata。

Storage 保存：

文件。

不要把文件直接存数据库。

## 为什么保留原始文件

- 支持重新解析（Chunk 策略升级后无需重新上传）
- 支持重新 Embedding（模型升级后无需重新上传）
- 方便排查问题（对比原始文件和解析结果）
- 后续支持 OCR、图片提取等能力

## 开发环境

本地开发使用本地文件系统。

接口与 MinIO 保持一致。

生产环境切换 MinIO，无需修改业务代码。

---

# Cache

V1：

不启用。

V2：

增加：

Redis。

用于：

热门检索。

Session。

Streaming。

缓存。

不要提前引入。

---

# LLM

AI Engine 不绑定具体模型。

统一：

LLM Gateway。

## V1

只接入一个 Provider：

DeepSeek。

保留统一 LLMProvider 接口。

不实现多 Provider 切换。

## V2+

增加多模型支持：

OpenAI。

Claude。

Gemini。

Qwen。

GLM。

以后增加 Provider，Application 不需要修改，Knowledge Core 不需要修改。

---

# Embedding

Embedding Provider。

独立抽象。

支持：

OpenAI Embedding。

BGE。

Jina。

Nomic。

未来：

允许切换。

Knowledge Core 不依赖具体模型。

---

# Document Parser

V1：

单一入口，使用 Docling。

```
parser.parse(file)
    ↓
Docling
```

不实现 Factory / Registry / Plugin 体系。

V2+ 如有格式不支持，再演进为 Provider 模式。

统一输出：Plain Text。

---

# Monorepo

固定：

```
apps/

packages/

docker/

scripts/

.ai/
```

apps：

运行。

packages：

业务。

docker：

部署。

scripts：

工具。

.ai：

开发规范。

禁止：

业务代码进入：

.ai。

## Monorepo 工具

V1 采用：

- **Turborepo**：任务编排（build / dev / lint 统一调度）
- **pnpm workspace**：Node.js 依赖管理（apps/web）
- **uv**：Python 依赖管理（apps/api + packages/*）

Turborepo 负责跨语言任务的编排，不参与依赖安装本身。

Polyglot Monorepo 中，依赖安装由各自工具负责。

---

# Docker

V1：

Docker Compose。

包含：

api。

web。

postgres。

minio。

后续：

redis。

worker。

qdrant。

均允许增加。

不要影响已有服务。

---

# Environment

统一：

.env。

不要在代码中写：

Provider。

API Key。

Database。

全部读取：

Environment。

---

# ORM

SQLAlchemy。

职责：

数据库访问。

Repository。

Migration。

不要在 Router 写 SQL。

不要在 Frontend 写 SQL。

---

# API

统一：

REST。

Streaming：

WebSocket。

不要设计：

GraphQL。

V1：

保持简单。

---

# Logging

统一 Logger。

不要：

print。

日志：

集中输出。

方便以后：

Docker。

Kubernetes。

ELK。

接入。

---

# Deployment

V1：

Docker Compose。

↓

Ubuntu。

V2：

允许：

Nginx。

HTTPS。

CI/CD。

GitHub Actions。

不要影响：

代码结构。

---

# Why Not LangChain

V1：

不依赖 LangChain。

原因：

Knowledge Core。

AI Engine。

均自行实现。

避免：

框架限制。

未来如果：

LangChain。

能够降低维护成本。

允许：

在 AI Engine 内部接入。

不允许：

Knowledge Core 依赖：

LangChain。

Knowledge Core 应保持纯净。

---

# Upgrade Strategy

整个项目遵循：

Replace。

而不是：

Rewrite。

例如：

PgVector

↓

Qdrant。

OpenAI

↓

Claude。

DeepSeek。

Parser。

↓

Docling。

↓

其它 Parser。

整个系统：

接口保持一致。

Application 无需修改。

Knowledge Core 尽量保持稳定。

# Knowledge Core

## Position

Knowledge Core 是整个 AI Knowledge Platform 的核心。

负责：

Document

↓

Knowledge

↓

Retrieval

它不负责：

LLM。

Prompt。

Workflow。

Memory。

Application。

Knowledge Core 应保持独立。

任何 AI Application 都应复用它，而不是重新实现知识处理流程。

---

# Responsibilities

Knowledge Core 包含：

- Document Import
- Parser
- Chunk
- Embedding
- Metadata
- Storage
- Retrieval
- Search

Knowledge Core 不关心：

谁在使用知识。

它只负责：

知识如何进入系统。

知识如何被检索。

---

# Pipeline

知识进入平台：

```
Document

↓

Import

↓

Parser

↓

Chunk

↓

Embedding

↓

Metadata

↓

Storage

↓

Index Complete
```

整个流程由 Knowledge Core 完成。

---

# Document Import

作用：

负责导入知识。

V1 支持：

- PDF
- Markdown
- TXT
- DOCX

未来：

- HTML
- URL
- Notion
- Obsidian
- Git Repository
- Confluence
- Wiki

Import 不解析内容。

只负责：

接收。

校验。

存储文件。

创建异步任务。

## Ingest 异步流程

Ingest 是长耗时流程（尤其 Embedding 调用外部 API）。

V1：

使用 FastAPI BackgroundTasks。

```
Upload
    ↓
返回 document_id (立即)
    ↓
BackgroundTask
    ↓
Parser
    ↓
Chunk
    ↓
Embedding
    ↓
Index
    ↓
更新状态
```

Document Status：

- PENDING
- PROCESSING
- READY
- FAILED

前端轮询 GET /knowledge/{id} 查看状态。

V1 不引入 Celery / Redis。

V2 升级为 Celery + Redis。

---

# Parser

Parser 负责：

把不同文件。

统一转换成：

标准文本。

输出：

```
Document

↓

Paragraph

↓

Plain Text
```

Parser 不负责：

Chunk。

Embedding。

Retrieval。

Parser 是可替换模块。

## V1

只保留一个 Parser 入口：

```
parser.parse(file)
    ↓
Docling
```

不实现：

- Factory
- Registry
- Plugin 体系

V1 Docling 已覆盖 PDF/Markdown/TXT/DOCX。

## V2+

如果某种格式 Docling 支持不好。

允许增加：

- PyMuPDF
- python-docx
- Markdown Parser
- Unstructured

届时再演进为 Provider 模式。

---

# Normalization

Parser 完成后：

统一进行文本规范化。

包括：

- Unicode
- 空格
- 换行
- 编码
- 标题
- 列表
- 表格

目标：

保证后续 Chunk 一致。

---

# Chunk

Chunk 是整个知识平台最重要的能力之一。

作用：

把长文本。

切成适合 Embedding 的片段。

## V1 Chunk Strategy

V1 使用最简单方案：

- Sliding Window
- chunk_size（可配置）
- chunk_overlap（可配置）

不实现：

- Semantic Chunk
- Heading Aware
- Document Tree
- 跨章节感知

这些属于 V2。

## V2 升级

以后允许升级为语义感知 Chunk：

```
Document

↓

Heading

↓

Paragraph

↓

Sentence

↓

Chunk
```

V1 先保证能跑通。

---

# Chunk Metadata

每一个 Chunk。

必须保存：

- Chunk ID
- Document ID
- Position
- Title
- Source
- Page
- Token Count

以后：

Retriever。

引用。

全部依赖 Metadata。

---

# Embedding

Embedding 负责：

把 Chunk。

转换成向量。

```
Chunk

↓

Embedding Model

↓

Vector
```

Knowledge Core 不绑定：

OpenAI。

BGE。

Jina。

统一：

Embedding Provider。

以后允许切换模型。

---

# Storage

Storage 分两部分。

## Metadata

保存：

PostgreSQL。

包括：

Document。

Chunk。

Tag。

Project。

History。

Metadata。

---

## Vector

保存：

PgVector。

包括：

Embedding。

Similarity。

以后：

允许升级：

Qdrant。

Knowledge Core 外部接口保持一致。

---

# Index

当：

Embedding 完成。

表示：

Knowledge Ready。

此时：

知识可以搜索。

Index 不属于 AI Engine。

属于：

Knowledge Core。

---

# Retrieval

Retriever：

负责知识检索。

流程：

```
Question

↓

Embedding

↓

Similarity Search

↓

Top K Chunk

↓

Return
```

Retriever 不负责：

Prompt。

LLM。

Answer。

只负责：

找到最相关知识。

---

# Search Strategy

V1：

使用：

Vector Search。

以后：

增加：

Hybrid Search。

包括：

Keyword。

BM25。

Vector。

最终：

融合排序。

V1 不提前实现。

---

# Ranking

Retriever 返回：

Top K。

默认：

按相似度排序。

以后：

增加：

ReRank。

V1：

保持简单。

---

# Context

Knowledge Core 返回：

Chunk。

Metadata。

Source。

Reference。

不生成：

Prompt。

Prompt 属于：

AI Engine。

---

# Knowledge Update

新增文档：

重新：

Parser。

Chunk。

Embedding。

更新：

Index。

删除文档：

删除：

Metadata。

Vector。

Storage。

保持一致。

---

# Knowledge Isolation

V1：

只有一个 Knowledge Base。

不实现：

- 多知识库隔离
- Tenant
- Workspace
- Organization
- 权限

V3 企业版再扩展这些能力。

---

# Responsibilities Summary

Knowledge Core 只负责：

```
Import

↓

Parser

↓

Chunk

↓

Embedding

↓

Storage

↓

Retrieval
```

任何：

LLM。

Prompt。

Workflow。

Agent。

均不属于：

Knowledge Core。

Knowledge Core 永远保持纯净。

---

# Design Principles

Knowledge Core 必须：

- 独立。
- 可测试。
- 可替换。
- 可扩展。

未来：

无论：

AI Tutor。

Interview。

Enterprise Search。

Learning Assistant。

全部复用这一套知识能力。

Knowledge Core 是整个项目生命周期中最稳定的模块。

# AI Engine

## Position

AI Engine 是连接 Knowledge Core 与 LLM 的中间层。

职责：

Knowledge

↓

Context

↓

Prompt

↓

LLM

↓

Response

AI Engine 不属于 Knowledge Core。

Knowledge Core 不依赖 AI Engine。

AI Engine 可以依赖 Knowledge Core。

AI Engine 是整个系统唯一允许访问 LLM 的模块。

---

# Responsibilities

AI Engine 负责：

- Query Preprocess
- Context Assemble
- Prompt Build
- LLM Gateway (Chat / Streaming)
- Streaming Response

AI Engine 不负责：

- Parser
- Chunk
- Embedding
- Vector Search
- Metadata
- Storage
- Knowledge Retrieval（调用 Knowledge Core，不自建检索）

以上全部属于 Knowledge Core。

Embedding 明确归属 Knowledge Core。

AI Engine 通过 Knowledge.search() 获取知识，不直接检索数据库。

---

# Pipeline

用户问题进入系统：

```
Question

↓

AI Engine

↓

调用 Knowledge.search()

↓

Context Assemble

↓

Prompt

↓

LLM

↓

Streaming

↓

Frontend
```

Knowledge Core 只负责返回知识。

AI Engine 负责组织整个 AI 推理过程。

AI Engine 不自己检索数据库，统一通过 Knowledge Core API 获取知识。

---

# Query Preprocess

用户输入：

```
介绍一下 React Hooks
```

AI Engine 可以进行：

- Trim
- Normalize
- Language Detect

V1 不进行：

Rewrite

Expand Query

Decompose Question

这些属于后续版本。

---

# Retrieval

AI Engine 不直接检索数据库。

统一调用：

Knowledge Core。

```
Question

↓

Knowledge.search()

↓

Chunks
```

Knowledge Core 返回：

Chunk。

Metadata。

Source。

Reference。

---

# Context Assemble

AI Engine 将 Retrieval 返回结果组织成上下文。

例如：

```
Question

Knowledge 1

Knowledge 2

Knowledge 3

Reference
```

AI Engine 不修改知识内容。

只负责拼接。

---

# Prompt Builder

Prompt 统一由 AI Engine 生成。

不要让不同 Application 自己维护 Prompt。

Prompt Builder 应支持：

System Prompt

Context

User Question

Output Format

Prompt 模板统一管理。

以后支持：

不同场景。

不同模板。

---

# LLM Gateway

所有模型统一经过 Gateway。

例如：

```
Chat()

Stream()
```

不含 Embedding。

Embedding 由 Knowledge Core 独立管理。

不要在业务代码中直接调用 OpenAI。

不要直接调用 Claude。

统一 Provider。

以后增加模型：

Application 无需修改。

---

# Streaming

AI Engine 负责：

LLM Streaming。

统一：

WebSocket。

或者：

SSE。

Frontend 不关心 Provider。

只接收：

Stream。

---

# Error Handling

AI Engine 负责处理：

Provider Error。

Timeout。

Retry。

Rate Limit。

Knowledge Core 不处理：

LLM Error。

---

# Conversation

V1 严格区分三个概念：

## Session Context

仅当前会话上下文。

Session 结束即释放。

不持久化。

## Interview History

保存到数据库。

目的：

- 用户查看历史记录
- 数据统计

AI 不自动读取 History 作为上下文。

History ≠ Memory。

## Memory

长期记忆。

自动参与 Prompt。

V1 不实现。

V3 增加。

## V1 规则

Session 内可以保留上下文。

Session 结束，上下文释放。

History 保存但不影响 AI 行为。

---

# AI Application

V1 包含两个 Application：

## Knowledge Chat

```
用户提问
    ↓
Knowledge Retrieval
    ↓
LLM
    ↓
AI 回答（引用来源）
```

## AI Interview

```
AI 提问
    ↓
用户回答
    ↓
Knowledge Retrieval
    ↓
LLM 评价
```

两者共享同一套 Knowledge Core + AI Engine。

Knowledge Core 不关心具体应用。

以后增加：

AI Tutor。

AI Notes。

Enterprise Search。

Learning Assistant。

所有 Application：

统一调用：

AI Engine。

不要重复实现 Prompt。

不要重复调用 LLM。

---

# AI Interview

AI Interview 是 V1 两大应用之一。

流程：

```
上传知识

↓

建立知识库

↓

AI 根据知识库出题

↓

用户回答

↓

Knowledge Retrieval

↓

LLM 评价回答

↓

下一题
```

区别于 Knowledge Chat：

Chat 是用户问 AI 答。

Interview 是 AI 问用户答再评价。

---

# Interview Scope

V1 Interview：

支持：

- AI 根据知识库出题
- 用户回答
- AI 评价回答
- 引用知识来源

V1 Knowledge Chat：

支持：

- 用户提问
- AI 基于知识库回答
- 引用知识来源
- Streaming 返回

V1 不支持：

自动评分。

学习计划。

错题本。

长期记忆。

这些属于：

V2。

---

# Backend

Backend 使用：

FastAPI。

职责：

Router。

Authentication（预留）。

Upload。

Knowledge API。

Chat API。

Interview API。

Streaming。

Backend 不负责：

知识处理。

Prompt。

Embedding。

统一调用 Packages。

---

# API Design

API 保持简单。

例如：

Knowledge

```
POST /knowledge/upload

GET /knowledge

DELETE /knowledge/{id}
```

Search

```
POST /knowledge/search
```

Knowledge Chat

```
POST /chat
```

Streaming

```
/ws/chat
```

Interview

```
POST /interview/chat

POST /interview/next-question
```

Streaming

```
/ws/interview
```

不要提前设计几十个接口。

遵循：

MVP。

---

# Database

PostgreSQL 保存：

Document。

Chunk Metadata。

Interview History。

Knowledge Base。

Project。

User（预留）。

Embedding：

PgVector。

Object：

MinIO。

数据库不要保存：

原始 PDF。

Word。

Image。

---

# Frontend

Frontend 使用：

Next.js。

页面：

V1 只保留两个核心页面：

```
Upload（上传 + 知识管理）

Interview（Knowledge Chat + AI Interview）
```

不做：

- Dashboard
- Settings
- 复杂后台

V2 再增加 Dashboard、Settings 等。

---

# Upload

上传：

Document。

↓

Backend。

↓

Knowledge Core。

↓

Index。

↓

Ready。

用户可以看到：

Index Status。

---

# Search

支持：

Knowledge Search。

搜索结果：

显示：

Chunk。

Source。

Reference。

不要只返回 AI 回答。

用户需要知道：

知识来源。

---

# Streaming UI

Chat 和 Interview 页面：

采用：

Streaming。

不要等待整个回答结束。

提升体验。

---

# Future

新增 Application：

不得修改：

Knowledge Core。

新增：

Prompt。

不得修改：

Retriever。

新增：

LLM。

不得修改：

Storage。

整个项目遵循：

Open For Extension。

Closed For Modification。

# Development Principles

本项目所有开发均围绕 AI Knowledge Platform。

任何设计均以：

- 保持架构稳定
- 保持模块职责单一
- 保持模块可复用

作为第一原则。

不要为了未来版本增加 V1 不需要的能力。

始终优先保证：

整个知识平台可以完整运行。

---

# Core Philosophy

整个项目只有三个核心模块。

```
Knowledge Core

↓

AI Engine

↓

Application
```

Knowledge Core：

负责知识。

AI Engine：

负责 AI。

Application：

负责业务。

任何模块都不能承担多个职责。

---

# Package Responsibilities

## packages/knowledge

负责：

知识生命周期。

包括：

Import。

Parser。

Chunk。

Embedding。

Metadata。

Retrieval。

Search。

任何知识能力。

全部进入：

Knowledge Package。

---

## packages/ai-engine

负责：

AI 生命周期。

包括：

Context。

Prompt。

Provider。

Streaming。

AI Engine 不关心：

Document。

Chunk。

Storage。

---

## packages/shared

负责：

公共能力。

例如：

Config。

Logger。

Exception。

Utils。

Types。

不要放业务逻辑。

---

# Apps Responsibilities

## apps/web

负责：

UI。

Interaction。

Upload。

Search。

Chat。

Interview。

调用：

Backend API。

不要写业务逻辑。

---

## apps/api

负责：

HTTP。

WebSocket。

Authentication（预留）。

调用：

Knowledge。

AI Engine。

不要直接操作数据库。

不要直接调用 LLM。

---

# Dependency Rules

依赖关系固定。

```
Web

↓

API

↓

AI Engine

↓

Knowledge

↓

Database
```

禁止：

Knowledge

↓

AI Engine。

禁止：

Frontend

↓

Database。

禁止：

Application

↓

Database。

所有访问：

必须经过：

Knowledge。

---

# Data Ownership

Knowledge Core：

拥有：

Document。

Chunk。

Embedding。

Metadata。

AI Engine：

拥有：

Prompt。

Conversation。

Streaming。

Application：

拥有：

UI。

Workflow。

Interaction。

不要交叉拥有数据。

---

# Version Strategy

V1：

只完成：

Knowledge Platform MVP。

保证：

上传。

解析。

建库。

检索。

AI 回答。

整个闭环。

不要增加：

企业能力。

不要增加：

复杂 Agent。

---

V2：

增强：

Knowledge。

增加：

Application。

例如：

Tutor。

Notes。

Hybrid Search。

Redis。

Docker Production。

---

V3：

企业能力。

包括：

Workflow。

Memory。

Permission。

Enterprise Search。

Multi Knowledge Base。

不要提前实现。

---

# Replace Strategy

允许替换：

Parser。

Embedding。

Vector Database。

LLM。

Storage。

要求：

接口保持一致。

Application：

无需修改。

Knowledge Core：

尽量稳定。

---

# Claude Code Workflow

Claude Code 开发流程：

第一步：

阅读：

```
brain.md
```

恢复项目背景。

第二步：

生成：

Project Kit。

包括：

```
.ai/

context/

specs/current/

tasks/
```

第三步：

阅读：

Project Kit。

第四步：

开始开发。

不要直接根据：

brain.md。

生成代码。

brain.md：

负责恢复上下文。

Project Kit：

负责驱动开发。

---

# Development Order

推荐开发顺序：

①

Monorepo。

↓

②

Backend。

↓

③

Database。

↓

④

Knowledge Core。

↓

⑤

AI Engine。

↓

⑥

Frontend。

↓

⑦

Knowledge Chat + Interview。

↓

⑧

Docker。

↓

⑨

Integration。

↓

⑩

Testing。

Knowledge Core 完成之前。

不要开发：

Interview。

---

# Definition Of Done

V1 完成标准：

用户可以：

上传文档。

↓

系统解析。

↓

建立知识库。

↓

完成 Embedding。

↓

建立索引。

↓

开始 Knowledge Chat。

↓

AI 检索知识。

↓

LLM 回答。

↓

Streaming 返回。

↓

显示引用来源。

也可以进行 AI Interview。

↓

AI 出题。

↓

用户回答。

↓

LLM 评价。

整个流程无需人工介入。

即可完成。

---

# Non Goals

V1 不属于项目目标：

- Agent
- Workflow
- Memory
- Planner
- Tool Calling
- Multi Agent
- MCP
- LangGraph
- GraphRAG
- 企业权限
- 多租户
- 企业组织架构

不要因为未来需求增加当前复杂度。

---

# Future Principles

未来任何版本。

新增能力。

优先新增：

Application。

其次增强：

AI Engine。

最后才修改：

Knowledge Core。

Knowledge Core 是整个项目生命周期中最稳定的模块。

---

# Final Goal

本项目最终目标不是构建聊天机器人。

也不是构建 Agent。

而是构建：

一个能够持续积累知识。

持续管理知识。

持续检索知识。

持续衍生 AI 应用。

的 AI Knowledge Platform。

Knowledge Core 是平台基础。

AI Engine 是平台能力。

Application 是平台价值。

三者共同组成整个系统。

整个项目始终围绕这一架构持续演进。