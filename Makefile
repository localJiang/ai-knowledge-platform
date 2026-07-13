.PHONY: dev dev-web dev-api build lint test install clean

# 启动全部服务（前端 + 后端）
dev:
	@echo "Starting web (Next.js) and api (FastAPI)..."
	@turborepo dev

# 仅启动前端
dev-web:
	cd apps/web && pnpm dev

# 仅启动后端
dev-api:
	cd apps/api && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 安装所有依赖
install:
	pnpm install
	uv sync

# 构建
build:
	pnpm run build

# Lint
lint:
	pnpm run lint
	uv run ruff check .

# 测试
test:
	uv run pytest

# 清理
clean:
	rm -rf apps/web/.next
	rm -rf apps/web/node_modules
	rm -rf .venv
	rm -rf **/__pycache__
