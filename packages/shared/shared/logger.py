"""统一日志管理。

所有日志通过此模块输出，禁止在代码中使用 print()。
V1 使用 Python logging 模块，输出到 stdout（Docker 友好）。
"""

import logging
import sys

from shared.config import settings

# 日志格式
FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name: str | None = None) -> logging.Logger:
    """创建 logger 实例。

    Args:
        name: logger 名称（通常传 __name__）

    Returns:
        配置好的 Logger 实例
    """
    logger = logging.getLogger(name or "ai_knowledge")

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(FORMAT, datefmt=DATE_FORMAT))

    logger.addHandler(handler)

    level = logging.DEBUG if settings.debug else logging.INFO
    logger.setLevel(level)

    return logger


# 模块级 logger
logger = setup_logger("ai_knowledge")
