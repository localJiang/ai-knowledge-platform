# Backlog

> V2/V3 功能记录。不在 V1 范围内，不进入 V1 Spec。

---

## V2

| 功能 | 说明 |
|------|------|
| AI Tutor | 基于知识库的智能辅导 |
| AI Notes | 自动生成学习笔记 |
| URL Import | 从 URL 导入网页内容 |
| Hybrid Search | Keyword + BM25 + Vector 融合搜索 |
| Redis Cache | 热门检索缓存 + Session + Streaming |
| Docker Production | Nginx + HTTPS + CI/CD (GitHub Actions) |
| Celery + Redis | 异步任务升级 |
| Semantic Chunk | Heading Aware / Document Tree |
| Multi LLM Provider | OpenAI / Claude / Gemini / Qwen / GLM |
| Parser Provider 模式 | 可插拔 Parser（PyMuPDF / python-docx / Unstructured） |
| Dashboard 页面 | 知识统计、使用统计 |
| Settings 页面 | 基本配置 |

---

## V3

| 功能 | 说明 |
|------|------|
| 企业知识库 | 多知识库管理 |
| 权限系统 | RBAC + 组织架构 |
| Workflow | 知识处理工作流 |
| Memory | 长期记忆，自动参与 Prompt |
| Agent | AI Agent 能力 |
| Multi Tenant | 多租户隔离 |
| Qdrant | 向量数据库升级（大数据规模） |
| Enterprise Search | 企业级搜索 |
| OAuth / SSO | 企业登录 |

---

## 未排期

| 功能 | 说明 |
|------|------|
| GraphRAG | 图增强 RAG |
| MCP | Model Context Protocol |
| Notion Import | Notion 集成 |
| Obsidian Import | Obsidian 集成 |
| Git Repository Import | 代码仓库知识化 |
| Confluence / Wiki Import | 企业 Wiki 集成 |
| OCR | 图片文字提取 |
| Audio Transcription | 音频转文字 |
| i18n | 多语言支持 |
| PWA | 离线支持 |

---

## 原则

- 新增能力：优先新增 Application，其次增强 AI Engine，最后才修改 Knowledge Core
- Knowledge Core 永远保持稳定，是整个项目生命周期中最稳定的模块
- 遵循 Open For Extension, Closed For Modification
