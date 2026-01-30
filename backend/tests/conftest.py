"""
玄心理命 - 测试配置
"""

import os
import sys
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from httpx import AsyncClient

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app


# 事件循环
@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# 异步HTTP客户端
@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """创建测试客户端"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# 模拟用户数据
@pytest.fixture
def sample_birth_data():
    """示例出生数据"""
    return {
        "year": 1990,
        "month": 6,
        "day": 15,
        "hour": 10,
        "gender": "男",
        "is_lunar": False
    }


@pytest.fixture
def sample_mbti_answers():
    """示例MBTI答案"""
    return [{"question_id": i, "answer": "A" if i % 2 == 0 else "B"} for i in range(32)]


@pytest.fixture
def sample_big5_answers():
    """示例大五人格答案"""
    return [{"question_id": i, "score": 3 + (i % 3)} for i in range(60)]


@pytest.fixture
def sample_yijing_question():
    """示例易经问题"""
    return {
        "method": "meihua",
        "question": "今日运势如何？"
    }
