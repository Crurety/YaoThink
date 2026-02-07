"""
玄心理命 - 易经占卜API
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.core.yijing import (
    meihua_by_time, meihua_by_numbers, meihua_by_text,
    liuyao_by_coins, analyze_hexagram, divine,
    BAGUA, SIXTY_FOUR_GUA
)
from app.core.auth import get_current_user, TokenData
# from app.core.analysis.rule_engine import engine (Removed)

router = APIRouter()


def _attach_ai_analysis(result: dict):
    """附加大数据分析"""
    try:
        # Prepare data for rule engine
        # result['original_hexagram'] contains 'name', 'upper', 'lower' etc.
        # result['dong_yao'] is index (1-6)
        # result['changed_gua'] contains the transformed hexagram info
        
        main_gua = result.get("main_gua", result.get("original_hexagram", {}))
        
        hex_data = {
            "main_gua": main_gua,
            "dong_yao": result.get("dong_yao"),
            "changed_gua": result.get("changed_gua", {})
        }
        
        from app.core.analysis.intelligent_analyst import analysis_service
        ai_report = analysis_service.analyze_yijing(hex_data)
        if ai_report:
           if "extra_info" not in result:
               result["extra_info"] = {}
           result["extra_info"]["ai_analysis"] = ai_report.get("content", "")
           result["extra_info"]["ai_analysis_structured"] = ai_report.get("structured", {})
    except Exception as e:
        print(f"Yijing AI Analysis failed: {e}")



class MeihuaTimeRequest(BaseModel):
    """梅花易数时间起卦请求"""
    question: Optional[str] = Field(None, description="问题（可选）")
    datetime_str: Optional[str] = Field(None, description="指定时间，格式：YYYY-MM-DD HH:MM")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "今日运势如何？"
            }
        }


class MeihuaNumberRequest(BaseModel):
    """梅花易数数字起卦请求"""
    number1: int = Field(..., ge=1, description="第一个数字")
    number2: int = Field(..., ge=1, description="第二个数字")
    question: Optional[str] = Field(None, description="问题（可选）")

    class Config:
        json_schema_extra = {
            "example": {
                "number1": 5,
                "number2": 8,
                "question": "事业发展如何？"
            }
        }


class MeihuaTextRequest(BaseModel):
    """梅花易数文字起卦请求"""
    text: str = Field(..., min_length=1, description="任意文字")
    question: Optional[str] = Field(None, description="问题（可选）")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "问事业",
                "question": "今年事业如何？"
            }
        }


class LiuYaoRequest(BaseModel):
    """六爻起卦请求"""
    question: Optional[str] = Field(None, description="问题（可选）")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "此事可成否？"
            }
        }


@router.post("/meihua/time", summary="梅花易数 - 时间起卦")
async def meihua_time(
    request: MeihuaTimeRequest, 
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    梅花易数时间起卦法（需要登录）
    
    根据当前或指定时间起卦
    """
    try:
        if request.datetime_str:
            dt = datetime.strptime(request.datetime_str, "%Y-%m-%d %H:%M")
        else:
            dt = None
        
        hexagram = meihua_by_time(dt)
        result = analyze_hexagram(hexagram, request.question or "")

        # Attach AI Analysis
        _attach_ai_analysis(result)
        
        # 保存记录
        from app.core.user_service import HistoryService
        history_service = HistoryService(db)
        await history_service.save_divination(
            user_id=current_user.user_id,
            method="meihua_time",
            question=request.question or "时间起卦",
            result_data=result
        )

        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/meihua/number", summary="梅花易数 - 数字起卦")
async def meihua_number(
    request: MeihuaNumberRequest, 
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    梅花易数数字起卦法（需要登录）
    
    输入两个数字起卦
    """
    try:
        hexagram = meihua_by_numbers(request.number1, request.number2)
        result = analyze_hexagram(hexagram, request.question or "")

        # Attach AI Analysis
        _attach_ai_analysis(result)
        
        # 保存记录
        from app.core.user_service import HistoryService
        history_service = HistoryService(db)
        await history_service.save_divination(
            user_id=current_user.user_id,
            method="meihua_number",
            question=request.question or f"数字起卦: {request.number1}, {request.number2}",
            result_data=result
        )

        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/meihua/text", summary="梅花易数 - 文字起卦")
async def meihua_text(
    request: MeihuaTextRequest, 
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    梅花易数文字起卦法（需要登录）
    
    根据任意文字起卦
    """
    try:
        hexagram = meihua_by_text(request.text)
        result = analyze_hexagram(hexagram, request.question or request.text)
        
        # Attach AI Analysis
        _attach_ai_analysis(result)
        
        # 保存记录
        from app.core.user_service import HistoryService
        history_service = HistoryService(db)
        await history_service.save_divination(
            user_id=current_user.user_id,
            method="meihua_text",
            question=request.question or request.text,
            result_data=result
        )
        
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/liuyao", summary="六爻 - 摇钱起卦")
async def liuyao(
    request: LiuYaoRequest, 
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    六爻摇钱起卦法（需要登录）
    
    模拟三枚铜钱摇六次
    """
    try:
        hexagram = liuyao_by_coins()
        result = analyze_hexagram(hexagram, request.question or "")

        # Attach AI Analysis
        _attach_ai_analysis(result)
        
        # 保存记录
        from app.core.user_service import HistoryService
        history_service = HistoryService(db)
        await history_service.save_divination(
            user_id=current_user.user_id,
            method="liuyao",
            question=request.question or "六爻起卦",
            result_data=result
        )
        
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gua/{gua_name}", summary="查询卦象信息")
async def get_gua_info(gua_name: str):
    """
    查询八卦或六十四卦信息
    """
    # 查询八卦
    if gua_name in BAGUA:
        return {
            "success": True,
            "data": {
                "type": "八卦",
                "name": gua_name,
                **BAGUA[gua_name]
            }
        }
    
    # 查询六十四卦
    for (upper, lower), full_name in SIXTY_FOUR_GUA.items():
        if gua_name == full_name or gua_name == f"{upper}{lower}":
            from app.core.yijing.hexagram import GUA_INTERPRETATIONS, DEFAULT_INTERPRETATION
            interp = GUA_INTERPRETATIONS.get(full_name, DEFAULT_INTERPRETATION)
            return {
                "success": True,
                "data": {
                    "type": "六十四卦",
                    "name": full_name,
                    "upper_gua": upper,
                    "lower_gua": lower,
                    **interp
                }
            }
    
    raise HTTPException(status_code=404, detail=f"未找到卦象：{gua_name}")


@router.get("/bagua", summary="获取八卦列表")
async def get_bagua_list():
    """
    获取八卦完整信息
    """
    return {
        "success": True,
        "data": [
            {"name": name, **info}
            for name, info in BAGUA.items()
        ]
    }


@router.get("/hexagrams", summary="获取六十四卦列表")
async def get_hexagrams_list():
    """
    获取六十四卦名称列表
    """
    hexagrams = []
    for (upper, lower), name in SIXTY_FOUR_GUA.items():
        hexagrams.append({
            "name": name,
            "upper_gua": upper,
            "lower_gua": lower,
            "upper_symbol": BAGUA[upper]["symbol"],
            "lower_symbol": BAGUA[lower]["symbol"]
        })
    
    return {
        "success": True,
        "data": hexagrams
    }
