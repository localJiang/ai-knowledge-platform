"""Chat routes.

V1 endpoints:
- POST /chat     — 非流式 Chat
- WS   /ws/chat  — 流式 Chat
"""

from fastapi import APIRouter

router = APIRouter(tags=["chat"])

# Routes will be implemented in Phase 6 (Task 6.2)
