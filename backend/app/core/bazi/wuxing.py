"""
玄心理命 - 五行分析模块
五行强弱、生克关系、喜用神分析
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

from .calendar import (
    SiZhu, GanZhi, TIAN_GAN, DI_ZHI,
    TIAN_GAN_WUXING, DI_ZHI_WUXING, DI_ZHI_CANG_GAN,
    TIAN_GAN_YINYANG, DI_ZHI_YINYANG
)


class WuXing(Enum):
    """五行枚举"""
    MU = "木"
    HUO = "火"
    TU = "土"
    JIN = "金"
    SHUI = "水"


# 五行相生关系：木生火，火生土，土生金，金生水，水生木
WUXING_SHENG = {
    "木": "火", "火": "土", "土": "金", "金": "水", "水": "木"
}

# 五行相克关系：木克土，土克水，水克火，火克金，金克木
WUXING_KE = {
    "木": "土", "土": "水", "水": "火", "火": "金", "金": "木"
}

# 五行被克关系
WUXING_BEI_KE = {
    "木": "金", "火": "水", "土": "木", "金": "火", "水": "土"
}

# 五行被生关系
WUXING_BEI_SHENG = {
    "木": "水", "火": "木", "土": "火", "金": "土", "水": "金"
}

# 地支五行力量（以月令为基准）
# 当令为旺，相令为相，休谿为休，囚令为囚，死令为死
WUXING_SEASONAL_STRENGTH = {
    # 春季（寅卯辰月）
    "寅": {"木": 1.2, "火": 1.0, "土": 0.6, "金": 0.4, "水": 0.8},
    "卯": {"木": 1.2, "火": 1.0, "土": 0.6, "金": 0.4, "水": 0.8},
    "辰": {"木": 1.0, "火": 0.8, "土": 1.2, "金": 0.6, "水": 0.6},
    # 夏季（巳午未月）
    "巳": {"木": 0.8, "火": 1.2, "土": 1.0, "金": 0.4, "水": 0.4},
    "午": {"木": 0.8, "火": 1.2, "土": 1.0, "金": 0.4, "水": 0.4},
    "未": {"木": 0.6, "火": 1.0, "土": 1.2, "金": 0.6, "水": 0.4},
    # 秋季（申酉戌月）
    "申": {"木": 0.4, "火": 0.6, "土": 1.0, "金": 1.2, "水": 0.8},
    "酉": {"木": 0.4, "火": 0.6, "土": 1.0, "金": 1.2, "水": 0.8},
    "戌": {"木": 0.4, "火": 0.6, "土": 1.2, "金": 1.0, "水": 0.6},
    # 冬季（亥子丑月）
    "亥": {"木": 1.0, "火": 0.4, "土": 0.6, "金": 0.8, "水": 1.2},
    "子": {"木": 1.0, "火": 0.4, "土": 0.6, "金": 0.8, "水": 1.2},
    "丑": {"木": 0.6, "火": 0.4, "土": 1.2, "金": 1.0, "水": 1.0}
}

# 天干力量基础值
GAN_BASE_STRENGTH = 1.0
# 地支正气力量基础值
ZHI_ZHENGQI_STRENGTH = 1.0
# 地支中气力量
ZHI_ZHONGQI_STRENGTH = 0.5
# 地支余气力量
ZHI_YUQI_STRENGTH = 0.3


@dataclass
class WuXingScore:
    """五行得分"""
    mu: float = 0.0   # 木
    huo: float = 0.0  # 火
    tu: float = 0.0   # 土
    jin: float = 0.0  # 金
    shui: float = 0.0 # 水
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "木": round(self.mu, 3),
            "火": round(self.huo, 3),
            "土": round(self.tu, 3),
            "金": round(self.jin, 3),
            "水": round(self.shui, 3)
        }
    
    def get(self, wuxing: str) -> float:
        mapping = {"木": self.mu, "火": self.huo, "土": self.tu, "金": self.jin, "水": self.shui}
        return mapping.get(wuxing, 0)
    
    def add(self, wuxing: str, value: float):
        if wuxing == "木":
            self.mu += value
        elif wuxing == "火":
            self.huo += value
        elif wuxing == "土":
            self.tu += value
        elif wuxing == "金":
            self.jin += value
        elif wuxing == "水":
            self.shui += value
    
    def total(self) -> float:
        return self.mu + self.huo + self.tu + self.jin + self.shui
    
    def percentages(self) -> Dict[str, float]:
        """返回各五行百分比"""
        total = self.total()
        if total == 0:
            return {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        return {
            "木": round(self.mu / total * 100, 1),
            "火": round(self.huo / total * 100, 1),
            "土": round(self.tu / total * 100, 1),
            "金": round(self.jin / total * 100, 1),
            "水": round(self.shui / total * 100, 1)
        }
    
    def strongest(self) -> Tuple[str, float]:
        """返回最强的五行"""
        d = self.to_dict()
        max_wx = max(d, key=d.get)
        return max_wx, d[max_wx]
    
    def weakest(self) -> Tuple[str, float]:
        """返回最弱的五行"""
        d = self.to_dict()
        min_wx = min(d, key=d.get)
        return min_wx, d[min_wx]
    
    def balance_analysis(self) -> Dict[str, str]:
        """五行平衡分析"""
        percentages = self.percentages()
        avg = 20.0  # 平均每个五行应占20%
        
        result = {}
        for wx, pct in percentages.items():
            if pct > avg * 1.5:
                result[wx] = "过旺"
            elif pct > avg * 1.2:
                result[wx] = "偏旺"
            elif pct < avg * 0.5:
                result[wx] = "过弱"
            elif pct < avg * 0.8:
                result[wx] = "偏弱"
            else:
                result[wx] = "平衡"
        
        return result


def calculate_wuxing_score(sizhu: SiZhu) -> WuXingScore:
    """
    计算八字五行得分
    
    Args:
        sizhu: 四柱八字
    
    Returns:
        五行得分对象
    """
    score = WuXingScore()
    month_zhi = sizhu.month.zhi
    seasonal_factor = WUXING_SEASONAL_STRENGTH.get(month_zhi, {})
    
    # 计算天干五行得分
    for gan in sizhu.get_all_gan():
        wuxing = TIAN_GAN_WUXING[gan]
        strength = GAN_BASE_STRENGTH * seasonal_factor.get(wuxing, 1.0)
        score.add(wuxing, strength)
    
    # 计算地支藏干五行得分
    for zhi in sizhu.get_all_zhi():
        cang_gan = DI_ZHI_CANG_GAN[zhi]
        
        for i, gan in enumerate(cang_gan):
            wuxing = TIAN_GAN_WUXING[gan]
            
            # 根据藏干位置确定力量
            if i == 0:  # 正气（本气）
                base = ZHI_ZHENGQI_STRENGTH
            elif i == 1:  # 中气
                base = ZHI_ZHONGQI_STRENGTH
            else:  # 余气
                base = ZHI_YUQI_STRENGTH
            
            strength = base * seasonal_factor.get(wuxing, 1.0)
            score.add(wuxing, strength)
    
    return score


def get_day_master_strength(sizhu: SiZhu) -> Dict:
    """
    分析日主强弱
    
    Args:
        sizhu: 四柱八字
    
    Returns:
        日主强弱分析结果
    """
    day_master = sizhu.day_master
    day_master_wuxing = TIAN_GAN_WUXING[day_master]
    
    score = calculate_wuxing_score(sizhu)
    day_master_score = score.get(day_master_wuxing)
    
    # 计算同类五行力量（生我和同我）
    sheng_wo = WUXING_BEI_SHENG[day_master_wuxing]  # 生我的五行
    same_and_support = day_master_score + score.get(sheng_wo)
    
    # 计算异类五行力量（我生、克我、我克）
    wo_sheng = WUXING_SHENG[day_master_wuxing]      # 我生的五行
    ke_wo = WUXING_BEI_KE[day_master_wuxing]        # 克我的五行
    wo_ke = WUXING_KE[day_master_wuxing]            # 我克的五行
    opposite = score.get(wo_sheng) + score.get(ke_wo) + score.get(wo_ke)
    
    total = score.total()
    strength_ratio = same_and_support / total if total > 0 else 0
    
    # 判断日主强弱
    if strength_ratio > 0.55:
        strength_level = "身强"
        description = "日主力量充足，自信坚定"
    elif strength_ratio > 0.45:
        strength_level = "中和"
        description = "日主力量平衡，进退自如"
    else:
        strength_level = "身弱"
        description = "日主力量不足，需要扶助"
    
    return {
        "day_master": day_master,
        "day_master_wuxing": day_master_wuxing,
        "strength_ratio": round(strength_ratio, 3),
        "strength_level": strength_level,
        "description": description,
        "same_and_support": round(same_and_support, 2),
        "opposite": round(opposite, 2)
    }


def get_xi_yong_shen(sizhu: SiZhu) -> Dict:
    """
    分析喜用神
    
    Args:
        sizhu: 四柱八字
    
    Returns:
        喜用神分析结果
    """
    day_master = sizhu.day_master
    day_master_wuxing = TIAN_GAN_WUXING[day_master]
    strength = get_day_master_strength(sizhu)
    score = calculate_wuxing_score(sizhu)
    
    xi_shen = []   # 喜神
    yong_shen = []  # 用神
    ji_shen = []   # 忌神
    chou_shen = [] # 仇神
    
    sheng_wo = WUXING_BEI_SHENG[day_master_wuxing]
    wo_sheng = WUXING_SHENG[day_master_wuxing]
    ke_wo = WUXING_BEI_KE[day_master_wuxing]
    wo_ke = WUXING_KE[day_master_wuxing]
    
    if strength["strength_level"] == "身强":
        # 身强喜泄耗克：我生、我克、克我的五行
        yong_shen.append(wo_sheng)  # 食伤泄秀
        xi_shen.append(wo_ke)       # 财星耗身
        xi_shen.append(ke_wo)       # 官杀克身
        ji_shen.append(day_master_wuxing)  # 比劫
        chou_shen.append(sheng_wo)  # 印星
    else:
        # 身弱喜生扶：生我、同我的五行
        yong_shen.append(sheng_wo)  # 印星生扶
        xi_shen.append(day_master_wuxing)  # 比劫帮身
        ji_shen.append(wo_sheng)    # 食伤泄身
        ji_shen.append(wo_ke)       # 财星耗身
        chou_shen.append(ke_wo)     # 官杀克身
    
    return {
        "strength_level": strength["strength_level"],
        "yong_shen": yong_shen,
        "xi_shen": xi_shen,
        "ji_shen": ji_shen,
        "chou_shen": chou_shen,
        "analysis": _get_xi_yong_analysis(yong_shen, xi_shen, strength["strength_level"])
    }


def _get_xi_yong_analysis(yong: List[str], xi: List[str], level: str) -> str:
    """生成喜用神分析文案"""
    yong_str = "、".join(yong)
    xi_str = "、".join(xi)
    
    if level == "身强":
        return f"八字身强，需要泄耗。用神为{yong_str}，喜神为{xi_str}。宜从事与用神相关的行业，穿戴用神属性的颜色。"
    else:
        return f"八字身弱，需要生扶。用神为{yong_str}，喜神为{xi_str}。宜接近用神属性的人事物，增强自身能量。"


def get_wuxing_relationship(wuxing1: str, wuxing2: str) -> str:
    """
    获取两个五行的关系
    
    Args:
        wuxing1: 第一个五行
        wuxing2: 第二个五行
    
    Returns:
        关系描述
    """
    if wuxing1 == wuxing2:
        return "比和"
    elif WUXING_SHENG.get(wuxing1) == wuxing2:
        return "我生"
    elif WUXING_SHENG.get(wuxing2) == wuxing1:
        return "生我"
    elif WUXING_KE.get(wuxing1) == wuxing2:
        return "我克"
    elif WUXING_KE.get(wuxing2) == wuxing1:
        return "克我"
    else:
        return "未知"


# 五行对应的颜色
WUXING_COLOR = {
    "木": ["绿色", "青色", "翠色"],
    "火": ["红色", "紫色", "粉色"],
    "土": ["黄色", "棕色", "咖啡色"],
    "金": ["白色", "金色", "银色"],
    "水": ["黑色", "蓝色", "灰色"]
}

# 五行对应的方位
WUXING_DIRECTION = {
    "木": "东方",
    "火": "南方",
    "土": "中央",
    "金": "西方",
    "水": "北方"
}

# 五行对应的数字
WUXING_NUMBER = {
    "木": [3, 8],
    "火": [2, 7],
    "土": [5, 10],
    "金": [4, 9],
    "水": [1, 6]
}

# 五行对应的行业
WUXING_CAREER = {
    "木": ["教育", "出版", "文化", "医疗", "园艺", "家具", "服装", "木材"],
    "火": ["电子", "能源", "餐饮", "娱乐", "传媒", "化工", "照明", "美容"],
    "土": ["房地产", "建筑", "农业", "矿业", "陶瓷", "仓储", "殡葬", "养殖"],
    "金": ["金融", "机械", "珠宝", "汽车", "五金", "司法", "军警", "IT"],
    "水": ["航运", "水产", "旅游", "物流", "贸易", "清洁", "酒店", "传播"]
}


def get_wuxing_suggestions(xi_yong: Dict) -> Dict:
    """
    根据喜用神获取建议
    
    Args:
        xi_yong: 喜用神分析结果
    
    Returns:
        各方面建议
    """
    yong_shen = xi_yong["yong_shen"][0] if xi_yong["yong_shen"] else None
    if not yong_shen:
        return {}
    
    return {
        "colors": WUXING_COLOR.get(yong_shen, []),
        "direction": WUXING_DIRECTION.get(yong_shen, ""),
        "numbers": WUXING_NUMBER.get(yong_shen, []),
        "careers": WUXING_CAREER.get(yong_shen, []),
        "description": f"根据您的用神{yong_shen}，建议多使用{WUXING_COLOR.get(yong_shen, [''])[0]}，"
                      f"发展方向宜往{WUXING_DIRECTION.get(yong_shen, '')}，"
                      f"幸运数字为{WUXING_NUMBER.get(yong_shen, [])}。"
    }


if __name__ == "__main__":
    from .calendar import calculate_sizhu
    
    # 测试示例
    sizhu = calculate_sizhu(1990, 5, 15, 10)
    print(f"八字: {sizhu.bazi}")
    
    # 五行得分
    score = calculate_wuxing_score(sizhu)
    print(f"五行得分: {score.to_dict()}")
    print(f"五行百分比: {score.percentages()}")
    print(f"五行平衡: {score.balance_analysis()}")
    
    # 日主强弱
    strength = get_day_master_strength(sizhu)
    print(f"日主强弱: {strength}")
    
    # 喜用神
    xi_yong = get_xi_yong_shen(sizhu)
    print(f"喜用神: {xi_yong}")
    
    # 建议
    suggestions = get_wuxing_suggestions(xi_yong)
    print(f"建议: {suggestions}")
