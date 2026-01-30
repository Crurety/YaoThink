"""
玄心理命 - 应用配置
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用信息
    APP_NAME: str = "玄心理命"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "东方玄学与西方心理学融合的命理分析平台"
    DEBUG: bool = True
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # 数据库配置
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/yaothink"
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_DEFAULT_EXPIRE: int = 3600  # 默认缓存1小时
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production-玄心理命-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    
    # 限流配置
    RATE_LIMIT_REQUESTS: int = 100  # 每分钟最大请求数
    RATE_LIMIT_WINDOW: int = 60     # 限流窗口（秒）
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


# 全局配置实例
settings = get_settings()
