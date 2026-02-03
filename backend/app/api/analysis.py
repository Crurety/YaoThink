
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

from app.core.analysis.rule_engine import engine
from app.core.auth import get_current_user

router = APIRouter()

class AnalysisRequest(BaseModel):
    """通用分析请求"""
    data: Dict[str, Any] = Field(..., description="分析所需的数据（如八字排盘结果）")
    type: str = Field(..., description="分析类型：bazi/ziwei/yijing")

@router.on_event("startup")
async def startup_event():
    """应用启动时加载规则库"""
    engine.load_rules()

@router.post("/analyze", summary="大数据智能分析")
async def analyze(request: AnalysisRequest, current_user = Depends(get_current_user)):
    """
    基于本地规则引擎的详细分析
    """
    try:
        # 确保规则已加载
        engine.load_rules()
        
        result = ""
        from app.core.analysis.intelligent_analyst import analysis_service
        
        result = ""
        if request.type == "bazi":
            result = analysis_service.analyze_bazi(request.data)
        elif request.type == "ziwei":
            result = analysis_service.analyze_ziwei(request.data)
        elif request.type == "yijing":
             result = analysis_service.analyze_yijing(request.data)
        else:
            raise HTTPException(status_code=400, detail="不支持的分析类型")
            
        return {
            "success": True, 
            "data": result,
            "engine_info": "Local Rule Engine v1.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
