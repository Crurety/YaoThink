"""
玄心理命 - 后端API主入口
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.logging import logger, log_request
from app.api import bazi, ziwei, yijing, auth, psychology, fusion, user, analysis


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} 正在启动...")
    
    # 尝试连接数据库（失败不阻止启动）
    try:
        await init_db()
        logger.info("✅ 数据库连接已建立")
    except Exception as e:
        logger.warning(f"⚠️ 数据库连接失败，将在请求时重试: {e}")
    
    yield
    
    # 关闭时
    logger.info("🛑 应用正在关闭...")
    try:
        await close_db()
        logger.info("✅ 数据库连接已关闭")
    except Exception:
        pass


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    # Trigger redeploy for psychology module fix
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# ==================== 中间件 ====================

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    """请求日志中间件"""
    start_time = time.time()
    
    response = await call_next(request)
    
    # 计算处理时间
    duration_ms = (time.time() - start_time) * 1000
    
    # 记录请求日志
    log_request(
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=duration_ms
    )
    
    # 添加响应头
    response.headers["X-Process-Time"] = f"{duration_ms:.2f}ms"
    
    return response


# ==================== 异常处理 ====================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    logger.exception(f"未捕获的异常: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "服务器内部错误",
            "detail": str(exc) if settings.DEBUG else "请稍后重试"
        }
    )


# ==================== 注册路由 ====================

app.include_router(auth.router, prefix="/api/auth", tags=["用户认证"])
app.include_router(user.router, prefix="/api/users", tags=["用户管理"])
app.include_router(bazi.router, prefix="/api/bazi", tags=["八字命理"])
app.include_router(ziwei.router, prefix="/api/ziwei", tags=["紫微斗数"])
app.include_router(yijing.router, prefix="/api/yijing", tags=["易经占卜"])
app.include_router(psychology.router, prefix="/api/psychology", tags=["心理评测"])
app.include_router(fusion.router, prefix="/api/fusion", tags=["玄心融合"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["大数据分析"])
app.include_router(user.router, prefix="/api", tags=["用户中心"])


# ==================== 基础端点 ====================

@app.get("/", summary="API首页")
async def root():
    """API首页"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "docs": "/docs",
        "modules": ["八字命理", "紫微斗数", "易经占卜", "心理测评", "融合分析"]
    }


@app.get("/health", summary="健康检查")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.get("/api/info", summary="API信息")
async def api_info():
    """获取API详细信息"""
    return {
        "success": True,
        "data": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "endpoints": {
                "auth": {
                    "register": "POST /api/auth/register",
                    "login": "POST /api/auth/login",
                    "me": "GET /api/auth/me"
                },
                "bazi": {
                    "analyze": "POST /api/bazi/analyze",
                    "paipan": "POST /api/bazi/paipan"
                },
                "ziwei": {
                    "analyze": "POST /api/ziwei/analyze"
                },
                "yijing": {
                    "meihua_time": "POST /api/yijing/meihua/time",
                    "meihua_number": "POST /api/yijing/meihua/number",
                    "liuyao": "POST /api/yijing/liuyao"
                }
            }
        }
    }
