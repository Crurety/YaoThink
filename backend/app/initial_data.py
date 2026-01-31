"""
初试化数据脚本
用于在应用启动前检查数据库连接并创建表
"""
import asyncio
import logging
import sys
from sqlalchemy import text
from app.core.database import init_db, engine

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


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
