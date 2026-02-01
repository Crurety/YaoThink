"""
玄心理命 - 心理学测试API
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

from ..core.psychology import (
    # MBTI
    calculate_mbti, get_mbti_questions, get_mbti_compatibility,
    MBTI_TYPES, MBTI_DESCRIPTIONS,
    
    # 大五人格
    calculate_big5, get_big5_questions, get_big5_interpretation,
    BIG5_DIMENSIONS,
    
    # 荣格原型
    calculate_archetype, get_archetype_questions,
    ARCHETYPES,
    
    # 九型人格
    calculate_enneagram, get_enneagram_questions, get_enneagram_compatibility,
    ENNEAGRAM_TYPES
)

router = APIRouter(tags=["心理学测试"])


# ==================== 请求/响应模型 ====================

class TestAnswer(BaseModel):
    """测试答案"""
    question_id: int
    value: int = Field(ge=1, le=5, description="答案值 1-5")


class MBTIAnswer(BaseModel):
    """MBTI答案"""
    question_id: int
    option_index: int = Field(ge=0, le=1, description="选项索引 0-1")


class SubmitTestRequest(BaseModel):
    """提交测试请求"""
    answers: List[TestAnswer]


class SubmitMBTIRequest(BaseModel):
    """提交MBTI测试请求"""
    answers: List[MBTIAnswer]


class CompatibilityRequest(BaseModel):
    """兼容性分析请求"""
    type1: str
    type2: str


class EnneagramCompatibilityRequest(BaseModel):
    """九型人格兼容性请求"""
    type1: int = Field(ge=1, le=9)
    type2: int = Field(ge=1, le=9)


# ==================== MBTI API ====================

@router.get("/mbti/questions")
async def get_mbti_test_questions(level: str = "master"):
    """
    获取MBTI测试题目
    
    Args:
        level: 难度等级 (simple/professional/master)
    """
    questions = get_mbti_questions(level)
    
    # 估算时间
    count = len(questions)
    estimated_time = f"{max(5, count // 3)}-{max(10, count // 2)}分钟"
    
    return {
        "test_name": "MBTI人格类型测试",
        "description": "迈尔斯-布里格斯类型指标，分析你的性格类型",
        "total_questions": count,
        "level": level,
        "estimated_time": estimated_time,
        "questions": questions
    }


@router.post("/mbti/submit")
async def submit_mbti_test(request: SubmitMBTIRequest):
    """提交MBTI测试并获取结果"""
    try:
        answers = [{"question_id": a.question_id, "option_index": a.option_index} 
                   for a in request.answers]
        
        result = calculate_mbti(answers)
        
        return {
            "success": True,
            "result": {
                "type_code": result.type_code,
                "type_name": result.type_name,
                "dimensions": result.dimensions,
                "description": result.description,
                "confidence": result.confidence
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/mbti/types")
async def get_all_mbti_types():
    """获取所有MBTI类型信息"""
    return {
        "types": MBTI_TYPES,
        "descriptions": MBTI_DESCRIPTIONS
    }


@router.get("/mbti/type/{type_code}")
async def get_mbti_type_detail(type_code: str):
    """获取特定MBTI类型详情"""
    type_code = type_code.upper()
    if type_code not in MBTI_DESCRIPTIONS:
        raise HTTPException(status_code=404, detail="类型不存在")
    
    return {
        "type_code": type_code,
        **MBTI_DESCRIPTIONS[type_code]
    }


@router.post("/mbti/compatibility")
async def check_mbti_compatibility(request: CompatibilityRequest):
    """检查两种MBTI类型的兼容性"""
    type1 = request.type1.upper()
    type2 = request.type2.upper()
    
    if type1 not in MBTI_TYPES or type2 not in MBTI_TYPES:
        raise HTTPException(status_code=400, detail="无效的MBTI类型")
    
    result = get_mbti_compatibility(type1, type2)
    return result


# ==================== 大五人格 API ====================

@router.get("/big5/questions")
async def get_big5_test_questions(level: str = "master"):
    """
    获取大五人格测试题目
    
    Args:
        level: 难度等级 (simple/professional/master)
    """
    questions = get_big5_questions(level)
    
    count = len(questions)
    estimated_time = f"{max(3, count // 4)}-{max(8, count // 3)}分钟"
    
    return {
        "test_name": "大五人格测试",
        "description": "NEO-FFI量表，评估五大人格维度",
        "total_questions": count,
        "level": level,
        "estimated_time": estimated_time,
        "dimensions": list(BIG5_DIMENSIONS.keys()),
        "questions": questions
    }


@router.post("/big5/submit")
async def submit_big5_test(request: SubmitTestRequest):
    """提交大五人格测试并获取结果"""
    try:
        answers = [{"question_id": a.question_id, "value": a.value} 
                   for a in request.answers]
        
        result = calculate_big5(answers)
        interpretation = get_big5_interpretation(result.scores)
        
        return {
            "success": True,
            "result": {
                "scores": result.scores,
                "percentiles": result.percentiles,
                "levels": result.levels,
                "profile": result.profile,
                "interpretation": interpretation,
                "reliability": result.reliability
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/big5/dimensions")
async def get_big5_dimensions():
    """获取大五人格维度说明"""
    return {"dimensions": BIG5_DIMENSIONS}


# ==================== 荣格原型 API ====================

@router.get("/archetype/questions")
async def get_archetype_test_questions(level: str = "master"):
    """
    获取荣格原型测试题目
    
    Args:
        level: 难度等级 (simple/professional/master)
    """
    questions = get_archetype_questions(level)
    
    count = len(questions)
    estimated_time = f"{max(5, count // 4)}-{max(8, count // 3)}分钟"
    
    return {
        "test_name": "荣格原型测试",
        "description": "发现你的主要心理原型",
        "total_questions": count,
        "level": level,
        "estimated_time": estimated_time,
        "archetypes": list(ARCHETYPES.keys()),
        "questions": questions
    }


@router.post("/archetype/submit")
async def submit_archetype_test(request: SubmitTestRequest):
    """提交荣格原型测试并获取结果"""
    try:
        answers = [{"question_id": a.question_id, "value": a.value} 
                   for a in request.answers]
        
        result = calculate_archetype(answers)
        
        return {
            "success": True,
            "result": {
                "primary": result.primary,
                "secondary": result.secondary,
                "all_scores": result.all_scores,
                "profile": result.profile
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/archetype/types")
async def get_all_archetypes():
    """获取所有荣格原型信息"""
    return {"archetypes": ARCHETYPES}


@router.get("/archetype/type/{archetype_code}")
async def get_archetype_detail(archetype_code: str):
    """获取特定原型详情"""
    archetype_code = archetype_code.upper()
    if archetype_code not in ARCHETYPES:
        raise HTTPException(status_code=404, detail="原型不存在")
    
    return {
        "code": archetype_code,
        **ARCHETYPES[archetype_code]
    }


# ==================== 九型人格 API ====================

@router.get("/enneagram/questions")
async def get_enneagram_test_questions(level: str = "master"):
    """
    获取九型人格测试题目
    
    Args:
        level: 难度等级 (simple/professional/master)
    """
    questions = get_enneagram_questions(level)
    
    count = len(questions)
    estimated_time = f"{max(5, count // 4)}-{max(10, count // 3)}分钟"
    
    return {
        "test_name": "九型人格测试",
        "description": "发现你的核心人格类型",
        "total_questions": count,
        "level": level,
        "estimated_time": estimated_time,
        "types": list(range(1, 10)),
        "questions": questions
    }


@router.post("/enneagram/submit")
async def submit_enneagram_test(request: SubmitTestRequest):
    """提交九型人格测试并获取结果"""
    try:
        answers = [{"question_id": a.question_id, "value": a.value} 
                   for a in request.answers]
        
        result = calculate_enneagram(answers)
        
        return {
            "success": True,
            "result": {
                "primary_type": result.primary_type,
                "primary_info": result.primary_info,
                "wing": result.wing,
                "all_scores": result.all_scores,
                "stress_direction": result.stress_direction,
                "growth_direction": result.growth_direction,
                "profile": result.profile
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/enneagram/types")
async def get_all_enneagram_types():
    """获取所有九型人格信息"""
    return {"types": ENNEAGRAM_TYPES}


@router.get("/enneagram/type/{type_num}")
async def get_enneagram_type_detail(type_num: int):
    """获取特定类型详情"""
    if type_num not in ENNEAGRAM_TYPES:
        raise HTTPException(status_code=404, detail="类型不存在")
    
    return {
        "type": type_num,
        **ENNEAGRAM_TYPES[type_num]
    }


@router.post("/enneagram/compatibility")
async def check_enneagram_compatibility(request: EnneagramCompatibilityRequest):
    """检查两种九型人格的兼容性"""
    result = get_enneagram_compatibility(request.type1, request.type2)
    return result


# ==================== 综合测试入口 ====================

@router.get("/tests")
async def get_available_tests():
    """获取所有可用的心理测试"""
    return {
        "tests": [
            {
                "id": "mbti",
                "name": "MBTI人格类型",
                "description": "16种人格类型测评",
                "questions": 93,
                "time": "20-30分钟"
            },
            {
                "id": "big5",
                "name": "大五人格",
                "description": "五大人格维度评估",
                "questions": 60,
                "time": "15-20分钟"
            },
            {
                "id": "archetype",
                "name": "荣格原型",
                "description": "12种心理原型分析",
                "questions": 72,
                "time": "15-20分钟"
            },
            {
                "id": "enneagram",
                "name": "九型人格",
                "description": "九种核心人格类型",
                "questions": 108,
                "time": "20-30分钟"
            }
        ]
    }
