"""
玄心理命 - 八字命理API
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

from app.core.bazi import analyze_bazi, calculate_sizhu, Gender
from app.core.auth import get_current_user, TokenData

router = APIRouter()


class BaZiRequest(BaseModel):
    """八字分析请求"""
    year: int = Field(..., ge=1900, le=2100, description="公历年份")
    month: int = Field(..., ge=1, le=12, description="公历月份")
    day: int = Field(..., ge=1, le=31, description="公历日")
    hour: int = Field(..., ge=0, le=23, description="出生时辰(24小时制)")
    gender: str = Field(default="男", description="性别：男/女")
    target_year: Optional[int] = Field(None, description="流年分析目标年份")

    class Config:
        json_schema_extra = {
            "example": {
                "year": 1990,
                "month": 5,
                "day": 15,
                "hour": 10,
                "gender": "男"
            }
        }


class QuickBaZiRequest(BaseModel):
    """快速排盘请求"""
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: int = Field(..., ge=0, le=23)


@router.post("/analyze", summary="八字完整分析")
async def analyze(request: BaZiRequest, current_user: TokenData = Depends(get_current_user)):
    """
    八字完整分析（需要登录）
    
    包含：四柱排盘、五行分析、十神分析、格局判断、大运流年、神煞分析
    """
    try:
        # 尝试从缓存获取
        from app.core.cache import cache, CacheService
        cache_key = CacheService.bazi_key(request.year, request.month, request.day, request.hour)
        
        try:
            cached_result = await cache.get(cache_key)
            if cached_result:
                return {"success": True, "data": cached_result, "cached": True}
        except Exception:
            pass  # 缓存失败不影响正常流程
        
        result = analyze_bazi(
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            gender=request.gender,
            target_year=request.target_year
        )
        
        # 存入缓存（1小时）
        try:
            await cache.set(cache_key, result, expire=3600)
        except Exception:
            pass  # 缓存失败不影响返回结果
        
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/paipan", summary="快速排盘")
async def paipan(request: QuickBaZiRequest):
    """
    快速排盘
    
    仅返回四柱八字基本信息
    """
    try:
        sizhu = calculate_sizhu(
            request.year,
            request.month,
            request.day,
            request.hour
        )
        
        return {
            "success": True,
            "data": {
                "bazi": sizhu.bazi,
                "year": str(sizhu.year),
                "month": str(sizhu.month),
                "day": str(sizhu.day),
                "hour": str(sizhu.hour),
                "day_master": sizhu.day_master
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/wuxing/{wuxing}", summary="五行信息查询")
async def get_wuxing_info(wuxing: str):
    """
    查询五行相关信息
    
    包含：颜色、方位、数字、行业等
    """
    from app.core.bazi.wuxing import WUXING_COLOR, WUXING_DIRECTION, WUXING_NUMBER, WUXING_CAREER
    
    if wuxing not in ["木", "火", "土", "金", "水"]:
        raise HTTPException(status_code=400, detail="无效的五行，请输入：木、火、土、金、水")
    
    return {
        "success": True,
        "data": {
            "wuxing": wuxing,
            "colors": WUXING_COLOR.get(wuxing, []),
            "direction": WUXING_DIRECTION.get(wuxing, ""),
            "numbers": WUXING_NUMBER.get(wuxing, []),
            "careers": WUXING_CAREER.get(wuxing, [])
        }
    }
