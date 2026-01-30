"""
玄心理命 - 性能优化中间件
缓存、限流、监控
"""

import time
import hashlib
import json
from functools import wraps
from typing import Optional, Callable, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import redis.asyncio as redis

from .config import settings
from .logging import logger


# Redis客户端
_redis_client: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    """获取Redis客户端"""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    return _redis_client


# ==================== 缓存装饰器 ====================

def cache_response(
    expire: int = 300,
    key_prefix: str = "",
    key_builder: Optional[Callable] = None
):
    """
    缓存响应装饰器
    
    Args:
        expire: 过期时间(秒)
        key_prefix: 缓存键前缀
        key_builder: 自定义键生成函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                # 默认使用参数哈希
                param_str = json.dumps(kwargs, sort_keys=True, default=str)
                param_hash = hashlib.md5(param_str.encode()).hexdigest()[:8]
                cache_key = f"{key_prefix}:{func.__name__}:{param_hash}"
            
            try:
                redis_client = await get_redis()
                
                # 尝试获取缓存
                cached = await redis_client.get(cache_key)
                if cached:
                    logger.debug(f"Cache hit: {cache_key}")
                    return json.loads(cached)
                
                # 执行函数
                result = await func(*args, **kwargs)
                
                # 存入缓存
                await redis_client.setex(
                    cache_key,
                    expire,
                    json.dumps(result, default=str)
                )
                
                return result
                
            except Exception as e:
                logger.warning(f"Cache error: {e}")
                # 缓存失败时直接执行函数
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator


async def invalidate_cache(pattern: str):
    """
    使缓存失效
    
    Args:
        pattern: 缓存键模式(支持通配符)
    """
    try:
        redis_client = await get_redis()
        keys = await redis_client.keys(pattern)
        if keys:
            await redis_client.delete(*keys)
            logger.info(f"Invalidated {len(keys)} cache keys")
    except Exception as e:
        logger.warning(f"Cache invalidation error: {e}")


# ==================== 限流中间件 ====================

class RateLimitMiddleware(BaseHTTPMiddleware):
    """请求限流中间件"""
    
    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        burst_size: int = 10
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.burst_size = burst_size
    
    async def dispatch(self, request: Request, call_next):
        # 获取客户端标识
        client_id = self._get_client_id(request)
        
        # 检查限流
        is_allowed = await self._check_rate_limit(client_id)
        
        if not is_allowed:
            return Response(
                content='{"error": "Rate limit exceeded"}',
                status_code=429,
                media_type="application/json"
            )
        
        response = await call_next(request)
        return response
    
    def _get_client_id(self, request: Request) -> str:
        """获取客户端标识"""
        # 优先使用X-Forwarded-For
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"
    
    async def _check_rate_limit(self, client_id: str) -> bool:
        """检查限流"""
        try:
            redis_client = await get_redis()
            key = f"rate_limit:{client_id}"
            
            # 使用滑动窗口算法
            now = time.time()
            window_start = now - 60  # 1分钟窗口
            
            # 原子操作
            pipe = redis_client.pipeline()
            pipe.zremrangebyscore(key, 0, window_start)
            pipe.zadd(key, {str(now): now})
            pipe.zcard(key)
            pipe.expire(key, 60)
            results = await pipe.execute()
            
            request_count = results[2]
            return request_count <= self.requests_per_minute
            
        except Exception as e:
            logger.warning(f"Rate limit check error: {e}")
            return True  # 出错时放行


# ==================== 响应时间监控中间件 ====================

class PerformanceMiddleware(BaseHTTPMiddleware):
    """性能监控中间件"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        # 计算响应时间
        process_time = time.time() - start_time
        
        # 添加响应头
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        
        # 记录慢请求
        if process_time > 1.0:  # 超过1秒
            logger.warning(
                f"Slow request: {request.method} {request.url.path} "
                f"took {process_time:.2f}s"
            )
        
        return response


# ==================== 数据库查询优化 ====================

def batch_query(batch_size: int = 100):
    """
    批量查询装饰器
    用于优化大量数据的查询
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(ids: list, *args, **kwargs):
            results = []
            
            for i in range(0, len(ids), batch_size):
                batch_ids = ids[i:i + batch_size]
                batch_results = await func(batch_ids, *args, **kwargs)
                results.extend(batch_results)
            
            return results
        
        return wrapper
    return decorator


# ==================== 响应压缩 ====================

COMPRESS_MIN_SIZE = 1024  # 最小压缩大小

def should_compress(response: Response) -> bool:
    """判断是否需要压缩"""
    content_type = response.headers.get("content-type", "")
    
    if "application/json" in content_type or "text/" in content_type:
        content_length = len(response.body) if hasattr(response, 'body') else 0
        return content_length >= COMPRESS_MIN_SIZE
    
    return False
