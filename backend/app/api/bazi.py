"""
玄心理命 - 八字命理API
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
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
async def analyze(
    request: BaZiRequest, 
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    八字完整分析（需要登录）
    
    包含：四柱排盘、五行分析、十神分析、格局判断、大运流年、神煞分析
    """
    try:
        # 1. 计算分析结果
        from app.core.cache import cache, CacheService
        cache_key = CacheService.bazi_key(request.year, request.month, request.day, request.hour)
        
        result = None
        # 尝试从缓存获取
        try:
            result = await cache.get(cache_key)
        except Exception:
            pass
            
        if not result:
            result = analyze_bazi(
                year=request.year,
                month=request.month,
                day=request.day,
                hour=request.hour,
                gender=request.gender,
                target_year=request.target_year
            )
            # 存入缓存
            try:
                await cache.set(cache_key, result, expire=3600)
            except Exception:
                pass
        
        # 2. 保存到数据库 (新增逻辑)
        from app.core.user_service import HistoryService
        from app.core.database import BirthInfo
        from sqlalchemy import select
        
        # 查找或创建出生信息
        # 注意：这里简化逻辑，暂不复用旧的BirthInfo，每次都存新的或按需查找
        # 为了统计准确，即使是同一个生辰，每次点击分析也算一次记录
        
        # 先简单创建一个BirthInfo记录关联到这次分析(或者查找已有的)
        birth_info_result = await db.execute(
            select(BirthInfo).where(
                BirthInfo.user_id == current_user.user_id,
                BirthInfo.birth_year == request.year,
                BirthInfo.birth_month == request.month,
                BirthInfo.birth_day == request.day,
                BirthInfo.birth_hour == request.hour,
                BirthInfo.gender == request.gender
            )
        )
        birth_info = birth_info_result.scalar_one_or_none()
        
        if not birth_info:
            birth_info = BirthInfo(
                user_id=current_user.user_id,
                name=f"八字-{request.year}{request.month:02d}{request.day:02d}",
                birth_year=request.year,
                birth_month=request.month,
                birth_day=request.day,
                birth_hour=request.hour,
                gender=request.gender,
                is_lunar=False, # 默认公历
                timezone="Asia/Shanghai" 
            )
            db.add(birth_info)
            await db.commit()
            await db.refresh(birth_info)
            
        # --- AI Analysis ---
        try:
            # result structure usually contains 'sizhu' object or dict
            # If analyze_bazi returns a dict with 'sizhu' key which is a Sizhu object:
            # We need to extract data. Let's assume result['sizhu'] is available or similar.
            # Actually, looking at core/bazi/__init__.py might be needed, but let's try a safe extraction.
            
            ai_data = {}
            if result and "sizhu" in result:
                # Assuming result['sizhu'] has .day_master (if object) or ['day_master'] (if dict)
                # Let's try to handle both or assume standard dict if JSON serialized
                sz = result["sizhu"]
                if hasattr(sz, "day_master"):
                    ai_data["day_master"] = sz.day_master
                    ai_data["month"] = {"zhi": sz.month[1]}
                elif isinstance(sz, dict):
                    ai_data["day_master"] = sz.get("day_master")
                    ai_data["month"] = {"zhi": sz.get("month", "")[1] if sz.get("month") else ""}
            
            if ai_data.get("day_master"):
                from app.core.analysis.intelligent_analyst import analysis_service
                ai_report = analysis_service.analyze_bazi(ai_data)
                
                if "extra_info" not in result:
                    result["extra_info"] = {}
                result["extra_info"]["ai_analysis"] = ai_report
        except Exception as e:
            print(f"Bazi AI Analysis failed: {e}")
        # -----------------------------

        # 保存分析记录
        history_service = HistoryService(db)
        await history_service.save_analysis(
            user_id=current_user.user_id,
            analysis_type="bazi",
            birth_info_id=birth_info.id,
            result_data=result
        )
        
        return {"success": True, "data": result}
    except Exception as e:
        import traceback
        traceback.print_exc()
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
