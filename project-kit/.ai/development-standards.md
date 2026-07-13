# Development Standards

> V1 AI Knowledge Platform 编码规范。Claude Code 开发时必须遵守。

---

## 语言与运行时

| 层级 | 语言 | 版本管理 |
|------|------|----------|
| apps/web | TypeScript | pnpm |
| apps/api | Python 3.12+ | uv |
| packages/knowledge | Python 3.12+ | uv |
| packages/ai-engine | Python 3.12+ | uv |
| packages/shared | Python 3.12+ | uv |

---

## 目录约定

```
ai-knowledge-platform/
├── project-kit/               # 开发文档（Project Kit）
│   ├── brain.md               # 产品概念文档（参考，不驱动开发）
│   ├── .ai/                   # Claude Code 规范（不是业务代码）
│   ├── context/               # 项目背景文档
│   ├── specs/current/         # V1 规格文档
│   └── tasks/                 # 任务拆分
├── apps/                      # 运行入口，不含业务逻辑
│   ├── web/                   # Next.js 前端
│   └── api/                   # FastAPI 后端
├── packages/                  # 可复用业务能力
│   ├── knowledge/             # Knowledge Core
│   ├── ai-engine/             # AI Engine
│   └── shared/                # 公共能力
├── docker/                    # 部署配置
│   ├── compose.yaml
│   ├── postgres/
│   ├── minio/
│   └── nginx/
├── scripts/                   # 工具脚本
│   ├── dev/
│   ├── db/
│   └── tools/
├── Makefile
└── .env
```

---

## 依赖规则（强制）

```
apps/web → apps/api → packages/ai-engine → packages/knowledge → database
```

**禁止：**

- `packages/knowledge` 依赖 `packages/ai-engine`
- `apps/web` 直接访问数据库
- `apps/api` 直接操作数据库（必须经过 packages）
- 任何 Application 直接调用 LLM（必须经过 ai-engine）

---

## 文件命名

| 类型 | Python | TypeScript |
|------|--------|------------|
| 模块 | `snake_case.py` | `kebab-case.ts` |
| 类 | `PascalCase` | `PascalCase` |
| 函数 | `snake_case` | `camelCase` |
| 常量 | `UPPER_SNAKE_CASE` | `UPPER_SNAKE_CASE` |
| 测试 | `test_*.py` | `*.test.ts` |

---

## Python 规范

- Type Hints 强制（所有 public 函数）
- 使用 `ruff` 做 lint + format
- 使用 `pydantic` 做数据校验
- 使用 `SQLAlchemy 2.0` style（declarative）
- Logger 统一使用 `shared.logger`，禁止 `print()`
- 配置统一读取 `shared.config`，禁止硬编码

## TypeScript 规范

- 使用 `prettier` + `eslint` 
- 组件使用函数组件 + Hooks
- 状态管理：Zustand
- 服务端数据：TanStack Query
- UI 组件：shadcn/ui
- 样式：Tailwind CSS

---

## API 规范

- RESTful 风格
- Streaming 使用 WebSocket
- 错误统一返回 JSON `{ "error": { "code": "...", "message": "..." } }`
- Router 不允许写业务逻辑，只做参数校验 + 调用 packages

---

## Git 规范

- 分支命名：`feature/*` / `fix/*` / `chore/*`
- Commit 消息：中文，简洁描述做了什么
- 不提交 `.env`、`node_modules`、`__pycache__`、`.claude/settings.local.json`

---

## V1 禁止事项

以下技术在 V1 不允许引入：

- LangChain / LangGraph / AutoGen
- Celery / Redis（异步用 BackgroundTasks）
- GraphQL
- Agent / Workflow / Memory / Planner / Tool Calling / MCP
- 多租户 / 企业权限 / 多知识库
- OAuth / SSO（只预留接口）
