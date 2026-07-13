"""Interview routes.

V1 endpoints:
- POST /interview/next-question  — 获取下一题
- POST /interview/evaluate       — 提交回答并评价
- WS   /ws/interview             — 流式评价
"""

from fastapi import APIRouter

router = APIRouter(prefix="/interview", tags=["interview"])

# Routes will be implemented in Phase 6 (Task 6.3)
