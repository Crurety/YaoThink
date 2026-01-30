"""
玄心理命 - 融合分析API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

from ..fusion import (
    FusionAnalyzer,
    quick_fusion_analysis,
    generate_report,
    map_mbti_to_wuxing,
    get_wuxing_psychology,
    get_shishen_psychology,
    WUXING_MBTI_MAP,
    MBTI_WUXING_MAP
)

router = APIRouter(prefix="/fusion", tags=["融合分析"])


# ==================== 请求模型 ====================

class QuickFusionRequest(BaseModel):
    """快速融合分析请求"""
    mbti_type: Optional[str] = Field(None, description="MBTI类型")
    wuxing_scores: Optional[Dict[str, float]] = Field(None, description="五行得分")
    shishen_pattern: Optional[Dict[str, int]] = Field(None, description="十神格局")


class FullFusionRequest(BaseModel):
    """完整融合分析请求"""
    # 东方数据
    bazi_data: Optional[Dict[str, Any]] = Field(None, description="八字分析数据")
    ziwei_data: Optional[Dict[str, Any]] = Field(None, description="紫微分析数据")
    
    # 西方数据
    mbti_type: Optional[str] = Field(None, description="MBTI类型")
    big5_scores: Optional[Dict[str, float]] = Field(None, description="大五人格得分")
    archetype: Optional[str] = Field(None, description="荣格原型")
    enneagram_type: Optional[int] = Field(None, ge=1, le=9, description="九型人格类型")


class MappingRequest(BaseModel):
    """映射查询请求"""
    mbti_type: Optional[str] = None
    wuxing: Optional[str] = None


# ==================== API端点 ====================

@router.get("/info")
async def get_fusion_info():
    """获取融合分析模块信息"""
    return {
        "name": "融合分析引擎",
        "description": "整合东方命理与西方心理学的综合分析系统",
        "features": [
            "五行↔MBTI映射",
            "十神↔荣格原型映射",
            "宫位↔生活领域映射",
            "一致性分析",
            "个性化报告生成"
        ],
        "supported_inputs": {
            "eastern": ["八字命理", "紫微斗数"],
            "western": ["MBTI", "大五人格", "荣格原型", "九型人格"]
        }
    }


@router.post("/quick")
async def quick_fusion(request: QuickFusionRequest):
    """
    快速融合分析
    根据有限的输入数据进行快速分析
    """
    try:
        result = quick_fusion_analysis(
            mbti_type=request.mbti_type,
            wuxing_scores=request.wuxing_scores,
            shishen_pattern=request.shishen_pattern
        )
        
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/analyze")
async def full_fusion_analysis(request: FullFusionRequest):
    """
    完整融合分析
    整合所有可用数据进行综合分析
    """
    try:
        analyzer = FusionAnalyzer()
        
        result = analyzer.analyze(
            bazi_data=request.bazi_data,
            ziwei_data=request.ziwei_data,
            mbti_type=request.mbti_type,
            big5_scores=request.big5_scores,
            archetype=request.archetype,
            enneagram_type=request.enneagram_type
        )
        
        # 转换为可序列化的字典
        return {
            "success": True,
            "result": {
                "personality_fusion": result.personality_fusion,
                "consistency_analysis": result.consistency_analysis,
                "life_guidance": result.life_guidance,
                "confidence": result.confidence,
                "analysis_time": result.analysis_time
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/report")
async def generate_fusion_report(request: FullFusionRequest):
    """
    生成融合分析报告
    返回Markdown格式的完整报告
    """
    try:
        analyzer = FusionAnalyzer()
        
        fusion_result = analyzer.analyze(
            bazi_data=request.bazi_data,
            ziwei_data=request.ziwei_data,
            mbti_type=request.mbti_type,
            big5_scores=request.big5_scores,
            archetype=request.archetype,
            enneagram_type=request.enneagram_type
        )
        
        # 转换为字典
        result_dict = {
            "bazi_analysis": fusion_result.bazi_analysis,
            "ziwei_analysis": fusion_result.ziwei_analysis,
            "mbti_result": fusion_result.mbti_result,
            "big5_result": fusion_result.big5_result,
            "archetype_result": fusion_result.archetype_result,
            "enneagram_result": fusion_result.enneagram_result,
            "personality_fusion": fusion_result.personality_fusion,
            "consistency_analysis": fusion_result.consistency_analysis,
            "life_guidance": fusion_result.life_guidance,
            "confidence": fusion_result.confidence,
            "analysis_time": fusion_result.analysis_time
        }
        
        report_md = generate_report(result_dict, format="markdown")
        
        return {
            "success": True,
            "report": report_md,
            "format": "markdown"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/mapping/mbti/{mbti_type}")
async def get_mbti_mapping(mbti_type: str):
    """获取MBTI类型的五行映射"""
    mbti_type = mbti_type.upper()
    
    if mbti_type not in MBTI_WUXING_MAP:
        raise HTTPException(status_code=404, detail="无效的MBTI类型")
    
    mapping = map_mbti_to_wuxing(mbti_type)
    
    return {
        "mbti_type": mbti_type,
        "mapping": mapping,
        "wuxing_detail": WUXING_MBTI_MAP.get(mapping.get("primary"), {})
    }


@router.get("/mapping/wuxing/{wuxing}")
async def get_wuxing_mapping(wuxing: str):
    """获取五行的MBTI映射"""
    if wuxing not in WUXING_MBTI_MAP:
        raise HTTPException(status_code=404, detail="无效的五行")
    
    mapping = WUXING_MBTI_MAP[wuxing]
    
    return {
        "wuxing": wuxing,
        "mapping": mapping
    }


@router.post("/mapping/wuxing-psychology")
async def analyze_wuxing_psychology(wuxing_scores: Dict[str, float]):
    """根据五行得分分析心理特质"""
    try:
        result = get_wuxing_psychology(wuxing_scores)
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/mapping/shishen-psychology")
async def analyze_shishen_psychology(shishen_pattern: Dict[str, int]):
    """根据十神格局分析心理原型"""
    try:
        result = get_shishen_psychology(shishen_pattern)
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/mappings")
async def get_all_mappings():
    """获取所有映射关系"""
    return {
        "wuxing_mbti": WUXING_MBTI_MAP,
        "mbti_wuxing": MBTI_WUXING_MAP
    }
