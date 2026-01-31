"""
玄心理命 - MBTI人格测试模块
16种人格类型测评系统
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


# ==================== MBTI维度定义 ====================

class MBTIDimension(Enum):
    """MBTI四个维度"""
    EI = "精力来源"   # E外向 / I内向
    SN = "信息获取"   # S实感 / N直觉
    TF = "决策方式"   # T思考 / F情感
    JP = "生活态度"   # J判断 / P感知


# 16种人格类型
MBTI_TYPES = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]


# ==================== MBTI类型详细描述 ====================

MBTI_DESCRIPTIONS = {
    "INTJ": {
        "name": "建筑师",
        "nickname": "独立思想家",
        "keywords": ["战略", "独立", "创新", "完美主义"],
        "description": "富有想象力和战略性思维的计划者，对一切都有详尽的计划。",
        "strengths": ["战略思维", "高度自信", "独立强", "追求效率"],
        "weaknesses": ["过于理性", "难以亲近", "完美主义", "不善表达情感"],
        "career": ["科学家", "工程师", "战略顾问", "投资分析师"],
        "famous": ["尼古拉·特斯拉", "艾萨克·牛顿", "埃隆·马斯克"],
        "percentage": "2.1%"
    },
    "INTP": {
        "name": "逻辑学家",
        "nickname": "理性思考者",
        "keywords": ["逻辑", "创新", "好奇", "理论"],
        "description": "具有创造力的发明家，对知识有着无法满足的渴望。",
        "strengths": ["分析能力强", "独立客观", "创意无限", "思维敏捷"],
        "weaknesses": ["脱离现实", "不擅社交", "拖延", "过于批判"],
        "career": ["程序员", "数学家", "哲学家", "研究员"],
        "famous": ["阿尔伯特·爱因斯坦", "比尔·盖茨", "亚伯拉罕·林肯"],
        "percentage": "3.3%"
    },
    "ENTJ": {
        "name": "指挥官",
        "nickname": "天生领导者",
        "keywords": ["领导", "果断", "高效", "战略"],
        "description": "大胆、富有想象力且意志力强的领导者，总能找到或创造出方法。",
        "strengths": ["高效率", "精力充沛", "自信果断", "领导力强"],
        "weaknesses": ["不耐烦", "傲慢", "情感冷淡", "强势专横"],
        "career": ["企业家", "CEO", "律师", "项目经理"],
        "famous": ["史蒂夫·乔布斯", "玛格丽特·撒切尔", "拿破仑"],
        "percentage": "1.8%"
    },
    "ENTP": {
        "name": "辩论家",
        "nickname": "聪明博学者",
        "keywords": ["机智", "辩论", "创新", "挑战"],
        "description": "聪明好奇的思考者，不会放弃任何智力上的挑战。",
        "strengths": ["知识渊博", "思维敏捷", "充满自信", "创意发散"],
        "weaknesses": ["争强好胜", "不切实际", "缺乏耐心", "难以专注"],
        "career": ["企业家", "发明家", "辩护律师", "咨询顾问"],
        "famous": ["本杰明·富兰克林", "托马斯·爱迪生", "马克·吐温"],
        "percentage": "3.2%"
    },
    "INFJ": {
        "name": "提倡者",
        "nickname": "神秘理想主义者",
        "keywords": ["洞察", "理想", "同理心", "使命感"],
        "description": "安静而神秘，鼓舞人心且不知疲倦的理想主义者。",
        "strengths": ["有远见", "坚定决心", "利他主义", "创造力强"],
        "weaknesses": ["敏感多疑", "极度私密", "完美主义", "容易倦怠"],
        "career": ["心理咨询师", "作家", "人力资源", "社会工作者"],
        "famous": ["马丁·路德·金", "纳尔逊·曼德拉", "特蕾莎修女"],
        "percentage": "1.5%"
    },
    "INFP": {
        "name": "调停者",
        "nickname": "诗意理想主义者",
        "keywords": ["理想", "同情", "创造", "真诚"],
        "description": "诗意、善良的利他主义者，总是热切地为善事提供帮助。",
        "strengths": ["深度同理心", "创造力强", "忠诚", "价值观坚定"],
        "weaknesses": ["过于理想", "自我批评", "不切实际", "逃避冲突"],
        "career": ["作家", "艺术家", "心理学家", "教师"],
        "famous": ["威廉·莎士比亚", "约翰·列侬", "J.K.罗琳"],
        "percentage": "4.4%"
    },
    "ENFJ": {
        "name": "主人公",
        "nickname": "有魅力的领导者",
        "keywords": ["魅力", "启发", "利他", "领导"],
        "description": "富有魅力鼓舞人心的领导者，能够迷住他们的听众。",
        "strengths": ["天生领袖", "善于交际", "可靠负责", "利他包容"],
        "weaknesses": ["过度理想", "过于敏感", "难以决断", "批评敏感"],
        "career": ["教师", "政治家", "公关", "人力资源经理"],
        "famous": ["巴拉克·奥巴马", "奥普拉·温弗瑞", "马丁·路德·金"],
        "percentage": "2.5%"
    },
    "ENFP": {
        "name": "竞选者",
        "nickname": "热情活力派",
        "keywords": ["热情", "创造", "自由", "社交"],
        "description": "热情、有创造力和社交能力，总能找到微笑的理由。",
        "strengths": ["热情洋溢", "创意无限", "社交高手", "乐观积极"],
        "weaknesses": ["缺乏专注", "过度思考", "难以实施", "情绪化"],
        "career": ["记者", "演员", "创业者", "心理咨询师"],
        "famous": ["罗宾·威廉姆斯", "威尔·史密斯", "马克·吐温"],
        "percentage": "8.1%"
    },
    "ISTJ": {
        "name": "物流师",
        "nickname": "可靠实干家",
        "keywords": ["责任", "可靠", "传统", "组织"],
        "description": "实际和注重事实的个人，其可靠性是不容置疑的。",
        "strengths": ["诚实率直", "意志坚定", "责任心强", "守时守信"],
        "weaknesses": ["固执己见", "不善变通", "判断他人", "习惯压抑情感"],
        "career": ["会计师", "审计师", "军人", "法官"],
        "famous": ["乔治·华盛顿", "沃伦·巴菲特", "安吉拉·默克尔"],
        "percentage": "11.6%"
    },
    "ISFJ": {
        "name": "守卫者",
        "nickname": "忠诚守护者",
        "keywords": ["守护", "忠诚", "奉献", "细心"],
        "description": "非常专注和热心的保护者，随时准备保护所爱的人。",
        "strengths": ["支持性强", "可靠耐心", "观察细致", "热情好客"],
        "weaknesses": ["过于谦虚", "压抑感情", "过度承担", "回避改变"],
        "career": ["护士", "教师", "社工", "行政助理"],
        "famous": ["贝雅·阿瑟", "凯特王妃", "文森特·梵高"],
        "percentage": "13.8%"
    },
    "ESTJ": {
        "name": "总经理",
        "nickname": "高效执行者",
        "keywords": ["秩序", "效率", "领导", "传统"],
        "description": "出色的管理者，在管理事物或人方面无与伦比。",
        "strengths": ["奉献精神", "意志坚强", "直接诚实", "忠诚负责"],
        "weaknesses": ["固执刻板", "不善创新", "喜欢指责", "社交僵化"],
        "career": ["经理", "法官", "军官", "财务总监"],
        "famous": ["约翰·洛克菲勒", "希拉里·克林顿", "亨利·福特"],
        "percentage": "8.7%"
    },
    "ESFJ": {
        "name": "执政官",
        "nickname": "温暖社交官",
        "keywords": ["和谐", "关怀", "忠诚", "传统"],
        "description": "极有爱心、合群和受欢迎的人，总是热切地帮助别人。",
        "strengths": ["热爱助人", "忠诚可靠", "敏感细腻", "社交能力强"],
        "weaknesses": ["过于在乎他人评价", "缺乏灵活性", "脆弱敏感", "过度忘我"],
        "career": ["护士", "教师", "社工", "人力资源"],
        "famous": ["泰勒·斯威夫特", "比尔·克林顿", "玛丽莲·梦露"],
        "percentage": "12.3%"
    },
    "ISTP": {
        "name": "鉴赏家",
        "nickname": "技术高手",
        "keywords": ["实践", "逻辑", "灵活", "好奇"],
        "description": "大胆而务实的实验家，擅长使用各种形式的工具。",
        "strengths": ["乐观能量", "创造实践", "知难而上", "理性果断"],
        "weaknesses": ["冷漠麻木", "私密封闭", "容易无聊", "风险偏好"],
        "career": ["工程师", "技工", "飞行员", "运动员"],
        "famous": ["克林特·伊斯特伍德", "米歇尔·乔丹", "小布鲁斯·李"],
        "percentage": "5.4%"
    },
    "ISFP": {
        "name": "探险家",
        "nickname": "艺术家",
        "keywords": ["艺术", "和谐", "敏感", "当下"],
        "description": "灵活而有魅力的艺术家，随时准备探索和体验新事物。",
        "strengths": ["迷人敏感", "想象丰富", "热情曲调", "艺术天赋"],
        "weaknesses": ["独立过度", "难以预测", "容易焦虑", "自尊心脆弱"],
        "career": ["艺术家", "设计师", "厨师", "自然保护工作者"],
        "famous": ["迈克尔·杰克逊", "玛丽莲·梦露", "奥黛丽·赫本"],
        "percentage": "8.8%"
    },
    "ESTP": {
        "name": "企业家",
        "nickname": "冒险实践者",
        "keywords": ["行动", "实践", "灵活", "冒险"],
        "description": "聪明、精力充沛且善于观察的人，真正享受在边缘生活。",
        "strengths": ["大胆直接", "理性实际", "善于观察", "社交能力强"],
        "weaknesses": ["不敏感", "缺乏耐心", "冲动冒险", "忽视大局"],
        "career": ["企业家", "销售", "运动员", "急救员"],
        "famous": ["欧内斯特·海明威", "杰克·尼克尔森", "麦当娜"],
        "percentage": "4.3%"
    },
    "ESFP": {
        "name": "表演者",
        "nickname": "娱乐明星",
        "keywords": ["热情", "表演", "乐趣", "社交"],
        "description": "自发的、精力充沛和热情的表演者，生活永远不会因为他们而无聊。",
        "strengths": ["大胆乐观", "实际动手", "善于观察", "社交能力强"],
        "weaknesses": ["敏感脆弱", "缺乏规划", "容易无聊", "缺乏专注"],
        "career": ["演员", "销售", "活动策划", "导游"],
        "famous": ["玛丽莲·梦露", "埃尔顿·约翰", "杰米·福克斯"],
        "percentage": "8.5%"
    }
}


# ==================== MBTI测试题库 ====================
# 共93题的标准版本（简化展示，实际有93题）

MBTI_QUESTIONS = [
    # ==================== E/I 维度 (23题) ====================
    {"id": 1, "text": "在社交活动后，你通常感觉？", "dimension": "EI",
     "options": [{"text": "精力充沛，想继续社交", "score": {"E": 1}}, 
                 {"text": "有些疲惫，想独处恢复", "score": {"I": 1}}]},
    {"id": 2, "text": "你更喜欢？", "dimension": "EI",
     "options": [{"text": "与许多人进行短暂互动", "score": {"E": 1}}, 
                 {"text": "与少数人进行深入交流", "score": {"I": 1}}]},
    {"id": 3, "text": "在团队讨论中，你通常？", "dimension": "EI",
     "options": [{"text": "积极发言并引导讨论", "score": {"E": 1}}, 
                 {"text": "先倾听思考再发表意见", "score": {"I": 1}}]},
    {"id": 4, "text": "你的朋友圈？", "dimension": "EI",
     "options": [{"text": "广泛，认识很多人", "score": {"E": 1}}, 
                 {"text": "较小，但关系深厚", "score": {"I": 1}}]},
    {"id": 5, "text": "周末你更喜欢？", "dimension": "EI",
     "options": [{"text": "参加聚会或社交活动", "score": {"E": 1}}, 
                 {"text": "在家阅读或独处", "score": {"I": 1}}]},
    {"id": 6, "text": "工作时你更喜欢？", "dimension": "EI",
     "options": [{"text": "开放式办公，随时交流", "score": {"E": 1}}, 
                 {"text": "独立空间，专注工作", "score": {"I": 1}}]},
    {"id": 7, "text": "遇到问题时？", "dimension": "EI",
     "options": [{"text": "先和他人讨论", "score": {"E": 1}}, 
                 {"text": "先自己思考分析", "score": {"I": 1}}]},
    {"id": 8, "text": "你的能量更多来自？", "dimension": "EI",
     "options": [{"text": "与他人互动", "score": {"E": 1}}, 
                 {"text": "独处和反思", "score": {"I": 1}}]},
    {"id": 9, "text": "在聚会上，你通常？", "dimension": "EI",
     "options": [{"text": "经常介绍陌生人互相认识", "score": {"E": 1}}, 
                 {"text": "虽然并不排斥，但多半是别人介绍给你", "score": {"I": 1}}]},
    {"id": 10, "text": "你认为自己是？", "dimension": "EI",
     "options": [{"text": "一个善于交际的人", "score": {"E": 1}}, 
                 {"text": "一个比较私密的人", "score": {"I": 1}}]},
    {"id": 11, "text": "当电话铃响时？", "dimension": "EI",
     "options": [{"text": "你通常会急切地去接听", "score": {"E": 1}}, 
                 {"text": "你希望别人去接听", "score": {"I": 1}}]},
    {"id": 12, "text": "在排队等候时？", "dimension": "EI",
     "options": [{"text": "你会经常找人聊天", "score": {"E": 1}}, 
                 {"text": "你习惯通过手机或专注于自己的事", "score": {"I": 1}}]},
    {"id": 13, "text": "你更容易？", "dimension": "EI",
     "options": [{"text": "通过交谈来理解事物", "score": {"E": 1}}, 
                 {"text": "通过阅读和思考来理解事物", "score": {"I": 1}}]},
    {"id": 14, "text": "在大多数情况下？", "dimension": "EI",
     "options": [{"text": "你是坦率而开放的", "score": {"E": 1}}, 
                 {"text": "你是保留而含蓄的", "score": {"I": 1}}]},
    {"id": 15, "text": "你更倾向于？", "dimension": "EI",
     "options": [{"text": "主动发起对话", "score": {"E": 1}}, 
                 {"text": "等待别人来和你说话", "score": {"I": 1}}]},
    {"id": 16, "text": "当需要在众人面前讲话时？", "dimension": "EI",
     "options": [{"text": "你感到兴奋和自然", "score": {"E": 1}}, 
                 {"text": "你感到紧张和不适", "score": {"I": 1}}]},
    {"id": 17, "text": "你朋友对你的评价倾向于？", "dimension": "EI",
     "options": [{"text": "充满活力", "score": {"E": 1}}, 
                 {"text": "沉稳安静", "score": {"I": 1}}]},
    {"id": 18, "text": "你更喜欢哪种工作方式？", "dimension": "EI",
     "options": [{"text": "团队合作，集思广益", "score": {"E": 1}}, 
                 {"text": "独立完成，专注深入", "score": {"I": 1}}]},
    {"id": 19, "text": "在空闲时间，你更想？", "dimension": "EI",
     "options": [{"text": "出门找朋友玩", "score": {"E": 1}}, 
                 {"text": "宅在家里看电影或玩游戏", "score": {"I": 1}}]},
    {"id": 20, "text": "遇到好消息时？", "dimension": "EI",
     "options": [{"text": "你会立刻告诉很多人", "score": {"E": 1}}, 
                 {"text": "你只告诉几个亲密的人", "score": {"I": 1}}]},
    {"id": 21, "text": "你更习惯于？", "dimension": "EI",
     "options": [{"text": "边说边想", "score": {"E": 1}}, 
                 {"text": "想好再说", "score": {"I": 1}}]},
    {"id": 22, "text": "在聚餐时，你通常是？", "dimension": "EI",
     "options": [{"text": "那个活跃气氛的人", "score": {"E": 1}}, 
                 {"text": "那个安静聆听的人", "score": {"I": 1}}]},
    {"id": 23, "text": "你认为独处是？", "dimension": "EI",
     "options": [{"text": "有时会感到孤单", "score": {"E": 1}}, 
                 {"text": "一种享受", "score": {"I": 1}}]},

    # ==================== S/N 维度 (23题) ====================
    {"id": 24, "text": "学习新事物时，你更关注？", "dimension": "SN",
     "options": [{"text": "具体步骤和实际操作", "score": {"S": 1}}, 
                 {"text": "整体概念和背后原理", "score": {"N": 1}}]},
    {"id": 25, "text": "描述事物时，你倾向于？", "dimension": "SN",
     "options": [{"text": "用具体的事实和细节", "score": {"S": 1}}, 
                 {"text": "用隐喻和比较", "score": {"N": 1}}]},
    {"id": 26, "text": "你更相信？", "dimension": "SN",
     "options": [{"text": "亲身经历和实践", "score": {"S": 1}}, 
                 {"text": "直觉和灵感", "score": {"N": 1}}]},
    {"id": 27, "text": "在阅读时，你更关注？", "dimension": "SN",
     "options": [{"text": "文字本身的含义", "score": {"S": 1}}, 
                 {"text": "文字之间的隐含意思", "score": {"N": 1}}]},
    {"id": 28, "text": "做计划时？", "dimension": "SN",
     "options": [{"text": "详细规划每个步骤", "score": {"S": 1}}, 
                 {"text": "大致方向即可，灵活调整", "score": {"N": 1}}]},
    {"id": 29, "text": "你更欣赏？", "dimension": "SN",
     "options": [{"text": "脚踏实地的人", "score": {"S": 1}}, 
                 {"text": "富有创意的人", "score": {"N": 1}}]},
    {"id": 30, "text": "工作中你更关注？", "dimension": "SN",
     "options": [{"text": "当下需要完成的任务", "score": {"S": 1}}, 
                 {"text": "未来的可能性和发展", "score": {"N": 1}}]},
    {"id": 31, "text": "你更喜欢？", "dimension": "SN",
     "options": [{"text": "使用已验证的方法", "score": {"S": 1}}, 
                 {"text": "尝试新的创新方法", "score": {"N": 1}}]},
    {"id": 32, "text": "你更倾向于？", "dimension": "SN",
     "options": [{"text": "活在当下", "score": {"S": 1}}, 
                 {"text": "展望未来", "score": {"N": 1}}]},
    {"id": 33, "text": "在看电影时，你更关注？", "dimension": "SN",
     "options": [{"text": "故事情节和画面细节", "score": {"S": 1}}, 
                 {"text": "电影的主题和象征意义", "score": {"N": 1}}]},
    {"id": 34, "text": "你通常更擅长？", "dimension": "SN",
     "options": [{"text": "处理具体的细节工作", "score": {"S": 1}}, 
                 {"text": "构思整体的宏观方案", "score": {"N": 1}}]},
    {"id": 35, "text": "你认为常识？", "dimension": "SN",
     "options": [{"text": "非常重要，值得遵循", "score": {"S": 1}}, 
                 {"text": "经常是可疑的，需要挑战", "score": {"N": 1}}]},
    {"id": 36, "text": "你倾向于？", "dimension": "SN",
     "options": [{"text": "从实际出发解决问题", "score": {"S": 1}}, 
                 {"text": "从新颖的角度解决问题", "score": {"N": 1}}]},
    {"id": 37, "text": "对于细节？", "dimension": "SN",
     "options": [{"text": "你记忆力很好，能记住很多细节", "score": {"S": 1}}, 
                 {"text": "你经常忽略细节，只记大意", "score": {"N": 1}}]},
    {"id": 38, "text": "你更喜欢哪种课程？", "dimension": "SN",
     "options": [{"text": "涉及具体事实和数据的课程", "score": {"S": 1}}, 
                 {"text": "涉及理论和假设的课程", "score": {"N": 1}}]},
    {"id": 39, "text": "在听别人说话时？", "dimension": "SN",
     "options": [{"text": "你关注他们实际说了什么", "score": {"S": 1}}, 
                 {"text": "你关注他们暗示了什么", "score": {"N": 1}}]},
    {"id": 40, "text": "你更看重？", "dimension": "SN",
     "options": [{"text": "经验", "score": {"S": 1}}, 
                 {"text": "预感", "score": {"N": 1}}]},
    {"id": 41, "text": "你通常是？", "dimension": "SN",
     "options": [{"text": "现实的", "score": {"S": 1}}, 
                 {"text": "富有想象力的", "score": {"N": 1}}]},
    {"id": 42, "text": "你更容易被什么说服？", "dimension": "SN",
     "options": [{"text": "无可辩驳的事实", "score": {"S": 1}}, 
                 {"text": "令人激动的可能性", "score": {"N": 1}}]},
    {"id": 43, "text": "你更喜欢做？", "dimension": "SN",
     "options": [{"text": "制作和修理东西", "score": {"S": 1}}, 
                 {"text": "设计和构思东西", "score": {"N": 1}}]},
    {"id": 44, "text": "在旅行时，你？", "dimension": "SN",
     "options": [{"text": "关注风景、美食和住宿", "score": {"S": 1}}, 
                 {"text": "关注当地的文化氛围和意义", "score": {"N": 1}}]},
    {"id": 45, "text": "对于规则？", "dimension": "SN",
     "options": [{"text": "你倾向于遵守和维护", "score": {"S": 1}}, 
                 {"text": "你倾向于质疑和改进", "score": {"N": 1}}]},
    {"id": 46, "text": "你认为自己更像？", "dimension": "SN",
     "options": [{"text": "观测者", "score": {"S": 1}}, 
                 {"text": "预言家", "score": {"N": 1}}]},

    # ==================== T/F 维度 (23题) ====================
    {"id": 47, "text": "做决定时，你更看重？", "dimension": "TF",
     "options": [{"text": "逻辑分析和客观事实", "score": {"T": 1}}, 
                 {"text": "个人价值观和他人感受", "score": {"F": 1}}]},
    {"id": 48, "text": "给别人反馈时，你倾向于？", "dimension": "TF",
     "options": [{"text": "直接指出问题所在", "score": {"T": 1}}, 
                 {"text": "考虑对方感受委婉表达", "score": {"F": 1}}]},
    {"id": 49, "text": "遇到冲突时？", "dimension": "TF",
     "options": [{"text": "用理性分析找到解决方案", "score": {"T": 1}}, 
                 {"text": "关注情感和关系的修复", "score": {"F": 1}}]},
    {"id": 50, "text": "你认为更重要的是？", "dimension": "TF",
     "options": [{"text": "真实坦诚", "score": {"T": 1}}, 
                 {"text": "体贴友善", "score": {"F": 1}}]},
    {"id": 51, "text": "评判一件事时？", "dimension": "TF",
     "options": [{"text": "关注对错与效率", "score": {"T": 1}}, 
                 {"text": "关注好坏与和谐", "score": {"F": 1}}]},
    {"id": 52, "text": "你更容易被打动的是？", "dimension": "TF",
     "options": [{"text": "有力的论证和数据", "score": {"T": 1}}, 
                 {"text": "感人的故事和情感", "score": {"F": 1}}]},
    {"id": 53, "text": "面对批评时？", "dimension": "TF",
     "options": [{"text": "理性分析是否有道理", "score": {"T": 1}}, 
                 {"text": "首先感到情感上的受挫", "score": {"F": 1}}]},
    {"id": 54, "text": "领导团队时，你更强调？", "dimension": "TF",
     "options": [{"text": "目标达成和效率", "score": {"T": 1}}, 
                 {"text": "团队和谐和成员感受", "score": {"F": 1}}]},
    {"id": 55, "text": "你认为这更是一种赞美？", "dimension": "TF",
     "options": [{"text": "“这是一个很有逻辑的人”", "score": {"T": 1}}, 
                 {"text": "“这是一个很感性的人”", "score": {"F": 1}}]},
    {"id": 56, "text": "你更倾向于？", "dimension": "TF",
     "options": [{"text": "客观地看待事物", "score": {"T": 1}}, 
                 {"text": "带入个人情感看事物", "score": {"F": 1}}]},
    {"id": 57, "text": "在安慰别人时？", "dimension": "TF",
     "options": [{"text": "你会分析问题并提供建议", "score": {"T": 1}}, 
                 {"text": "你会给予情感上的支持和共情", "score": {"F": 1}}]},
    {"id": 58, "text": "你认为原则？", "dimension": "TF",
     "options": [{"text": "比人情更重要", "score": {"T": 1}}, 
                 {"text": "有时需要为人情让路", "score": {"F": 1}}]},
    {"id": 59, "text": "在辩论中，你？", "dimension": "TF",
     "options": [{"text": "坚持真理，不惜得罪人", "score": {"T": 1}}, 
                 {"text": "为了避免伤害感情而妥协", "score": {"F": 1}}]},
    {"id": 60, "text": "你更看重哪种品质？", "dimension": "TF",
     "options": [{"text": "聪明", "score": {"T": 1}}, 
                 {"text": "仁慈", "score": {"F": 1}}]},
    {"id": 61, "text": "你做事的动力更多来自？", "dimension": "TF",
     "options": [{"text": "成就感和胜任感", "score": {"T": 1}}, 
                 {"text": "被欣赏和归属感", "score": {"F": 1}}]},
    {"id": 62, "text": "你认为自己更像？", "dimension": "TF",
     "options": [{"text": "坚定的执法者", "score": {"T": 1}}, 
                 {"text": "温柔的守护者", "score": {"F": 1}}]},
    {"id": 63, "text": "当面对不合理的请求时？", "dimension": "TF",
     "options": [{"text": "你会直接拒绝", "score": {"T": 1}}, 
                 {"text": "你会感到为难，难以启齿", "score": {"F": 1}}]},
    {"id": 64, "text": "你在做重要选择时？", "dimension": "TF",
     "options": [{"text": "列出利弊清单", "score": {"T": 1}}, 
                 {"text": "听从内心的呼唤", "score": {"F": 1}}]},
    {"id": 65, "text": "你认为争论是？", "dimension": "TF",
     "options": [{"text": "思想碰撞的好机会", "score": {"T": 1}}, 
                 {"text": "伤感情的坏事", "score": {"F": 1}}]},
    {"id": 66, "text": "你更难接受？", "dimension": "TF",
     "options": [{"text": "不合逻辑的行为", "score": {"T": 1}}, 
                 {"text": "冷酷无情的行为", "score": {"F": 1}}]},
    {"id": 67, "text": "你的决策风格？", "dimension": "TF",
     "options": [{"text": "果断、客观", "score": {"T": 1}}, 
                 {"text": "犹豫、感性", "score": {"F": 1}}]},
    {"id": 68, "text": "在观看比赛时？", "dimension": "TF",
     "options": [{"text": "你关注比分和战术", "score": {"T": 1}}, 
                 {"text": "你关注选手的努力和精神", "score": {"F": 1}}]},
    {"id": 69, "text": "你更信任？", "dimension": "TF",
     "options": [{"text": "大脑", "score": {"T": 1}}, 
                 {"text": "心灵", "score": {"F": 1}}]},

    # ==================== J/P 维度 (24题) ====================
    {"id": 70, "text": "你的生活方式更倾向于？", "dimension": "JP",
     "options": [{"text": "有计划有条理", "score": {"J": 1}}, 
                 {"text": "灵活随性", "score": {"P": 1}}]},
    {"id": 71, "text": "面对截止日期？", "dimension": "JP",
     "options": [{"text": "提前完成，留有余地", "score": {"J": 1}}, 
                 {"text": "截止前才能激发动力", "score": {"P": 1}}]},
    {"id": 72, "text": "日程表对你来说？", "dimension": "JP",
     "options": [{"text": "是必要的规划工具", "score": {"J": 1}}, 
                 {"text": "是一种限制和束缚", "score": {"P": 1}}]},
    {"id": 73, "text": "做决定时？", "dimension": "JP",
     "options": [{"text": "喜欢快速做出决定", "score": {"J": 1}}, 
                 {"text": "喜欢保持开放选项", "score": {"P": 1}}]},
    {"id": 74, "text": "你的工作桌面通常？", "dimension": "JP",
     "options": [{"text": "整洁有序", "score": {"J": 1}}, 
                 {"text": "创意性混乱", "score": {"P": 1}}]},
    {"id": 75, "text": "出门旅行时？", "dimension": "JP",
     "options": [{"text": "详细规划行程", "score": {"J": 1}}, 
                 {"text": "随性探索", "score": {"P": 1}}]},
    {"id": 76, "text": "开始新项目时？", "dimension": "JP",
     "options": [{"text": "先制定详细计划", "score": {"J": 1}}, 
                 {"text": "边做边调整", "score": {"P": 1}}]},
    {"id": 77, "text": "你更享受？", "dimension": "JP",
     "options": [{"text": "完成任务的满足感", "score": {"J": 1}}, 
                 {"text": "探索过程的乐趣", "score": {"P": 1}}]},
    {"id": 78, "text": "你通常会？", "dimension": "JP",
     "options": [{"text": "先把工作做完再玩", "score": {"J": 1}}, 
                 {"text": "先玩一会儿，压力大了再工作", "score": {"P": 1}}]},
    {"id": 79, "text": "对于突发事件？", "dimension": "JP",
     "options": [{"text": "你可能会感到被打扰", "score": {"J": 1}}, 
                 {"text": "你觉得这很有趣", "score": {"P": 1}}]},
    {"id": 80, "text": "你更喜欢？", "dimension": "JP",
     "options": [{"text": "确定的结果", "score": {"J": 1}}, 
                 {"text": "不确定性", "score": {"P": 1}}]},
    {"id": 81, "text": "在购物时？", "dimension": "JP",
     "options": [{"text": "你会列好清单再去", "score": {"J": 1}}, 
                 {"text": "你会看心情购买", "score": {"P": 1}}]},
    {"id": 82, "text": "你做事倾向于？", "dimension": "JP",
     "options": [{"text": "稳扎稳打", "score": {"J": 1}}, 
                 {"text": "此时不搏更待何时", "score": {"P": 1}}]},
    {"id": 83, "text": "如果计划改变了？", "dimension": "JP",
     "options": [{"text": "这会让你感到不安", "score": {"J": 1}}, 
                 {"text": "你很容易适应新情况", "score": {"P": 1}}]},
    {"id": 84, "text": "你更喜欢的工作环境是？", "dimension": "JP",
     "options": [{"text": "结构清晰，职责明确", "score": {"J": 1}}, 
                 {"text": "灵活宽松，自由度大", "score": {"P": 1}}]},
    {"id": 85, "text": "你认为最后期限是？", "dimension": "JP",
     "options": [{"text": "必须严格遵守的", "score": {"J": 1}}, 
                 {"text": "一个参考建议", "score": {"P": 1}}]},
    {"id": 86, "text": "你更擅长？", "dimension": "JP",
     "options": [{"text": "收尾工作", "score": {"J": 1}}, 
                 {"text": "开创工作", "score": {"P": 1}}]},
    {"id": 87, "text": "你的生活座右铭更像？", "dimension": "JP",
     "options": [{"text": "“凡事预则立”", "score": {"J": 1}}, 
                 {"text": "“船到桥头自然直”", "score": {"P": 1}}]},
    {"id": 88, "text": "你喜欢？", "dimension": "JP",
     "options": [{"text": "看到任务清单被一项项勾掉", "score": {"J": 1}}, 
                 {"text": "由于有了新发现而改变任务清单", "score": {"P": 1}}]},
    {"id": 89, "text": "在日常生活中？", "dimension": "JP",
     "options": [{"text": "你有固定的习惯", "score": {"J": 1}}, 
                 {"text": "你喜欢每天都有新花样", "score": {"P": 1}}]},
    {"id": 90, "text": "你认为自己是？", "dimension": "JP",
     "options": [{"text": "一个更有条理的人", "score": {"J": 1}}, 
                 {"text": "一个更随意的人", "score": {"P": 1}}]},
    {"id": 91, "text": "在看书时？", "dimension": "JP",
     "options": [{"text": "你倾向于读完一本再开下一本", "score": {"J": 1}}, 
                 {"text": "你经常同时看好几本书", "score": {"P": 1}}]},
    {"id": 92, "text": "在会议中？", "dimension": "JP",
     "options": [{"text": "你看重议程和结论", "score": {"J": 1}}, 
                 {"text": "你看重讨论的过程和新想法", "score": {"P": 1}}]},
    {"id": 93, "text": "对于未来？", "dimension": "JP",
     "options": [{"text": "你已经规划好了", "score": {"J": 1}}, 
                 {"text": "你拭目以待", "score": {"P": 1}}]}
]


# ==================== MBTI计算与分析 ====================

@dataclass
class MBTIResult:
    """MBTI测试结果"""
    type_code: str              # 如 "INTJ"
    type_name: str              # 如 "建筑师"
    dimensions: Dict[str, Dict] # 四个维度的得分和倾向
    description: Dict           # 类型详细描述
    scores: Dict[str, int]      # 各维度原始得分
    confidence: float           # 结果可信度


def calculate_mbti(answers: List[Dict]) -> MBTIResult:
    """
    计算MBTI类型
    
    Args:
        answers: 答案列表 [{"question_id": 1, "option_index": 0}, ...]
    
    Returns:
        MBTI结果
    """
    # 初始化得分
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    
    # 计算得分
    for answer in answers:
        q_id = answer.get("question_id")
        opt_idx = answer.get("option_index", 0)
        
        question = next((q for q in MBTI_QUESTIONS if q["id"] == q_id), None)
        if question and opt_idx < len(question["options"]):
            score_dict = question["options"][opt_idx]["score"]
            for key, value in score_dict.items():
                scores[key] += value
    
    # 确定各维度倾向
    dimensions = {}
    
    # E/I维度
    e_total = scores["E"]
    i_total = scores["I"]
    ei_total = e_total + i_total
    ei_pref = "E" if e_total >= i_total else "I"
    dimensions["EI"] = {
        "preference": ei_pref,
        "E_score": e_total,
        "I_score": i_total,
        "clarity": abs(e_total - i_total) / max(ei_total, 1) * 100
    }
    
    # S/N维度
    s_total = scores["S"]
    n_total = scores["N"]
    sn_total = s_total + n_total
    sn_pref = "S" if s_total >= n_total else "N"
    dimensions["SN"] = {
        "preference": sn_pref,
        "S_score": s_total,
        "N_score": n_total,
        "clarity": abs(s_total - n_total) / max(sn_total, 1) * 100
    }
    
    # T/F维度
    t_total = scores["T"]
    f_total = scores["F"]
    tf_total = t_total + f_total
    tf_pref = "T" if t_total >= f_total else "F"
    dimensions["TF"] = {
        "preference": tf_pref,
        "T_score": t_total,
        "F_score": f_total,
        "clarity": abs(t_total - f_total) / max(tf_total, 1) * 100
    }
    
    # J/P维度
    j_total = scores["J"]
    p_total = scores["P"]
    jp_total = j_total + p_total
    jp_pref = "J" if j_total >= p_total else "P"
    dimensions["JP"] = {
        "preference": jp_pref,
        "J_score": j_total,
        "P_score": p_total,
        "clarity": abs(j_total - p_total) / max(jp_total, 1) * 100
    }
    
    # 组合类型
    type_code = f"{ei_pref}{sn_pref}{tf_pref}{jp_pref}"
    
    # 计算可信度（根据各维度清晰度）
    avg_clarity = sum(d["clarity"] for d in dimensions.values()) / 4
    confidence = min(avg_clarity / 50 * 100, 100)  # 归一化到0-100
    
    # 获取类型描述
    description = MBTI_DESCRIPTIONS.get(type_code, {})
    
    return MBTIResult(
        type_code=type_code,
        type_name=description.get("name", "未知类型"),
        dimensions=dimensions,
        description=description,
        scores=scores,
        confidence=confidence
    )


def get_mbti_compatibility(type1: str, type2: str) -> Dict:
    """
    计算两种MBTI类型的兼容性
    
    Args:
        type1: 第一个类型（如 "INTJ"）
        type2: 第二个类型（如 "ENFP"）
    
    Returns:
        兼容性分析
    """
    # 计算维度匹配度
    matches = 0
    differences = []
    
    for i, (d1, d2) in enumerate(zip(type1, type2)):
        if d1 == d2:
            matches += 1
        else:
            dim_names = ["精力来源", "信息获取", "决策方式", "生活态度"]
            differences.append({
                "dimension": dim_names[i],
                "type1": d1,
                "type2": d2
            })
    
    # 计算兼容性分数
    base_score = (matches / 4) * 60  # 基础分最高60
    
    # 互补加分
    complementary_pairs = [
        ("INTJ", "ENFP"), ("INFJ", "ENTP"),
        ("INFP", "ENTJ"), ("INTP", "ENFJ"),
        ("ISTJ", "ESFP"), ("ISFJ", "ESTP"),
        ("ISTP", "ESFJ"), ("ISFP", "ESTJ")
    ]
    
    for pair in complementary_pairs:
        if (type1, type2) in [pair, pair[::-1]]:
            base_score += 25
            break
    
    # 完全相同加分
    if type1 == type2:
        base_score += 15
    
    score = min(base_score, 100)
    
    if score >= 80:
        level = "非常契合"
        advice = "你们有极佳的默契和互补性"
    elif score >= 60:
        level = "比较契合"
        advice = "你们可以相互理解和欣赏"
    elif score >= 40:
        level = "需要磨合"
        advice = "需要更多沟通和理解"
    else:
        level = "挑战较大"
        advice = "需要有意识地调适相处方式"
    
    return {
        "score": round(score),
        "level": level,
        "matches": matches,
        "differences": differences,
        "advice": advice
    }


def get_mbti_questions(count: int = None) -> List[Dict]:
    """获取MBTI测试题目"""
    questions = MBTI_QUESTIONS.copy()
    if count:
        questions = questions[:count]
    return questions
