"""Knowledge routes.

V1 endpoints:
- POST /knowledge/upload   — 上传文档
- GET  /knowledge          — 知识列表
- GET  /knowledge/{id}     — 文档详情
- DELETE /knowledge/{id}   — 删除文档
- POST /knowledge/search   — 知识搜索
"""

from fastapi import APIRouter

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

# Routes will be implemented in Phase 6 (Task 6.1)
