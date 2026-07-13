"""统一错误处理中间件。

V1 错误响应格式：
{ "error": { "code": "ERROR_CODE", "message": "描述" } }
"""

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class APIError(Exception):
    """API 业务异常基类。"""

    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code


class NotFoundError(APIError):
    """资源不存在。"""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(code="NOT_FOUND", message=message, status_code=404)


class ValidationError(APIError):
    """参数校验失败。"""

    def __init__(self, message: str = "Validation failed"):
        super().__init__(code="VALIDATION_ERROR", message=message, status_code=422)


class InternalError(APIError):
    """内部错误。"""

    def __init__(self, message: str = "Internal server error"):
        super().__init__(code="INTERNAL_ERROR", message=message, status_code=500)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """捕获未处理异常，统一返回 JSON 错误格式。"""

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except APIError as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"error": {"code": e.code, "message": e.message}},
            )
        except Exception:
            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "code": "INTERNAL_ERROR",
                        "message": "An unexpected error occurred",
                    }
                },
            )
