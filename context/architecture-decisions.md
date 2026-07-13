# Architecture Decisions

> 关键架构决策记录（ADR）。防止后续开发偏离设计初衷。

---

## ADR-001: 为什么是 Next.js + FastAPI（而不是纯 Next.js）

**决策：** Browser 直调 FastAPI，Next.js 仅负责 UI 渲染。

**原因：** Knowledge Core 基于 Python AI 生态（Docling 文档解析、Embedding 模型、OCR 等），这些能力只有 Python 侧能提供。

**V1 方案：** Browser → FastAPI（开启 CORS），不增加 BFF 层。

**代价：** CORS 配置，前后端分属不同服务需要分别启动。

---

## ADR-002: 为什么使用 Docling（不是 Unstructured / PyMuPDF）

**决策：** V1 使用 Docling 作为唯一文档解析器。

**原因：** Docling 原生支持 PDF/Markdown/TXT/DOCX，V1 的 4 种格式全部覆盖，单一依赖即可。

**V1 方案：** `parser.parse(file) → Docling`，不实现 Parser Factory/Registry/Plugin 体系。

**代价：** 如果某种格式 Docling 处理不好，需要等 V2 再增加替代 Parser。

---

## ADR-003: 为什么使用 Turborepo + pnpm + uv（不是 Nx / poetry）

**决策：** Turborepo 做任务编排，pnpm 管 Node 依赖，uv 管 Python 依赖。

**原因：** 本项目是 Polyglot Monorepo（Python + TypeScript），没有单一工具能同时管理两种语言。Turborepo 不参与依赖安装，只做 `dev`/`build`/`lint` 的任务编排。

---

## ADR-004: 为什么使用 BackgroundTasks（不是 Celery）

**决策：** V1 使用 FastAPI 内置 BackgroundTasks 处理异步 ingest 流程。

**原因：** V1 是单机部署，不需要分布式任务队列。BackgroundTasks 零额外依赖。

**V2 方案：** 升级 Celery + Redis。

**V1 设计要点：**
- Upload 立即返回 `document_id`
- 前端轮询 `GET /knowledge/{id}` 查看状态（PENDING → PROCESSING → READY/FAILED）
- BackgroundTasks 只做 ingest，不处理 Streaming

---

## ADR-005: 为什么保留 MinIO

**决策：** V1 保留 MinIO 存储原始文件。

**原因：**
- 支持重新解析（Chunk 策略升级后无需重新上传）
- 支持重新 Embedding（模型升级后无需重新上传）
- 方便排查问题（对比原始文件和解析结果）
- 后续支持 OCR、图片提取等能力

**开发环境：** 使用本地文件系统，接口与 MinIO 保持一致。

---

## ADR-006: 为什么 V1 只用 DeepSeek（不多 Provider）

**决策：** V1 只接入 DeepSeek 一个 LLM Provider。

**原因：** V1 目标是跑通闭环，多 Provider 切换增加不必要的复杂度。

**V1 方案：** 保留 `LLMProvider` 接口，但只实现 `DeepSeekProvider`。

**V2 升级：** 增加 OpenAI、Claude、Gemini 等 Provider。

---

## ADR-007: 为什么 Chunk 用 Sliding Window（不是 Semantic Chunk）

**决策：** V1 使用固定大小的 Sliding Window（chunk_size + chunk_overlap）。

**原因：** 最简单方案保证 V1 跑通。Semantic Chunk、Heading Aware 等增加实现复杂度。

**V2 升级：** 增加语义感知 Chunk 策略。

**注意：** 这正是保留 MinIO 原始文件的原因——Chunk 策略升级后可以重新解析。

---

## ADR-008: 为什么 Interview History ≠ Memory

**决策：** V1 严格区分 Session Context、Interview History、Memory 三层概念。

- **Session Context：** 仅当前会话，Session 结束即释放，不持久化
- **Interview History：** 存数据库，仅用于查看历史+数据统计，AI 不自动读取
- **Memory：** 长期记忆自动参与 Prompt，V3 实现

**原因：** 防止 History 被误当作 Memory 使用，导致 Prompt 膨胀。
