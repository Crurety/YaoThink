"""
玄心理命 - 紫微斗数API
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from pydantic import BaseModel, Field
from typing import Optional

from app.core.ziwei import analyze_ziwei, MAIN_STAR_TRAITS
from app.core.auth import get_current_user, TokenData

router = APIRouter()


class ZiWeiRequest(BaseModel):
    """紫微斗数请求"""
    year_gan: str = Field(..., description="年干")
    year_zhi: str = Field(..., description="年支")
    lunar_month: int = Field(..., ge=1, le=12, description="农历月份")
    lunar_day: int = Field(..., ge=1, le=30, description="农历日")
    birth_hour_zhi: str = Field(..., description="出生时辰地支")

    class Config:
        json_schema_extra = {
            "example": {
                "year_gan": "庚",
                "year_zhi": "午",
                "lunar_month": 5,
                "lunar_day": 15,
                "birth_hour_zhi": "巳"
            }
        }


class ZiWeiFromSolarRequest(BaseModel):
    """紫微斗数请求（公历输入）"""
    year: int = Field(..., ge=1900, le=2100, description="公历年份")
    month: int = Field(..., ge=1, le=12, description="公历月份")
    day: int = Field(..., ge=1, le=31, description="公历日")
    hour: int = Field(..., ge=0, le=23, description="出生时辰(24小时制)")

    class Config:
        json_schema_extra = {
            "example": {
                "year": 1990,
                "month": 6,
                "day": 15,
                "hour": 10
            }
        }


@router.post("/analyze", summary="紫微斗数分析")
async def analyze(
    request: ZiWeiRequest, 
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    紫微斗数命盘分析（需要登录）
    
    包含：十二宫排列、主星安排、格局判断、运势分析
    """
    try:
        # 1. 计算结果
        from app.core.cache import cache, CacheService
        cache_key = CacheService.ziwei_key(
            request.year_gan, request.year_zhi, 
            request.lunar_month, request.lunar_day, 
            request.birth_hour_zhi
        )
        
        result = None
        try:
            result = await cache.get(cache_key)
        except Exception:
            pass
            
        if not result:
            result = analyze_ziwei(
                year_gan=request.year_gan,
                year_zhi=request.year_zhi,
                lunar_month=request.lunar_month,
                lunar_day=request.lunar_day,
                birth_hour_zhi=request.birth_hour_zhi
            )
            try:
                await cache.set(cache_key, result, expire=3600)
            except Exception:
                pass
        
        # 2. 保存到数据库 (尝试保存，虽然没有具体年份)
        # 由于手动输入没有具体年份，我们创建一个特殊的BirthInfo或者仅记录分析
        # 这里为了统计，我们创建一个标记性的BirthInfo，年份设为0
        from app.core.user_service import HistoryService
        from app.core.database import BirthInfo
        
        birth_info = BirthInfo(
            user_id=current_user.user_id,
            name=f"紫微排盘-{request.year_gan}{request.year_zhi}年",
            birth_year=0, # 标记为无特定年份
            birth_month=request.lunar_month,
            birth_day=request.lunar_day,
            birth_hour=0,
            gender="未知",
            is_lunar=True
        )
        db.add(birth_info)
        await db.commit()
        await db.refresh(birth_info)
        
        history_service = HistoryService(db)
        await history_service.save_analysis(
            user_id=current_user.user_id,
            analysis_type="ziwei",
            birth_info_id=birth_info.id,
            result_data=result
        )
        
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze_solar", summary="紫微斗数分析（公历输入）")
async def analyze_from_solar(
    request: ZiWeiFromSolarRequest,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    紫微斗数命盘分析（自动转换公历为农历）
    """
    try:
        # 计算年干支
        from app.core.bazi.calendar import get_year_ganzhi, solar_to_lunar
        
        year_gz = get_year_ganzhi(request.year)
        
        # 公历转农历
        try:
            lunar_year, lunar_month, lunar_day, is_leap = solar_to_lunar(
                request.year, request.month, request.day
            )
        except NotImplementedError:
            # 简化处理：直接使用公历月日
            lunar_month = request.month
            lunar_day = request.day
        
        # 时辰地支
        DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        hour_zhi_map = {
            0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3,
            8: 4, 9: 4, 10: 5, 11: 5, 12: 6, 13: 6, 14: 7, 15: 7,
            16: 8, 17: 8, 18: 9, 19: 9, 20: 10, 21: 10, 22: 11, 23: 11
        }
        birth_hour_zhi = DI_ZHI[hour_zhi_map[request.hour]]
        
        result = analyze_ziwei(
            year_gan=year_gz.gan,
            year_zhi=year_gz.zhi,
            lunar_month=lunar_month,
            lunar_day=lunar_day,
            birth_hour_zhi=birth_hour_zhi
        )
        
        # 保存到数据库
        from app.core.user_service import HistoryService
        from app.core.database import BirthInfo
        from sqlalchemy import select
        
        # 查找或创建出生信息
        birth_info_result = await db.execute(
            select(BirthInfo).where(
                BirthInfo.user_id == current_user.user_id,
                BirthInfo.birth_year == request.year,
                BirthInfo.birth_month == request.month,
                BirthInfo.birth_day == request.day,
                BirthInfo.birth_hour == request.hour,
                BirthInfo.is_lunar == False
            )
        )
        birth_info = birth_info_result.scalar_one_or_none()
        
        if not birth_info:
            birth_info = BirthInfo(
                user_id=current_user.user_id,
                name=f"紫微-{request.year}{request.month:02d}{request.day:02d}",
                birth_year=request.year,
                birth_month=request.month,
                birth_day=request.day,
                birth_hour=request.hour,
                gender="未知",
                is_lunar=False,
                timezone="Asia/Shanghai"
            )
            db.add(birth_info)
            await db.commit()
            await db.refresh(birth_info)
            
        history_service = HistoryService(db)
        await history_service.save_analysis(
            user_id=current_user.user_id,
            analysis_type="ziwei",
            birth_info_id=birth_info.id,
            result_data=result
        )
        
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/star/{star_name}", summary="查询主星特性")
async def get_star_info(star_name: str):
    """
    查询十四主星特性
    """
    if star_name not in MAIN_STAR_TRAITS:
        raise HTTPException(
            status_code=400, 
            detail=f"无效的星名，可选：{list(MAIN_STAR_TRAITS.keys())}"
        )
    
    return {
        "success": True,
        "data": {
            "name": star_name,
            **MAIN_STAR_TRAITS[star_name]
        }
    }


@router.get("/stars", summary="获取所有主星列表")
async def get_all_stars():
    """
    获取十四主星完整列表
    """
    return {
        "success": True,
        "data": [
            {"name": name, **traits}
            for name, traits in MAIN_STAR_TRAITS.items()
        ]
    }
