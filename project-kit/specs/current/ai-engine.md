# AI Engine Specification

> packages/ai-engine 包规格。连接 Knowledge Core 与 LLM 的中间层。

---

## 定位

AI Engine 是 Knowledge Core 与 LLM 之间的薄层。

**职责边界：**

```
Question → Query Preprocess → 调用 Knowledge.search() → Context Assemble → Prompt → LLM → Streaming Response
```

**不负责：** Parser / Chunk / Embedding / Vector Search / Metadata / Storage（全部属于 Knowledge Core）

---

## 模块结构

```
packages/ai-engine/
├── __init__.py
├── api.py                  # 对外暴露的 AI Engine API
├── services/
│   ├── __init__.py
│   ├── query_processor.py  # Query 预处理
│   ├── context_builder.py  # Context 组装
│   ├── prompt_builder.py   # Prompt 构建
│   └── stream_handler.py   # Streaming 处理
├── gateway/
│   ├── __init__.py
│   ├── llm_gateway.py      # LLM Gateway 统一入口
│   └── providers/
│       ├── __init__.py
│       ├── base.py          # LLMProvider 抽象接口
│       └── deepseek.py      # DeepSeek Provider
└── models/
    ├── __init__.py
    ├── chat.py              # Chat 相关数据模型
    └── context.py           # Context 数据模型
```

---

## 对外 API（api.py）

```python
class AIEngineAPI:
    """AI Engine 对外 API"""

    def __init__(self, knowledge_api: KnowledgeAPI):
        self.knowledge = knowledge_api  # 依赖 Knowledge Core

    async def chat(self, message: str, session_context: list[Message] | None = None) -> ChatResponse:
        """
        非流式 Chat：
        1. Query Preprocess
        2. 调用 Knowledge.search()
        3. Context Assemble
        4. Prompt Build
        5. LLM Gateway.chat()
        6. 返回 ChatResponse
        """
        ...

    async def chat_stream(self, message: str, session_context: list[Message] | None = None) -> AsyncIterator[str]:
        """
        流式 Chat：
        同上，但通过 LLM Gateway.stream() 逐 token 返回
        """
        ...

    async def generate_question(self, session_context: list[Message] | None = None) -> str:
        """
        Interview: AI 根据知识库出一道题
        """
        ...

    async def evaluate_answer(self, question: str, answer: str) -> AsyncIterator[str]:
        """
        Interview: AI 流式评价用户回答
        """
        ...
```

---

## QueryProcessor（services/query_processor.py）

```python
class QueryProcessor:
    """V1 简单预处理"""

    def process(self, query: str) -> str:
        """
        - Trim 首尾空白
        - 基础规范化
        - Language Detect（可选）
        V1 不做: Rewrite / Expand Query / Decompose Question
        """
        ...
```

---

## ContextBuilder（services/context_builder.py）

```python
class ContextBuilder:
    """将 Knowledge Core 返回的 Chunk 组装为 LLM 上下文"""

    def build(self, query: str, search_results: list[SearchResult]) -> str:
        """
        组装格式：

        Question:
        {query}

        Relevant Knowledge:
        1. {chunk_1_content}
           Source: {filename}, Page {page}
        2. {chunk_2_content}
           Source: {filename}, Page {page}
        ...

        不修改知识内容，只负责拼接。
        """
        ...
```

---

## PromptBuilder（services/prompt_builder.py）

```python
class PromptBuilder:
    """Prompt 模板管理"""

    def build_system_prompt(self, scenario: str) -> str:
        """
        场景：
        - "chat": 知识问答
        - "interview_question": 出题
        - "interview_evaluate": 评价

        模板统一管理，不要让 Application 自己维护 Prompt。
        """
        ...

    def build_user_prompt(self, context: str, user_message: str) -> str:
        """
        {context}

        {user_message}
        """
        ...
```

**Prompt 模板示例：**

```
# Chat System Prompt
你是一个知识助手。请基于提供的知识内容回答问题。
如果知识内容不足以回答问题，请明确告知用户。
回答时请引用知识来源。

# Interview Question System Prompt
你是一个面试官。请基于提供的知识内容出一道面试题。
题目应有针对性，考察对知识内容的理解。

# Interview Evaluate System Prompt  
你是一个面试官。请评价用户的回答。
指出正确之处和不足之处，引用知识来源作为依据。
```

---

## LLMGateway（gateway/llm_gateway.py）

```python
class LLMGateway:
    """LLM 统一入口"""

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def chat(self, messages: list[dict]) -> str:
        """非流式调用"""
        return await self.provider.chat(messages)

    async def stream(self, messages: list[dict]) -> AsyncIterator[str]:
        """流式调用，逐 token yield"""
        async for token in self.provider.stream(messages):
            yield token
```

---

## LLMProvider（gateway/providers/base.py）

```python
class LLMProvider(ABC):
    """LLM Provider 抽象接口"""

    @abstractmethod
    async def chat(self, messages: list[dict]) -> str:
        ...

    @abstractmethod
    async def stream(self, messages: list[dict]) -> AsyncIterator[str]:
        ...
```

---

## DeepSeekProvider（gateway/providers/deepseek.py）

```python
class DeepSeekProvider(LLMProvider):
    """V1 唯一 Provider。使用 OpenAI 兼容 API。"""

    def __init__(self, api_key: str, model: str = "deepseek-chat",
                 base_url: str = "https://api.deepseek.com/v1"):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model
```

**V1 不实现其他 Provider。**

---

## ErrorHandler

AI Engine 统一处理 LLM 相关错误：

```python
class LLMErrorHandler:
    """LLM 错误处理"""

    async def handle(self, error: Exception) -> None:
        """
        - Provider Error → 记录日志 + 返回友好错误
        - Timeout → 重试 1 次
        - Rate Limit → 等待后重试
        - 其他错误 → 记录日志 + 返回通用错误
        """
        ...
```

**Knowledge Core 不处理 LLM Error。**

---

## Conversation 管理

V1 规则：

- **Session Context:** 当前会话保留上下文，Session 结束后释放（不持久化）
- **History:** ChatMessage / InterviewQA 存数据库，仅用于查看和统计，AI 不自动读取
- **Memory:** V1 不实现
