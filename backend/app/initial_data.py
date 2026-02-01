"""
初试化数据脚本
用于在应用启动前检查数据库连接并创建表
"""
import asyncio
import logging
import sys
from sqlalchemy import text
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.database import init_db, engine
from app.core.config import settings

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


async def ensure_database_exists():
    """Ensure the target database exists, create if not."""
    try:
        # Parse the configured database URL
        db_url = make_url(settings.DATABASE_URL)
        target_db = db_url.database
        
        # Connect to 'postgres' database to check/create target db
        # We replace the database name in the URL with 'postgres'
        postgres_url = db_url.set(database="postgres")
        
        # Create temporary engine with AUTOCOMMIT for CREATE DATABASE
        temp_engine = create_async_engine(
            postgres_url,
            isolation_level="AUTOCOMMIT",
            echo=False
        )
        
        async with temp_engine.connect() as conn:
            # Check if database exists
            # We use text() for raw SQL
            check_query = text(f"SELECT 1 FROM pg_database WHERE datname='{target_db}'")
            result = await conn.execute(check_query)
            if not result.scalar():
                logger.warning(f"数据库 '{target_db}' 不存在，正在自动创建...")
                await conn.execute(text(f"CREATE DATABASE {target_db}"))
                logger.info(f"数据库 '{target_db}' 创建成功！")
            else:
                logger.info(f"数据库 '{target_db}' 已存在，跳过创建。")
                
        await temp_engine.dispose()
    except Exception as e:
        # Log error but verify main connection later
        logger.error(f"尝试自动创建数据库失败 (可能是权限不足或已存在): {e}")
        logger.info("将尝试直接连接目标数据库...")


async def init() -> None:
    """初始化数据库"""
    try:
        await init_db()
        logger.info("数据库表创建成功")
    except Exception as e:
        logger.error(f"数据库表创建失败: {e}")
        raise e


async def check_db_connection() -> None:
    """检查数据库连接"""
    logger.info("正在尝试连接数据库...")
    from app.core.database import DATABASE_URL
    safe_url = str(DATABASE_URL).replace("postgres:postgres", "postgres:***")
    logger.info(f"Target Database URL: {safe_url}")
    
    for i in range(max_tries):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("数据库连接成功")
            return
        except Exception as e:
            if i % 5 == 0:  # 每5次打印一次日志
                logger.warning(f"数据库连接失败，正在重试 ({i+1}/{max_tries}): {e}")
            await asyncio.sleep(wait_seconds)
    
    raise Exception("无法连接到数据库")


async def main() -> None:
    logger.info("开始初始化数据...")
    await ensure_database_exists()
    await check_db_connection()
    await init()
    logger.info("初始化数据完成")


if __name__ == "__main__":
    try:
        if sys.platform == 'win32':
             asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except Exception as e:
        logger.error(f"初始化失败: {e}")
        sys.exit(1)
