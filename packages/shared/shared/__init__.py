"""shared package - AI Knowledge Platform

公共能力：Config / Logger / Exception / Common Types
"""

from shared.config import Settings, settings
from shared.exceptions import (
    APIError,
    InternalError,
    KnowledgeError,
    LLMError,
    NotFoundError,
    ValidationError,
)
from shared.logger import logger, setup_logger
from shared.types import (
    DocumentStatus,
    ErrorResponse,
    FileType,
    HealthResponse,
    PaginatedResponse,
)

__all__ = [
    # config
    "Settings",
    "settings",
    # logger
    "logger",
    "setup_logger",
    # exceptions
    "APIError",
    "NotFoundError",
    "ValidationError",
    "InternalError",
    "KnowledgeError",
    "LLMError",
    # types
    "DocumentStatus",
    "FileType",
    "ErrorResponse",
    "PaginatedResponse",
    "HealthResponse",
]
