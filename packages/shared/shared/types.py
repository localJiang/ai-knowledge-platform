"""公共类型定义。"""

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class DocumentStatus(StrEnum):
    """文档处理状态。"""

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"


class FileType(StrEnum):
    """支持的文档类型。"""

    PDF = "PDF"
    MARKDOWN = "MARKDOWN"
    TXT = "TXT"
    DOCX = "DOCX"


class ErrorResponse(BaseModel):
    """统一错误响应格式。"""

    error: dict[str, str]
    """{ "code": "ERROR_CODE", "message": "描述" }"""


class PaginatedResponse(BaseModel):
    """分页响应。"""

    items: list[Any]
    total: int


class HealthResponse(BaseModel):
    """健康检查响应。"""

    status: str = "ok"
    version: str = "0.1.0"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
