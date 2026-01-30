"""
玄心理命 - 八字核心算法模块
"""

from .calendar import (
    TIAN_GAN, DI_ZHI, SHENGXIAO,
    TIAN_GAN_WUXING, DI_ZHI_WUXING, DI_ZHI_CANG_GAN,
    TIAN_GAN_YINYANG, DI_ZHI_YINYANG,
    GanZhi, SiZhu,
    get_year_ganzhi, get_month_ganzhi, get_day_ganzhi, get_hour_ganzhi,
    get_shengxiao, calculate_sizhu,
    solar_to_lunar, lunar_to_solar
)

from .wuxing import (
    WuXing, WuXingScore,
    WUXING_SHENG, WUXING_KE, WUXING_BEI_KE, WUXING_BEI_SHENG,
    WUXING_COLOR, WUXING_DIRECTION, WUXING_NUMBER, WUXING_CAREER,
    calculate_wuxing_score,
    get_day_master_strength,
    get_xi_yong_shen,
    get_wuxing_relationship,
    get_wuxing_suggestions
)

from .shishen import (
    SHISHEN_NAMES, SHISHEN_SHORT, SHISHEN_TRAITS,
    get_shishen, analyze_shishen,
    count_shishen, get_dominant_shishen,
    get_shishen_personality,
    analyze_geju
)

from .dayun import (
    Gender, DaYun, LiuNian,
    calculate_qiyun_age, calculate_dayun, calculate_liunian,
    get_current_dayun, analyze_dayun_liunian
)

from .shensha import (
    ShenShaType, ShenSha,
    analyze_shensha, get_shensha_for_liunian,
    analyze_dizhi_relations
)


def analyze_bazi(year: int, month: int, day: int, hour: int, 
                 gender: str = "男", target_year: int = None) -> dict:
    """
    八字完整分析
    
    Args:
        year: 公历年份
        month: 公历月份
        day: 公历日
        hour: 24小时制的小时数
        gender: 性别（"男" 或 "女"）
        target_year: 目标年份（用于流年分析，默认当年）
    
    Returns:
        完整的八字分析结果
    """
    # 1. 计算四柱
    sizhu = calculate_sizhu(year, month, day, hour)
    
    # 2. 五行分析
    wuxing_score = calculate_wuxing_score(sizhu)
    day_master_strength = get_day_master_strength(sizhu)
    xi_yong = get_xi_yong_shen(sizhu)
    suggestions = get_wuxing_suggestions(xi_yong)
    
    # 3. 十神分析
    shishen = analyze_shishen(sizhu)
    shishen_counts = count_shishen(sizhu)
    personality = get_shishen_personality(sizhu)
    geju = analyze_geju(sizhu)
    
    # 4. 大运流年
    gender_enum = Gender.MALE if gender == "男" else Gender.FEMALE
    dayun_liunian = analyze_dayun_liunian(sizhu, gender_enum, year, month, day, target_year)
    
    # 5. 神煞分析
    shensha = analyze_shensha(sizhu)
    dizhi_relations = analyze_dizhi_relations(sizhu)
    
    return {
        "basic_info": {
            "birth_datetime": f"{year}年{month}月{day}日 {hour}时",
            "gender": gender,
            "shengxiao": get_shengxiao(year),
            "bazi": sizhu.bazi,
            "sizhu": {
                "year": str(sizhu.year),
                "month": str(sizhu.month),
                "day": str(sizhu.day),
                "hour": str(sizhu.hour)
            },
            "day_master": sizhu.day_master,
            "day_master_wuxing": day_master_strength["day_master_wuxing"]
        },
        "wuxing": {
            "scores": wuxing_score.to_dict(),
            "percentages": wuxing_score.percentages(),
            "balance": wuxing_score.balance_analysis(),
            "strongest": wuxing_score.strongest(),
            "weakest": wuxing_score.weakest()
        },
        "day_master_analysis": day_master_strength,
        "xi_yong_shen": xi_yong,
        "suggestions": suggestions,
        "shishen": shishen,
        "shishen_counts": shishen_counts,
        "personality": personality,
        "geju": geju,
        "dayun_liunian": dayun_liunian,
        "shensha": shensha,
        "dizhi_relations": dizhi_relations
    }


__all__ = [
    # 基础常量
    "TIAN_GAN", "DI_ZHI", "SHENGXIAO",
    "TIAN_GAN_WUXING", "DI_ZHI_WUXING", "DI_ZHI_CANG_GAN",
    # 数据类
    "GanZhi", "SiZhu", "WuXing", "WuXingScore", "Gender", "DaYun", "LiuNian",
    "ShenShaType", "ShenSha",
    # 核心函数
    "calculate_sizhu", "analyze_bazi",
    "calculate_wuxing_score", "get_day_master_strength", "get_xi_yong_shen",
    "analyze_shishen", "get_shishen_personality", "analyze_geju",
    "calculate_dayun", "calculate_liunian", "analyze_dayun_liunian",
    "analyze_shensha", "analyze_dizhi_relations"
]
