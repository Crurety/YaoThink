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
    __table_args__ = {'comment': '用户信息表'}
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    phone = Column(String(20), unique=True, nullable=True, index=True, comment="手机号")
    email = Column(String(100), unique=True, nullable=True, index=True, comment="邮箱")
    hashed_password = Column(String(255), nullable=True, comment="加密密码")
    nickname = Column(String(50), comment="昵称")
    avatar = Column(String(255), comment="头像URL")
    gender = Column(String(10), comment="性别")
    birthday = Column(DateTime, nullable=True, comment="出生日期")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_vip = Column(Boolean, default=False, comment="是否为VIP")
    vip_expire_date = Column(DateTime, nullable=True, comment="VIP过期时间")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")


class BirthInfo(Base):
    """用户出生信息表"""
    __tablename__ = "birth_info"
    __table_args__ = {'comment': '用户生辰八字基础信息表'}
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    user_id = Column(Integer, index=True, nullable=False, comment="关联用户ID")
    name = Column(String(50), comment="姓名")
    birth_year = Column(Integer, nullable=False, comment="公历年份")
    birth_month = Column(Integer, nullable=False, comment="公历月份")
    birth_day = Column(Integer, nullable=False, comment="公历日期")
    birth_hour = Column(Integer, nullable=False, comment="出生小时(0-23)")
    is_lunar = Column(Boolean, default=False, comment="是否为农历输入")
    gender = Column(String(10), default="男", comment="性别")
    birth_place = Column(String(100), comment="出生地点")
    timezone = Column(String(50), default="Asia/Shanghai", comment="时区")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")


class AnalysisRecord(Base):
    """分析记录表"""
    __tablename__ = "analysis_records"
    __table_args__ = {'comment': '八字/紫微分析记录表'}
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    user_id = Column(Integer, index=True, comment="关联用户ID")
    birth_info_id = Column(Integer, index=True, comment="关联出生信息ID")
    analysis_type = Column(String(20), nullable=False, comment="分析类型(bazi/ziwei)")
    result_data = Column(JSON, comment="分析结果JSON")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")


class DivinationRecord(Base):
    """占卜记录表"""
    __tablename__ = "divination_records"
    __table_args__ = {'comment': '占卜记录表'}
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    user_id = Column(Integer, index=True, comment="关联用户ID")
    method = Column(String(20), nullable=False, comment="占卜方式(meihua/liuyao)")
    question = Column(Text, comment="求测问题")
    result_data = Column(JSON, comment="占卜结果JSON")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")


class PsychologyTest(Base):
    """心理测试记录表"""
    __tablename__ = "psychology_tests"
    __table_args__ = {'comment': '心理测试记录表'}
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    user_id = Column(Integer, index=True, comment="关联用户ID")
    test_type = Column(String(20), nullable=False, comment="测试类型(mbti/big5/archetype/enneagram)")
    answers = Column(JSON, comment="用户答案JSON")
    result_data = Column(JSON, comment="测试结果JSON")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")


class FusionRecord(Base):
    """融合分析记录表"""
    __tablename__ = "fusion_records"
    __table_args__ = {'comment': '融合分析记录表'}
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    user_id = Column(Integer, index=True, nullable=False, comment="关联用户ID")
    title = Column(String(100), comment="报告标题")
    bazi_record_id = Column(Integer, nullable=True, comment="关联八字记录ID")
    ziwei_record_id = Column(Integer, nullable=True, comment="关联紫微记录ID")
    psychology_test_ids = Column(JSON, comment="关联心理测试ID列表")
    fusion_result = Column(JSON, comment="融合计算结果JSON")
    report_markdown = Column(Text, comment="AI生成的文字报告")
    confidence = Column(Float, comment="置信度评分")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")


class Favorite(Base):
    """用户收藏表"""
    __tablename__ = "favorites"
    __table_args__ = {'comment': '用户收藏表'}
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    user_id = Column(Integer, index=True, nullable=False, comment="关联用户ID")
    item_type = Column(String(30), nullable=False, comment="收藏项类型(bazi/ziwei/yijing/psychology/fusion)")
    item_id = Column(Integer, nullable=False, comment="对应记录ID")
    note = Column(Text, comment="收藏备注")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")


class UserSettings(Base):
    """用户设置表"""
    __tablename__ = "user_settings"
    __table_args__ = {'comment': '用户设置表'}
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    user_id = Column(Integer, unique=True, index=True, nullable=False, comment="关联用户ID")
    theme = Column(String(20), default="dark", comment="界面主题")
    language = Column(String(10), default="zh-CN", comment="界面语言")
    timezone = Column(String(50), default="Asia/Shanghai", comment="用户时区")
    notification_enabled = Column(Boolean, default=True, comment="是否开启通知")
    preferences = Column(JSON, comment="其他偏好设置JSON")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")


class ExportHistory(Base):
    """导出历史表"""
    __tablename__ = "export_history"
    __table_args__ = {'comment': '导出历史表'}
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    user_id = Column(Integer, index=True, nullable=False, comment="关联用户ID")
    export_type = Column(String(20), nullable=False, comment="导出文件类型(pdf/json/markdown)")
    record_type = Column(String(30), nullable=False, comment="源记录类型")
    record_id = Column(Integer, comment="源记录ID")
    file_path = Column(String(255), comment="文件存储路径")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")


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
