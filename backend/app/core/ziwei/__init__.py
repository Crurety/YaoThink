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

# 高级算法
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


def analyze_ziwei(year_gan: str, year_zhi: str,
                  lunar_month: int, lunar_day: int,
                  birth_hour_zhi: str, advanced: bool = True) -> dict:
    """
    紫微斗数完整分析
    
    Args:
        year_gan: 年干
        year_zhi: 年支
        lunar_month: 农历月份 (1-12)
        lunar_day: 农历日 (1-30)
        birth_hour_zhi: 出生时辰地支
        advanced: 是否使用高级算法
    
    Returns:
        完整的紫微斗数分析结果
    """
    # 创建命盘
    chart = create_ziwei_chart(
        year_gan=year_gan,
        year_zhi=year_zhi,
        lunar_month=lunar_month,
        lunar_day=lunar_day,
        birth_hour_zhi=birth_hour_zhi
    )
    
    if advanced:
        # 应用高级算法
        arrange_sihua(chart.palaces, year_gan)
        arrange_lucun_tianma(chart.palaces, year_gan, year_zhi)
        arrange_qingyang_tuoluo(chart.palaces, year_gan)
        arrange_tiankui_tianyue(chart.palaces, year_gan)
        set_star_brightness(chart.palaces)
    
    # 分析命盘
    analysis = analyze_ziwei_chart(chart)
    
    # 高级格局分析
    if advanced:
        analysis["advanced_patterns"] = analyze_advanced_patterns(chart)
        
        # 各宫评分
        analysis["palace_scores"] = {}
        for palace in chart.palaces:
            analysis["palace_scores"][palace.name] = calculate_palace_score(palace)
    
    # 添加命盘图表数据
    chart_data = {
        "wuxing_ju": chart.wuxing_ju,
        "ming_gong": DI_ZHI[chart.ming_gong_index],
        "shen_gong": DI_ZHI[chart.shen_gong_index],
        "palaces": []
    }
    
    for palace in chart.palaces:
        main_stars = palace.get_main_stars()
        palace_data = {
            "name": palace.name,
            "position": f"{palace.tiangan}{palace.dizhi}",
            "stars": {
                "main": [{
                    "name": s.name,
                    "brightness": s.brightness,
                    "hua": s.hua
                } for s in main_stars],
                "auxiliary": [s.name for s in palace.get_auxiliary_stars()],
                "sha": [s.name for s in palace.get_sha_stars()]
            }
        }
        chart_data["palaces"].append(palace_data)
    
    return {
        "chart_data": chart_data,
        "analysis": analysis
    }


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
