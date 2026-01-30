"""
玄心理命 - 九型人格测试模块
Enneagram 九种人格类型
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


# ==================== 九型人格定义 ====================

class EnneagramType(Enum):
    """九型人格类型"""
    TYPE1 = "完美主义者"
    TYPE2 = "助人者"
    TYPE3 = "成就者"
    TYPE4 = "自我者"
    TYPE5 = "观察者"
    TYPE6 = "忠诚者"
    TYPE7 = "享乐者"
    TYPE8 = "挑战者"
    TYPE9 = "和平者"


# 九型人格详细信息
ENNEAGRAM_TYPES = {
    1: {
        "name": "完美主义者",
        "english": "The Perfectionist",
        "core_fear": "堕落、成为坏人",
        "core_desire": "正确、正直、有道德",
        "core_motivation": "追求完美和正确",
        "basic_proposition": "这个世界是不完美的，我必须努力让它变得更好",
        "keywords": ["原则", "道德", "改进", "完美", "自律"],
        "positive_traits": ["有原则", "公正", "负责", "追求卓越", "自律"],
        "negative_traits": ["苛责", "挑剔", "过于严肃", "压抑愤怒", "难以放松"],
        "stress_direction": 4,  # 压力下变成4号
        "growth_direction": 7,  # 成长方向是7号
        "wing_options": [9, 2],  # 可能的翼型
        "description": "一号人格追求完美和正确，他们有很强的道德感和责任心。",
        "growth_advice": "学会接受不完美，允许自己和他人犯错。"
    },
    2: {
        "name": "助人者",
        "english": "The Helper",
        "core_fear": "不被爱、不被需要",
        "core_desire": "被爱、被需要",
        "core_motivation": "想要被爱和欣赏",
        "basic_proposition": "只有满足他人需求，我才值得被爱",
        "keywords": ["关爱", "付出", "热情", "慷慨", "同理心"],
        "positive_traits": ["温暖", "大方", "善解人意", "乐于助人", "富有同情心"],
        "negative_traits": ["讨好他人", "忽视自我", "控制", "感情用事", "期望回报"],
        "stress_direction": 8,
        "growth_direction": 4,
        "wing_options": [1, 3],
        "description": "二号人格天生乐于助人，他们通过帮助他人来获得爱和认可。",
        "growth_advice": "学会关注自己的需求，给予不求回报。"
    },
    3: {
        "name": "成就者",
        "english": "The Achiever",
        "core_fear": "没有价值、失败",
        "core_desire": "有价值、成功",
        "core_motivation": "想要成功和被认可",
        "basic_proposition": "我必须成功才有价值",
        "keywords": ["成功", "效率", "形象", "适应", "目标"],
        "positive_traits": ["高效", "自信", "适应力强", "积极进取", "鼓舞人心"],
        "negative_traits": ["虚荣", "工作狂", "过于在意形象", "忽视感情", "竞争过度"],
        "stress_direction": 9,
        "growth_direction": 6,
        "wing_options": [2, 4],
        "description": "三号人格追求成功和认可，他们适应力强，善于展现自己。",
        "growth_advice": "学会真实面对自己，成功不是唯一的价值。"
    },
    4: {
        "name": "自我者",
        "english": "The Individualist",
        "core_fear": "没有身份认同、平庸",
        "core_desire": "独特、与众不同",
        "core_motivation": "想要真实地表达自我",
        "basic_proposition": "我与众不同，别人不理解我",
        "keywords": ["独特", "深刻", "艺术", "敏感", "真实"],
        "positive_traits": ["有创意", "敏感", "真诚", "富有内涵", "艺术天赋"],
        "negative_traits": ["情绪化", "自我中心", "嫉妒", "沉溺悲伤", "戏剧化"],
        "stress_direction": 2,
        "growth_direction": 1,
        "wing_options": [3, 5],
        "description": "四号人格追求独特和深刻，他们艺术性强，情感丰富。",
        "growth_advice": "学会活在当下，接受平凡也是一种美。"
    },
    5: {
        "name": "观察者",
        "english": "The Investigator",
        "core_fear": "无能、被侵入",
        "core_desire": "有能力、有知识",
        "core_motivation": "想要理解世界",
        "basic_proposition": "世界充满威胁，我需要知识来保护自己",
        "keywords": ["知识", "分析", "独立", "洞察", "沉默"],
        "positive_traits": ["有洞察力", "独立", "专注", "客观", "知识渊博"],
        "negative_traits": ["封闭", "过于理性", "脱离现实", "吝啬", "疏离"],
        "stress_direction": 7,
        "growth_direction": 8,
        "wing_options": [4, 6],
        "description": "五号人格追求知识和理解，他们善于观察和分析。",
        "growth_advice": "学会走出头脑，与他人建立联系。"
    },
    6: {
        "name": "忠诚者",
        "english": "The Loyalist",
        "core_fear": "不安全、没有支持",
        "core_desire": "安全、有保障",
        "core_motivation": "想要安全和确定性",
        "basic_proposition": "世界充满危险，我需要做好准备",
        "keywords": ["忠诚", "安全", "责任", "可靠", "谨慎"],
        "positive_traits": ["忠诚", "负责", "勇敢", "务实", "值得信赖"],
        "negative_traits": ["焦虑", "多疑", "犹豫不决", "过度警惕", "依赖"],
        "stress_direction": 3,
        "growth_direction": 9,
        "wing_options": [5, 7],
        "description": "六号人格追求安全和确定，他们忠诚可靠，善于预见风险。",
        "growth_advice": "学会信任自己和他人，活在当下而非担忧未来。"
    },
    7: {
        "name": "享乐者",
        "english": "The Enthusiast",
        "core_fear": "痛苦、被限制",
        "core_desire": "快乐、满足",
        "core_motivation": "想要快乐和自由",
        "basic_proposition": "人生苦短，我要尽情享受",
        "keywords": ["乐观", "多才", "冒险", "自由", "计划"],
        "positive_traits": ["乐观", "精力充沛", "多才多艺", "有远见", "友善"],
        "negative_traits": ["逃避", "不专注", "不负责", "贪心", "浅尝辄止"],
        "stress_direction": 1,
        "growth_direction": 5,
        "wing_options": [6, 8],
        "description": "七号人格追求快乐和多样性，他们精力充沛，充满热情。",
        "growth_advice": "学会面对痛苦，专注于当下而非追逐新鲜。"
    },
    8: {
        "name": "挑战者",
        "english": "The Challenger",
        "core_fear": "被控制、软弱",
        "core_desire": "保护自己、掌控生活",
        "core_motivation": "想要强大和自主",
        "basic_proposition": "弱肉强食，我必须强大",
        "keywords": ["力量", "正义", "保护", "直接", "独立"],
        "positive_traits": ["自信", "果断", "保护者", "正义感", "领导力"],
        "negative_traits": ["霸道", "控制欲", "无法示弱", "报复心", "冲动"],
        "stress_direction": 5,
        "growth_direction": 2,
        "wing_options": [7, 9],
        "description": "八号人格追求力量和掌控，他们强势但也有保护欲。",
        "growth_advice": "学会表达脆弱，力量不在于控制而在于连接。"
    },
    9: {
        "name": "和平者",
        "english": "The Peacemaker",
        "core_fear": "冲突、分离",
        "core_desire": "和平、和谐",
        "core_motivation": "想要内心平静和和谐的关系",
        "basic_proposition": "我的意见不重要，避免冲突最重要",
        "keywords": ["和平", "调和", "包容", "平静", "接纳"],
        "positive_traits": ["平和", "包容", "善于调解", "有耐心", "接纳"],
        "negative_traits": ["回避、懒散", "消极", "固执", "忽视自我", "优柔寡断"],
        "stress_direction": 6,
        "growth_direction": 3,
        "wing_options": [8, 1],
        "description": "九号人格追求和平与和谐，他们善于调解，包容大度。",
        "growth_advice": "学会表达自我，你的声音和意见同样重要。"
    }
}


# ==================== 九型人格测试题库 ====================

ENNEAGRAM_QUESTIONS = [
    # Type 1 完美主义者
    {"id": 1, "type": 1, "text": "我有很强的是非观念，总想纠正错误"},
    {"id": 2, "type": 1, "text": "我对自己和他人要求很高"},
    {"id": 3, "type": 1, "text": "我很难接受不完美的事物"},
    {"id": 4, "type": 1, "text": "我经常压抑愤怒，尽量表现得理性"},
    
    # Type 2 助人者
    {"id": 5, "type": 2, "text": "我喜欢照顾别人，关心他人的需求"},
    {"id": 6, "type": 2, "text": "我很难拒绝别人的请求"},
    {"id": 7, "type": 2, "text": "我通过帮助别人来感受自己的价值"},
    {"id": 8, "type": 2, "text": "我希望自己对别人很重要"},
    
    # Type 3 成就者
    {"id": 9, "type": 3, "text": "成功和成就对我来说非常重要"},
    {"id": 10, "type": 3, "text": "我很在意别人如何看待我"},
    {"id": 11, "type": 3, "text": "我善于根据环境调整自己的形象"},
    {"id": 12, "type": 3, "text": "我总是忙于完成目标和任务"},
    
    # Type 4 自我者
    {"id": 13, "type": 4, "text": "我觉得自己与众不同，别人不理解我"},
    {"id": 14, "type": 4, "text": "我经常体验强烈而复杂的情绪"},
    {"id": 15, "type": 4, "text": "我追求独特和真实的自我表达"},
    {"id": 16, "type": 4, "text": "我有时会嫉妒别人拥有的东西"},
    
    # Type 5 观察者
    {"id": 17, "type": 5, "text": "我喜欢独处和思考"},
    {"id": 18, "type": 5, "text": "我通过积累知识来获得安全感"},
    {"id": 19, "type": 5, "text": "我需要很多私人空间"},
    {"id": 20, "type": 5, "text": "我更喜欢观察而非参与"},
    
    # Type 6 忠诚者
    {"id": 21, "type": 6, "text": "我经常担心可能出错的事情"},
    {"id": 22, "type": 6, "text": "我重视忠诚和承诺"},
    {"id": 23, "type": 6, "text": "我在做决定前会考虑很多风险"},
    {"id": 24, "type": 6, "text": "我有时会质疑权威，有时又依赖权威"},
    
    # Type 7 享乐者
    {"id": 25, "type": 7, "text": "我喜欢尝试新事物，追求多样性"},
    {"id": 26, "type": 7, "text": "我通常很乐观，看事情积极的一面"},
    {"id": 27, "type": 7, "text": "我很难忍受无聊和限制"},
    {"id": 28, "type": 7, "text": "我有很多计划和想法"},
    
    # Type 8 挑战者
    {"id": 29, "type": 8, "text": "我喜欢掌控局面，不喜欢被控制"},
    {"id": 30, "type": 8, "text": "我敢于直接表达意见，即使有冲突"},
    {"id": 31, "type": 8, "text": "我有保护弱者的倾向"},
    {"id": 32, "type": 8, "text": "我很难展现脆弱的一面"},
    
    # Type 9 和平者
    {"id": 33, "type": 9, "text": "我不喜欢冲突，会尽量避免争论"},
    {"id": 34, "type": 9, "text": "我很容易看到不同立场的道理"},
    {"id": 35, "type": 9, "text": "我有时会忽视自己的需求"},
    {"id": 36, "type": 9, "text": "我追求内心的平静和和谐"}
]

ENNEAGRAM_OPTIONS = [
    {"value": 1, "text": "完全不符合"},
    {"value": 2, "text": "不太符合"},
    {"value": 3, "text": "有时符合"},
    {"value": 4, "text": "比较符合"},
    {"value": 5, "text": "非常符合"}
]


# ==================== 九型人格计算 ====================

@dataclass
class EnneagramResult:
    """九型人格测试结果"""
    primary_type: int           # 主要类型 (1-9)
    primary_info: Dict          # 主要类型信息
    wing: Optional[int]         # 翼型
    all_scores: Dict[int, float]  # 所有类型得分
    stress_direction: int       # 压力方向
    growth_direction: int       # 成长方向
    profile: str               # 综合描述


def calculate_enneagram(answers: List[Dict]) -> EnneagramResult:
    """
    计算九型人格
    
    Args:
        answers: 答案列表 [{"question_id": 1, "value": 4}, ...]
    
    Returns:
        九型人格结果
    """
    # 初始化各类型得分
    type_scores = {i: [] for i in range(1, 10)}
    
    # 收集得分
    for answer in answers:
        q_id = answer.get("question_id")
        value = answer.get("value", 3)
        
        question = next((q for q in ENNEAGRAM_QUESTIONS if q["id"] == q_id), None)
        if question:
            type_num = question["type"]
            type_scores[type_num].append(value)
    
    # 计算各类型平均分 (转换为百分制)
    scores = {}
    for type_num, values in type_scores.items():
        if values:
            avg = sum(values) / len(values)
            scores[type_num] = round((avg - 1) / 4 * 100, 1)
        else:
            scores[type_num] = 0
    
    # 找出主要类型
    primary_type = max(scores, key=scores.get)
    primary_info = ENNEAGRAM_TYPES[primary_type]
    
    # 确定翼型（相邻两个类型中得分较高的）
    wing_options = primary_info["wing_options"]
    wing_scores = {w: scores.get(w, 0) for w in wing_options}
    wing = max(wing_scores, key=wing_scores.get) if wing_scores else None
    
    # 生成描述
    wing_name = ENNEAGRAM_TYPES[wing]["name"] if wing else ""
    profile = f"你是{primary_type}号{primary_info['name']}。{primary_info['description']}"
    if wing:
        profile += f" 你带有{wing}号{wing_name}的翼型特质。"
    profile += f" {primary_info['growth_advice']}"
    
    return EnneagramResult(
        primary_type=primary_type,
        primary_info=primary_info,
        wing=wing,
        all_scores=scores,
        stress_direction=primary_info["stress_direction"],
        growth_direction=primary_info["growth_direction"],
        profile=profile
    )


def get_enneagram_questions() -> List[Dict]:
    """获取九型人格测试题目"""
    return [{
        "id": q["id"],
        "text": q["text"],
        "type": q["type"],
        "options": ENNEAGRAM_OPTIONS
    } for q in ENNEAGRAM_QUESTIONS]


def get_enneagram_compatibility(type1: int, type2: int) -> Dict:
    """
    获取两种九型人格的兼容性
    
    Args:
        type1: 第一种类型 (1-9)
        type2: 第二种类型 (1-9)
    
    Returns:
        兼容性分析
    """
    # 兼容性矩阵（简化版）
    # 实际情况更复杂，这里用基础规则
    
    info1 = ENNEAGRAM_TYPES.get(type1, {})
    info2 = ENNEAGRAM_TYPES.get(type2, {})
    
    # 基础分数
    score = 60
    factors = []
    
    # 相同类型
    if type1 == type2:
        score = 75
        factors.append("相同类型，容易理解")
    
    # 成长方向匹配
    if info1.get("growth_direction") == type2:
        score += 15
        factors.append("成长方向互补")
    if info2.get("growth_direction") == type1:
        score += 15
        factors.append("成长方向互补")
    
    # 压力方向匹配（可能有挑战）
    if info1.get("stress_direction") == type2:
        score -= 10
        factors.append("可能带来压力")
    
    # 翼型相关
    if type2 in info1.get("wing_options", []):
        score += 10
        factors.append("翼型相近")
    
    score = max(0, min(100, score))
    
    if score >= 80:
        level = "非常契合"
    elif score >= 60:
        level = "比较契合"
    elif score >= 40:
        level = "需要磨合"
    else:
        level = "挑战较大"
    
    return {
        "score": score,
        "level": level,
        "factors": factors,
        "type1_info": {
            "type": type1,
            "name": info1.get("name", ""),
            "keywords": info1.get("keywords", [])
        },
        "type2_info": {
            "type": type2,
            "name": info2.get("name", ""),
            "keywords": info2.get("keywords", [])
        }
    }
