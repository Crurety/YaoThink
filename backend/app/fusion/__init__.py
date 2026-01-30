"""
玄心理命 - 融合分析模块
"""

from .mapper import (
    # 映射表
    WUXING_MBTI_MAP,
    MBTI_WUXING_MAP,
    SHISHEN_ARCHETYPE_MAP,
    PALACE_LIFE_DOMAIN_MAP,
    SHENSHA_TRAIT_MAP,
    
    # 映射函数
    get_wuxing_psychology,
    get_shishen_psychology,
    map_mbti_to_wuxing,
    map_palace_to_psychology
)

from .analyzer import (
    FusionResult,
    FusionAnalyzer,
    quick_fusion_analysis
)

from .report import (
    ReportGenerator,
    generate_report
)


__all__ = [
    # 映射表
    "WUXING_MBTI_MAP",
    "MBTI_WUXING_MAP", 
    "SHISHEN_ARCHETYPE_MAP",
    "PALACE_LIFE_DOMAIN_MAP",
    "SHENSHA_TRAIT_MAP",
    
    # 映射函数
    "get_wuxing_psychology",
    "get_shishen_psychology",
    "map_mbti_to_wuxing",
    "map_palace_to_psychology",
    
    # 分析器
    "FusionResult",
    "FusionAnalyzer",
    "quick_fusion_analysis",
    
    # 报告
    "ReportGenerator",
    "generate_report"
]
