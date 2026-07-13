# Knowledge Core Specification

> packages/knowledge 包规格。整个系统最核心的模块。

---

## 定位

Knowledge Core 是整个 AI Knowledge Platform 唯一负责知识管理的模块。

**职责边界：**

```
Import → Parser → Normalization → Chunk → Embedding → Metadata → Storage → Retrieval
```

**不负责：** LLM / Prompt / Workflow / Agent / Application 逻辑

---

## 模块结构

```
packages/knowledge/
├── __init__.py
├── api.py                  # 对外暴露的 Knowledge API
├── models/
│   ├── __init__.py
│   ├── document.py         # Document ORM Model
│   └── chunk.py            # Chunk ORM Model
├── services/
│   ├── __init__.py
│   ├── import_service.py   # Document Import
│   ├── parser.py           # Parser（Docling）
│   ├── normalizer.py       # 文本规范化
│   ├── chunker.py          # Sliding Window Chunk
│   ├── embedder.py         # Embedding Provider
│   ├── retriever.py        # Vector Search + Top K
│   └── indexer.py          # 编排 ingest 流程
├── storage/
│   ├── __init__.py
│   ├── file_storage.py     # 文件存储抽象（本地/MinIO）
│   └── vector_store.py     # PgVector 操作
└── repository/
    ├── __init__.py
    ├── document_repo.py    # Document CRUD
    └── chunk_repo.py       # Chunk CRUD
```

---

## 对外 API（api.py）

Knowledge Core 对外暴露的唯一接口。

```python
class KnowledgeAPI:
    """Knowledge Core 对外 API"""

    async def import_document(self, file: UploadFile) -> Document:
        """导入文档，返回 document（status=PENDING），触发后台 ingest"""
        ...

    async def get_document(self, document_id: UUID) -> Document:
        """获取文档详情（含状态）"""
        ...

    async def list_documents(self) -> list[Document]:
        """文档列表"""
        ...

    async def delete_document(self, document_id: UUID) -> None:
        """删除文档 + 关联 Chunk + 向量 + 原始文件"""
        ...

    async def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        """知识检索，返回 Top K Chunk + Score + Metadata"""
        ...
```

---

## Parser（services/parser.py）

**V1 实现：**

```python
class Parser:
    """文档解析器。V1 使用 Docling。"""

    def parse(self, file_path: str, file_type: str) -> str:
        """
        解析文件为 Plain Text。

        Args:
            file_path: 文件路径
            file_type: PDF / MARKDOWN / TXT / DOCX

        Returns:
            规范化后的纯文本
        """
        # 直接调用 Docling
        ...
```

**不实现：** Factory / Registry / Plugin 体系。

---

## Normalizer（services/normalizer.py）

Parser 完成后统一进行文本规范化。

```python
class Normalizer:
    """文本规范化"""

    def normalize(self, text: str) -> str:
        """
        - Unicode 规范化（NFC）
        - 统一换行符（\n）
        - 移除多余空白
        - 全角/半角统一
        - 编码清理
        """
        ...
```

---

## Chunker（services/chunker.py）

**V1 策略：Sliding Window**

```python
class Chunker:
    """V1: Sliding Window Chunk"""

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 64):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str) -> list[ChunkData]:
        """
        将文本切分为 Chunk 列表。

        每个 Chunk 包含:
        - content: str
        - token_count: int
        """
        ...
```

**不实现：** Semantic Chunk / Heading Aware / Document Tree

---

## Embedder（services/embedder.py）

```python
class Embedder:
    """Embedding Provider。V1 使用单一模型。"""

    def __init__(self, provider: str, model: str, api_key: str):
        ...

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """批量文本 → 向量列表"""
        ...

    async def embed_single(self, text: str) -> list[float]:
        """单条文本 → 向量"""
        ...
```

**注意：** Embedding 属于 Knowledge Core，不属于 AI Engine。

---

## Retriever（services/retriever.py）

```python
class Retriever:
    """知识检索器"""

    def __init__(self, embedder: Embedder, vector_store: VectorStore):
        ...

    async def retrieve(self, query: str, top_k: int = 5) -> list[SearchResult]:
        """
        1. query → Embedding
        2. PgVector Similarity Search
        3. 返回 Top K Chunk + Score + Metadata
        """
        ...

    async def retrieve_for_rag(self, query: str, top_k: int = 5) -> RAGContext:
        """
        返回组装好的 RAG 上下文：
        - chunks: list[Chunk]
        - sources: list[Source]
        """
        ...
```

**不负责：** Prompt / LLM / Answer

---

## Indexer（services/indexer.py）

编排 ingest 流程。

```python
class Indexer:
    """编排文档 → 知识的完整流程"""

    def __init__(self, parser: Parser, normalizer: Normalizer,
                 chunker: Chunker, embedder: Embedder,
                 vector_store: VectorStore, document_repo, chunk_repo):
        ...

    async def ingest(self, document_id: UUID) -> None:
        """
        BackgroundTask 入口：
        1. 更新状态 PROCESSING
        2. Parser.parse()
        3. Normalizer.normalize()
        4. Chunker.chunk()
        5. Embedder.embed() → Vector
        6. 保存 Chunk + Vector 到 DB
        7. 更新状态 READY
        失败 → 状态 FAILED + error_message
        """
        ...
```

---

## FileStorage（storage/file_storage.py）

```python
class FileStorage:
    """文件存储抽象"""

    async def save(self, file: UploadFile) -> str:
        """保存文件，返回 storage_path"""
        ...

    async def delete(self, storage_path: str) -> None:
        """删除文件"""
        ...

    async def get(self, storage_path: str) -> bytes:
        """读取文件内容"""
        ...
```

**实现：**
- 开发环境：`LocalFileStorage`（直接写本地文件系统）
- 生产环境：`MinioFileStorage`（S3 兼容 API）
- 接口一致，切换无需修改业务代码

---

## VectorStore（storage/vector_store.py）

```python
class VectorStore:
    """PgVector 操作封装"""

    async def insert(self, chunk_id: UUID, embedding: list[float]) -> None:
        ...

    async def search(self, embedding: list[float], top_k: int = 5,
                     filter_document_ids: list[UUID] | None = None) -> list[SearchResult]:
        """Cosine Similarity Search"""
        ...

    async def delete_by_document(self, document_id: UUID) -> None:
        """删除文档的所有向量"""
        ...
```

---

## SearchResult

```python
@dataclass
class SearchResult:
    chunk_id: UUID
    document_id: UUID
    filename: str
    content: str
    score: float
    metadata: dict
```

---

## RAGContext

```python
@dataclass  
class RAGContext:
    chunks: list[Chunk]
    sources: list[Source]

@dataclass
class Source:
    document_id: UUID
    filename: str
    chunk_id: UUID
    page: int | None
    content_snippet: str
```
