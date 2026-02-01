
from typing import Dict, List, Optional
from .palace import (
    ZiWeiChart, Palace, Star, StarType,
    create_ziwei_chart, analyze_ziwei_chart,
    DI_ZHI
)
from .advanced import (
    arrange_sihua, arrange_lucun_tianma,
    arrange_qingyang_tuoluo, arrange_tiankui_tianyue,
    set_star_brightness,
    analyze_advanced_patterns, calculate_palace_score
)

def analyze_ziwei(year_gan: str, year_zhi: str,
                  lunar_month: int, lunar_day: int,
                  birth_hour_zhi: str, advanced: bool = True) -> dict:
    """
    紫微斗数完整分析
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
