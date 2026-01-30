"""
玄心理命 - 西方心理学模块
包含 MBTI、大五人格、荣格原型、九型人格
"""

# MBTI 人格类型
from .mbti import (
    # 常量
    MBTI_TYPES, MBTI_DESCRIPTIONS, MBTI_QUESTIONS,
    
    # 枚举
    MBTIDimension,
    
    # 数据类
    MBTIResult,
    
    # 核心函数
    calculate_mbti,
    get_mbti_compatibility,
    get_mbti_questions
)

# 大五人格
from .big5 import (
    # 常量
    BIG5_DIMENSIONS, BIG5_QUESTIONS, BIG5_OPTIONS,
    
    # 枚举
    Big5Dimension,
    
    # 数据类
    Big5Result,
    
    # 核心函数
    calculate_big5,
    get_big5_interpretation,
    get_big5_questions
)

# 荣格原型
from .archetype import (
    # 常量
    ARCHETYPES, ARCHETYPE_QUESTIONS, ARCHETYPE_OPTIONS,
    
    # 枚举
    ArchetypeType,
    
    # 数据类
    ArchetypeResult,
    
    # 核心函数
    calculate_archetype,
    get_archetype_questions
)

# 九型人格
from .enneagram import (
    # 常量
    ENNEAGRAM_TYPES, ENNEAGRAM_QUESTIONS, ENNEAGRAM_OPTIONS,
    
    # 枚举
    EnneagramType,
    
    # 数据类
    EnneagramResult,
    
    # 核心函数
    calculate_enneagram,
    get_enneagram_questions,
    get_enneagram_compatibility
)


__all__ = [
    # MBTI
    "MBTI_TYPES", "MBTI_DESCRIPTIONS", "MBTI_QUESTIONS",
    "MBTIDimension", "MBTIResult",
    "calculate_mbti", "get_mbti_compatibility", "get_mbti_questions",
    
    # 大五人格
    "BIG5_DIMENSIONS", "BIG5_QUESTIONS",
    "Big5Dimension", "Big5Result",
    "calculate_big5", "get_big5_interpretation", "get_big5_questions",
    
    # 荣格原型
    "ARCHETYPES", "ARCHETYPE_QUESTIONS",
    "ArchetypeType", "ArchetypeResult",
    "calculate_archetype", "get_archetype_questions",
    
    # 九型人格
    "ENNEAGRAM_TYPES", "ENNEAGRAM_QUESTIONS",
    "EnneagramType", "EnneagramResult",
    "calculate_enneagram", "get_enneagram_questions", "get_enneagram_compatibility"
]
