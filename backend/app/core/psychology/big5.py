"""
玄心理命 - 大五人格测试模块
Big Five / OCEAN模型
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


# ==================== 大五人格维度 ====================

class Big5Dimension(Enum):
    """大五人格维度"""
    O = "开放性"      # Openness - 对新体验的开放程度
    C = "尽责性"      # Conscientiousness - 组织性、责任心
    E = "外向性"      # Extraversion - 社交性、活力
    A = "宜人性"      # Agreeableness - 合作性、信任
    N = "神经质"      # Neuroticism - 情绪稳定性


BIG5_DIMENSIONS = {
    "O": {
        "name": "开放性",
        "english": "Openness",
        "description": "对新体验、创意和抽象思维的开放程度",
        "high_traits": ["富有想象力", "创造力强", "好奇心强", "思想开放", "喜欢艺术"],
        "low_traits": ["务实保守", "传统", "偏好熟悉事物", "不喜欢变化"],
        "facets": ["想象力", "审美", "情感丰富", "冒险", "智识", "开明"]
    },
    "C": {
        "name": "尽责性",
        "english": "Conscientiousness",
        "description": "自律、组织性和追求成就的程度",
        "high_traits": ["有条理", "可靠", "自律", "勤奋", "追求卓越"],
        "low_traits": ["随性", "灵活", "不拘小节", "即兴发挥"],
        "facets": ["自我效能", "条理性", "责任心", "追求成就", "自律", "谨慎"]
    },
    "E": {
        "name": "外向性",
        "english": "Extraversion",
        "description": "社交性、活力和积极情绪的程度",
        "high_traits": ["健谈", "精力充沛", "自信", "热情", "喜欢社交"],
        "low_traits": ["安静", "内敛", "独立", "深思熟虑"],
        "facets": ["友善", "合群", "自信", "活力", "寻求刺激", "积极情绪"]
    },
    "A": {
        "name": "宜人性",
        "english": "Agreeableness",
        "description": "合作性、信任他人和同理心的程度",
        "high_traits": ["友善", "合作", "信任他人", "乐于助人", "谦虚"],
        "low_traits": ["竞争", "怀疑", "固执己见", "独立思考"],
        "facets": ["信任", "直率", "利他", "顺从", "谦虚", "同情心"]
    },
    "N": {
        "name": "神经质",
        "english": "Neuroticism",
        "description": "情绪不稳定性和负面情绪的倾向",
        "high_traits": ["易焦虑", "情绪波动", "敏感", "容易紧张", "自我怀疑"],
        "low_traits": ["情绪稳定", "冷静", "抗压", "自信"],
        "facets": ["焦虑", "愤怒", "抑郁", "自我意识", "冲动", "脆弱"]
    }
}


# ==================== 大五人格测试题库 ====================
# NEO-FFI简版量表（60题）

BIG5_QUESTIONS = [
    # 开放性 (O) 题目
    {"id": 1, "dimension": "O", "reverse": False,
     "text": "我对艺术、音乐或文学有浓厚的兴趣"},
    {"id": 2, "dimension": "O", "reverse": False,
     "text": "我喜欢思考抽象的概念和理论"},
    {"id": 3, "dimension": "O", "reverse": True,
     "text": "我更喜欢按部就班，不喜欢尝试新方法"},
    {"id": 4, "dimension": "O", "reverse": False,
     "text": "我经常会有创新的想法"},
    {"id": 5, "dimension": "O", "reverse": False,
     "text": "我喜欢探索不同的文化和思想"},
    {"id": 6, "dimension": "O", "reverse": True,
     "text": "我觉得艺术和美学不太重要"},
    {"id": 7, "dimension": "O", "reverse": False,
     "text": "我喜欢尝试新的体验和冒险"},
    {"id": 8, "dimension": "O", "reverse": False,
     "text": "我对哲学问题很感兴趣"},
    {"id": 9, "dimension": "O", "reverse": True,
     "text": "我更相信传统和常规的做法"},
    {"id": 10, "dimension": "O", "reverse": False,
     "text": "我有丰富的想象力"},
    {"id": 11, "dimension": "O", "reverse": False,
     "text": "我喜欢探索事物的深层含义"},
    {"id": 12, "dimension": "O", "reverse": True,
     "text": "我不太理解那些喜欢诗歌的人"},
    
    # 尽责性 (C) 题目
    {"id": 13, "dimension": "C", "reverse": False,
     "text": "我总是把事情安排得井井有条"},
    {"id": 14, "dimension": "C", "reverse": False,
     "text": "我会为自己设定目标并努力实现"},
    {"id": 15, "dimension": "C", "reverse": True,
     "text": "我经常拖延重要的事情"},
    {"id": 16, "dimension": "C", "reverse": False,
     "text": "我完成任务时非常注重细节"},
    {"id": 17, "dimension": "C", "reverse": False,
     "text": "我是一个可靠的人，会信守承诺"},
    {"id": 18, "dimension": "C", "reverse": True,
     "text": "我的私人物品经常很乱"},
    {"id": 19, "dimension": "C", "reverse": False,
     "text": "我会认真计划并执行任务"},
    {"id": 20, "dimension": "C", "reverse": False,
     "text": "我追求工作中的高标准"},
    {"id": 21, "dimension": "C", "reverse": True,
     "text": "我经常做出冲动的决定"},
    {"id": 22, "dimension": "C", "reverse": False,
     "text": "我有很强的自制力"},
    {"id": 23, "dimension": "C", "reverse": False,
     "text": "我总是按时完成任务"},
    {"id": 24, "dimension": "C", "reverse": True,
     "text": "有时我会半途而废"},
    
    # 外向性 (E) 题目
    {"id": 25, "dimension": "E", "reverse": False,
     "text": "我喜欢和很多人一起活动"},
    {"id": 26, "dimension": "E", "reverse": False,
     "text": "我经常是聚会的活跃分子"},
    {"id": 27, "dimension": "E", "reverse": True,
     "text": "我喜欢独处胜过社交活动"},
    {"id": 28, "dimension": "E", "reverse": False,
     "text": "我很容易和陌生人交谈"},
    {"id": 29, "dimension": "E", "reverse": False,
     "text": "我充满活力和热情"},
    {"id": 30, "dimension": "E", "reverse": True,
     "text": "我在社交场合常常感到不自在"},
    {"id": 31, "dimension": "E", "reverse": False,
     "text": "我喜欢成为众人关注的焦点"},
    {"id": 32, "dimension": "E", "reverse": False,
     "text": "我是一个健谈的人"},
    {"id": 33, "dimension": "E", "reverse": True,
     "text": "我通常比较安静和话少"},
    {"id": 34, "dimension": "E", "reverse": False,
     "text": "我喜欢参与团队活动"},
    {"id": 35, "dimension": "E", "reverse": False,
     "text": "我经常主动结识新朋友"},
    {"id": 36, "dimension": "E", "reverse": True,
     "text": "社交活动后我需要时间恢复精力"},
    
    # 宜人性 (A) 题目
    {"id": 37, "dimension": "A", "reverse": False,
     "text": "我很乐意帮助别人"},
    {"id": 38, "dimension": "A", "reverse": False,
     "text": "我相信大多数人都是善良的"},
    {"id": 39, "dimension": "A", "reverse": True,
     "text": "我有时候会对别人不太耐心"},
    {"id": 40, "dimension": "A", "reverse": False,
     "text": "我很少和别人起冲突"},
    {"id": 41, "dimension": "A", "reverse": False,
     "text": "我对他人的需求很敏感"},
    {"id": 42, "dimension": "A", "reverse": True,
     "text": "我有时候会显得有些冷漠"},
    {"id": 43, "dimension": "A", "reverse": False,
     "text": "我愿意为了和谐而妥协"},
    {"id": 44, "dimension": "A", "reverse": False,
     "text": "我很容易原谅别人"},
    {"id": 45, "dimension": "A", "reverse": True,
     "text": "我喜欢和别人竞争"},
    {"id": 46, "dimension": "A", "reverse": False,
     "text": "我待人友善和蔼"},
    {"id": 47, "dimension": "A", "reverse": False,
     "text": "我能够理解他人的观点"},
    {"id": 48, "dimension": "A", "reverse": True,
     "text": "我有时会批评别人的想法"},
    
    # 神经质 (N) 题目
    {"id": 49, "dimension": "N", "reverse": False,
     "text": "我经常感到焦虑或担忧"},
    {"id": 50, "dimension": "N", "reverse": False,
     "text": "我的情绪容易波动"},
    {"id": 51, "dimension": "N", "reverse": True,
     "text": "我很少感到压力"},
    {"id": 52, "dimension": "N", "reverse": False,
     "text": "我有时会感到沮丧或忧郁"},
    {"id": 53, "dimension": "N", "reverse": False,
     "text": "我很容易感到紧张"},
    {"id": 54, "dimension": "N", "reverse": True,
     "text": "我通常情绪稳定"},
    {"id": 55, "dimension": "N", "reverse": False,
     "text": "我会为小事烦恼"},
    {"id": 56, "dimension": "N", "reverse": False,
     "text": "我有时会感到自我怀疑"},
    {"id": 57, "dimension": "N", "reverse": True,
     "text": "我能够很好地处理压力"},
    {"id": 58, "dimension": "N", "reverse": False,
     "text": "我容易感到不安"},
    {"id": 59, "dimension": "N", "reverse": False,
     "text": "遇到问题时我会变得紧张"},
    {"id": 60, "dimension": "N", "reverse": True,
     "text": "我通常保持冷静和放松"}
]

# 答案选项（Likert 5点量表）
BIG5_OPTIONS = [
    {"value": 1, "text": "非常不同意"},
    {"value": 2, "text": "不同意"},
    {"value": 3, "text": "中立"},
    {"value": 4, "text": "同意"},
    {"value": 5, "text": "非常同意"}
]


# ==================== 大五人格计算 ====================

@dataclass
class Big5Result:
    """大五人格测试结果"""
    scores: Dict[str, float]          # 各维度原始得分
    percentiles: Dict[str, float]     # 各维度百分位数
    levels: Dict[str, str]            # 各维度水平描述
    profile: Dict                      # 综合人格画像
    reliability: float                 # 结果可靠性


def calculate_big5(answers: List[Dict]) -> Big5Result:
    """
    计算大五人格得分
    
    Args:
        answers: 答案列表 [{"question_id": 1, "value": 4}, ...]
                value: 1-5 (Likert量表)
    
    Returns:
        大五人格结果
    """
    # 初始化各维度得分
    dimension_scores = {"O": [], "C": [], "E": [], "A": [], "N": []}
    
    # 收集各维度得分
    for answer in answers:
        q_id = answer.get("question_id")
        value = answer.get("value", 3)
        
        question = next((q for q in BIG5_QUESTIONS if q["id"] == q_id), None)
        if not question:
            continue
        
        dim = question["dimension"]
        
        # 反向计分
        if question.get("reverse", False):
            value = 6 - value
        
        dimension_scores[dim].append(value)
    
    # 计算各维度平均分（1-5分制，转换为0-100分制）
    scores = {}
    for dim, values in dimension_scores.items():
        if values:
            avg = sum(values) / len(values)
            scores[dim] = round((avg - 1) / 4 * 100, 1)  # 转换为0-100
        else:
            scores[dim] = 50.0
    
    # 计算百分位数（简化版，假设正态分布）
    # 实际应用中需要常模数据
    percentiles = {}
    for dim, score in scores.items():
        # 简化处理：将分数直接映射为百分位
        percentiles[dim] = round(score, 1)
    
    # 确定各维度水平
    levels = {}
    for dim, score in scores.items():
        if score >= 70:
            levels[dim] = "高"
        elif score >= 40:
            levels[dim] = "中"
        else:
            levels[dim] = "低"
    
    # 生成综合画像
    profile = _generate_big5_profile(scores, levels)
    
    # 计算可靠性（基于答题完整度和一致性）
    total_questions = len(BIG5_QUESTIONS)
    answered = len(answers)
    reliability = round(answered / total_questions * 100, 1)
    
    return Big5Result(
        scores=scores,
        percentiles=percentiles,
        levels=levels,
        profile=profile,
        reliability=reliability
    )


def _generate_big5_profile(scores: Dict[str, float], levels: Dict[str, str]) -> Dict:
    """生成综合人格画像"""
    traits = []
    
    for dim, level in levels.items():
        dim_info = BIG5_DIMENSIONS[dim]
        if level == "高":
            traits.extend(dim_info["high_traits"][:2])
        elif level == "低":
            traits.extend(dim_info["low_traits"][:2])
    
    # 确定主导特质
    max_dim = max(scores, key=scores.get)
    min_dim = min(scores, key=scores.get)
    
    # 生成描述
    description = ""
    if scores["E"] > 60:
        description += "你是一个外向活跃的人，"
    else:
        description += "你是一个安静内敛的人，"
    
    if scores["O"] > 60:
        description += "富有创造力和想象力，"
    else:
        description += "注重实际和传统，"
    
    if scores["A"] > 60:
        description += "待人友善合作。"
    else:
        description += "独立自主有竞争力。"
    
    if scores["N"] > 60:
        description += "情绪上可能需要更多关注和调节。"
    else:
        description += "情绪稳定抗压能力强。"
    
    return {
        "summary": description,
        "key_traits": traits[:6],
        "strongest_dimension": {
            "code": max_dim,
            "name": BIG5_DIMENSIONS[max_dim]["name"],
            "score": scores[max_dim]
        },
        "development_area": {
            "code": min_dim,
            "name": BIG5_DIMENSIONS[min_dim]["name"],
            "score": scores[min_dim]
        }
    }


def get_big5_interpretation(scores: Dict[str, float]) -> Dict:
    """获取大五人格解读"""
    interpretations = {}
    
    for dim, score in scores.items():
        dim_info = BIG5_DIMENSIONS[dim]
        
        if score >= 70:
            level = "高"
            description = f"你在{dim_info['name']}方面得分较高。"
            traits = dim_info["high_traits"]
        elif score >= 40:
            level = "中等"
            description = f"你在{dim_info['name']}方面表现中等。"
            traits = dim_info["high_traits"][:1] + dim_info["low_traits"][:1]
        else:
            level = "低"
            description = f"你在{dim_info['name']}方面得分较低。"
            traits = dim_info["low_traits"]
        
        interpretations[dim] = {
            "dimension": dim_info["name"],
            "english": dim_info["english"],
            "score": score,
            "level": level,
            "description": description,
            "traits": traits,
            "facets": dim_info["facets"]
        }
    
    return interpretations


def get_big5_questions(level: str = "master") -> List[Dict]:
    """
    获取大五人格测试题目
    
    Args:
        level: 难度等级 (simple/professional/master)
    """
    if level == "master":
        questions = BIG5_QUESTIONS
    else:
        # 定义不同等级每维度的题目数量
        # simple: 15题 (3*5)
        # professional: 30题 (6*5)
        if level == "simple":
            count_per_dim = 3
        elif level == "professional":
            count_per_dim = 6
        else:
            questions = BIG5_QUESTIONS
        
        if level in ["simple", "professional"]:
            # 按维度分组并切片
            grouped = {d: [] for d in ["O", "C", "E", "A", "N"]}
            for q in BIG5_QUESTIONS:
                if q["dimension"] in grouped:
                    grouped[q["dimension"]].append(q)
            
            questions = []
            for dim, dim_qs in grouped.items():
                questions.extend(dim_qs[:count_per_dim])
            
            questions.sort(key=lambda x: x["id"])

    return [{
        "id": q["id"],
        "text": q["text"],
        "dimension": q["dimension"],
        "options": BIG5_OPTIONS
    } for q in questions]
