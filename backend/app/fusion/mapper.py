"""
玄心理命 - 东西方映射模块
五行↔MBTI、十神↔原型、宫位↔领域、神煞↔特质
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


# ==================== 五行与MBTI映射 ====================

# 五行 → MBTI倾向映射
WUXING_MBTI_MAP = {
    "木": {
        "mbti_tendencies": ["N", "P"],  # 直觉、感知
        "mbti_types": ["ENFP", "INFP", "ENTP", "INTP"],
        "description": "木主生发创新，对应直觉型(N)和感知型(P)的开放探索特质",
        "keywords": ["成长", "创新", "探索", "理想"],
        "big5_high": ["O"],  # 高开放性
        "big5_low": []
    },
    "火": {
        "mbti_tendencies": ["E", "F"],  # 外向、情感
        "mbti_types": ["ESFP", "ENFJ", "ESFJ", "ENFP"],
        "description": "火主热情表达，对应外向型(E)和情感型(F)的人际互动特质",
        "keywords": ["热情", "表达", "感染力", "活力"],
        "big5_high": ["E", "A"],  # 高外向性、高宜人性
        "big5_low": []
    },
    "土": {
        "mbti_tendencies": ["S", "J"],  # 实感、判断
        "mbti_types": ["ISFJ", "ISTJ", "ESFJ", "ESTJ"],
        "description": "土主稳重踏实，对应实感型(S)和判断型(J)的务实执行特质",
        "keywords": ["稳定", "责任", "踏实", "包容"],
        "big5_high": ["C", "A"],  # 高尽责性、高宜人性
        "big5_low": ["O"]
    },
    "金": {
        "mbti_tendencies": ["T", "J"],  # 思考、判断
        "mbti_types": ["INTJ", "ENTJ", "ISTJ", "ESTJ"],
        "description": "金主果断决绝，对应思考型(T)和判断型(J)的理性决策特质",
        "keywords": ["秩序", "效率", "果断", "原则"],
        "big5_high": ["C"],  # 高尽责性
        "big5_low": ["A"]
    },
    "水": {
        "mbti_tendencies": ["I", "N"],  # 内向、直觉
        "mbti_types": ["INFJ", "INTJ", "INTP", "INFP"],
        "description": "水主智慧深沉，对应内向型(I)和直觉型(N)的深度思考特质",
        "keywords": ["智慧", "深沉", "适应", "洞察"],
        "big5_high": ["O"],  # 高开放性
        "big5_low": ["E"]
    }
}


# MBTI → 五行反向映射
MBTI_WUXING_MAP = {
    "INTJ": {"primary": "水", "secondary": "金", "description": "水的智慧+金的决断"},
    "INTP": {"primary": "水", "secondary": "木", "description": "水的深思+木的创新"},
    "ENTJ": {"primary": "金", "secondary": "火", "description": "金的果断+火的领导力"},
    "ENTP": {"primary": "木", "secondary": "火", "description": "木的创新+火的表达"},
    "INFJ": {"primary": "水", "secondary": "木", "description": "水的洞察+木的理想"},
    "INFP": {"primary": "木", "secondary": "水", "description": "木的理想+水的敏感"},
    "ENFJ": {"primary": "火", "secondary": "土", "description": "火的热情+土的关怀"},
    "ENFP": {"primary": "木", "secondary": "火", "description": "木的创意+火的热情"},
    "ISTJ": {"primary": "土", "secondary": "金", "description": "土的稳重+金的原则"},
    "ISFJ": {"primary": "土", "secondary": "水", "description": "土的奉献+水的敏感"},
    "ESTJ": {"primary": "金", "secondary": "土", "description": "金的效率+土的责任"},
    "ESFJ": {"primary": "土", "secondary": "火", "description": "土的关怀+火的热情"},
    "ISTP": {"primary": "金", "secondary": "水", "description": "金的理性+水的灵活"},
    "ISFP": {"primary": "木", "secondary": "土", "description": "木的艺术+土的和谐"},
    "ESTP": {"primary": "火", "secondary": "金", "description": "火的行动+金的果断"},
    "ESFP": {"primary": "火", "secondary": "木", "description": "火的热情+木的自由"}
}


# ==================== 十神与荣格原型映射 ====================

SHISHEN_ARCHETYPE_MAP = {
    "比肩": {
        "archetypes": ["EVERYMAN", "HERO"],
        "description": "比肩代表同辈竞争，对应凡人的平等意识和英雄的挑战精神",
        "keywords": ["独立", "竞争", "合作", "自我"],
        "enneagram": [3, 8]  # 成就者、挑战者
    },
    "劫财": {
        "archetypes": ["REBEL", "HERO"],
        "description": "劫财代表争夺冒险，对应叛逆者的打破常规和英雄的勇气",
        "keywords": ["冒险", "争夺", "突破", "不羁"],
        "enneagram": [7, 8]
    },
    "食神": {
        "archetypes": ["CREATOR", "JESTER"],
        "description": "食神代表才华表达，对应创造者的艺术天赋和愚者的乐观",
        "keywords": ["才艺", "表达", "享受", "创作"],
        "enneagram": [4, 7]
    },
    "伤官": {
        "archetypes": ["REBEL", "CREATOR"],
        "description": "伤官代表叛逆创新，对应叛逆者的颠覆和创造者的独特表达",
        "keywords": ["叛逆", "创新", "个性", "尖锐"],
        "enneagram": [4, 8]
    },
    "正财": {
        "archetypes": ["EVERYMAN", "CAREGIVER"],
        "description": "正财代表稳定务实，对应凡人的踏实和照顾者的责任",
        "keywords": ["务实", "稳健", "积累", "节俭"],
        "enneagram": [1, 6]
    },
    "偏财": {
        "archetypes": ["EXPLORER", "MAGICIAN"],
        "description": "偏财代表机遇灵活，对应探险家的冒险和魔法师的转化能力",
        "keywords": ["机遇", "灵活", "社交", "投机"],
        "enneagram": [3, 7]
    },
    "正官": {
        "archetypes": ["RULER", "CAREGIVER"],
        "description": "正官代表权威责任，对应统治者的领导和照顾者的保护",
        "keywords": ["权威", "责任", "正统", "规范"],
        "enneagram": [1, 8]
    },
    "七杀": {
        "archetypes": ["HERO", "REBEL"],
        "description": "七杀代表魄力决断，对应英雄的勇气和叛逆者的果敢",
        "keywords": ["魄力", "决断", "压力", "突破"],
        "enneagram": [8, 3]
    },
    "正印": {
        "archetypes": ["SAGE", "CAREGIVER"],
        "description": "正印代表智慧庇护，对应智者的知识和照顾者的保护",
        "keywords": ["智慧", "庇护", "学识", "慈爱"],
        "enneagram": [5, 2]
    },
    "偏印": {
        "archetypes": ["SAGE", "MAGICIAN"],
        "description": "偏印代表玄学独特，对应智者的深思和魔法师的神秘",
        "keywords": ["玄学", "独特", "冷门", "孤高"],
        "enneagram": [4, 5]
    }
}


# ==================== 紫微宫位与生活领域映射 ====================

PALACE_LIFE_DOMAIN_MAP = {
    "命宫": {
        "life_domains": ["自我认知", "人生态度", "性格特质"],
        "psychology_aspects": ["自我概念", "核心价值观", "人格基础"],
        "questions": ["我是谁？", "我的核心特质是什么？"]
    },
    "兄弟宫": {
        "life_domains": ["手足关系", "同辈互动", "合作伙伴"],
        "psychology_aspects": ["同伴关系", "竞争合作", "社会支持"],
        "questions": ["我如何与同辈相处？", "我的合作模式是什么？"]
    },
    "夫妻宫": {
        "life_domains": ["亲密关系", "婚姻", "重要合作"],
        "psychology_aspects": ["依恋模式", "亲密需求", "关系期待"],
        "questions": ["我期望什么样的伴侣？", "我的亲密关系模式？"]
    },
    "子女宫": {
        "life_domains": ["子女", "创作", "投资"],
        "psychology_aspects": ["创造力", "养育态度", "表达方式"],
        "questions": ["我如何表达创意？", "我的养育风格？"]
    },
    "财帛宫": {
        "life_domains": ["财富", "价值观", "资源管理"],
        "psychology_aspects": ["金钱观", "安全感", "自我价值"],
        "questions": ["我如何看待金钱？", "我的赚钱方式？"]
    },
    "疾厄宫": {
        "life_domains": ["健康", "危机", "转化"],
        "psychology_aspects": ["压力应对", "阴影面", "转化能力"],
        "questions": ["我如何应对危机？", "我需要注意什么？"]
    },
    "迁移宫": {
        "life_domains": ["外出", "旅行", "外部环境"],
        "psychology_aspects": ["适应能力", "探索欲", "社会形象"],
        "questions": ["我在外如何表现？", "我的适应能力如何？"]
    },
    "仆役宫": {
        "life_domains": ["下属", "服务", "日常关系"],
        "psychology_aspects": ["人际边界", "助人模式", "日常互动"],
        "questions": ["我如何与他人合作？", "我的服务态度？"]
    },
    "官禄宫": {
        "life_domains": ["事业", "地位", "社会角色"],
        "psychology_aspects": ["成就动机", "职业认同", "权力态度"],
        "questions": ["我适合什么职业？", "我如何追求成功？"]
    },
    "田宅宫": {
        "life_domains": ["家庭", "不动产", "根基"],
        "psychology_aspects": ["安全需求", "归属感", "家庭模式"],
        "questions": ["家对我意味着什么？", "我的家庭模式？"]
    },
    "福德宫": {
        "life_domains": ["精神生活", "兴趣", "内心满足"],
        "psychology_aspects": ["内心世界", "幸福感", "精神追求"],
        "questions": ["什么让我感到幸福？", "我的精神追求？"]
    },
    "父母宫": {
        "life_domains": ["父母", "长辈", "权威关系"],
        "psychology_aspects": ["权威态度", "原生家庭", "内化父母"],
        "questions": ["我与权威的关系？", "父母对我的影响？"]
    }
}


# ==================== 紫微十四主星心理学映射 ====================

ZIWEI_STAR_PSYCHOLOGY_MAP = {
    "紫微": {
        "mbti_tendencies": ["N", "J"],
        "keywords": ["领导", "权威", "尊贵", "自信"],
        "archetypes": ["RULER", "SAGE"],
        "big5": {"E": 10, "C": 10},
        "description": "紫微帝星，主尊贵威严，对应领导者原型，体现计划性与远见"
    },
    "天机": {
        "mbti_tendencies": ["N", "P"],
        "keywords": ["智慧", "机变", "谋略", "敏锐"],
        "archetypes": ["SAGE", "MAGICIAN"],
        "big5": {"O": 15, "C": 5},
        "description": "天机善谋，主智慧变通，对应智者与魔法师原型"
    },
    "太阳": {
        "mbti_tendencies": ["E", "J"],
        "keywords": ["光明", "博爱", "付出", "积极"],
        "archetypes": ["HERO", "CAREGIVER"],
        "big5": {"E": 15, "A": 10},
        "description": "太阳光辉普照，主积极博爱，对应英雄与照顾者原型"
    },
    "武曲": {
        "mbti_tendencies": ["T", "J"],
        "keywords": ["果断", "财星", "刚毅", "执行"],
        "archetypes": ["HERO", "RULER"],
        "big5": {"C": 15, "A": -5},
        "description": "武曲财星，主果敢决断，对应英雄原型的行动力"
    },
    "天同": {
        "mbti_tendencies": ["F", "P"],
        "keywords": ["温和", "福星", "享受", "安逸"],
        "archetypes": ["INNOCENT", "JESTER"],
        "big5": {"A": 15, "N": -5},
        "description": "天同福星，主温和知足，对应天真者与愚者原型"
    },
    "廉贞": {
        "mbti_tendencies": ["E", "T"],
        "keywords": ["桃花", "政治", "复杂", "魅力"],
        "archetypes": ["LOVER", "MAGICIAN"],
        "big5": {"E": 10, "O": 10},
        "description": "廉贞次桃花，主魅力与复杂，对应恋人与魔法师原型"
    },
    "天府": {
        "mbti_tendencies": ["S", "J"],
        "keywords": ["稳重", "财库", "保守", "可靠"],
        "archetypes": ["CAREGIVER", "RULER"],
        "big5": {"C": 15, "A": 10},
        "description": "天府财库，主稳重可靠，对应照顾者与统治者原型"
    },
    "太阴": {
        "mbti_tendencies": ["I", "F"],
        "keywords": ["柔和", "细腻", "内敛", "艺术"],
        "archetypes": ["CREATOR", "CAREGIVER"],
        "big5": {"A": 10, "O": 10, "E": -10},
        "description": "太阴柔美，主细腻内敛，对应创造者原型的艺术天赋"
    },
    "贪狼": {
        "mbti_tendencies": ["E", "P"],
        "keywords": ["欲望", "才艺", "多变", "桃花"],
        "archetypes": ["EXPLORER", "LOVER"],
        "big5": {"E": 15, "O": 15},
        "description": "贪狼主桃花才艺，对应探险家与恋人原型的多元追求"
    },
    "巨门": {
        "mbti_tendencies": ["T", "P"],
        "keywords": ["口才", "是非", "分析", "质疑"],
        "archetypes": ["SAGE", "REBEL"],
        "big5": {"O": 10, "A": -10},
        "description": "巨门主口才是非，对应智者原型的分析与质疑精神"
    },
    "天相": {
        "mbti_tendencies": ["F", "J"],
        "keywords": ["印星", "辅助", "礼仪", "规矩"],
        "archetypes": ["CAREGIVER", "EVERYMAN"],
        "big5": {"A": 15, "C": 10},
        "description": "天相印星，主辅助规矩，对应照顾者与凡人原型"
    },
    "天梁": {
        "mbti_tendencies": ["I", "J"],
        "keywords": ["清高", "荫星", "老成", "化解"],
        "archetypes": ["SAGE", "CAREGIVER"],
        "big5": {"C": 10, "A": 10, "E": -5},
        "description": "天梁荫星，主清高化解，对应智者与照顾者原型"
    },
    "七杀": {
        "mbti_tendencies": ["T", "P"],
        "keywords": ["魄力", "将星", "冲劲", "独立"],
        "archetypes": ["HERO", "REBEL"],
        "big5": {"E": 10, "C": 5, "A": -10},
        "description": "七杀将星，主魄力独立，对应英雄与叛逆者原型"
    },
    "破军": {
        "mbti_tendencies": ["E", "P"],
        "keywords": ["变革", "冲锋", "破坏", "开创"],
        "archetypes": ["REBEL", "EXPLORER"],
        "big5": {"O": 15, "A": -5},
        "description": "破军主变革开创，对应叛逆者与探险家原型"
    }
}


# ==================== 神煞与心理特质映射 ====================

SHENSHA_TRAIT_MAP = {
    "天乙贵人": {
        "traits": ["受人帮助", "贵人运强", "人缘好"],
        "psychology": "高社会支持感，容易获得他人信任和帮助",
        "big5": {"A": 10, "E": 5},
        "positive": True
    },
    "文昌": {
        "traits": ["聪明", "学习能力强", "文采好"],
        "psychology": "高认知能力，学习动机强，思维敏捷",
        "big5": {"O": 15, "C": 5},
        "positive": True
    },
    "驿马": {
        "traits": ["奔波", "变动", "外出发展"],
        "psychology": "高探索欲，适应性强，不安于现状",
        "big5": {"O": 10, "E": 5},
        "positive": True
    },
    "桃花": {
        "traits": ["异性缘", "魅力", "感情丰富"],
        "psychology": "高人际吸引力，情感丰富，社交活跃",
        "big5": {"E": 15, "A": 5},
        "positive": True
    },
    "羊刃": {
        "traits": ["刚烈", "果断", "易冲动"],
        "psychology": "高行动力，但情绪控制需加强",
        "big5": {"N": 10, "C": -5},
        "positive": False
    },
    "华盖": {
        "traits": ["孤独", "艺术", "宗教"],
        "psychology": "高内省倾向，精神追求，可能社交孤立",
        "big5": {"O": 15, "E": -10},
        "positive": None  # 中性
    },
    "天德": {
        "traits": ["贵人", "逢凶化吉", "道德"],
        "psychology": "高道德感，正向人生态度",
        "big5": {"A": 10, "C": 5},
        "positive": True
    },
    "劫煞": {
        "traits": ["变故", "意外", "劫难"],
        "psychology": "需加强风险意识，抗压能力需培养",
        "big5": {"N": 10},
        "positive": False
    }
}


# ==================== 映射计算函数 ====================

def get_wuxing_psychology(wuxing_scores: Dict[str, float]) -> Dict:
    """
    根据五行得分推算心理特质
    
    Args:
        wuxing_scores: 五行强度 {"木": 30, "火": 20, ...}
    
    Returns:
        心理特质分析
    """
    # 找出最强和最弱的五行
    sorted_wuxing = sorted(wuxing_scores.items(), key=lambda x: x[1], reverse=True)
    strongest = sorted_wuxing[0][0]
    weakest = sorted_wuxing[-1][0]
    
    primary_map = WUXING_MBTI_MAP.get(strongest, {})
    weak_map = WUXING_MBTI_MAP.get(weakest, {})
    
    # 综合MBTI倾向
    mbti_tendencies = {}
    for wx, score in wuxing_scores.items():
        wx_map = WUXING_MBTI_MAP.get(wx, {})
        for tendency in wx_map.get("mbti_tendencies", []):
            mbti_tendencies[tendency] = mbti_tendencies.get(tendency, 0) + score
    
    # 推荐MBTI类型
    likely_types = primary_map.get("mbti_types", [])[:3]
    
    # 大五人格倾向
    big5_tendencies = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
    for wx, score in wuxing_scores.items():
        wx_map = WUXING_MBTI_MAP.get(wx, {})
        for dim in wx_map.get("big5_high", []):
            big5_tendencies[dim] += score * 0.5
        for dim in wx_map.get("big5_low", []):
            big5_tendencies[dim] -= score * 0.3
    
    return {
        "strongest_wuxing": strongest,
        "weakest_wuxing": weakest,
        "primary_traits": primary_map.get("keywords", []),
        "mbti_tendencies": mbti_tendencies,
        "likely_mbti_types": likely_types,
        "description": primary_map.get("description", ""),
        "big5_tendencies": big5_tendencies,
        "development_areas": weak_map.get("keywords", [])
    }


def get_shishen_psychology(shishen_pattern: Dict[str, int]) -> Dict:
    """
    根据十神格局推算心理原型
    
    Args:
        shishen_pattern: 十神强度 {"正官": 2, "七杀": 1, ...}
    
    Returns:
        心理原型分析
    """
    archetypes_scores = {}
    enneagram_scores = {i: 0 for i in range(1, 10)}
    
    for shishen, count in shishen_pattern.items():
        if shishen not in SHISHEN_ARCHETYPE_MAP:
            continue
        
        map_data = SHISHEN_ARCHETYPE_MAP[shishen]
        
        # 累计原型分数
        for archetype in map_data.get("archetypes", []):
            archetypes_scores[archetype] = archetypes_scores.get(archetype, 0) + count
        
        # 累计九型分数
        for ennea in map_data.get("enneagram", []):
            enneagram_scores[ennea] += count
    
    # 排序
    sorted_archetypes = sorted(archetypes_scores.items(), key=lambda x: x[1], reverse=True)
    sorted_enneagram = sorted(enneagram_scores.items(), key=lambda x: x[1], reverse=True)
    
    primary_archetype = sorted_archetypes[0][0] if sorted_archetypes else "EVERYMAN"
    primary_enneagram = sorted_enneagram[0][0] if sorted_enneagram else 9
    
    return {
        "primary_archetype": primary_archetype,
        "archetype_scores": dict(sorted_archetypes[:5]),
        "likely_enneagram": primary_enneagram,
        "enneagram_scores": dict(sorted_enneagram[:3])
    }


def map_mbti_to_wuxing(mbti_type: str) -> Dict:
    """将MBTI类型映射到五行"""
    return MBTI_WUXING_MAP.get(mbti_type, {
        "primary": "土",
        "secondary": "水",
        "description": "综合平衡"
    })


def map_palace_to_psychology(palace_name: str) -> Dict:
    """将宫位映射到心理领域"""
    return PALACE_LIFE_DOMAIN_MAP.get(palace_name, {
        "life_domains": [],
        "psychology_aspects": [],
        "questions": []
    })


def get_star_psychology(star_name: str) -> Dict:
    """
    获取单颗星曜的心理学映射
    
    Args:
        star_name: 星曜名称（如 "紫微", "天机" 等）
    
    Returns:
        心理学映射字典，包含 mbti_tendencies, keywords, archetypes, big5, description
    """
    return ZIWEI_STAR_PSYCHOLOGY_MAP.get(star_name, {})


def get_palace_stars_psychology(palace_stars: list) -> Dict:
    """
    获取宫位内所有星曜的综合心理分析
    
    Args:
        palace_stars: 星曜列表，每个元素可以是字符串或包含 'name' 键的字典
    
    Returns:
        综合心理分析结果
    """
    combined = {
        "mbti_tendencies": {},
        "keywords": [],
        "archetypes": {},
        "big5": {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0},
        "descriptions": []
    }
    
    for star in palace_stars:
        star_name = star.get("name") if isinstance(star, dict) else star
        psychology = get_star_psychology(star_name)
        
        if not psychology:
            continue
        
        # 累计 MBTI 倾向
        for tendency in psychology.get("mbti_tendencies", []):
            combined["mbti_tendencies"][tendency] = combined["mbti_tendencies"].get(tendency, 0) + 1
        
        # 收集关键词
        combined["keywords"].extend(psychology.get("keywords", []))
        
        # 累计原型分数
        for archetype in psychology.get("archetypes", []):
            combined["archetypes"][archetype] = combined["archetypes"].get(archetype, 0) + 1
        
        # 累计大五人格调整值
        for dim, val in psychology.get("big5", {}).items():
            combined["big5"][dim] = combined["big5"].get(dim, 0) + val
        
        # 收集描述
        if psychology.get("description"):
            combined["descriptions"].append(f"{star_name}: {psychology['description']}")
    
    # 提取主要倾向
    if combined["mbti_tendencies"]:
        sorted_tendencies = sorted(combined["mbti_tendencies"].items(), key=lambda x: x[1], reverse=True)
        combined["primary_mbti_tendencies"] = [t[0] for t in sorted_tendencies[:4]]
    
    if combined["archetypes"]:
        sorted_archetypes = sorted(combined["archetypes"].items(), key=lambda x: x[1], reverse=True)
        combined["primary_archetype"] = sorted_archetypes[0][0]
    
    return combined

