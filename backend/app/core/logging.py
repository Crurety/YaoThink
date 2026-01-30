"""
玄心理命 - 日志系统配置
"""

import logging
import sys
import os
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import json


# 日志目录
LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
LOG_DIR.mkdir(exist_ok=True)

# 日志级别
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


class JSONFormatter(logging.Formatter):
    """JSON格式的日志格式化器"""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # 添加异常信息
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # 添加额外字段
        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)
        
        return json.dumps(log_data, ensure_ascii=False)


class ColorFormatter(logging.Formatter):
    """彩色控制台日志格式化器"""
    
    COLORS = {
        "DEBUG": "\033[36m",     # 青色
        "INFO": "\033[32m",      # 绿色
        "WARNING": "\033[33m",   # 黄色
        "ERROR": "\033[31m",     # 红色
        "CRITICAL": "\033[35m",  # 紫色
    }
    RESET = "\033[0m"
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        record.msg = f"{color}{record.msg}{self.RESET}"
        return super().format(record)


def setup_logging(app_name: str = "yaothink") -> logging.Logger:
    """
    配置日志系统
    
    Args:
        app_name: 应用名称
    
    Returns:
        配置好的Logger实例
    """
    logger = logging.getLogger(app_name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # 防止重复添加handler
    if logger.handlers:
        return logger
    
    # 控制台处理器（彩色输出）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_format = ColorFormatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # 文件处理器（普通日志）
    file_handler = TimedRotatingFileHandler(
        LOG_DIR / f"{app_name}.log",
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(module)s:%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    
    # 错误日志处理器
    error_handler = RotatingFileHandler(
        LOG_DIR / f"{app_name}_error.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_format)
    logger.addHandler(error_handler)
    
    # JSON格式日志（用于日志分析系统）
    json_handler = RotatingFileHandler(
        LOG_DIR / f"{app_name}.json.log",
        maxBytes=50 * 1024 * 1024,  # 50MB
        backupCount=10,
        encoding="utf-8"
    )
    json_handler.setLevel(logging.INFO)
    json_handler.setFormatter(JSONFormatter())
    logger.addHandler(json_handler)
    
    return logger


# 创建全局logger
logger = setup_logging()


# ==================== 日志辅助函数 ====================

def log_request(method: str, path: str, status_code: int, duration_ms: float,
                user_id: int = None, extra: dict = None):
    """记录API请求日志"""
    message = f"{method} {path} -> {status_code} ({duration_ms:.2f}ms)"
    
    extra_data = {
        "request_method": method,
        "request_path": path,
        "status_code": status_code,
        "duration_ms": duration_ms
    }
    
    if user_id:
        extra_data["user_id"] = user_id
    
    if extra:
        extra_data.update(extra)
    
    record = logging.LogRecord(
        name="yaothink.request",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg=message,
        args=(),
        exc_info=None
    )
    record.extra_data = extra_data
    
    logger.handle(record)


def log_analysis(analysis_type: str, user_id: int = None, params: dict = None,
                 success: bool = True, error: str = None):
    """记录分析操作日志"""
    status = "成功" if success else "失败"
    message = f"[{analysis_type}] 分析{status}"
    
    if error:
        message += f": {error}"
    
    extra_data = {
        "analysis_type": analysis_type,
        "success": success
    }
    
    if user_id:
        extra_data["user_id"] = user_id
    
    if params:
        extra_data["params"] = params
    
    if error:
        extra_data["error"] = error
    
    level = logging.INFO if success else logging.ERROR
    logger.log(level, message, extra={"extra_data": extra_data})


def log_error(error: Exception, context: str = "", extra: dict = None):
    """记录错误日志"""
    message = f"[ERROR] {context}: {str(error)}" if context else str(error)
    
    extra_data = {
        "error_type": type(error).__name__,
        "error_message": str(error)
    }
    
    if extra:
        extra_data.update(extra)
    
    logger.exception(message, extra={"extra_data": extra_data})
