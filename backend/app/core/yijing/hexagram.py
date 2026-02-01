"""
玄心理命 - 易经占卜模块
梅花易数、六爻、卦象解读
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import random


# 八卦基础数据
BAGUA = {
    "乾": {"number": 1, "element": "金", "symbol": "☰", "trigram": "111", "nature": "天", "family": "父"},
    "兑": {"number": 2, "element": "金", "symbol": "☱", "trigram": "110", "nature": "泽", "family": "少女"},
    "离": {"number": 3, "element": "火", "symbol": "☲", "trigram": "101", "nature": "火", "family": "中女"},
    "震": {"number": 4, "element": "木", "symbol": "☳", "trigram": "100", "nature": "雷", "family": "长男"},
    "巽": {"number": 5, "element": "木", "symbol": "☴", "trigram": "011", "nature": "风", "family": "长女"},
    "坎": {"number": 6, "element": "水", "symbol": "☵", "trigram": "010", "nature": "水", "family": "中男"},
    "艮": {"number": 7, "element": "土", "symbol": "☶", "trigram": "001", "nature": "山", "family": "少男"},
    "坤": {"number": 8, "element": "土", "symbol": "☷", "trigram": "000", "nature": "地", "family": "母"}
}

# 八卦数字映射
NUMBER_TO_GUA = {1: "乾", 2: "兑", 3: "离", 4: "震", 5: "巽", 6: "坎", 7: "艮", 8: "坤"}
GUA_TO_NUMBER = {v: k for k, v in NUMBER_TO_GUA.items()}

# 六十四卦名称（上卦+下卦）
SIXTY_FOUR_GUA = {
    ("乾", "乾"): "乾为天", ("坤", "坤"): "坤为地",
    ("坎", "震"): "水雷屯", ("艮", "坎"): "山水蒙",
    ("坎", "乾"): "水天需", ("乾", "坎"): "天水讼",
    ("坤", "坎"): "地水师", ("坎", "坤"): "水地比",
    ("巽", "乾"): "风天小畜", ("乾", "兑"): "天泽履",
    ("坤", "乾"): "地天泰", ("乾", "坤"): "天地否",
    ("乾", "离"): "天火同人", ("离", "乾"): "火天大有",
    ("坤", "艮"): "地山谦", ("震", "坤"): "雷地豫",
    ("兑", "震"): "泽雷随", ("艮", "巽"): "山风蛊",
    ("坤", "兑"): "地泽临", ("巽", "坤"): "风地观",
    ("离", "震"): "火雷噬嗑", ("艮", "离"): "山火贲",
    ("艮", "坤"): "山地剥", ("坤", "震"): "地雷复",
    ("乾", "震"): "天雷无妄", ("艮", "乾"): "山天大畜",
    ("艮", "震"): "山雷颐", ("兑", "巽"): "泽风大过",
    ("坎", "坎"): "坎为水", ("离", "离"): "离为火",
    ("兑", "艮"): "泽山咸", ("震", "巽"): "雷风恒",
    ("乾", "艮"): "天山遁", ("震", "乾"): "雷天大壮",
    ("离", "坤"): "火地晋", ("坤", "离"): "地火明夷",
    ("巽", "离"): "风火家人", ("离", "兑"): "火泽睽",
    ("坎", "艮"): "水山蹇", ("震", "坎"): "雷水解",
    ("艮", "兑"): "山泽损", ("巽", "震"): "风雷益",
    ("兑", "乾"): "泽天夬", ("乾", "巽"): "天风姤",
    ("兑", "坤"): "泽地萃", ("坤", "巽"): "地风升",
    ("兑", "坎"): "泽水困", ("坎", "巽"): "水风井",
    ("兑", "离"): "泽火革", ("离", "巽"): "火风鼎",
    ("震", "震"): "震为雷", ("艮", "艮"): "艮为山",
    ("巽", "艮"): "风山渐", ("震", "兑"): "雷泽归妹",
    ("震", "离"): "雷火丰", ("离", "艮"): "火山旅",
    ("巽", "巽"): "巽为风", ("兑", "兑"): "兑为泽",
    ("巽", "坎"): "风水涣", ("坎", "兑"): "水泽节",
    ("巽", "兑"): "风泽中孚", ("震", "艮"): "雷山小过",
    ("坎", "离"): "水火既济", ("离", "坎"): "火水未济"
}

# 卦象解读模板
# 导入卦象解读数据
from .data import GUA_INTERPRETATIONS

# 默认卦象解读（用于未定义的卦）
DEFAULT_INTERPRETATION = {
    "summary": "此卦需详细分析",
    "keywords": ["变化", "时机", "选择"],
    "fortune": "顺应自然，观察变化",
    "career": "谨慎行事，把握时机",
    "relationship": "以诚相待，随缘",
    "wealth": "量入为出，稳健理财"
}


class YaoType(Enum):
    """爻类型"""
    YANG = "阳爻"   # ———
    YIN = "阴爻"    # — —
    YANG_DONG = "老阳"  # 阳爻动变阴
    YIN_DONG = "老阴"   # 阴爻动变阳


@dataclass
class Yao:
    """爻"""
    position: int       # 位置 (1-6, 从下往上)
    yao_type: YaoType   # 爻类型
    is_dong: bool       # 是否动爻
    
    @property
    def symbol(self) -> str:
        if self.yao_type in [YaoType.YANG, YaoType.YANG_DONG]:
            return "———"
        else:
            return "— —"
    
    @property
    def changed_symbol(self) -> str:
        """变爻后的符号"""
        if self.is_dong:
            if self.yao_type == YaoType.YANG_DONG:
                return "— —"
            elif self.yao_type == YaoType.YIN_DONG:
                return "———"
        return self.symbol


@dataclass
class Hexagram:
    """卦象"""
    upper_gua: str          # 上卦
    lower_gua: str          # 下卦
    yaos: List[Yao]         # 六爻
    dong_yao: Optional[int] # 动爻位置
    
    @property
    def name(self) -> str:
        """获取卦名"""
        return SIXTY_FOUR_GUA.get((self.upper_gua, self.lower_gua), f"{self.upper_gua}{self.lower_gua}")
    
    @property
    def changed_hexagram(self) -> Optional['Hexagram']:
        """获取变卦"""
        if not self.dong_yao:
            return None
        
        # 复制六爻并变动
        new_yaos = []
        for yao in self.yaos:
            if yao.position == self.dong_yao:
                # 动爻变化
                new_type = YaoType.YIN if yao.yao_type in [YaoType.YANG, YaoType.YANG_DONG] else YaoType.YANG
                new_yaos.append(Yao(yao.position, new_type, False))
            else:
                new_yaos.append(Yao(yao.position, yao.yao_type, False))
        
        # 重新计算上下卦
        lower_binary = "".join("1" if y.yao_type in [YaoType.YANG, YaoType.YANG_DONG] else "0" 
                               for y in new_yaos[:3])
        upper_binary = "".join("1" if y.yao_type in [YaoType.YANG, YaoType.YANG_DONG] else "0" 
                               for y in new_yaos[3:])
        
        new_lower = _binary_to_gua(lower_binary)
        new_upper = _binary_to_gua(upper_binary)
        
        return Hexagram(new_upper, new_lower, new_yaos, None)
    
    def get_interpretation(self) -> Dict:
        """获取卦象解读"""
        interp = GUA_INTERPRETATIONS.get(self.name, DEFAULT_INTERPRETATION)
        return {
            "name": self.name,
            "upper_gua": self.upper_gua,
            "lower_gua": self.lower_gua,
            "upper_symbol": BAGUA[self.upper_gua]["symbol"],
            "lower_symbol": BAGUA[self.lower_gua]["symbol"],
            "dong_yao": self.dong_yao,
            **interp
        }


def _binary_to_gua(binary: str) -> str:
    """二进制转卦名"""
    mapping = {
        "111": "乾", "110": "兑", "101": "离", "100": "震",
        "011": "巽", "010": "坎", "001": "艮", "000": "坤"
    }
    return mapping.get(binary, "乾")


def _number_to_gua(number: int) -> str:
    """数字转卦名（取模8）"""
    n = number % 8
    if n == 0:
        n = 8
    return NUMBER_TO_GUA[n]


# ==================== 梅花易数 ====================

def meihua_by_time(dt: datetime = None) -> Hexagram:
    """
    梅花易数 - 时间起卦法
    
    上卦：年月日之和 ÷ 8
    下卦：年月日时之和 ÷ 8
    动爻：年月日时之和 ÷ 6
    
    Args:
        dt: 日期时间，默认当前时间
    
    Returns:
        卦象
    """
    if dt is None:
        dt = datetime.now()
    
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    
    # 计算上卦
    upper_sum = year + month + day
    upper_gua = _number_to_gua(upper_sum)
    
    # 计算下卦
    lower_sum = year + month + day + hour
    lower_gua = _number_to_gua(lower_sum)
    
    # 计算动爻
    dong_yao = (year + month + day + hour) % 6
    if dong_yao == 0:
        dong_yao = 6
    
    # 生成六爻
    yaos = _generate_yaos(upper_gua, lower_gua, dong_yao)
    
    return Hexagram(upper_gua, lower_gua, yaos, dong_yao)


def meihua_by_numbers(number1: int, number2: int) -> Hexagram:
    """
    梅花易数 - 数字起卦法
    
    Args:
        number1: 第一个数字（上卦）
        number2: 第二个数字（下卦）
    
    Returns:
        卦象
    """
    upper_gua = _number_to_gua(number1)
    lower_gua = _number_to_gua(number2)
    
    # 动爻
    dong_yao = (number1 + number2) % 6
    if dong_yao == 0:
        dong_yao = 6
    
    yaos = _generate_yaos(upper_gua, lower_gua, dong_yao)
    
    return Hexagram(upper_gua, lower_gua, yaos, dong_yao)


def meihua_by_text(text: str) -> Hexagram:
    """
    梅花易数 - 文字起卦法
    
    Args:
        text: 任意文字
    
    Returns:
        卦象
    """
    # 根据文字长度和字符计算
    text_len = len(text)
    char_sum = sum(ord(c) for c in text)
    
    # 上卦：文字长度
    upper_gua = _number_to_gua(text_len)
    
    # 下卦：字符和
    lower_gua = _number_to_gua(char_sum)
    
    # 动爻
    dong_yao = (text_len + char_sum) % 6
    if dong_yao == 0:
        dong_yao = 6
    
    yaos = _generate_yaos(upper_gua, lower_gua, dong_yao)
    
    return Hexagram(upper_gua, lower_gua, yaos, dong_yao)


def _generate_yaos(upper_gua: str, lower_gua: str, dong_yao: int) -> List[Yao]:
    """生成六爻"""
    upper_trigram = BAGUA[upper_gua]["trigram"]
    lower_trigram = BAGUA[lower_gua]["trigram"]
    
    yaos = []
    
    # 下卦（爻1-3）
    for i, bit in enumerate(reversed(lower_trigram)):
        pos = i + 1
        yao_type = YaoType.YANG if bit == "1" else YaoType.YIN
        if pos == dong_yao:
            yao_type = YaoType.YANG_DONG if bit == "1" else YaoType.YIN_DONG
        yaos.append(Yao(pos, yao_type, pos == dong_yao))
    
    # 上卦（爻4-6）
    for i, bit in enumerate(reversed(upper_trigram)):
        pos = i + 4
        yao_type = YaoType.YANG if bit == "1" else YaoType.YIN
        if pos == dong_yao:
            yao_type = YaoType.YANG_DONG if bit == "1" else YaoType.YIN_DONG
        yaos.append(Yao(pos, yao_type, pos == dong_yao))
    
    return yaos


# ==================== 六爻 ====================

def liuyao_by_coins() -> Hexagram:
    """
    六爻 - 摇钱起卦法（模拟）
    
    三枚铜钱摇六次
    两正一反：少阳 ———
    两反一正：少阴 — —
    三正：老阴 — — → ——— (动)
    三反：老阳 ——— → — — (动)
    
    Returns:
        卦象
    """
    yaos = []
    dong_yao = None
    
    for pos in range(1, 7):
        # 模拟三枚铜钱（0=反，1=正）
        coins = [random.randint(0, 1) for _ in range(3)]
        coin_sum = sum(coins)
        
        if coin_sum == 3:  # 三正 - 老阴
            yao_type = YaoType.YIN_DONG
            is_dong = True
            if dong_yao is None:
                dong_yao = pos
        elif coin_sum == 0:  # 三反 - 老阳
            yao_type = YaoType.YANG_DONG
            is_dong = True
            if dong_yao is None:
                dong_yao = pos
        elif coin_sum == 2:  # 两正一反 - 少阳
            yao_type = YaoType.YANG
            is_dong = False
        else:  # 两反一正 - 少阴
            yao_type = YaoType.YIN
            is_dong = False
        
        yaos.append(Yao(pos, yao_type, is_dong))
    
    # 计算上下卦
    lower_binary = "".join("1" if y.yao_type in [YaoType.YANG, YaoType.YANG_DONG] else "0" 
                           for y in yaos[:3])
    upper_binary = "".join("1" if y.yao_type in [YaoType.YANG, YaoType.YANG_DONG] else "0" 
                           for y in yaos[3:])
    
    lower_gua = _binary_to_gua(lower_binary)
    upper_gua = _binary_to_gua(upper_binary)
    
    return Hexagram(upper_gua, lower_gua, yaos, dong_yao)


def liuyao_by_random() -> Hexagram:
    """
    六爻 - 随机起卦法
    
    Returns:
        卦象
    """
    return liuyao_by_coins()


# ==================== 卦象分析 ====================

def analyze_hexagram(hexagram: Hexagram, question: str = "") -> Dict:
    """
    分析卦象
    
    Args:
        hexagram: 卦象
        question: 问题（可选）
    
    Returns:
        分析结果
    """
    main_interp = hexagram.get_interpretation()
    
    result = {
        "question": question,
        "main_gua": {
            "name": hexagram.name,
            "upper": {
                "name": hexagram.upper_gua,
                "symbol": BAGUA[hexagram.upper_gua]["symbol"],
                "element": BAGUA[hexagram.upper_gua]["element"],
                "nature": BAGUA[hexagram.upper_gua]["nature"]
            },
            "lower": {
                "name": hexagram.lower_gua,
                "symbol": BAGUA[hexagram.lower_gua]["symbol"],
                "element": BAGUA[hexagram.lower_gua]["element"],
                "nature": BAGUA[hexagram.lower_gua]["nature"]
            },
            "interpretation": main_interp
        },
        "yaos": [
            {
                "position": yao.position,
                "type": yao.yao_type.value,
                "symbol": yao.symbol,
                "is_dong": yao.is_dong
            }
            for yao in hexagram.yaos
        ],
        "dong_yao": hexagram.dong_yao,
        "dong_yao_meaning": _get_dong_yao_meaning(hexagram.dong_yao) if hexagram.dong_yao else None,
        "changed_gua": None,
        "overall_fortune": _calculate_overall_fortune(hexagram)
    }
    
    # 变卦分析
    changed = hexagram.changed_hexagram
    if changed:
        changed_interp = changed.get_interpretation()
        result["changed_gua"] = {
            "name": changed.name,
            "interpretation": changed_interp
        }
    
    return result


def _get_dong_yao_meaning(position: int) -> str:
    """获取动爻含义"""
    meanings = {
        1: "初爻动，事情刚开始，需打好基础",
        2: "二爻动，事情正在进行，需坚持努力",
        3: "三爻动，事情到了转折点，需谨慎决断",
        4: "四爻动，事情接近成功，需防小人阻碍",
        5: "五爻动，事情将成，贵人相助",
        6: "上爻动，事情到了极点，需防物极必反"
    }
    return meanings.get(position, "")


def _calculate_overall_fortune(hexagram: Hexagram) -> Dict:
    """计算综合运势"""
    upper_element = BAGUA[hexagram.upper_gua]["element"]
    lower_element = BAGUA[hexagram.lower_gua]["element"]
    
    # 五行生克关系
    sheng_ke = {
        ("木", "火"): "生", ("火", "土"): "生", ("土", "金"): "生",
        ("金", "水"): "生", ("水", "木"): "生",
        ("木", "土"): "克", ("土", "水"): "克", ("水", "火"): "克",
        ("火", "金"): "克", ("金", "木"): "克"
    }
    
    relation = sheng_ke.get((lower_element, upper_element), "比")
    
    if relation == "生":
        fortune_level = "吉"
        description = "下卦生上卦，内助外成，事业顺遂"
    elif relation == "克":
        fortune_level = "凶"
        description = "下卦克上卦，内外不和，需谨慎行事"
    else:
        fortune_level = "平"
        description = "上下卦五行相比，平稳发展"
    
    # 有变卦时的调整
    if hexagram.dong_yao:
        changed = hexagram.changed_hexagram
        if changed:
            changed_upper_element = BAGUA[changed.upper_gua]["element"]
            changed_relation = sheng_ke.get((lower_element, changed_upper_element), "比")
            
            if fortune_level == "凶" and changed_relation == "生":
                fortune_level = "先凶后吉"
                description += "，但有转机"
            elif fortune_level == "吉" and changed_relation == "克":
                fortune_level = "先吉后凶"
                description += "，需防变故"
    
    return {
        "level": fortune_level,
        "description": description,
        "upper_element": upper_element,
        "lower_element": lower_element,
        "relation": relation
    }


def divine(question: str = "", method: str = "time") -> Dict:
    """
    占卜入口函数
    
    Args:
        question: 问题
        method: 起卦方法 (time/random/coins)
    
    Returns:
        占卜结果
    """
    if method == "time":
        hexagram = meihua_by_time()
    elif method == "coins":
        hexagram = liuyao_by_coins()
    else:
        hexagram = liuyao_by_random()
    
    return analyze_hexagram(hexagram, question)


if __name__ == "__main__":
    # 测试梅花易数
    print("=== 梅花易数（时间起卦）===")
    hex1 = meihua_by_time()
    result1 = analyze_hexagram(hex1, "今日运势如何？")
    print(f"卦名: {result1['main_gua']['name']}")
    print(f"动爻: 第{result1['dong_yao']}爻")
    print(f"卦象: {result1['main_gua']['interpretation']['summary']}")
    print(f"运势: {result1['overall_fortune']['level']}")
    
    print("\n=== 六爻（摇钱起卦）===")
    hex2 = liuyao_by_coins()
    result2 = analyze_hexagram(hex2, "事业发展如何？")
    print(f"卦名: {result2['main_gua']['name']}")
    print(f"动爻: 第{result2['dong_yao']}爻" if result2['dong_yao'] else "无动爻")
    if result2['changed_gua']:
        print(f"变卦: {result2['changed_gua']['name']}")
    print(f"运势: {result2['overall_fortune']['level']}")
