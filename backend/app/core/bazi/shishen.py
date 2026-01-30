"""
玄心理命 - 十神分析模块
十神推演、十神关系、格局判断
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass

from .calendar import (
    SiZhu, GanZhi, TIAN_GAN, DI_ZHI,
    TIAN_GAN_WUXING, DI_ZHI_WUXING, DI_ZHI_CANG_GAN,
    TIAN_GAN_YINYANG
)
from .wuxing import WUXING_SHENG, WUXING_KE


# 十神名称
SHISHEN_NAMES = {
    "比肩": "比肩",  # 同我阳阴
    "劫财": "劫财",  # 同我异阴阳
    "食神": "食神",  # 我生同阴阳
    "伤官": "伤官",  # 我生异阴阳
    "偏财": "偏财",  # 我克同阴阳
    "正财": "正财",  # 我克异阴阳
    "七杀": "七杀",  # 克我同阴阳
    "正官": "正官",  # 克我异阴阳
    "偏印": "偏印",  # 生我同阴阳
    "正印": "正印"   # 生我异阴阳
}

# 十神简称
SHISHEN_SHORT = {
    "比肩": "比", "劫财": "劫",
    "食神": "食", "伤官": "伤",
    "偏财": "偏", "正财": "财",
    "七杀": "杀", "正官": "官",
    "偏印": "枭", "正印": "印"
}

# 十神特性描述
SHISHEN_TRAITS = {
    "比肩": {
        "keywords": ["独立", "自主", "坚持", "竞争"],
        "positive": "独立自主、意志坚定、自信勇敢、重义气",
        "negative": "固执己见、不善变通、争强好胜、我行我素",
        "career": "适合独立创业、自由职业、竞技运动等"
    },
    "劫财": {
        "keywords": ["社交", "投机", "冲动", "豪爽"],
        "positive": "豪爽大方、善于交际、行动力强、敢于冒险",
        "negative": "冲动浮躁、易破财、嫉妒心强、不守规则",
        "career": "适合销售、投资、娱乐行业等"
    },
    "食神": {
        "keywords": ["才华", "享受", "温和", "艺术"],
        "positive": "才华横溢、性情温和、懂得享受、有艺术天赋",
        "negative": "贪图安逸、缺乏进取、过于理想化",
        "career": "适合餐饮、艺术、教育、创意产业等"
    },
    "伤官": {
        "keywords": ["创新", "叛逆", "表现", "聪明"],
        "positive": "聪明伶俐、才思敏捷、创新能力强、表现欲强",
        "negative": "恃才傲物、尖酸刻薄、叛逆不羁、口舌是非",
        "career": "适合艺术、法律、技术创新、演艺等"
    },
    "偏财": {
        "keywords": ["灵活", "社交", "横财", "慷慨"],
        "positive": "善于理财、人缘极好、慷慨大方、机会多",
        "negative": "贪婪浮躁、投机取巧、感情不专、易破财",
        "career": "适合商业、金融、贸易、娱乐业等"
    },
    "正财": {
        "keywords": ["稳健", "节俭", "务实", "守财"],
        "positive": "勤俭持家、踏实可靠、理财有道、重视家庭",
        "negative": "过于保守、小气吝啬、缺乏魄力、患得患失",
        "career": "适合会计、银行、实业经营等"
    },
    "七杀": {
        "keywords": ["魄力", "权威", "果断", "压力"],
        "positive": "有魄力、敢担当、决断力强、有领导才能",
        "negative": "性格暴躁、压力大、易招是非、专制霸道",
        "career": "适合军警、管理层、外科医生等"
    },
    "正官": {
        "keywords": ["正派", "规矩", "责任", "稳重"],
        "positive": "品行端正、守规矩、有责任感、稳重可靠",
        "negative": "过于刻板、胆小怕事、缺乏变通、压力敏感",
        "career": "适合公务员、管理、法律、教育等"
    },
    "偏印": {
        "keywords": ["独特", "孤僻", "灵感", "偏门"],
        "positive": "思维独特、有灵感、适合偏门学问、悟性高",
        "negative": "性格孤僻、多疑敏感、不善交际、想法极端",
        "career": "适合宗教、命理、医学、研究等"
    },
    "正印": {
        "keywords": ["学识", "仁慈", "保守", "贵人"],
        "positive": "学识渊博、心地善良、有贵人相助、受人尊敬",
        "negative": "过于依赖、缺乏主见、保守固执、懒惰",
        "career": "适合教育、学术研究、慈善、文化等"
    }
}


def get_shishen(day_master: str, other_gan: str) -> str:
    """
    计算十神关系
    
    Args:
        day_master: 日主（日干）
        other_gan: 其他天干
    
    Returns:
        十神名称
    """
    dm_wuxing = TIAN_GAN_WUXING[day_master]
    other_wuxing = TIAN_GAN_WUXING[other_gan]
    dm_yinyang = TIAN_GAN_YINYANG[day_master]
    other_yinyang = TIAN_GAN_YINYANG[other_gan]
    
    same_yinyang = (dm_yinyang == other_yinyang)
    
    # 判断五行关系
    if dm_wuxing == other_wuxing:
        # 同我
        return "比肩" if same_yinyang else "劫财"
    elif WUXING_SHENG[dm_wuxing] == other_wuxing:
        # 我生
        return "食神" if same_yinyang else "伤官"
    elif WUXING_KE[dm_wuxing] == other_wuxing:
        # 我克
        return "偏财" if same_yinyang else "正财"
    elif WUXING_KE[other_wuxing] == dm_wuxing:
        # 克我
        return "七杀" if same_yinyang else "正官"
    elif WUXING_SHENG[other_wuxing] == dm_wuxing:
        # 生我
        return "偏印" if same_yinyang else "正印"
    
    return "未知"


@dataclass
class ShiShenResult:
    """十神分析结果"""
    position: str       # 位置（年干、月干等）
    gan: str            # 天干
    shishen: str        # 十神名称
    shishen_short: str  # 十神简称


def analyze_shishen(sizhu: SiZhu) -> Dict:
    """
    分析四柱十神
    
    Args:
        sizhu: 四柱八字
    
    Returns:
        十神分析结果
    """
    day_master = sizhu.day_master
    
    results = []
    
    # 年柱天干
    year_shishen = get_shishen(day_master, sizhu.year.gan)
    results.append(ShiShenResult("年干", sizhu.year.gan, year_shishen, SHISHEN_SHORT[year_shishen]))
    
    # 月柱天干
    month_shishen = get_shishen(day_master, sizhu.month.gan)
    results.append(ShiShenResult("月干", sizhu.month.gan, month_shishen, SHISHEN_SHORT[month_shishen]))
    
    # 日柱天干（日主本身）
    results.append(ShiShenResult("日干", sizhu.day.gan, "日主", "主"))
    
    # 时柱天干
    hour_shishen = get_shishen(day_master, sizhu.hour.gan)
    results.append(ShiShenResult("时干", sizhu.hour.gan, hour_shishen, SHISHEN_SHORT[hour_shishen]))
    
    # 分析地支藏干的十神
    zhi_shishen = {}
    for name, zhi in [("年支", sizhu.year.zhi), ("月支", sizhu.month.zhi), 
                       ("日支", sizhu.day.zhi), ("时支", sizhu.hour.zhi)]:
        cang_gan = DI_ZHI_CANG_GAN[zhi]
        zhi_shishen[name] = []
        for gan in cang_gan:
            ss = get_shishen(day_master, gan)
            zhi_shishen[name].append({
                "gan": gan,
                "shishen": ss,
                "shishen_short": SHISHEN_SHORT[ss]
            })
    
    return {
        "day_master": day_master,
        "gan_shishen": [
            {"position": r.position, "gan": r.gan, "shishen": r.shishen, "short": r.shishen_short}
            for r in results
        ],
        "zhi_shishen": zhi_shishen
    }


def count_shishen(sizhu: SiZhu) -> Dict[str, int]:
    """
    统计八字中各十神的数量
    
    Args:
        sizhu: 四柱八字
    
    Returns:
        各十神出现次数
    """
    counts = {name: 0 for name in SHISHEN_NAMES.keys()}
    analysis = analyze_shishen(sizhu)
    
    # 统计天干十神
    for item in analysis["gan_shishen"]:
        if item["shishen"] != "日主":
            counts[item["shishen"]] += 1
    
    # 统计地支藏干十神
    for zhi_name, gan_list in analysis["zhi_shishen"].items():
        for gan_info in gan_list:
            if gan_info["shishen"] != "日主":
                counts[gan_info["shishen"]] += 1
    
    return counts


def get_dominant_shishen(sizhu: SiZhu) -> List[Tuple[str, int]]:
    """
    获取主导十神（数量最多的十神）
    
    Args:
        sizhu: 四柱八字
    
    Returns:
        主导十神列表，按数量排序
    """
    counts = count_shishen(sizhu)
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return [(name, count) for name, count in sorted_counts if count > 0]


def get_shishen_personality(sizhu: SiZhu) -> Dict:
    """
    根据十神分析性格特征
    
    Args:
        sizhu: 四柱八字
    
    Returns:
        性格分析结果
    """
    dominant = get_dominant_shishen(sizhu)
    if not dominant:
        return {"error": "无法分析"}
    
    # 取前三个主导十神
    top_shishen = dominant[:3]
    
    keywords = []
    positive_traits = []
    negative_traits = []
    careers = []
    
    for shishen, count in top_shishen:
        traits = SHISHEN_TRAITS.get(shishen, {})
        keywords.extend(traits.get("keywords", []))
        positive_traits.append(traits.get("positive", ""))
        negative_traits.append(traits.get("negative", ""))
        careers.append(traits.get("career", ""))
    
    return {
        "dominant_shishen": top_shishen,
        "keywords": list(set(keywords)),
        "positive_traits": positive_traits,
        "negative_traits": negative_traits,
        "career_suggestions": careers,
        "summary": _generate_personality_summary(top_shishen)
    }


def _generate_personality_summary(top_shishen: List[Tuple[str, int]]) -> str:
    """生成性格总结"""
    if not top_shishen:
        return ""
    
    main_shishen = top_shishen[0][0]
    traits = SHISHEN_TRAITS.get(main_shishen, {})
    
    summary = f"您的八字以{main_shishen}为主导，"
    
    if main_shishen in ["比肩", "劫财"]:
        summary += "属于比劫旺的格局，独立自主，有进取心。"
    elif main_shishen in ["食神", "伤官"]:
        summary += "属于食伤旺的格局，才华出众，富有创意。"
    elif main_shishen in ["偏财", "正财"]:
        summary += "属于财星旺的格局，善于理财，务实勤劳。"
    elif main_shishen in ["七杀", "正官"]:
        summary += "属于官杀旺的格局，有责任感，事业心强。"
    elif main_shishen in ["偏印", "正印"]:
        summary += "属于印星旺的格局，学识渊博，有贵人运。"
    
    return summary


# 格局判断
GEJU_PATTERNS = {
    "正官格": {"condition": lambda ss: ss.get("正官", 0) >= 1 and ss.get("七杀", 0) == 0},
    "七杀格": {"condition": lambda ss: ss.get("七杀", 0) >= 1},
    "正财格": {"condition": lambda ss: ss.get("正财", 0) >= 1},
    "偏财格": {"condition": lambda ss: ss.get("偏财", 0) >= 1},
    "正印格": {"condition": lambda ss: ss.get("正印", 0) >= 1},
    "偏印格": {"condition": lambda ss: ss.get("偏印", 0) >= 1},
    "食神格": {"condition": lambda ss: ss.get("食神", 0) >= 1 and ss.get("伤官", 0) == 0},
    "伤官格": {"condition": lambda ss: ss.get("伤官", 0) >= 1},
    "比肩格": {"condition": lambda ss: ss.get("比肩", 0) >= 2},
    "劫财格": {"condition": lambda ss: ss.get("劫财", 0) >= 2}
}

GEJU_DESCRIPTIONS = {
    "正官格": "正官格者，为人正直守规，有责任感，适合从政或管理工作。",
    "七杀格": "七杀格者，有魄力胆识，敢于担当，适合军警或企业管理。",
    "正财格": "正财格者，勤俭持家，理财有道，适合稳定的财务工作。",
    "偏财格": "偏财格者，善于交际，财运活跃，适合商业经营。",
    "正印格": "正印格者，学识渊博，有贵人相助，适合学术教育工作。",
    "偏印格": "偏印格者，思维独特，适合研究或偏门技艺。",
    "食神格": "食神格者，才华横溢，性情温和，适合艺术创作或餐饮业。",
    "伤官格": "伤官格者，聪明伶俐，创新能力强，适合技术创新或艺术表演。",
    "比肩格": "比肩格者，独立自主，竞争意识强，适合独立创业。",
    "劫财格": "劫财格者，社交能力强，善于投机，需注意理财。"
}


def analyze_geju(sizhu: SiZhu) -> Dict:
    """
    分析命局格局
    
    Args:
        sizhu: 四柱八字
    
    Returns:
        格局分析结果
    """
    counts = count_shishen(sizhu)
    
    # 获取月令（月支藏干透出为格）
    month_zhi = sizhu.month.zhi
    month_canggan = DI_ZHI_CANG_GAN[month_zhi]
    day_master = sizhu.day_master
    
    # 判断主格局
    main_geju = None
    for geju_name, geju_info in GEJU_PATTERNS.items():
        if geju_info["condition"](counts):
            main_geju = geju_name
            break
    
    if not main_geju:
        main_geju = "普通格"
    
    return {
        "main_geju": main_geju,
        "description": GEJU_DESCRIPTIONS.get(main_geju, "普通格局，各方面较为平衡。"),
        "shishen_counts": counts,
        "month_zhi": month_zhi,
        "month_canggan": month_canggan
    }


if __name__ == "__main__":
    from .calendar import calculate_sizhu
    
    # 测试示例
    sizhu = calculate_sizhu(1990, 5, 15, 10)
    print(f"八字: {sizhu.bazi}")
    
    # 十神分析
    shishen = analyze_shishen(sizhu)
    print(f"十神分析: {shishen}")
    
    # 十神统计
    counts = count_shishen(sizhu)
    print(f"十神统计: {counts}")
    
    # 主导十神
    dominant = get_dominant_shishen(sizhu)
    print(f"主导十神: {dominant}")
    
    # 性格分析
    personality = get_shishen_personality(sizhu)
    print(f"性格分析: {personality}")
    
    # 格局分析
    geju = analyze_geju(sizhu)
    print(f"格局分析: {geju}")
