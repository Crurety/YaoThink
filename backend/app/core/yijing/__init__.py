"""
玄心理命 - 易经占卜模块
"""

from .hexagram import (
    # 常量
    BAGUA, NUMBER_TO_GUA, GUA_TO_NUMBER,
    SIXTY_FOUR_GUA, GUA_INTERPRETATIONS,
    
    # 枚举类
    YaoType,
    
    # 数据类
    Yao, Hexagram,
    
    # 梅花易数基础
    meihua_by_time,
    meihua_by_numbers,
    meihua_by_text,
    
    # 六爻基础
    liuyao_by_coins,
    liuyao_by_random,
    
    # 分析函数
    analyze_hexagram,
    divine
)

# 梅花易数高级算法
from .meihua_advanced import (
    # 更多起卦方法
    meihua_by_direction,
    meihua_by_color,
    meihua_by_sound,
    
    # 互卦、错卦、综卦
    get_hugua,
    get_cuogua,
    get_zonggua,
    
    # 高级分析
    analyze_meihua,
    calculate_yingqi
)

# 六爻高级算法
from .liuyao_advanced import (
    # 六亲
    LiuQin,
    get_liuqin,
    
    # 六神
    LiuShen,
    get_liushen,
    
    # 世应
    get_shi_ying,
    SHIYAO_TABLE,
    
    # 纳甲
    NAJIA_TABLE,
    get_yao_dizhi,
    
    # 高级数据结构
    LiuYaoYao,
    LiuYaoGua,
    create_liuyao_gua,
    
    # 用神
    YONGSHEN_MAPPING,
    find_yongshen,
    
    # 综合分析
    analyze_liuyao
)


def divine_meihua(question: str = "", method: str = "time", **kwargs) -> dict:
    """
    梅花易数占卜（高级版）
    
    Args:
        question: 问题
        method: 起卦方法 (time/numbers/text/direction/color/sound)
        **kwargs: 起卦参数
    
    Returns:
        占卜结果
    """
    if method == "time":
        hexagram = meihua_by_time(kwargs.get("dt"))
    elif method == "numbers":
        hexagram = meihua_by_numbers(kwargs.get("num1", 1), kwargs.get("num2", 2))
    elif method == "text":
        hexagram = meihua_by_text(kwargs.get("text", ""))
    elif method == "direction":
        hexagram = meihua_by_direction(kwargs.get("direction", "东"), kwargs.get("dt"))
    elif method == "color":
        hexagram = meihua_by_color(kwargs.get("color", "红"), kwargs.get("dt"))
    elif method == "sound":
        hexagram = meihua_by_sound(kwargs.get("count", 3), kwargs.get("dt"))
    else:
        hexagram = meihua_by_time()
    
    # 使用高级分析
    result = analyze_meihua(hexagram, question)
    result["yingqi"] = calculate_yingqi(hexagram)
    
    return result


def divine_liuyao(question: str = "", question_type: str = "问事业", day_gan: str = "甲") -> dict:
    """
    六爻占卜（高级版）
    
    Args:
        question: 问题
        question_type: 问题类型
        day_gan: 日干（用于起六神）
    
    Returns:
        占卜结果
    """
    # 摇卦
    hexagram = liuyao_by_coins()
    
    # 创建完整六爻
    liuyao_gua = create_liuyao_gua(hexagram, day_gan)
    
    # 分析
    result = analyze_liuyao(liuyao_gua, question, question_type)
    
    return result


__all__ = [
    # 常量
    "BAGUA", "SIXTY_FOUR_GUA", "GUA_INTERPRETATIONS",
    "SHIYAO_TABLE", "NAJIA_TABLE", "YONGSHEN_MAPPING",
    
    # 类型
    "YaoType", "Yao", "Hexagram",
    "LiuQin", "LiuShen", "LiuYaoYao", "LiuYaoGua",
    
    # 梅花易数
    "meihua_by_time", "meihua_by_numbers", "meihua_by_text",
    "meihua_by_direction", "meihua_by_color", "meihua_by_sound",
    "get_hugua", "get_cuogua", "get_zonggua",
    "analyze_meihua", "calculate_yingqi",
    
    # 六爻
    "liuyao_by_coins", "liuyao_by_random",
    "get_liuqin", "get_liushen", "get_shi_ying", "get_yao_dizhi",
    "create_liuyao_gua", "find_yongshen", "analyze_liuyao",
    
    # 高级占卜入口
    "divine_meihua", "divine_liuyao",
    
    # 基础分析
    "analyze_hexagram", "divine"
]
