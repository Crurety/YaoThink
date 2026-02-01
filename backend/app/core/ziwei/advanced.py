
from typing import Dict, List, Tuple, Optional
from .palace import Palace, Star, StarType, ZiWeiChart

# ==================== 四化星表 ====================
SIHUA_TABLE = {
    "甲": {"禄": "廉贞", "权": "破军", "科": "武曲", "忌": "太阳"},
    "乙": {"禄": "天机", "权": "天梁", "科": "紫微", "忌": "太阴"},
    "丙": {"禄": "天同", "权": "天机", "科": "文昌", "忌": "廉贞"},
    "丁": {"禄": "太阴", "权": "天同", "科": "天机", "忌": "巨门"},
    "戊": {"禄": "贪狼", "权": "太阴", "科": "右弼", "忌": "天机"},
    "己": {"禄": "武曲", "权": "贪狼", "科": "天梁", "忌": "文曲"},
    "庚": {"禄": "太阳", "权": "武曲", "科": "太阴", "忌": "天同"},
    "辛": {"禄": "巨门", "权": "太阳", "科": "文曲", "忌": "文昌"},
    "壬": {"禄": "天梁", "权": "紫微", "科": "左辅", "忌": "武曲"},
    "癸": {"禄": "破军", "权": "巨门", "科": "太阴", "忌": "贪狼"}
}

# ==================== 禄存安星表 ====================
LUCUN_TABLE = {
    "甲": "寅", "乙": "卯", "丙": "巳", "丁": "午",
    "戊": "巳", "己": "午", "庚": "申", "辛": "酉",
    "壬": "亥", "癸": "子"
}

# ==================== 天马安星表 ====================
TIANMA_TABLE = {
    "寅": "申", "午": "申", "戌": "申",  
    "申": "寅", "子": "寅", "辰": "寅",  
    "巳": "亥", "酉": "亥", "丑": "亥",  
    "亥": "巳", "卯": "巳", "未": "巳"   
}

# ==================== 擎羊陀罗安星表 ====================
QINGYANG_TABLE = {
    "甲": "卯", "乙": "辰", "丙": "午", "丁": "未",
    "戊": "午", "己": "未", "庚": "酉", "辛": "戌",
    "壬": "子", "癸": "丑"
}

TUOLUO_TABLE = {
    "甲": "丑", "乙": "寅", "丙": "辰", "丁": "巳",
    "戊": "辰", "己": "巳", "庚": "未", "辛": "申",
    "壬": "戌", "癸": "亥"
}

# ==================== 天魁天钺安星表 ====================
TIANKUI_TABLE = {
    "甲": "丑", "戊": "丑", "庚": "丑",
    "乙": "子", "己": "子",
    "丙": "亥", "丁": "亥",
    "辛": "午", "壬": "卯", "癸": "卯"
}

TIANYUE_TABLE = {
    "甲": "未", "戊": "未", "庚": "未",
    "乙": "申", "己": "申",
    "丙": "酉", "丁": "酉",
    "辛": "寅", "壬": "巳", "癸": "巳"
}

# ==================== 星曜庙旺落陷表 ====================
STAR_BRIGHTNESS_GROUPS = {
    "紫微": {
        "庙": ["午", "巳"],
        "旺": ["寅", "卯", "未", "申"],
        "得地": ["子", "丑", "酉", "戌"],
        "平和": ["辰", "亥"],
        "落陷": []
    },
    "天机": {
        "庙": ["丑", "未", "卯", "酉"],
        "旺": ["寅", "申"],
        "得地": ["子", "午"],
        "平和": ["辰", "戌"],
        "落陷": ["巳", "亥"]
    },
    "太阳": {
        "庙": ["卯", "辰", "巳", "午"],
        "旺": ["寅"],
        "得地": ["未"],
        "平和": ["申"],
        "落陷": ["酉", "戌", "亥", "子", "丑"]
    },
    "武曲": {
        "庙": ["辰", "戌", "丑", "未"],
        "旺": ["寅", "申", "卯", "酉"],
        "得地": ["子", "午"],
        "平和": [],
        "落陷": ["巳", "亥"]
    },
    "天同": {
        "庙": ["子", "丑", "申", "酉"],
        "旺": ["亥", "寅"],
        "得地": ["卯", "辰", "午"],
        "平和": ["巳", "未"],
        "落陷": ["戌"]
    },
    "廉贞": {
        "庙": ["寅", "申"],
        "旺": ["卯", "酉", "未"],
        "得地": ["子", "午"],
        "平和": ["辰", "戌", "丑"],
        "落陷": ["巳", "亥"]
    },
    "天府": {
        "庙": ["丑", "卯", "巳", "酉", "亥"],
        "旺": ["子", "寅", "午", "申", "戌"],
        "得地": ["辰", "未"],
        "平和": [],
        "落陷": []
    },
    "太阴": {
        "庙": ["酉", "戌", "亥", "子"],
        "旺": ["丑"],
        "得地": ["寅", "申"],
        "平和": ["未"],
        "落陷": ["卯", "辰", "巳", "午"]
    },
    "贪狼": {
        "庙": ["寅", "申", "丑", "未"],
        "旺": ["卯", "酉", "辰", "戌"],
        "得地": ["巳", "亥"],
        "平和": ["子", "午"],
        "落陷": []
    },
    "巨门": {
        "庙": ["子", "丑", "卯", "辰"],
        "旺": ["午", "未", "酉", "戌"],
        "得地": ["寅", "申"],
        "平和": ["巳", "亥"],
        "落陷": []
    },
    "天相": {
        "庙": ["丑", "未", "卯", "酉"],
        "旺": ["子", "午", "寅", "申"],
        "得地": ["辰", "戌"],
        "平和": [],
        "落陷": ["巳", "亥"]
    },
    "天梁": {
        "庙": ["子", "午", "丑", "未", "卯", "酉"],
        "旺": ["寅", "申"],
        "得地": ["辰", "戌"],
        "平和": [],
        "落陷": ["巳", "亥"]
    },
    "七杀": {
        "庙": ["寅", "申", "子", "午"],
        "旺": ["丑", "未", "辰", "戌"],
        "得地": [],
        "平和": ["卯", "酉"],
        "落陷": ["巳", "亥"]
    },
    "破军": {
        "庙": ["子", "午"],
        "旺": ["寅", "申"],
        "得地": ["辰", "戌"],
        "平和": ["丑", "未"],
        "落陷": ["卯", "酉", "巳", "亥"]
    }
}

# Alias for compatibility with __init__
STAR_BRIGHTNESS = STAR_BRIGHTNESS_GROUPS

# ==================== Optimization: Inverted Index ====================
STAR_BRIGHTNESS_INDEX = {}
for star, levels in STAR_BRIGHTNESS_GROUPS.items():
    for level, positions in levels.items():
        for pos in positions:
            STAR_BRIGHTNESS_INDEX[(star, pos)] = level


def get_star_brightness(star_name: str, dizhi: str) -> str:
    """获取星曜在某宫位的亮度 (O(1) Optimized)"""
    return STAR_BRIGHTNESS_INDEX.get((star_name, dizhi), "平和")

# ==================== 更多格局 ====================

ADVANCED_PATTERNS = {
    "紫府同宫": {
        "condition": lambda stars: "紫微" in stars and "天府" in stars,
        "level": "上上格",
        "description": "帝王之相，大富大贵，领导才能卓越"
    },
    "紫贪同宫": {
        "condition": lambda stars: "紫微" in stars and "贪狼" in stars,
        "level": "上格",
        "description": "才艺出众，有领导魅力，适合文艺领域"
    },
    "机月同梁": {
        "condition": lambda stars: len({"天机", "太阴", "天同", "天梁"}.intersection(stars)) >= 2,
        "level": "中上格",
        "description": "适合公职、技术、幕僚工作"
    },
    "日月同明": {
        "condition": lambda stars: "太阳" in stars and "太阴" in stars,
        "level": "上格",
        "description": "聪明才智，事业财运两全"
    },
    "杀破狼会": {
        "condition": lambda stars: not {"七杀", "破军", "贪狼"}.isdisjoint(stars),
        "level": "变格",
        "description": "变动开创，适合冒险创业"
    },
    "府相朝垣": {
        "condition": lambda stars: "天府" in stars or "天相" in stars,
        "level": "中上格",
        "description": "财官双美，稳定发展"
    },
    "武贪格": {
        "condition": lambda stars: "武曲" in stars and "贪狼" in stars,
        "level": "中上格",
        "description": "中年后发达，财运亨通"
    },
    "阳梁昌禄": {
        "condition": lambda stars: "太阳" in stars and "天梁" in stars,
        "level": "上格",
        "description": "适合考试、公职、名声"
    },
    "火贪格": {
        # Note: stars and sha are passed separately
        "condition": lambda stars, sha, _: "贪狼" in stars and "火星" in sha,
        "level": "中格",
        "description": "意外发财，横财运佳"
    },
    "铃贪格": {
        "condition": lambda stars, sha, _: "贪狼" in stars and "铃星" in sha,
        "level": "中格",
        "description": "意外收获，但需防变故"
    }
}


def analyze_advanced_patterns(chart: 'ZiWeiChart') -> List[Dict]:
    """
    分析高级格局 (Optimized)
    """
    ming_gong = chart.get_palace_by_name("命宫")
    if not ming_gong:
        return []
    
    # Pre-compute sets for O(1) checking
    main_star_set = {s.name for s in ming_gong.get_main_stars()}
    sha_star_set = {s.name for s in ming_gong.get_sha_stars()}
    
    patterns = []
    
    for pattern_name, pattern_info in ADVANCED_PATTERNS.items():
        condition = pattern_info["condition"]
        try:
            # Note: We need to handle lambda args generically
            # Check lambda arg count using code object
            arg_count = condition.__code__.co_argcount
            
            is_match = False
            if arg_count == 1:
                is_match = condition(main_star_set)
            elif arg_count == 2: # old impl had 2
                is_match = condition(main_star_set, sha_star_set)
            elif arg_count == 3: # new impl for fire/bell greed, dummy arg for safety
                is_match = condition(main_star_set, sha_star_set, None)
                
            if is_match:
                patterns.append({
                    "name": pattern_name,
                    "level": pattern_info["level"],
                    "description": pattern_info["description"]
                })
        except Exception:
            # Fail safely for pattern checks
            pass
    
    return patterns

def arrange_sihua(palaces: List[Palace], year_gan: str) -> None:
    if year_gan not in SIHUA_TABLE:
        return
    sihua = SIHUA_TABLE[year_gan]
    for palace in palaces:
        for star in palace.stars:
            for hua_type, star_name in sihua.items():
                if star.name == star_name:
                    star.hua = hua_type

def arrange_lucun_tianma(palaces: List[Palace], year_gan: str, year_zhi: str) -> None:
    palace_map = {p.dizhi: p for p in palaces}
    if year_gan in LUCUN_TABLE:
        lucun_zhi = LUCUN_TABLE[year_gan]
        if lucun_zhi in palace_map:
            palace_map[lucun_zhi].stars.append(Star(name="禄存", star_type=StarType.JIXING, description="财禄之星，主稳定财运"))
    if year_zhi in TIANMA_TABLE:
        tianma_zhi = TIANMA_TABLE[year_zhi]
        if tianma_zhi in palace_map:
            palace_map[tianma_zhi].stars.append(Star(name="天马", star_type=StarType.JIXING, description="奔波走动，利外出发展"))

def arrange_qingyang_tuoluo(palaces: List[Palace], year_gan: str) -> None:
    palace_map = {p.dizhi: p for p in palaces}
    if year_gan in QINGYANG_TABLE:
        qy_zhi = QINGYANG_TABLE[year_gan]
        if qy_zhi in palace_map:
            palace_map[qy_zhi].stars.append(Star(name="擎羊", star_type=StarType.SHAXING, description="刚烈冲动，易有意外"))
    if year_gan in TUOLUO_TABLE:
        tl_zhi = TUOLUO_TABLE[year_gan]
        if tl_zhi in palace_map:
            palace_map[tl_zhi].stars.append(Star(name="陀罗", star_type=StarType.SHAXING, description="拖延纠缠，做事反复"))

def arrange_tiankui_tianyue(palaces: List[Palace], year_gan: str) -> None:
    palace_map = {p.dizhi: p for p in palaces}
    if year_gan in TIANKUI_TABLE:
        tk_zhi = TIANKUI_TABLE[year_gan]
        if tk_zhi in palace_map:
            palace_map[tk_zhi].stars.append(Star(name="天魁", star_type=StarType.JIXING, description="阳贵人，主贵人相助"))
    if year_gan in TIANYUE_TABLE:
        ty_zhi = TIANYUE_TABLE[year_gan]
        if ty_zhi in palace_map:
            palace_map[ty_zhi].stars.append(Star(name="天钺", star_type=StarType.JIXING, description="阴贵人，主贵人相助"))

def set_star_brightness(palaces: List[Palace]) -> None:
    for palace in palaces:
        for star in palace.stars:
            if star.star_type == StarType.ZHUXING:
                star.brightness = get_star_brightness(star.name, palace.dizhi)

def calculate_palace_score(palace: Palace) -> Dict:
    score = 50
    positive_factors = []
    negative_factors = []
    main_stars = palace.get_main_stars()
    for star in main_stars:
        if star.brightness == "庙": score += 20; positive_factors.append(f"{star.name}入庙")
        elif star.brightness == "旺": score += 15; positive_factors.append(f"{star.name}旺")
        elif star.brightness == "得地": score += 10
        elif star.brightness == "落陷": score -= 15; negative_factors.append(f"{star.name}落陷")
        if star.hua == "禄": score += 15; positive_factors.append(f"{star.name}化禄")
        elif star.hua == "权": score += 12; positive_factors.append(f"{star.name}化权")
        elif star.hua == "科": score += 10; positive_factors.append(f"{star.name}化科")
        elif star.hua == "忌": score -= 15; negative_factors.append(f"{star.name}化忌")
    aux_stars = palace.get_auxiliary_stars()
    for star in aux_stars:
        if star.name in ["左辅", "右弼"]: score += 8; positive_factors.append(star.name)
        elif star.name in ["文昌", "文曲"]: score += 6; positive_factors.append(star.name)
        elif star.name in ["天魁", "天钺"]: score += 10; positive_factors.append(star.name)
        elif star.name in ["禄存"]: score += 12; positive_factors.append(star.name)
        elif star.name in ["天马"]: score += 5
    sha_stars = palace.get_sha_stars()
    for star in sha_stars:
        if star.name in ["擎羊", "陀罗"]: score -= 10; negative_factors.append(star.name)
        elif star.name in ["火星", "铃星"]: score -= 8; negative_factors.append(star.name)
        elif star.name in ["地空", "地劫"]: score -= 12; negative_factors.append(star.name)
    score = max(0, min(100, score))
    if score >= 80: level = "极佳"
    elif score >= 65: level = "良好"
    elif score >= 50: level = "中等"
    elif score >= 35: level = "偏弱"
    else: level = "不佳"
    return {"score": score, "level": level, "positive_factors": positive_factors, "negative_factors": negative_factors}
