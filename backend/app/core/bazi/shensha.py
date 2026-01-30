"""
玄心理命 - 神煞模块
神煞判断、吉凶分析
"""

from typing import Dict, List, Set
from dataclasses import dataclass
from enum import Enum

from .calendar import (
    SiZhu, GanZhi, TIAN_GAN, DI_ZHI,
    TIAN_GAN_WUXING, DI_ZHI_WUXING
)


class ShenShaType(Enum):
    """神煞类型"""
    JI = "吉神"      # 吉神
    XIONG = "凶煞"   # 凶煞
    ZHONG = "中性"   # 中性


@dataclass
class ShenSha:
    """神煞"""
    name: str           # 名称
    type: ShenShaType   # 类型
    position: str       # 所在位置
    description: str    # 描述
    influence: str      # 影响


# 天乙贵人查法（以日干查）
TIANYI_GUIREN = {
    "甲": ["丑", "未"], "戊": ["丑", "未"],
    "乙": ["子", "申"], "己": ["子", "申"],
    "丙": ["亥", "酉"], "丁": ["亥", "酉"],
    "庚": ["丑", "未"], "辛": ["寅", "午"],
    "壬": ["卯", "巳"], "癸": ["卯", "巳"]
}

# 文昌贵人查法（以日干查）
WENCHANG_GUIREN = {
    "甲": "巳", "乙": "午", "丙": "申", "丁": "酉",
    "戊": "申", "己": "酉", "庚": "亥", "辛": "子",
    "壬": "寅", "癸": "卯"
}

# 驿马查法（以年支或日支查）
YIMA = {
    "寅": "申", "午": "申", "戌": "申",
    "申": "寅", "子": "寅", "辰": "寅",
    "巳": "亥", "酉": "亥", "丑": "亥",
    "亥": "巳", "卯": "巳", "未": "巳"
}

# 桃花（咸池）查法（以年支或日支查）
TAOHUA = {
    "寅": "卯", "午": "卯", "戌": "卯",
    "申": "酉", "子": "酉", "辰": "酉",
    "巳": "午", "酉": "午", "丑": "午",
    "亥": "子", "卯": "子", "未": "子"
}

# 华盖查法（以年支或日支查）
HUAGAI = {
    "寅": "戌", "午": "戌", "戌": "戌",
    "申": "辰", "子": "辰", "辰": "辰",
    "巳": "丑", "酉": "丑", "丑": "丑",
    "亥": "未", "卯": "未", "未": "未"
}

# 羊刃查法（以日干查）
YANGREN = {
    "甲": "卯", "乙": "寅", "丙": "午", "丁": "巳",
    "戊": "午", "己": "巳", "庚": "酉", "辛": "申",
    "壬": "子", "癸": "亥"
}

# 禄神查法（以日干查）
LUSHEN = {
    "甲": "寅", "乙": "卯", "丙": "巳", "丁": "午",
    "戊": "巳", "己": "午", "庚": "申", "辛": "酉",
    "壬": "亥", "癸": "子"
}

# 将星查法（以年支或日支查）
JIANGXING = {
    "寅": "午", "午": "午", "戌": "午",
    "申": "子", "子": "子", "辰": "子",
    "巳": "酉", "酉": "酉", "丑": "酉",
    "亥": "卯", "卯": "卯", "未": "卯"
}

# 亡神查法（以年支查）
WANGSHEN = {
    "寅": "巳", "午": "巳", "戌": "巳",
    "申": "亥", "子": "亥", "辰": "亥",
    "巳": "申", "酉": "申", "丑": "申",
    "亥": "寅", "卯": "寅", "未": "寅"
}

# 劫煞查法（以年支查）
JIESHA = {
    "寅": "巳", "午": "亥", "戌": "巳",
    "申": "亥", "子": "巳", "辰": "亥",
    "巳": "寅", "酉": "卯", "丑": "戌",
    "亥": "申", "卯": "辰", "未": "辰"
}

# 孤辰寡宿查法（以年支查）
GUCHEN = {
    "寅": "巳", "卯": "巳", "辰": "巳",
    "巳": "申", "午": "申", "未": "申",
    "申": "亥", "酉": "亥", "戌": "亥",
    "亥": "寅", "子": "寅", "丑": "寅"
}

GUASU = {
    "寅": "丑", "卯": "丑", "辰": "丑",
    "巳": "辰", "午": "辰", "未": "辰",
    "申": "未", "酉": "未", "戌": "未",
    "亥": "戌", "子": "戌", "丑": "戌"
}

# 神煞描述
SHENSHA_DESC = {
    "天乙贵人": {
        "type": ShenShaType.JI,
        "description": "天乙贵人是最有力的吉神，主逢凶化吉，遇难呈祥",
        "influence": "一生多得贵人相助，逢凶化吉，事业有成，人缘极佳"
    },
    "文昌贵人": {
        "type": ShenShaType.JI,
        "description": "文昌主聪明才智，学业有成",
        "influence": "聪明好学，考试运佳，适合从事文化教育工作"
    },
    "驿马": {
        "type": ShenShaType.ZHONG,
        "description": "驿马主奔波走动，变迁变动",
        "influence": "一生多奔波劳碌，适合从事外出、物流、旅游等行业"
    },
    "桃花": {
        "type": ShenShaType.ZHONG,
        "description": "桃花主异性缘、社交魅力",
        "influence": "异性缘佳，人缘好，但需注意感情纠纷"
    },
    "华盖": {
        "type": ShenShaType.ZHONG,
        "description": "华盖主孤高、艺术才华、宗教缘",
        "influence": "性格孤独清高，有艺术才华，适合研究神秘学问"
    },
    "羊刃": {
        "type": ShenShaType.XIONG,
        "description": "羊刃主刚强、暴躁、意外",
        "influence": "性格刚强，脾气暴躁，需防意外伤害和血光之灾"
    },
    "禄神": {
        "type": ShenShaType.JI,
        "description": "禄神主财禄、衣食无忧",
        "influence": "一生衣食无忧，财运稳定，不为生计发愁"
    },
    "将星": {
        "type": ShenShaType.JI,
        "description": "将星主权威、领导才能",
        "influence": "有领导才能，适合担任管理职务，受人敬重"
    },
    "亡神": {
        "type": ShenShaType.XIONG,
        "description": "亡神主聪明但易招是非",
        "influence": "聪明伶俐但性格偏激，易招惹是非口舌"
    },
    "劫煞": {
        "type": ShenShaType.XIONG,
        "description": "劫煞主灾祸、意外",
        "influence": "需防突发灾祸和意外事故，宜小心谨慎"
    },
    "孤辰": {
        "type": ShenShaType.XIONG,
        "description": "孤辰主孤独、男命忌",
        "influence": "性格孤僻，婚姻不顺，男命尤忌"
    },
    "寡宿": {
        "type": ShenShaType.XIONG,
        "description": "寡宿主孤寡、女命忌",
        "influence": "性格孤僻，婚姻不顺，女命尤忌"
    }
}


def analyze_shensha(sizhu: SiZhu) -> Dict:
    """
    分析八字神煞
    
    Args:
        sizhu: 四柱八字
    
    Returns:
        神煞分析结果
    """
    day_master = sizhu.day_master
    year_zhi = sizhu.year.zhi
    day_zhi = sizhu.day.zhi
    all_zhi = sizhu.get_all_zhi()
    
    shensha_list = []
    
    # 天乙贵人
    tianyi_zhi = TIANYI_GUIREN.get(day_master, [])
    for zhi in tianyi_zhi:
        if zhi in all_zhi:
            pos = _find_position(sizhu, zhi)
            shensha_list.append(_create_shensha("天乙贵人", pos))
    
    # 文昌贵人
    wenchang_zhi = WENCHANG_GUIREN.get(day_master)
    if wenchang_zhi and wenchang_zhi in all_zhi:
        pos = _find_position(sizhu, wenchang_zhi)
        shensha_list.append(_create_shensha("文昌贵人", pos))
    
    # 驿马（以年支查）
    yima_zhi = YIMA.get(year_zhi)
    if yima_zhi and yima_zhi in all_zhi:
        pos = _find_position(sizhu, yima_zhi)
        shensha_list.append(_create_shensha("驿马", pos))
    
    # 桃花（以年支查）
    taohua_zhi = TAOHUA.get(year_zhi)
    if taohua_zhi and taohua_zhi in all_zhi:
        pos = _find_position(sizhu, taohua_zhi)
        shensha_list.append(_create_shensha("桃花", pos))
    
    # 华盖（以年支查）
    huagai_zhi = HUAGAI.get(year_zhi)
    if huagai_zhi and huagai_zhi in all_zhi:
        pos = _find_position(sizhu, huagai_zhi)
        shensha_list.append(_create_shensha("华盖", pos))
    
    # 羊刃
    yangren_zhi = YANGREN.get(day_master)
    if yangren_zhi and yangren_zhi in all_zhi:
        pos = _find_position(sizhu, yangren_zhi)
        shensha_list.append(_create_shensha("羊刃", pos))
    
    # 禄神
    lushen_zhi = LUSHEN.get(day_master)
    if lushen_zhi and lushen_zhi in all_zhi:
        pos = _find_position(sizhu, lushen_zhi)
        shensha_list.append(_create_shensha("禄神", pos))
    
    # 将星（以年支查）
    jiangxing_zhi = JIANGXING.get(year_zhi)
    if jiangxing_zhi and jiangxing_zhi in all_zhi:
        pos = _find_position(sizhu, jiangxing_zhi)
        shensha_list.append(_create_shensha("将星", pos))
    
    # 孤辰
    guchen_zhi = GUCHEN.get(year_zhi)
    if guchen_zhi and guchen_zhi in all_zhi:
        pos = _find_position(sizhu, guchen_zhi)
        shensha_list.append(_create_shensha("孤辰", pos))
    
    # 寡宿
    guasu_zhi = GUASU.get(year_zhi)
    if guasu_zhi and guasu_zhi in all_zhi:
        pos = _find_position(sizhu, guasu_zhi)
        shensha_list.append(_create_shensha("寡宿", pos))
    
    # 分类统计
    ji_shensha = [s for s in shensha_list if s["type"] == "吉神"]
    xiong_shensha = [s for s in shensha_list if s["type"] == "凶煞"]
    zhong_shensha = [s for s in shensha_list if s["type"] == "中性"]
    
    return {
        "all_shensha": shensha_list,
        "ji_shensha": ji_shensha,
        "xiong_shensha": xiong_shensha,
        "zhong_shensha": zhong_shensha,
        "summary": _generate_shensha_summary(ji_shensha, xiong_shensha, zhong_shensha)
    }


def _find_position(sizhu: SiZhu, zhi: str) -> str:
    """查找地支所在位置"""
    if sizhu.year.zhi == zhi:
        return "年支"
    elif sizhu.month.zhi == zhi:
        return "月支"
    elif sizhu.day.zhi == zhi:
        return "日支"
    elif sizhu.hour.zhi == zhi:
        return "时支"
    return "未知"


def _create_shensha(name: str, position: str) -> Dict:
    """创建神煞对象"""
    desc = SHENSHA_DESC.get(name, {})
    return {
        "name": name,
        "type": desc.get("type", ShenShaType.ZHONG).value,
        "position": position,
        "description": desc.get("description", ""),
        "influence": desc.get("influence", "")
    }


def _generate_shensha_summary(ji: List, xiong: List, zhong: List) -> str:
    """生成神煞总结"""
    summary_parts = []
    
    if ji:
        ji_names = [s["name"] for s in ji]
        summary_parts.append(f"八字带有{len(ji)}个吉神：{'、'.join(ji_names)}，主一生多贵人相助，运势较好。")
    
    if xiong:
        xiong_names = [s["name"] for s in xiong]
        summary_parts.append(f"同时带有{len(xiong)}个凶煞：{'、'.join(xiong_names)}，需注意相关事项。")
    
    if zhong:
        zhong_names = [s["name"] for s in zhong]
        summary_parts.append(f"中性神煞有：{'、'.join(zhong_names)}，影响因人而异。")
    
    if not summary_parts:
        summary_parts.append("八字中无明显神煞。")
    
    return " ".join(summary_parts)


def get_shensha_for_liunian(sizhu: SiZhu, liunian_zhi: str) -> List[Dict]:
    """
    查询流年会遇到的神煞
    
    Args:
        sizhu: 四柱八字
        liunian_zhi: 流年地支
    
    Returns:
        流年神煞列表
    """
    day_master = sizhu.day_master
    year_zhi = sizhu.year.zhi
    
    shensha_list = []
    
    # 检查流年地支是否触发各种神煞
    tianyi_zhi = TIANYI_GUIREN.get(day_master, [])
    if liunian_zhi in tianyi_zhi:
        shensha_list.append(_create_shensha("天乙贵人", "流年"))
    
    if WENCHANG_GUIREN.get(day_master) == liunian_zhi:
        shensha_list.append(_create_shensha("文昌贵人", "流年"))
    
    if YIMA.get(year_zhi) == liunian_zhi:
        shensha_list.append(_create_shensha("驿马", "流年"))
    
    if TAOHUA.get(year_zhi) == liunian_zhi:
        shensha_list.append(_create_shensha("桃花", "流年"))
    
    if YANGREN.get(day_master) == liunian_zhi:
        shensha_list.append(_create_shensha("羊刃", "流年"))
    
    if LUSHEN.get(day_master) == liunian_zhi:
        shensha_list.append(_create_shensha("禄神", "流年"))
    
    return shensha_list


# 六冲
LIU_CHONG = {
    "子": "午", "丑": "未", "寅": "申", "卯": "酉", "辰": "戌", "巳": "亥",
    "午": "子", "未": "丑", "申": "寅", "酉": "卯", "戌": "辰", "亥": "巳"
}

# 六合
LIU_HE = {
    "子": "丑", "丑": "子", "寅": "亥", "卯": "戌", "辰": "酉", "巳": "申",
    "午": "未", "未": "午", "申": "巳", "酉": "辰", "戌": "卯", "亥": "寅"
}

# 三合局
SAN_HE = {
    "申子辰": "水局", "寅午戌": "火局", "巳酉丑": "金局", "亥卯未": "木局"
}

# 三刑
SAN_XING = [
    ("寅", "巳", "申"),  # 无恩之刑
    ("丑", "戌", "未"),  # 恃势之刑
    ("子", "卯"),        # 无礼之刑
    ("辰",), ("午",), ("酉",), ("亥",)  # 自刑
]


def analyze_dizhi_relations(sizhu: SiZhu) -> Dict:
    """
    分析地支关系（冲、合、刑、害）
    
    Args:
        sizhu: 四柱八字
    
    Returns:
        地支关系分析结果
    """
    all_zhi = sizhu.get_all_zhi()
    zhi_positions = ["年支", "月支", "日支", "时支"]
    
    chong_list = []  # 六冲
    he_list = []     # 六合
    sanhe_list = []  # 三合
    xing_list = []   # 三刑
    
    # 检查六冲和六合
    for i, zhi1 in enumerate(all_zhi):
        for j, zhi2 in enumerate(all_zhi):
            if i >= j:
                continue
            
            # 六冲
            if LIU_CHONG.get(zhi1) == zhi2:
                chong_list.append({
                    "zhi1": zhi1,
                    "zhi2": zhi2,
                    "pos1": zhi_positions[i],
                    "pos2": zhi_positions[j],
                    "description": f"{zhi_positions[i]}{zhi1}与{zhi_positions[j]}{zhi2}相冲"
                })
            
            # 六合
            if LIU_HE.get(zhi1) == zhi2:
                he_list.append({
                    "zhi1": zhi1,
                    "zhi2": zhi2,
                    "pos1": zhi_positions[i],
                    "pos2": zhi_positions[j],
                    "description": f"{zhi_positions[i]}{zhi1}与{zhi_positions[j]}{zhi2}相合"
                })
    
    # 检查三合
    zhi_set = set(all_zhi)
    for sanhe_zhi, ju_name in SAN_HE.items():
        sanhe_set = set(sanhe_zhi)
        if sanhe_set.issubset(zhi_set):
            sanhe_list.append({
                "zhi": sanhe_zhi,
                "ju": ju_name,
                "description": f"八字中有{sanhe_zhi}三合{ju_name}"
            })
    
    # 生成总结
    summary = _generate_dizhi_summary(chong_list, he_list, sanhe_list)
    
    return {
        "chong": chong_list,
        "he": he_list,
        "sanhe": sanhe_list,
        "xing": xing_list,
        "summary": summary
    }


def _generate_dizhi_summary(chong: List, he: List, sanhe: List) -> str:
    """生成地支关系总结"""
    parts = []
    
    if sanhe:
        parts.append(f"八字有三合局：{'、'.join([s['ju'] for s in sanhe])}，五行力量加强。")
    
    if he:
        parts.append(f"有六合：{'、'.join([f'{h['zhi1']}{h['zhi2']}' for h in he])}，主和谐贵人。")
    
    if chong:
        parts.append(f"有六冲：{'、'.join([f'{c['zhi1']}{c['zhi2']}' for c in chong])}，主变动不安。")
    
    if not parts:
        parts.append("八字地支关系较为平和。")
    
    return " ".join(parts)


if __name__ == "__main__":
    from .calendar import calculate_sizhu
    
    # 测试示例
    sizhu = calculate_sizhu(1990, 5, 15, 10)
    print(f"八字: {sizhu.bazi}")
    
    # 神煞分析
    shensha = analyze_shensha(sizhu)
    print(f"\n神煞分析:")
    print(f"吉神: {[s['name'] for s in shensha['ji_shensha']]}")
    print(f"凶煞: {[s['name'] for s in shensha['xiong_shensha']]}")
    print(f"中性: {[s['name'] for s in shensha['zhong_shensha']]}")
    print(f"总结: {shensha['summary']}")
    
    # 地支关系
    dizhi = analyze_dizhi_relations(sizhu)
    print(f"\n地支关系:")
    print(f"六冲: {dizhi['chong']}")
    print(f"六合: {dizhi['he']}")
    print(f"三合: {dizhi['sanhe']}")
    print(f"总结: {dizhi['summary']}")
