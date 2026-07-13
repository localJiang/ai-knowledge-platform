"""统一异常类。

所有业务异常均继承 APIError。
"""


class APIError(Exception):
    """API 业务异常基类。

    Attributes:
        code: 错误码（如 "NOT_FOUND"、"VALIDATION_ERROR"）
        message: 错误描述
        status_code: HTTP 状态码
    """

    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(APIError):
    """资源不存在 (404)。"""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(code="NOT_FOUND", message=message, status_code=404)


class ValidationError(APIError):
    """参数校验失败 (422)。"""

    def __init__(self, message: str = "Validation failed"):
        super().__init__(code="VALIDATION_ERROR", message=message, status_code=422)


class InternalError(APIError):
    """内部错误 (500)。"""

    def __init__(self, message: str = "Internal server error"):
        super().__init__(code="INTERNAL_ERROR", message=message, status_code=500)


class KnowledgeError(APIError):
    """知识处理相关错误。"""

    def __init__(self, message: str, code: str = "KNOWLEDGE_ERROR", status_code: int = 400):
        super().__init__(code=code, message=message, status_code=status_code)


class LLMError(APIError):
    """LLM 调用相关错误。"""

    def __init__(self, message: str, code: str = "LLM_ERROR", status_code: int = 502):
        super().__init__(code=code, message=message, status_code=status_code)
