# Frontend Specification

> apps/web 规格。Next.js 前端，纯 UI 渲染，不含业务逻辑。

---

## 技术栈

| 技术 | 用途 |
|------|------|
| Next.js (App Router) | 框架 |
| React + TypeScript | UI |
| Tailwind CSS | 样式 |
| shadcn/ui | 组件 |
| TanStack Query | 服务端状态（API 调用/缓存/轮询） |
| Zustand | 客户端状态（UI 状态） |

---

## 页面路由（V1 仅 2 个）

```
/upload          → Upload 页面（文件上传 + 知识列表 + 状态）
/interview       → Interview 页面（Knowledge Chat + AI Interview 切换）
```

**不做：** Dashboard / Settings / 复杂后台

---

## Upload 页面（/upload）

### 功能

1. 文件上传区域（拖拽 + 点击选择）
2. 已上传文档列表（表格/卡片）
3. 每行显示：文件名、类型、大小、状态（带颜色标识）、Chunk 数、时间
4. 删除按钮
5. 上传后自动轮询状态（TanStack Query `refetchInterval`）

### 状态标识

| 状态 | 颜色 | 显示 |
|------|------|------|
| PENDING | 灰色 | 等待处理 |
| PROCESSING | 蓝色 + spinner | 处理中... |
| READY | 绿色 | 就绪 (N chunks) |
| FAILED | 红色 + error message | 失败 |

### 组件树

```
UploadPage
├── UploadZone              # 拖拽上传区域
│   └── FileInput           # 文件选择
└── DocumentList            # 文档列表
    └── DocumentCard[]      # 每行文档卡片
        ├── StatusBadge     # 状态标识
        └── DeleteButton    # 删除按钮
```

---

## Interview 页面（/interview）

### 功能

1. 顶部模式切换（Knowledge Chat / AI Interview）
2. Chat 模式：消息列表 + 输入框 + Streaming 实时显示
3. Interview 模式：AI 出题 → 用户输入回答 → AI 流式评价
4. 引用来源展示（消息下方显示引用的文档名 + 页码）
5. 新建会话 / 会话列表

### Chat 模式组件树

```
ChatView
├── ChatHeader              # 模式切换 + 新建会话
├── MessageList             # 消息列表
│   └── Message[]           # 每条消息
│       ├── MessageContent  # 消息内容（Markdown 渲染）
│       └── References      # 引用来源列表
└── ChatInput              # 输入框 + 发送按钮
```

### Interview 模式组件树

```
InterviewView
├── InterviewHeader         # 模式切换 + 新建会话
├── QuestionCard            # AI 出的题
├── AnswerInput             # 用户回答输入框 + 提交按钮
└── EvaluationCard          # AI 评价（流式显示）
    └── References          # 引用来源
```

---

## 状态管理

### TanStack Query（服务端状态）

| Query Key | 用途 | 轮询 |
|-----------|------|------|
| `['documents']` | 文档列表 | 否 |
| `['document', id]` | 文档详情 + 状态 | 是（PROCESSING 时 2s 间隔） |
| `['search', query]` | 知识搜索 | 否 |

| Mutation | 用途 |
|----------|------|
| `uploadDocument` | 上传文件 |
| `deleteDocument` | 删除文档 |
| `sendChatMessage` | 发送 Chat 消息 |
| `nextQuestion` | 获取面试题 |
| `evaluateAnswer` | 提交评价 |

### Zustand（客户端状态）

```typescript
interface AppStore {
  // Interview 模式
  mode: 'chat' | 'interview';
  setMode: (mode: 'chat' | 'interview') => void;

  // 当前会话
  chatSessionId: string | null;
  setChatSessionId: (id: string | null) => void;
  interviewSessionId: string | null;
  setInterviewSessionId: (id: string | null) => void;
}
```

---

## WebSocket 连接

Chat 和 Interview 的 Streaming 走 WebSocket。

```typescript
// 连接管理
const ws = new WebSocket('ws://localhost:8000/ws/chat');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  switch (data.type) {
    case 'token':
      // 追加 token 到当前消息
      break;
    case 'done':
      // 消息完成，附加 references
      break;
    case 'error':
      // 显示错误
      break;
  }
};
```

---

## API 调用封装

```typescript
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function uploadDocument(file: File): Promise<Document> { ... }
export async function getDocuments(): Promise<Document[]> { ... }
export async function getDocument(id: string): Promise<Document> { ... }
export async function deleteDocument(id: string): Promise<void> { ... }
export async function searchKnowledge(query: string, topK?: number): Promise<SearchResult[]> { ... }
export async function chat(message: string, sessionId?: string): Promise<ChatResponse> { ... }
```

---

## V1 不做

- Dashboard 统计图表
- Settings 页面
- 用户系统（登录/注册）
- 多知识库选择
- 暗色模式切换（直接用系统默认）
- i18n 国际化
- PWA / 离线支持
