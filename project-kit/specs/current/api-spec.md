# API Specification

> V1 REST API + WebSocket 规格。所有端点的请求/响应格式。

---

## 通用约定

- Base URL: `http://localhost:8000`
- Content-Type: `application/json`
- 错误格式: `{ "error": { "code": "ERROR_CODE", "message": "描述" } }`
- Streaming: WebSocket

---

## Knowledge API

### POST /knowledge/upload

上传文档。

**Request:** `multipart/form-data`

| 字段 | 类型 | 说明 |
|------|------|------|
| file | file | 文件（PDF/Markdown/TXT/DOCX） |

**Response:** `201 Created`

```json
{
  "id": "uuid",
  "filename": "example.pdf",
  "file_type": "PDF",
  "file_size": 102400,
  "status": "PENDING",
  "created_at": "2026-07-14T10:00:00Z"
}
```

**说明：** 上传后立即返回，后台异步处理。状态通过 `GET /knowledge/{id}` 轮询。

---

### GET /knowledge

知识列表。

**Response:** `200 OK`

```json
{
  "items": [
    {
      "id": "uuid",
      "filename": "example.pdf",
      "file_type": "PDF",
      "file_size": 102400,
      "status": "READY",
      "chunk_count": 42,
      "created_at": "2026-07-14T10:00:00Z"
    }
  ],
  "total": 1
}
```

---

### GET /knowledge/{id}

文档详情 + 处理状态。

**Response:** `200 OK`

```json
{
  "id": "uuid",
  "filename": "example.pdf",
  "file_type": "PDF",
  "file_size": 102400,
  "status": "READY",
  "chunk_count": 42,
  "error_message": null,
  "created_at": "2026-07-14T10:00:00Z",
  "updated_at": "2026-07-14T10:01:30Z"
}
```

---

### DELETE /knowledge/{id}

删除文档及关联的 Chunk、向量、原始文件。

**Response:** `204 No Content`

---

### POST /knowledge/search

知识搜索（纯检索，不含 LLM）。

**Request:**

```json
{
  "query": "React Hooks 的使用方法",
  "top_k": 5
}
```

**Response:** `200 OK`

```json
{
  "results": [
    {
      "chunk_id": "uuid",
      "document_id": "uuid",
      "filename": "react-guide.pdf",
      "content": "Chunk 文本内容...",
      "score": 0.92,
      "metadata": {
        "title": "React Hooks",
        "page": 42
      }
    }
  ]
}
```

---

## Chat API

### POST /chat

Knowledge Chat（非流式）。

**Request:**

```json
{
  "session_id": "uuid | null",
  "message": "React Hooks 是什么？"
}
```

**Response:** `200 OK`

```json
{
  "session_id": "uuid",
  "message": {
    "id": "uuid",
    "role": "assistant",
    "content": "React Hooks 是...",
    "references": [
      {
        "chunk_id": "uuid",
        "document_id": "uuid",
        "filename": "react-guide.pdf",
        "content_snippet": "...",
        "page": 42
      }
    ]
  }
}
```

**说明：** 首次调用不传 `session_id`，后端创建新 session 并返回。后续调用传入 `session_id` 保持上下文。

---

### WebSocket /ws/chat

Knowledge Chat（流式）。

**连接后发送：**

```json
{
  "session_id": "uuid | null",
  "message": "React Hooks 是什么？"
}
```

**接收（逐 token 推送）：**

```json
{
  "type": "token",
  "data": "React"
}
```

```json
{
  "type": "token",
  "data": " Hooks"
}
```

```json
{
  "type": "done",
  "session_id": "uuid",
  "message_id": "uuid",
  "references": [...]
}
```

```json
{
  "type": "error",
  "message": "错误描述"
}
```

---

## Interview API

### POST /interview/next-question

获取下一道 AI 出的题。

**Request:**

```json
{
  "session_id": "uuid | null"
}
```

**Response:** `200 OK`

```json
{
  "session_id": "uuid",
  "question_id": "uuid",
  "question": "请解释 React Hooks 的规则..."
}
```

---

### POST /interview/evaluate

提交回答，AI 评价。

**Request:**

```json
{
  "session_id": "uuid",
  "question_id": "uuid",
  "answer": "React Hooks 的规则包括..."
}
```

**Response:** `200 OK`

```json
{
  "evaluation": "回答正确，但遗漏了...",
  "references": [...]
}
```

---

### WebSocket /ws/interview

Interview 流式评价。

**连接后发送：**

```json
{
  "action": "evaluate",
  "session_id": "uuid",
  "question_id": "uuid",
  "answer": "React Hooks 的规则包括..."
}
```

**接收（流式评价）：**

```json
{
  "type": "token",
  "data": "回答"
}
```

```json
{
  "type": "done",
  "references": [...]
}
```
