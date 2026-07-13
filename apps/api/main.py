"""AI Knowledge Platform - FastAPI Application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from middleware.error_handler import ErrorHandlerMiddleware
from routers import chat, health, interview, knowledge

app = FastAPI(
    title="AI Knowledge Platform API",
    version="0.1.0",
)

# --- Middleware (order matters: last added = first executed) ---

# 1. Error handler — catch unhandled exceptions
app.add_middleware(ErrorHandlerMiddleware)

# 2. CORS — V1: allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---

app.include_router(health.router)
app.include_router(knowledge.router)
app.include_router(chat.router)
app.include_router(interview.router)
