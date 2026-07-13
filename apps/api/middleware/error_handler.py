"""统一错误处理中间件。

V1 错误响应格式：
{ "error": { "code": "ERROR_CODE", "message": "描述" } }
"""

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from shared.exceptions import APIError


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
