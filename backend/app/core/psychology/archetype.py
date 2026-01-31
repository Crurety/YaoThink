"""
玄心理命 - 荣格原型测试模块
12种荣格心理原型
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


# ==================== 12种荣格原型 ====================

class ArchetypeType(Enum):
    """荣格原型类型"""
    INNOCENT = "天真者"
    EVERYMAN = "凡人"
    HERO = "英雄"
    CAREGIVER = "照顾者"
    EXPLORER = "探险家"
    REBEL = "叛逆者"
    LOVER = "情人"
    CREATOR = "创造者"
    JESTER = "愚者"
    SAGE = "智者"
    MAGICIAN = "魔法师"
    RULER = "统治者"


# 原型详细信息
ARCHETYPES = {
    "INNOCENT": {
        "name": "天真者",
        "english": "The Innocent",
        "motto": "自由做自己",
        "core_desire": "获得幸福",
        "goal": "获得幸福",
        "fear": "做错事而受惩罚",
        "strategy": "做正确的事",
        "gift": "信心和乐观",
        "shadow": "否认、压抑",
        "keywords": ["纯真", "乐观", "忠诚", "信任", "简单"],
        "positive_traits": ["乐观积极", "相信美好", "内心纯净", "简单快乐"],
        "negative_traits": ["过于天真", "容易被欺骗", "逃避现实", "依赖他人"],
        "brands": ["可口可乐", "麦当劳", "迪士尼"],
        "color": "#FFD700",
        "description": "天真者代表着纯真和乐观，他们相信世界的美好，追求简单的幸福。"
    },
    "EVERYMAN": {
        "name": "凡人",
        "english": "The Everyman",
        "motto": "人人平等",
        "core_desire": "与他人建立联系",
        "goal": "归属感",
        "fear": "被排斥或孤立",
        "strategy": "发展普通的美德，融入群体",
        "gift": "现实主义和同理心",
        "shadow": "失去自我，随波逐流",
        "keywords": ["亲和", "平等", "务实", "连接", "归属"],
        "positive_traits": ["脚踏实地", "善于共情", "真实可靠", "谦逊朴实"],
        "negative_traits": ["缺乏个性", "害怕出头", "过度妥协", "从众心理"],
        "brands": ["宜家", "GAP", "沃尔玛"],
        "color": "#8B4513",
        "description": "凡人代表着普通人的美德，他们重视归属感和与他人的真诚联系。"
    },
    "HERO": {
        "name": "英雄",
        "english": "The Hero",
        "motto": "有志者事竟成",
        "core_desire": "通过勇敢行动证明自己的价值",
        "goal": "通过勇敢行为改善世界",
        "fear": "软弱、脆弱",
        "strategy": "变得强大并战斗",
        "gift": "能力和勇气",
        "shadow": "傲慢、需要敌人",
        "keywords": ["勇气", "力量", "荣誉", "竞争", "胜利"],
        "positive_traits": ["勇敢无畏", "意志坚定", "追求卓越", "保护他人"],
        "negative_traits": ["过于好斗", "傲慢自大", "不懂示弱", "忽视情感"],
        "brands": ["耐克", "FedEx", "美国陆军"],
        "color": "#DC143C",
        "description": "英雄代表着勇气和力量，他们勇于面对挑战，追求胜利和成就。"
    },
    "CAREGIVER": {
        "name": "照顾者",
        "english": "The Caregiver",
        "motto": "爱你的邻居如同爱自己",
        "core_desire": "保护和关心他人",
        "goal": "帮助他人",
        "fear": "自私和忘恩负义",
        "strategy": "为他人做事",
        "gift": "同情心和慷慨",
        "shadow": "殉道者、纵容",
        "keywords": ["关爱", "保护", "奉献", "慷慨", "支持"],
        "positive_traits": ["富有爱心", "乐于奉献", "善解人意", "保护他人"],
        "negative_traits": ["过度牺牲", "忽视自我", "控制欲强", "情感绑架"],
        "brands": ["强生", "联合国儿童基金会", "沃尔沃"],
        "color": "#FFB6C1",
        "description": "照顾者代表着爱与关怀，他们以帮助和保护他人为使命。"
    },
    "EXPLORER": {
        "name": "探险家",
        "english": "The Explorer",
        "motto": "不要束缚我",
        "core_desire": "自由探索世界",
        "goal": "体验更真实、更充实的生活",
        "fear": "被困住或束缚",
        "strategy": "旅行、寻求冒险",
        "gift": "自主性和野心",
        "shadow": "流浪、不合群",
        "keywords": ["自由", "冒险", "发现", "独立", "真实"],
        "positive_traits": ["追求自由", "勇于冒险", "独立自主", "开阔视野"],
        "negative_traits": ["逃避责任", "难以安定", "过于孤僻", "不顾后果"],
        "brands": ["Jeep", "星巴克", "REI"],
        "color": "#228B22",
        "description": "探险家代表着自由和发现，他们渴望突破边界，探索未知。"
    },
    "REBEL": {
        "name": "叛逆者",
        "english": "The Rebel/Outlaw",
        "motto": "规则就是用来打破的",
        "core_desire": "革命或复仇",
        "goal": "颠覆不起作用的东西",
        "fear": "无力或无效",
        "strategy": "打破、摧毁或颠覆",
        "gift": "狂野自由",
        "shadow": "犯罪、邪恶",
        "keywords": ["颠覆", "革命", "打破", "释放", "激进"],
        "positive_traits": ["敢于挑战", "追求变革", "独立思考", "打破常规"],
        "negative_traits": ["破坏性强", "难以合作", "愤世嫉俗", "自我毁灭"],
        "brands": ["哈雷", "维京", "苹果（早期）"],
        "color": "#000000",
        "description": "叛逆者代表着变革和颠覆，他们挑战权威，打破陈规。"
    },
    "LOVER": {
        "name": "情人",
        "english": "The Lover",
        "motto": "你是唯一",
        "core_desire": "亲密和体验",
        "goal": "与人、工作、环境建立关系",
        "fear": "不被爱、孤独",
        "strategy": "变得更有吸引力",
        "gift": "激情和感恩",
        "shadow": "沉溺、嫉妒",
        "keywords": ["激情", "浪漫", "感官", "亲密", "美丽"],
        "positive_traits": ["热爱生活", "懂得欣赏", "充满激情", "真诚投入"],
        "negative_traits": ["过于感性", "依赖他人", "嫉妒心强", "失去自我"],
        "brands": ["香奈儿", "维多利亚的秘密", "歌帝梵"],
        "color": "#FF1493",
        "description": "情人代表着激情和感官体验，他们追求亲密关系和美的享受。"
    },
    "CREATOR": {
        "name": "创造者",
        "english": "The Creator",
        "motto": "如果可以想象，就可以创造",
        "core_desire": "创造持久价值的东西",
        "goal": "实现愿景",
        "fear": "平庸的愿景或执行",
        "strategy": "发展艺术控制和技能",
        "gift": "创造力和想象力",
        "shadow": "完美主义、怀才不遇",
        "keywords": ["创新", "想象", "艺术", "表达", "愿景"],
        "positive_traits": ["创意无限", "追求完美", "富有远见", "独特表达"],
        "negative_traits": ["过度完美主义", "不切实际", "自我陶醉", "难以妥协"],
        "brands": ["乐高", "Adobe", "苹果"],
        "color": "#9370DB",
        "description": "创造者代表着创新和想象，他们通过创造来表达自我和改变世界。"
    },
    "JESTER": {
        "name": "愚者",
        "english": "The Jester",
        "motto": "人生苦短，及时行乐",
        "core_desire": "活在当下，享受乐趣",
        "goal": "拥有美好时光",
        "fear": "无聊或乏味",
        "strategy": "玩乐、开玩笑、有趣",
        "gift": "快乐和幽默",
        "shadow": "轻浮、不负责任",
        "keywords": ["乐趣", "幽默", "当下", "轻松", "娱乐"],
        "positive_traits": ["幽默风趣", "乐观开朗", "活在当下", "化解紧张"],
        "negative_traits": ["不够认真", "逃避责任", "过于轻浮", "难以深入"],
        "brands": ["M&M's", "Old Spice", "Ben & Jerry's"],
        "color": "#FFA500",
        "description": "愚者代表着欢乐和幽默，他们帮助人们放松并找到生活的乐趣。"
    },
    "SAGE": {
        "name": "智者",
        "english": "The Sage",
        "motto": "真相会让你自由",
        "core_desire": "发现真理",
        "goal": "运用智慧理解世界",
        "fear": "被欺骗、无知",
        "strategy": "寻求信息和知识",
        "gift": "智慧和洞察力",
        "shadow": "脱离实际、教条",
        "keywords": ["智慧", "知识", "真理", "洞察", "反思"],
        "positive_traits": ["追求真理", "思维深刻", "博学多识", "客观理性"],
        "negative_traits": ["过于理论", "脱离现实", "高高在上", "缺乏行动"],
        "brands": ["谷歌", "BBC", "《纽约时报》"],
        "color": "#4169E1",
        "description": "智者代表着知识和真理，他们通过理解来获得智慧。"
    },
    "MAGICIAN": {
        "name": "魔法师",
        "english": "The Magician",
        "motto": "我让事情发生",
        "core_desire": "理解宇宙的基本规律",
        "goal": "让梦想成真",
        "fear": "意外的负面后果",
        "strategy": "发展愿景并实现它",
        "gift": "找到双赢解决方案",
        "shadow": "操纵、变得邪恶",
        "keywords": ["转化", "愿景", "神奇", "实现", "洞察"],
        "positive_traits": ["洞察力强", "创造奇迹", "转化问题", "实现愿景"],
        "negative_traits": ["操纵他人", "自负傲慢", "脱离现实", "目的不择手段"],
        "brands": ["特斯拉", "TED", "Dyson"],
        "color": "#800080",
        "description": "魔法师代表着转化和奇迹，他们将愿景变为现实。"
    },
    "RULER": {
        "name": "统治者",
        "english": "The Ruler",
        "motto": "权力不是一切，而是唯一",
        "core_desire": "控制",
        "goal": "创造繁荣、成功的家庭或社区",
        "fear": "混乱，被推翻",
        "strategy": "行使权力",
        "gift": "责任和领导力",
        "shadow": "专制、控制欲",
        "keywords": ["权力", "控制", "领导", "成功", "责任"],
        "positive_traits": ["领导能力强", "责任感强", "追求秩序", "保护他人"],
        "negative_traits": ["控制欲强", "专制独裁", "难以放权", "害怕失控"],
        "brands": ["劳力士", "奔驰", "微软"],
        "color": "#8B0000",
        "description": "统治者代表着权力和责任，他们通过控制来创造秩序和成功。"
    }
}


# ==================== 原型测试题库 ====================

ARCHETYPE_QUESTIONS = [
    # ==================== 天真者 (Innocent) ====================
    {"id": 1, "archetype": "INNOCENT", "text": "我相信世界本质上是美好的"},
    {"id": 2, "archetype": "INNOCENT", "text": "我喜欢简单、纯粹的事物"},
    {"id": 3, "archetype": "INNOCENT", "text": "我总是看到事情积极的一面"},
    {"id": 4, "archetype": "INNOCENT", "text": "我害怕做错事而受到惩罚"},
    {"id": 5, "archetype": "INNOCENT", "text": "我追求简单而快乐的生活，不求大富大贵"},
    {"id": 6, "archetype": "INNOCENT", "text": "我相信只要保持善良，好运就会降临"},

    # ==================== 凡人 (Everyman) ====================
    {"id": 7, "archetype": "EVERYMAN", "text": "我喜欢融入群体，与大家打成一片"},
    {"id": 8, "archetype": "EVERYMAN", "text": "我认为每个人都值得被尊重，没有高低贵贱"},
    {"id": 9, "archetype": "EVERYMAN", "text": "我不喜欢太特立独行或引人注目"},
    {"id": 10, "archetype": "EVERYMAN", "text": "我最害怕被抛弃或被孤立"},
    {"id": 11, "archetype": "EVERYMAN", "text": "我认为诚实和脚踏实地是最重要的美德"},
    {"id": 12, "archetype": "EVERYMAN", "text": "我喜欢那种大家都认可和使用的东西"},

    # ==================== 英雄 (Hero) ====================
    {"id": 13, "archetype": "HERO", "text": "我喜欢迎接挑战并战胜它"},
    {"id": 14, "archetype": "HERO", "text": "我认为坚强和勇敢很重要，不能表现出软弱"},
    {"id": 15, "archetype": "HERO", "text": "我愿意为正义挺身而出，保护弱小"},
    {"id": 16, "archetype": "HERO", "text": "我希望通过我的行动让世界变得更好"},
    {"id": 17, "archetype": "HERO", "text": "为了达成目标，我愿意付出任何努力"},
    {"id": 18, "archetype": "HERO", "text": "我经常感到有责任去解决困难的问题"},

    # ==================== 照顾者 (Caregiver) ====================
    {"id": 19, "archetype": "CAREGIVER", "text": "帮助别人让我感到满足和快乐"},
    {"id": 20, "archetype": "CAREGIVER", "text": "我总是把别人的需求放在自己之前"},
    {"id": 21, "archetype": "CAREGIVER", "text": "我擅长照顾和支持他人，是大家倾诉的对象"},
    {"id": 22, "archetype": "CAREGIVER", "text": "我担心别人因为我的疏忽而受到伤害"},
    {"id": 23, "archetype": "CAREGIVER", "text": "我对他人的痛苦感同身受"},
    {"id": 24, "archetype": "CAREGIVER", "text": "即使牺牲自己，我也要保护我爱的人"},

    # ==================== 探险家 (Explorer) ====================
    {"id": 25, "archetype": "EXPLORER", "text": "我渴望自由，不喜欢被束缚或限制"},
    {"id": 26, "archetype": "EXPLORER", "text": "我喜欢探索未知的领域，尝试新鲜事物"},
    {"id": 27, "archetype": "EXPLORER", "text": "我享受独自旅行或冒险带来的刺激"},
    {"id": 28, "archetype": "EXPLORER", "text": "如果生活变得平淡无奇，我会感到窒息"},
    {"id": 29, "archetype": "EXPLORER", "text": "我一直在寻找更真实、更充实的生活方式"},
    {"id": 30, "archetype": "EXPLORER", "text": "我不愿意为了安稳而放弃探索世界的机会"},

    # ==================== 叛逆者 (Rebel) ====================
    {"id": 31, "archetype": "REBEL", "text": "我不喜欢遵守不合理的规则和传统"},
    {"id": 32, "archetype": "REBEL", "text": "我愿意为改变现状而打破常规"},
    {"id": 33, "archetype": "REBEL", "text": "我经常质疑权威，不盲从"},
    {"id": 34, "archetype": "REBEL", "text": "我认为很多社会规范都是束缚人的枷锁"},
    {"id": 35, "archetype": "REBEL", "text": "为了自由和变革，必要的破坏是可以接受的"},
    {"id": 36, "archetype": "REBEL", "text": "我喜欢那些具有颠覆性和震撼力的事物"},

    # ==================== 情人 (Lover) ====================
    {"id": 37, "archetype": "LOVER", "text": "我非常重视亲密关系，害怕孤独"},
    {"id": 38, "archetype": "LOVER", "text": "我很容易被美的事物吸引，追求感官享受"},
    {"id": 39, "archetype": "LOVER", "text": "我是一个充满激情的人，全情投入"},
    {"id": 40, "archetype": "LOVER", "text": "我希望在别人眼中是迷人且具吸引力的"},
    {"id": 41, "archetype": "LOVER", "text": "为了获得爱和认同，我愿意改变自己"},
    {"id": 42, "archetype": "LOVER", "text": "能够与他人建立深层的情感连接对我至关重要"},

    # ==================== 创造者 (Creator) ====================
    {"id": 43, "archetype": "CREATOR", "text": "我喜欢创造新事物，表达我的独特视角"},
    {"id": 44, "archetype": "CREATOR", "text": "我追求完美，对自己作品要求很高"},
    {"id": 45, "archetype": "CREATOR", "text": "我有很多创意和想法，需要将其实现"},
    {"id": 46, "archetype": "CREATOR", "text": "我害怕平庸，不希望自己和别人一样"},
    {"id": 47, "archetype": "CREATOR", "text": "我相信想象力可以改变现实"},
    {"id": 48, "archetype": "CREATOR", "text": "通过艺术或创新来表达自我，是我存在的意义"},

    # ==================== 愚者 (Jester) ====================
    {"id": 49, "archetype": "JESTER", "text": "我喜欢用幽默化解尴尬和紧张的气氛"},
    {"id": 50, "archetype": "JESTER", "text": "我认为人生苦短，应该及时行乐"},
    {"id": 51, "archetype": "JESTER", "text": "我喜欢让周围的人开心，是大家的开心果"},
    {"id": 52, "archetype": "JESTER", "text": "我讨厌通过严肃和沉重的方式来处理问题"},
    {"id": 53, "archetype": "JESTER", "text": "我经常打破常规，用玩笑的方式表达真话"},
    {"id": 54, "archetype": "JESTER", "text": "我不喜欢被无聊和乏味的事情困住"},

    # ==================== 智者 (Sage) ====================
    {"id": 55, "archetype": "SAGE", "text": "我追求知识和真理，想了解世界的运作方式"},
    {"id": 56, "archetype": "SAGE", "text": "我喜欢深入思考问题，分析事物的本质"},
    {"id": 57, "archetype": "SAGE", "text": "我认为理解比行动更重要，要做明智的决定"},
    {"id": 58, "archetype": "SAGE", "text": "我害怕被愚弄或因无知而犯错"},
    {"id": 59, "archetype": "SAGE", "text": "不管是买东西还是做决定，我都会做足功课"},
    {"id": 60, "archetype": "SAGE", "text": "我相信真理会让心灵获得自由"},

    # ==================== 魔法师 (Magician) ====================
    {"id": 61, "archetype": "MAGICIAN", "text": "我相信一切皆有可能，奇迹会发生"},
    {"id": 62, "archetype": "MAGICIAN", "text": "我善于发现事物之间隐秘的联系和规律"},
    {"id": 63, "archetype": "MAGICIAN", "text": "我能把愿景变为现实，促成转化和改变"},
    {"id": 64, "archetype": "MAGICIAN", "text": "我对宇宙法则、心理学或神秘学感兴趣"},
    {"id": 65, "archetype": "MAGICIAN", "text": "我想要找到双赢的解决方案，化腐朽为神奇"},
    {"id": 66, "archetype": "MAGICIAN", "text": "我相信直觉和意念的力量"},

    # ==================== 统治者 (Ruler) ====================
    {"id": 67, "archetype": "RULER", "text": "我喜欢掌控局面，建立秩序"},
    {"id": 68, "archetype": "RULER", "text": "我天生具有领导能力，习惯承担责任"},
    {"id": 69, "archetype": "RULER", "text": "我追求权力和影响力，希望在这个领域获得成功"},
    {"id": 70, "archetype": "RULER", "text": "我害怕混乱和失控，必须确保一切井井有条"},
    {"id": 71, "archetype": "RULER", "text": "我有很强的组织能力，能让事情高效运转"},
    {"id": 72, "archetype": "RULER", "text": "我认为遵循等级和规则是社会繁荣的基础"}
]

ARCHETYPE_OPTIONS = [
    {"value": 1, "text": "完全不符合"},
    {"value": 2, "text": "不太符合"},
    {"value": 3, "text": "有时符合"},
    {"value": 4, "text": "比较符合"},
    {"value": 5, "text": "非常符合"}
]


# ==================== 原型计算 ====================

@dataclass
class ArchetypeResult:
    """原型测试结果"""
    primary: Dict           # 主要原型
    secondary: Dict          # 次要原型
    all_scores: Dict[str, float]  # 所有原型得分
    profile: str            # 原型组合描述


def calculate_archetype(answers: List[Dict]) -> ArchetypeResult:
    """
    计算荣格原型
    
    Args:
        answers: 答案列表 [{"question_id": 1, "value": 4}, ...]
    
    Returns:
        原型结果
    """
    # 初始化各原型得分
    archetype_scores = {a: [] for a in ARCHETYPES.keys()}
    
    # 收集得分
    for answer in answers:
        q_id = answer.get("question_id")
        value = answer.get("value", 3)
        
        question = next((q for q in ARCHETYPE_QUESTIONS if q["id"] == q_id), None)
        if question:
            archetype = question["archetype"]
            archetype_scores[archetype].append(value)
    
    # 计算各原型平均分
    scores = {}
    for archetype, values in archetype_scores.items():
        if values:
            avg = sum(values) / len(values)
            scores[archetype] = round((avg - 1) / 4 * 100, 1)
        else:
            scores[archetype] = 0
    
    # 排序找出主要和次要原型
    sorted_archetypes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    primary_code = sorted_archetypes[0][0]
    secondary_code = sorted_archetypes[1][0]
    
    primary = {
        "code": primary_code,
        "score": sorted_archetypes[0][1],
        **ARCHETYPES[primary_code]
    }
    
    secondary = {
        "code": secondary_code,
        "score": sorted_archetypes[1][1],
        **ARCHETYPES[secondary_code]
    }
    
    # 生成描述
    profile = f"你的主要原型是{primary['name']}，次要原型是{secondary['name']}。"
    profile += f"作为{primary['name']}，{primary['description']} "
    profile += f"同时你也具有{secondary['name']}的特质，{secondary['keywords'][0]}和{secondary['keywords'][1]}在你身上也有体现。"
    
    return ArchetypeResult(
        primary=primary,
        secondary=secondary,
        all_scores=scores,
        profile=profile
    )


def get_archetype_questions() -> List[Dict]:
    """获取原型测试题目"""
    return [{
        "id": q["id"],
        "text": q["text"],
        "archetype": q["archetype"],
        "options": ARCHETYPE_OPTIONS
    } for q in ARCHETYPE_QUESTIONS]
