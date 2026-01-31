"""
玄心理命 - 数据库配置
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, JSON
from datetime import datetime
import os

# 数据库URL配置
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/yaothink"
)

# 创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "false").lower() == "true",
    pool_size=5,
    max_overflow=10
)

# 创建会话工厂
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 基类
Base = declarative_base()


# ==================== 数据模型 ====================

class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(20), unique=True, nullable=True, index=True)  # 手机号（可选）
    email = Column(String(100), unique=True, nullable=True, index=True)  # 邮箱（可选）
    hashed_password = Column(String(255), nullable=True)  # 密码（可选，验证码登录可不设密码）
    nickname = Column(String(50))
    avatar = Column(String(255))
    gender = Column(String(10))
    birthday = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    is_vip = Column(Boolean, default=False)
    vip_expire_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BirthInfo(Base):
    """用户出生信息表"""
    __tablename__ = "birth_info"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False)
    name = Column(String(50))
    birth_year = Column(Integer, nullable=False)
    birth_month = Column(Integer, nullable=False)
    birth_day = Column(Integer, nullable=False)
    birth_hour = Column(Integer, nullable=False)
    is_lunar = Column(Boolean, default=False)
    gender = Column(String(10), default="男")
    birth_place = Column(String(100))
    timezone = Column(String(50), default="Asia/Shanghai")
    created_at = Column(DateTime, default=datetime.utcnow)


class AnalysisRecord(Base):
    """分析记录表"""
    __tablename__ = "analysis_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    birth_info_id = Column(Integer, index=True)
    analysis_type = Column(String(20), nullable=False)
    result_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class DivinationRecord(Base):
    """占卜记录表"""
    __tablename__ = "divination_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    method = Column(String(20), nullable=False)
    question = Column(Text)
    result_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class PsychologyTest(Base):
    """心理测试记录表"""
    __tablename__ = "psychology_tests"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    test_type = Column(String(20), nullable=False)
    answers = Column(JSON)
    result_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class FusionRecord(Base):
    """融合分析记录表"""
    __tablename__ = "fusion_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False)
    title = Column(String(100))  # 分析标题
    bazi_record_id = Column(Integer, nullable=True)  # 关联八字记录
    ziwei_record_id = Column(Integer, nullable=True)  # 关联紫微记录
    psychology_test_ids = Column(JSON)  # 关联心理测试记录ID列表
    fusion_result = Column(JSON)  # 融合分析结果
    report_markdown = Column(Text)  # Markdown报告
    confidence = Column(Float)  # 置信度
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Favorite(Base):
    """用户收藏表"""
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False)
    item_type = Column(String(30), nullable=False)  # bazi/ziwei/yijing/psychology/fusion
    item_id = Column(Integer, nullable=False)  # 对应记录ID
    note = Column(Text)  # 收藏备注
    created_at = Column(DateTime, default=datetime.utcnow)


class UserSettings(Base):
    """用户设置表"""
    __tablename__ = "user_settings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)
    theme = Column(String(20), default="dark")  # 主题
    language = Column(String(10), default="zh-CN")  # 语言
    timezone = Column(String(50), default="Asia/Shanghai")  # 时区
    notification_enabled = Column(Boolean, default=True)  # 通知开关
    preferences = Column(JSON)  # 其他偏好设置
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ExportHistory(Base):
    """导出历史表"""
    __tablename__ = "export_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False)
    export_type = Column(String(20), nullable=False)  # pdf/json/markdown
    record_type = Column(String(30), nullable=False)  # 导出的记录类型
    record_id = Column(Integer)  # 对应记录ID
    file_path = Column(String(255))  # 文件路径
    created_at = Column(DateTime, default=datetime.utcnow)


# ==================== 数据库操作 ====================

async def init_db():
    """初始化数据库表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """获取数据库会话"""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def close_db():
    """关闭数据库连接"""
    await engine.dispose()
