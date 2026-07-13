# Claude Code Workflow

> Claude Code 每次开发本项目时的标准启动流程。

---

## 新会话启动流程

### 第一步：恢复上下文

阅读以下文件（按顺序）：

1. `project-kit/context/project-overview.md` — 项目定位、核心原则、V1 边界
2. `project-kit/context/tech-stack.md` — 技术选型
3. `project-kit/context/architecture-decisions.md` — 关键架构决策

时间：约 5 分钟。

### 第二步：了解当前进度

阅读：

1. `project-kit/tasks/v1-task-breakdown.md` — 查看当前任务状态
2. 对应的 `project-kit/specs/current/*.md` — 当前任务的规格文档

### 第三步：开始开发

根据 task 的规格文档进行开发。

---

## 开发时的行为准则

### 必须遵守

1. **只读 project-kit/specs/current/ 来写代码**，不要直接读 `brain.md`（brain.md 只作参考）
2. **每次只完成一个 task**，不要跨 task 开发
3. **完成任务后更新 task 状态**（`project-kit/tasks/v1-task-breakdown.md`）
4. **遵循 `project-kit/.ai/development-standards.md`** 中的编码规范
5. **不引入 V1 禁止事项**（参考 development-standards.md）
6. **所有业务逻辑放入 packages/**，apps 仅作运行入口

### 禁止行为

- 直接根据 `brain.md` 生成代码（brain.md 是概念文档，不是开发规格）
- 为 V2/V3 预留接口或抽象
- 修改 Knowledge Core 来适配 Application（应该是 Application 适配 Knowledge Core）
- 绕过依赖规则（参考 architecture-decisions.md）

---

## 开发顺序

1. Monorepo 初始化
2. Backend 骨架（FastAPI）
3. Database（PostgreSQL + PgVector）
4. Knowledge Core
5. AI Engine
6. Frontend（Next.js）
7. Knowledge Chat + AI Interview
8. Docker Compose
9. Integration
10. Testing

Knowledge Core 完成之前，不开发 Interview。

---

## Task 完成标准

- [ ] 代码通过 lint
- [ ] 代码通过 type check
- [ ] 相关测试通过
- [ ] 更新 `project-kit/tasks/v1-task-breakdown.md` 状态
