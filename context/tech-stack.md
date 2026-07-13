# Tech Stack

> V1 技术选型及原因。每项决策均可追溯。

---

## Frontend

| 技术 | 用途 | 选型原因 |
|------|------|----------|
| Next.js | 前端框架 | React 生态成熟，SSR 可选 |
| React | UI 库 | 生态最大，组件丰富 |
| TypeScript | 语言 | 类型安全 |
| Tailwind CSS | 样式 | 开发速度快，无需单独 CSS 文件 |
| shadcn/ui | 组件库 | 基于 Radix，可定制，不绑定 npm 包 |
| TanStack Query | 服务端状态 | 缓存/重试/轮询开箱即用 |
| Zustand | 客户端状态 | 轻量，比 Redux 简单 |

## Backend

| 技术 | 用途 | 选型原因 |
|------|------|----------|
| FastAPI | API 框架 | 高性能、自动 OpenAPI、WebSocket 原生支持 |
| Python 3.12+ | 语言 | AI/ML 生态（Docling、Embedding、OCR） |
| SQLAlchemy 2.0 | ORM | Python 生态标准，支持 async |
| Alembic | Migration | SQLAlchemy 配套 |
| Pydantic | 数据校验 | FastAPI 原生集成 |

## Database & Storage

| 技术 | 用途 | 选型原因 |
|------|------|----------|
| PostgreSQL | 关系数据库 | 成熟稳定，V1 唯一关系库 |
| PgVector | 向量数据库 | 与 PostgreSQL 集成，部署简单，V1 数据量足够 |
| MinIO | 对象存储 | S3 兼容，本地可部署，保存原始文件 |

## AI & LLM

| 技术 | 用途 | 选型原因 |
|------|------|----------|
| DeepSeek | V1 LLM Provider | 性价比高，API 兼容 OpenAI |
| Docling | 文档解析 | 统一处理 PDF/DOCX/Markdown/TXT |

## Monorepo & Dev Tools

| 技术 | 用途 |
|------|------|
| Turborepo | 任务编排（build/dev/lint 统一调度） |
| pnpm workspace | Node.js 依赖管理 |
| uv | Python 依赖管理 |
| ruff | Python lint + format |
| prettier + eslint | TypeScript lint + format |

## Infrastructure

| 技术 | 用途 |
|------|------|
| Docker Compose | V1 部署 |
| FastAPI BackgroundTasks | V1 异步任务 |
| Makefile | 统一开发命令 |

---

## V1 不引入的技术

| 技术 | 原因 | 计划 |
|------|------|------|
| LangChain | 过度抽象，Knowledge Core 自行实现 | V2+ 可选在 AI Engine 内部接入 |
| Celery + Redis | 过度复杂 | V2 升级 |
| Qdrant | PgVector 满足 V1 规模 | V2 可选升级 |
| GraphQL | 过度设计 | V1 REST 足够 |
| Nginx | V1 Docker Compose 直接暴露即可 | V2 加 HTTPS |
| OAuth/SSO | V1 无多用户场景 | V3 |
