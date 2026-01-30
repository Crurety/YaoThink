"""
玄心理命 - Redis缓存层
"""

import json
import os
from typing import Optional, Any
from datetime import timedelta
import redis.asyncio as redis


# Redis配置
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# 创建Redis连接池
redis_pool = redis.ConnectionPool.from_url(REDIS_URL, decode_responses=True)


class CacheService:
    """缓存服务"""
    
    def __init__(self):
        self.client = redis.Redis(connection_pool=redis_pool)
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        value = await self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    async def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值（自动JSON序列化）
            expire: 过期时间（秒），默认1小时
        
        Returns:
            是否设置成功
        """
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        return await self.client.setex(key, expire, value)
    
    async def delete(self, key: str) -> int:
        """删除缓存"""
        return await self.client.delete(key)
    
    async def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        return await self.client.exists(key) > 0
    
    async def expire(self, key: str, seconds: int) -> bool:
        """设置过期时间"""
        return await self.client.expire(key, seconds)
    
    async def ttl(self, key: str) -> int:
        """获取剩余过期时间"""
        return await self.client.ttl(key)
    
    async def incr(self, key: str) -> int:
        """自增"""
        return await self.client.incr(key)
    
    async def decr(self, key: str) -> int:
        """自减"""
        return await self.client.decr(key)
    
    # ==================== 业务缓存键 ====================
    
    @staticmethod
    def user_key(user_id: int) -> str:
        """用户信息缓存键"""
        return f"user:{user_id}"
    
    @staticmethod
    def bazi_key(year: int, month: int, day: int, hour: int) -> str:
        """八字分析缓存键"""
        return f"bazi:{year}:{month}:{day}:{hour}"
    
    @staticmethod
    def ziwei_key(year_gan: str, year_zhi: str, month: int, day: int, hour_zhi: str) -> str:
        """紫微斗数缓存键"""
        return f"ziwei:{year_gan}{year_zhi}:{month}:{day}:{hour_zhi}"
    
    @staticmethod
    def rate_limit_key(user_id: int, action: str) -> str:
        """速率限制缓存键"""
        return f"ratelimit:{user_id}:{action}"
    
    @staticmethod
    def session_key(session_id: str) -> str:
        """会话缓存键"""
        return f"session:{session_id}"


# ==================== 缓存装饰器 ====================

def cached(prefix: str, expire: int = 3600):
    """
    缓存装饰器
    
    用法：
        @cached("bazi", expire=7200)
        async def analyze_bazi(year, month, day, hour):
            ...
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{prefix}:{':'.join(str(a) for a in args)}:{':'.join(f'{k}={v}' for k,v in sorted(kwargs.items()))}"
            
            cache = CacheService()
            
            # 尝试从缓存获取
            cached_value = await cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # 执行函数
            result = await func(*args, **kwargs)
            
            # 存入缓存
            if result is not None:
                await cache.set(cache_key, result, expire)
            
            return result
        
        return wrapper
    return decorator


# ==================== 速率限制 ====================

class RateLimiter:
    """速率限制器"""
    
    def __init__(self, cache: CacheService = None):
        self.cache = cache or CacheService()
    
    async def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> bool:
        """
        检查是否允许请求
        
        Args:
            key: 限制键
            max_requests: 最大请求数
            window_seconds: 时间窗口（秒）
        
        Returns:
            是否允许
        """
        current = await self.cache.incr(key)
        
        if current == 1:
            await self.cache.expire(key, window_seconds)
        
        return current <= max_requests
    
    async def check_user_limit(self, user_id: int, action: str,
                                max_requests: int = 100,
                                window_seconds: int = 60) -> bool:
        """检查用户操作限制"""
        key = CacheService.rate_limit_key(user_id, action)
        return await self.is_allowed(key, max_requests, window_seconds)


# 全局缓存实例
cache = CacheService()
rate_limiter = RateLimiter(cache)
