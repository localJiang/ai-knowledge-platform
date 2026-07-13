"""统一配置管理。

所有配置通过环境变量读取，禁止在代码中硬编码。
V1 使用 pydantic-settings 实现。
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- App ---
    app_name: str = "AI Knowledge Platform"
    app_version: str = "0.1.0"
    debug: bool = False

    # --- Database ---
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_knowledge"
    database_sync_url: str = "postgresql://postgres:postgres@localhost:5432/ai_knowledge"

    # --- MinIO / Object Storage ---
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "knowledge"
    minio_secure: bool = False
    # 开发环境使用本地文件系统
    use_local_storage: bool = True
    local_storage_path: str = "./uploads"

    # --- LLM (DeepSeek V1) ---
    llm_provider: str = "deepseek"
    llm_api_key: str = ""
    llm_model: str = "deepseek-chat"
    llm_base_url: str = "https://api.deepseek.com/v1"

    # --- Embedding ---
    embedding_provider: str = "openai"
    embedding_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    embedding_base_url: str = "https://api.openai.com/v1"

    # --- Server ---
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = ["*"]


# Singleton
settings = Settings()
