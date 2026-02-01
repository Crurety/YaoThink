"""
玄心理命 - 紫微斗数模块
"""

from .palace import (
    # 常量
    TWELVE_PALACES, DI_ZHI, TIAN_GAN,
    FOURTEEN_MAIN_STARS, MAIN_STAR_TRAITS,
    AUXILIARY_STARS, SHA_STARS,
    
    # 枚举类
    StarType,
    
    # 数据类
    Star, Palace, ZiWeiChart,
    
    # 核心函数
    calculate_ming_gong,
    calculate_shen_gong,
    arrange_twelve_palaces,
    calculate_wuxing_ju,
    calculate_ziwei_position,
    arrange_main_stars,
    arrange_auxiliary_stars,
    arrange_sha_stars,
    create_ziwei_chart,
    analyze_ziwei_chart
)

from .advanced import (
    # 四化
    SIHUA_TABLE,
    arrange_sihua,
    
    # 禄存天马
    LUCUN_TABLE, TIANMA_TABLE,
    arrange_lucun_tianma,
    
    # 擎羊陀罗
    QINGYANG_TABLE, TUOLUO_TABLE,
    arrange_qingyang_tuoluo,
    
    # 天魁天钺
    TIANKUI_TABLE, TIANYUE_TABLE,
    arrange_tiankui_tianyue,
    
    # 星曜亮度
    STAR_BRIGHTNESS,
    get_star_brightness,
    set_star_brightness,
    
    # 格局分析
    ADVANCED_PATTERNS,
    analyze_advanced_patterns,
    
    # 宫位评分
    calculate_palace_score
)

from .analysis import analyze_ziwei


__all__ = [
    # 常量
    "TWELVE_PALACES", "FOURTEEN_MAIN_STARS", "MAIN_STAR_TRAITS",
    "AUXILIARY_STARS", "SHA_STARS",
    "SIHUA_TABLE", "LUCUN_TABLE", "TIANMA_TABLE",
    "STAR_BRIGHTNESS",
    
    # 类型
    "StarType", "Star", "Palace", "ZiWeiChart",
    
    # 函数
    "create_ziwei_chart", "analyze_ziwei_chart", "analyze_ziwei",
    
    # 高级函数
    "arrange_sihua", "arrange_lucun_tianma", 
    "arrange_qingyang_tuoluo", "arrange_tiankui_tianyue",
    "set_star_brightness", "get_star_brightness",
    "analyze_advanced_patterns", "calculate_palace_score"
]
