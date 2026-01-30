"""
玄心理命 - 梅花易数高级算法
多种起卦方法、互卦、错卦、综卦
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import random

from .hexagram import (
    Hexagram, Yao, YaoType, BAGUA, 
    NUMBER_TO_GUA, GUA_TO_NUMBER, SIXTY_FOUR_GUA,
    _number_to_gua, _generate_yaos, _binary_to_gua
)


# ==================== 梅花易数起卦法 ====================

def meihua_by_time(dt: datetime = None) -> Hexagram:
    """
    时间起卦法
    
    上卦：年月日之和 ÷ 8
    下卦：年月日时之和 ÷ 8
    动爻：年月日时之和 ÷ 6
    """
    if dt is None:
        dt = datetime.now()
    
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    
    upper_sum = year + month + day
    upper_gua = _number_to_gua(upper_sum)
    
    lower_sum = year + month + day + hour
    lower_gua = _number_to_gua(lower_sum)
    
    dong_yao = (year + month + day + hour) % 6
    if dong_yao == 0:
        dong_yao = 6
    
    yaos = _generate_yaos(upper_gua, lower_gua, dong_yao)
    return Hexagram(upper_gua, lower_gua, yaos, dong_yao)


def meihua_by_numbers(num1: int, num2: int) -> Hexagram:
    """
    数字起卦法
    
    第一个数定上卦，第二个数定下卦
    两数之和定动爻
    """
    upper_gua = _number_to_gua(num1)
    lower_gua = _number_to_gua(num2)
    
    dong_yao = (num1 + num2) % 6
    if dong_yao == 0:
        dong_yao = 6
    
    yaos = _generate_yaos(upper_gua, lower_gua, dong_yao)
    return Hexagram(upper_gua, lower_gua, yaos, dong_yao)


def meihua_by_text(text: str) -> Hexagram:
    """
    文字起卦法
    
    按字数和笔画计算
    """
    text_len = len(text)
    char_sum = sum(ord(c) for c in text)
    
    upper_gua = _number_to_gua(text_len)
    lower_gua = _number_to_gua(char_sum)
    
    dong_yao = (text_len + char_sum) % 6
    if dong_yao == 0:
        dong_yao = 6
    
    yaos = _generate_yaos(upper_gua, lower_gua, dong_yao)
    return Hexagram(upper_gua, lower_gua, yaos, dong_yao)


def meihua_by_direction(direction: str, dt: datetime = None) -> Hexagram:
    """
    方位起卦法
    
    八方对应八卦
    """
    if dt is None:
        dt = datetime.now()
    
    direction_map = {
        "南": "乾", "东南": "兑", "东": "离", "东北": "震",
        "西南": "巽", "西": "坎", "西北": "艮", "北": "坤"
    }
    
    upper_gua = direction_map.get(direction, "乾")
    
    lower_sum = dt.year + dt.month + dt.day + dt.hour
    lower_gua = _number_to_gua(lower_sum)
    
    dong_yao = (dt.year + dt.month + dt.day + dt.hour) % 6
    if dong_yao == 0:
        dong_yao = 6
    
    yaos = _generate_yaos(upper_gua, lower_gua, dong_yao)
    return Hexagram(upper_gua, lower_gua, yaos, dong_yao)


def meihua_by_color(color: str, dt: datetime = None) -> Hexagram:
    """
    颜色起卦法
    """
    if dt is None:
        dt = datetime.now()
    
    color_map = {
        "红": "离", "橙": "兑", "黄": "坤", "绿": "巽",
        "青": "震", "蓝": "坎", "紫": "艮", "白": "乾"
    }
    
    upper_gua = color_map.get(color, "乾")
    
    lower_sum = dt.year + dt.month + dt.day + dt.hour
    lower_gua = _number_to_gua(lower_sum)
    
    dong_yao = (dt.year + dt.month + dt.day + dt.hour) % 6
    if dong_yao == 0:
        dong_yao = 6
    
    yaos = _generate_yaos(upper_gua, lower_gua, dong_yao)
    return Hexagram(upper_gua, lower_gua, yaos, dong_yao)


def meihua_by_sound(sound_count: int, dt: datetime = None) -> Hexagram:
    """
    声音起卦法（听到几声）
    """
    if dt is None:
        dt = datetime.now()
    
    upper_gua = _number_to_gua(sound_count)
    
    lower_sum = sound_count + dt.hour
    lower_gua = _number_to_gua(lower_sum)
    
    dong_yao = (sound_count + dt.hour) % 6
    if dong_yao == 0:
        dong_yao = 6
    
    yaos = _generate_yaos(upper_gua, lower_gua, dong_yao)
    return Hexagram(upper_gua, lower_gua, yaos, dong_yao)


# ==================== 互卦、错卦、综卦 ====================

def get_hugua(hexagram: Hexagram) -> Hexagram:
    """
    获取互卦
    
    取二三四爻为下卦，三四五爻为上卦
    """
    # 获取六爻的阴阳状态
    yao_states = []
    for yao in hexagram.yaos:
        if yao.yao_type in [YaoType.YANG, YaoType.YANG_DONG]:
            yao_states.append("1")
        else:
            yao_states.append("0")
    
    # 互卦：2,3,4爻为下卦，3,4,5爻为上卦
    lower_binary = "".join(yao_states[1:4])  # 二三四爻
    upper_binary = "".join(yao_states[2:5])  # 三四五爻
    
    lower_gua = _binary_to_gua(lower_binary)
    upper_gua = _binary_to_gua(upper_binary)
    
    yaos = _generate_yaos(upper_gua, lower_gua, None)
    return Hexagram(upper_gua, lower_gua, yaos, None)


def get_cuogua(hexagram: Hexagram) -> Hexagram:
    """
    获取错卦
    
    所有爻阴阳互换
    """
    yao_states = []
    for yao in hexagram.yaos:
        if yao.yao_type in [YaoType.YANG, YaoType.YANG_DONG]:
            yao_states.append("0")  # 阳变阴
        else:
            yao_states.append("1")  # 阴变阳
    
    lower_binary = "".join(yao_states[0:3])
    upper_binary = "".join(yao_states[3:6])
    
    lower_gua = _binary_to_gua(lower_binary)
    upper_gua = _binary_to_gua(upper_binary)
    
    yaos = _generate_yaos(upper_gua, lower_gua, None)
    return Hexagram(upper_gua, lower_gua, yaos, None)


def get_zonggua(hexagram: Hexagram) -> Hexagram:
    """
    获取综卦
    
    将卦颠倒（上下翻转）
    """
    yao_states = []
    for yao in reversed(hexagram.yaos):
        if yao.yao_type in [YaoType.YANG, YaoType.YANG_DONG]:
            yao_states.append("1")
        else:
            yao_states.append("0")
    
    lower_binary = "".join(yao_states[0:3])
    upper_binary = "".join(yao_states[3:6])
    
    lower_gua = _binary_to_gua(lower_binary)
    upper_gua = _binary_to_gua(upper_binary)
    
    yaos = _generate_yaos(upper_gua, lower_gua, None)
    return Hexagram(upper_gua, lower_gua, yaos, None)


# ==================== 梅花易数断卦 ====================

def analyze_meihua(hexagram: Hexagram, question: str = "") -> Dict:
    """
    梅花易数综合分析
    
    包含体用分析、五行生克、互错综卦
    """
    # 确定体用
    dong_yao = hexagram.dong_yao
    
    if dong_yao and dong_yao <= 3:
        ti_gua = hexagram.upper_gua  # 上卦为体
        yong_gua = hexagram.lower_gua  # 下卦为用
        ti_position = "上"
    else:
        ti_gua = hexagram.lower_gua  # 下卦为体
        yong_gua = hexagram.upper_gua  # 上卦为用
        ti_position = "下"
    
    ti_wuxing = BAGUA[ti_gua]["element"]
    yong_wuxing = BAGUA[yong_gua]["element"]
    
    # 体用生克关系
    ti_yong_relation = _analyze_tiyong_relation(ti_wuxing, yong_wuxing)
    
    # 互卦、错卦、综卦
    hugua = get_hugua(hexagram)
    cuogua = get_cuogua(hexagram)
    zonggua = get_zonggua(hexagram)
    
    # 变卦分析
    changed = hexagram.changed_hexagram
    changed_analysis = None
    if changed:
        changed_analysis = {
            "name": changed.name,
            "upper": changed.upper_gua,
            "lower": changed.lower_gua,
            "meaning": _get_changed_meaning(hexagram, changed)
        }
    
    # 综合吉凶判断
    fortune = _calculate_meihua_fortune(hexagram, ti_yong_relation)
    
    return {
        "question": question,
        "main_gua": {
            "name": hexagram.name,
            "upper": hexagram.upper_gua,
            "lower": hexagram.lower_gua
        },
        "tiyong": {
            "ti_gua": ti_gua,
            "ti_wuxing": ti_wuxing,
            "ti_position": ti_position,
            "yong_gua": yong_gua,
            "yong_wuxing": yong_wuxing,
            "relation": ti_yong_relation
        },
        "dong_yao": {
            "position": dong_yao,
            "meaning": _get_dong_yao_analysis(dong_yao)
        },
        "hugua": {
            "name": hugua.name,
            "meaning": "互卦代表事情的内在发展"
        },
        "cuogua": {
            "name": cuogua.name,
            "meaning": "错卦代表事情的对立面"
        },
        "zonggua": {
            "name": zonggua.name,
            "meaning": "综卦代表他人的看法"
        },
        "changed_gua": changed_analysis,
        "fortune": fortune
    }


def _analyze_tiyong_relation(ti_wuxing: str, yong_wuxing: str) -> Dict:
    """分析体用关系"""
    sheng_map = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
    ke_map = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
    
    if ti_wuxing == yong_wuxing:
        relation = "比和"
        meaning = "体用相同，事情平稳"
        fortune = "平"
    elif sheng_map.get(yong_wuxing) == ti_wuxing:
        relation = "用生体"
        meaning = "用卦生体卦，大吉"
        fortune = "大吉"
    elif sheng_map.get(ti_wuxing) == yong_wuxing:
        relation = "体生用"
        meaning = "体卦生用卦，有付出"
        fortune = "小凶"
    elif ke_map.get(yong_wuxing) == ti_wuxing:
        relation = "用克体"
        meaning = "用卦克体卦，不利"
        fortune = "凶"
    elif ke_map.get(ti_wuxing) == yong_wuxing:
        relation = "体克用"
        meaning = "体卦克用卦，有利"
        fortune = "吉"
    else:
        relation = "其他"
        meaning = "需具体分析"
        fortune = "平"
    
    return {
        "relation": relation,
        "meaning": meaning,
        "fortune": fortune
    }


def _get_dong_yao_analysis(dong_yao: int) -> str:
    """动爻位置分析"""
    meanings = {
        1: "初爻动，事情刚起步，基础尚浅",
        2: "二爻动，事情发展中，需把握时机",
        3: "三爻动，事情到转折点，需谨慎决断",
        4: "四爻动，事情进入关键期，近臣位",
        5: "五爻动，事情将成，君位主贵",
        6: "上爻动，事情到极点，物极必反"
    }
    return meanings.get(dong_yao, "")


def _get_changed_meaning(main: Hexagram, changed: Hexagram) -> str:
    """变卦意义"""
    main_name = main.name
    changed_name = changed.name
    
    # 简单的变化判断
    if "乾" in changed_name:
        return "变卦见乾，事情向好发展"
    elif "坤" in changed_name:
        return "变卦见坤，需稳扎稳打"
    elif "坎" in changed_name:
        return "变卦见坎，需防波折"
    elif "离" in changed_name:
        return "变卦见离，光明显现"
    else:
        return f"由{main_name}变为{changed_name}，事情有转变"


def _calculate_meihua_fortune(hexagram: Hexagram, ti_yong_relation: Dict) -> Dict:
    """计算梅花易数综合运势"""
    base_fortune = ti_yong_relation["fortune"]
    
    fortune_scores = {
        "大吉": 90,
        "吉": 75,
        "平": 50,
        "小凶": 35,
        "凶": 20
    }
    
    score = fortune_scores.get(base_fortune, 50)
    
    # 变卦调整
    changed = hexagram.changed_hexagram
    if changed:
        changed_upper_wuxing = BAGUA[changed.upper_gua]["element"]
        changed_lower_wuxing = BAGUA[changed.lower_gua]["element"]
        
        # 变卦五行相生加分
        if changed_upper_wuxing == changed_lower_wuxing:
            score += 5
    
    score = max(0, min(100, score))
    
    if score >= 75:
        level = "吉"
        advice = "事情可行，积极推进"
    elif score >= 50:
        level = "平"
        advice = "事情尚可，需要努力"
    else:
        level = "凶"
        advice = "事情阻碍较多，谨慎行事"
    
    return {
        "score": score,
        "level": level,
        "advice": advice,
        "ti_yong_fortune": base_fortune
    }


# ==================== 应期推断 ====================

def calculate_yingqi(hexagram: Hexagram) -> Dict:
    """
    计算应期（应验时间）
    
    根据卦象五行和动爻判断应期
    """
    upper_element = BAGUA[hexagram.upper_gua]["element"]
    lower_element = BAGUA[hexagram.lower_gua]["element"]
    
    # 五行对应时间
    element_time = {
        "木": {"季节": "春", "月": "寅卯", "日": "甲乙"},
        "火": {"季节": "夏", "月": "巳午", "日": "丙丁"},
        "土": {"季节": "四季末", "月": "辰戌丑未", "日": "戊己"},
        "金": {"季节": "秋", "月": "申酉", "日": "庚辛"},
        "水": {"季节": "冬", "月": "亥子", "日": "壬癸"}
    }
    
    dong_yao = hexagram.dong_yao
    
    if dong_yao:
        # 动爻数可作为时间单位
        time_hint = f"约{dong_yao}个时间单位（天/周/月）"
    else:
        time_hint = "时间较长，需等待时机"
    
    return {
        "upper_element_time": element_time.get(upper_element, {}),
        "lower_element_time": element_time.get(lower_element, {}),
        "time_hint": time_hint,
        "advice": "应期仅供参考，需结合实际情况判断"
    }
