"""
玄心理命 - 紫微斗数模块
命宫定位、十二宫排列、星曜安排
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


# 十二宫位名称
TWELVE_PALACES = [
    "命宫", "兄弟宫", "夫妻宫", "子女宫", "财帛宫", "疾厄宫",
    "迁移宫", "仆役宫", "官禄宫", "田宅宫", "福德宫", "父母宫"
]

# 地支顺序
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 天干
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]


class StarType(Enum):
    """星曜类型"""
    ZHUXING = "主星"      # 十四主星
    JIXING = "吉星"       # 吉星
    SHAXING = "煞星"      # 煞星
    HUAXING = "化星"      # 四化星
    FUXING = "辅星"       # 辅佐星
    ZAXING = "杂曜"       # 杂曜


@dataclass
class Star:
    """星曜"""
    name: str                   # 星名
    star_type: StarType         # 星曜类型
    brightness: str = ""        # 亮度（庙旺得利平闲陷）
    hua: str = ""               # 四化（禄权科忌）
    description: str = ""       # 描述
    
    def __str__(self) -> str:
        result = self.name
        if self.brightness:
            result += f"({self.brightness})"
        if self.hua:
            result += f"化{self.hua}"
        return result


@dataclass
class Palace:
    """宫位"""
    name: str                           # 宫位名称
    dizhi: str                          # 所在地支
    tiangan: str = ""                   # 宫干
    stars: List[Star] = field(default_factory=list)  # 宫内星曜
    
    def __str__(self) -> str:
        return f"{self.name}({self.dizhi})"
    
    def get_main_stars(self) -> List[Star]:
        """获取主星"""
        return [s for s in self.stars if s.star_type == StarType.ZHUXING]
    
    def get_auxiliary_stars(self) -> List[Star]:
        """获取辅星"""
        return [s for s in self.stars if s.star_type in [StarType.JIXING, StarType.FUXING]]
    
    def get_sha_stars(self) -> List[Star]:
        """获取煞星"""
        return [s for s in self.stars if s.star_type == StarType.SHAXING]


# 十四主星
FOURTEEN_MAIN_STARS = [
    "紫微", "天机", "太阳", "武曲", "天同", "廉贞", "天府",
    "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军"
]

# 主星特性
MAIN_STAR_TRAITS = {
    "紫微": {
        "element": "土",
        "yin_yang": "阴",
        "keywords": ["领导", "尊贵", "权威", "骄傲"],
        "positive": "领导力强，有气度，受人尊敬，志向远大",
        "negative": "高傲自大，好面子，固执己见",
        "career": "适合管理、政治、大企业领导"
    },
    "天机": {
        "element": "木",
        "yin_yang": "阴",
        "keywords": ["智慧", "谋略", "变化", "敏感"],
        "positive": "聪明机智，善于谋划，反应敏捷，多才多艺",
        "negative": "想法多变，优柔寡断，过于敏感",
        "career": "适合策划、咨询、技术研发"
    },
    "太阳": {
        "element": "火",
        "yin_yang": "阳",
        "keywords": ["光明", "博爱", "热情", "奔波"],
        "positive": "热情开朗，乐于助人，有正义感，人缘好",
        "negative": "操心劳碌，付出多回报少，易招小人",
        "career": "适合公职、教育、慈善、外交"
    },
    "武曲": {
        "element": "金",
        "yin_yang": "阴",
        "keywords": ["财富", "刚毅", "果断", "孤独"],
        "positive": "意志坚定，理财能力强，果断干练，事业心强",
        "negative": "性格刚硬，缺乏情趣，过于现实",
        "career": "适合金融、财务、军警、运动"
    },
    "天同": {
        "element": "水",
        "yin_yang": "阳",
        "keywords": ["福气", "温和", "享受", "懒散"],
        "positive": "性格温和，有福气，人缘好，懂得享受",
        "negative": "意志不坚，贪图安逸，缺乏进取心",
        "career": "适合艺术、服务、休闲娱乐行业"
    },
    "廉贞": {
        "element": "火",
        "yin_yang": "阴",
        "keywords": ["桃花", "才艺", "复杂", "争斗"],
        "positive": "才艺出众，有魅力，适应力强，敢于竞争",
        "negative": "感情复杂，易招是非，心机较重",
        "career": "适合法律、艺术、公关、商业"
    },
    "天府": {
        "element": "土",
        "yin_yang": "阳",
        "keywords": ["稳重", "财库", "保守", "厚重"],
        "positive": "稳重踏实，有财运，包容力强，值得信赖",
        "negative": "过于保守，缺乏冲劲，固步自封",
        "career": "适合财务、行政、仓储物流"
    },
    "太阴": {
        "element": "水",
        "yin_yang": "阴",
        "keywords": ["细腻", "财富", "母性", "阴柔"],
        "positive": "心思细腻，有财运，温柔体贴，有艺术气质",
        "negative": "多愁善感，过于被动，缺乏魄力",
        "career": "适合艺术、设计、金融、教育"
    },
    "贪狼": {
        "element": "木",
        "yin_yang": "阳",
        "keywords": ["欲望", "才艺", "桃花", "多变"],
        "positive": "多才多艺，交际能力强，有艺术天赋，魅力十足",
        "negative": "欲望强烈，感情多变，贪心不足",
        "career": "适合艺术、娱乐、销售、公关"
    },
    "巨门": {
        "element": "水",
        "yin_yang": "阴",
        "keywords": ["口才", "是非", "分析", "怀疑"],
        "positive": "口才出众，分析能力强，适合研究，有洞察力",
        "negative": "多疑猜忌，口舌是非，人际关系差",
        "career": "适合律师、教师、研究、评论"
    },
    "天相": {
        "element": "水",
        "yin_yang": "阳",
        "keywords": ["辅佐", "正直", "印星", "依赖"],
        "positive": "为人正直，乐于助人，适合辅佐他人，有贵人运",
        "negative": "缺乏主见，过于依赖，缺少魄力",
        "career": "适合秘书、助理、行政、服务"
    },
    "天梁": {
        "element": "土",
        "yin_yang": "阳",
        "keywords": ["长寿", "化解", "老成", "清高"],
        "positive": "德高望重，有化解灾厄的能力，适合医疗宗教",
        "negative": "过于清高，不善交际，喜欢说教",
        "career": "适合医疗、宗教、慈善、顾问"
    },
    "七杀": {
        "element": "金",
        "yin_yang": "阴",
        "keywords": ["权威", "孤独", "开创", "冲动"],
        "positive": "开创力强，有魄力，敢于冒险，领导能力强",
        "negative": "性格暴躁，孤独无助，冲动冒险",
        "career": "适合军警、创业、外科、竞技"
    },
    "破军": {
        "element": "水",
        "yin_yang": "阴",
        "keywords": ["变动", "破坏", "创新", "不安"],
        "positive": "敢于突破，创新能力强，适应变化，不安于现状",
        "negative": "破坏力强，人生起伏大，难以安定",
        "career": "适合创业、研发、变革、探险"
    }
}

# 辅佐吉星
AUXILIARY_STARS = {
    "左辅": {"type": StarType.JIXING, "description": "贵人相助，增强主星力量"},
    "右弼": {"type": StarType.JIXING, "description": "贵人相助，增强主星力量"},
    "文昌": {"type": StarType.JIXING, "description": "主聪明好学，考试运佳"},
    "文曲": {"type": StarType.JIXING, "description": "主才艺文采，异性缘佳"},
    "天魁": {"type": StarType.JIXING, "description": "阳贵人，主贵人相助"},
    "天钺": {"type": StarType.JIXING, "description": "阴贵人，主贵人相助"},
    "禄存": {"type": StarType.JIXING, "description": "主财禄，有稳定财运"},
    "天马": {"type": StarType.JIXING, "description": "主奔波走动，利外出发展"}
}

# 六煞星
SHA_STARS = {
    "擎羊": {"type": StarType.SHAXING, "description": "主刚强暴躁，易有意外"},
    "陀罗": {"type": StarType.SHAXING, "description": "主拖延纠缠，做事反复"},
    "火星": {"type": StarType.SHAXING, "description": "主冲动暴躁，性急易怒"},
    "铃星": {"type": StarType.SHAXING, "description": "主阴暗不安，心绪不宁"},
    "地空": {"type": StarType.SHAXING, "description": "主空想虚幻，财来财去"},
    "地劫": {"type": StarType.SHAXING, "description": "主劫财破败，突发变故"}
}


def calculate_ming_gong(lunar_month: int, birth_hour_zhi_index: int) -> int:
    """
    计算命宫位置
    
    命宫口诀：寅起正月，逆数生月，顺数生时
    
    Args:
        lunar_month: 农历月份 (1-12)
        birth_hour_zhi_index: 出生时辰地支索引 (0-11, 0=子时)
    
    Returns:
        命宫地支索引 (0-11)
    """
    # 从寅宫起正月，逆数生月
    # 寅的索引是2
    base = 2  # 寅
    
    # 逆数生月（月份从1开始）
    month_position = (base - (lunar_month - 1)) % 12
    
    # 从月位起子时，顺数到生时
    ming_gong_index = (month_position + birth_hour_zhi_index) % 12
    
    return ming_gong_index


def calculate_shen_gong(lunar_month: int, birth_hour_zhi_index: int) -> int:
    """
    计算身宫位置
    
    身宫口诀：寅起正月，顺数生月，逆数生时
    
    Args:
        lunar_month: 农历月份 (1-12)
        birth_hour_zhi_index: 出生时辰地支索引 (0-11)
    
    Returns:
        身宫地支索引 (0-11)
    """
    base = 2  # 寅
    
    # 顺数生月
    month_position = (base + (lunar_month - 1)) % 12
    
    # 逆数生时
    shen_gong_index = (month_position - birth_hour_zhi_index) % 12
    
    return shen_gong_index


def arrange_twelve_palaces(ming_gong_index: int) -> List[Palace]:
    """
    排列十二宫
    
    Args:
        ming_gong_index: 命宫地支索引
    
    Returns:
        十二宫列表
    """
    palaces = []
    
    for i, palace_name in enumerate(TWELVE_PALACES):
        # 从命宫起，逆时针排列
        dizhi_index = (ming_gong_index - i) % 12
        palace = Palace(
            name=palace_name,
            dizhi=DI_ZHI[dizhi_index]
        )
        palaces.append(palace)
    
    return palaces


def calculate_wuhu_index(year_gan: str) -> int:
    """
    根据年干计算五虎遁起始天干索引
    
    Args:
        year_gan: 年干
    
    Returns:
        寅宫天干索引
    """
    # 五虎遁口诀
    wuhu_map = {
        "甲": 2, "己": 2,   # 甲己之年丙作首
        "乙": 4, "庚": 4,   # 乙庚之岁戊为头
        "丙": 6, "辛": 6,   # 丙辛必定寻庚起
        "丁": 8, "壬": 8,   # 丁壬壬位顺行流
        "戊": 0, "癸": 0    # 戊癸之年何方发，甲寅之上好追求
    }
    return wuhu_map.get(year_gan, 0)


def set_palace_tiangan(palaces: List[Palace], year_gan: str) -> None:
    """
    设置各宫天干（宫干）
    
    Args:
        palaces: 十二宫列表
        year_gan: 年干
    """
    # 计算寅宫天干索引
    yin_gan_index = calculate_wuhu_index(year_gan)
    
    for palace in palaces:
        dizhi_index = DI_ZHI.index(palace.dizhi)
        # 从寅宫起始天干，顺数到该宫位置
        gan_offset = (dizhi_index - 2) % 12  # 寅是索引2
        gan_index = (yin_gan_index + gan_offset) % 10
        palace.tiangan = TIAN_GAN[gan_index]


# 紫微星安星表（根据五行局和日数）
# 简化版：使用水二局的安星规则
def calculate_ziwei_position(wuxing_ju: int, lunar_day: int) -> int:
    """
    计算紫微星位置
    
    Args:
        wuxing_ju: 五行局数 (2/3/4/5/6)
        lunar_day: 农历日
    
    Returns:
        紫微星地支索引
    """
    # 简化算法：根据五行局和日数计算
    # 实际紫微斗数有复杂的安星表
    
    # 计算商和余数
    quotient = lunar_day // wuxing_ju
    remainder = lunar_day % wuxing_ju
    
    # 基础位置计算
    if remainder == 0:
        base_position = quotient - 1
    else:
        base_position = quotient
    
    # 根据余数调整
    # 余数奇偶决定顺逆
    if remainder == 0:
        position = base_position
    elif remainder % 2 == 1:  # 奇数余数，顺数
        position = base_position + remainder
    else:  # 偶数余数，逆数
        position = base_position - remainder + wuxing_ju
    
    return position % 12


def calculate_wuxing_ju(ming_gong_dizhi: str, year_gan: str) -> Tuple[str, int]:
    """
    计算五行局
    
    根据命宫纳音五行确定五行局
    
    Args:
        ming_gong_dizhi: 命宫地支
        year_gan: 年干
    
    Returns:
        (五行局名称, 局数)
    """
    # 简化版：根据命宫地支和年干确定
    # 实际应根据命宫干支的纳音五行
    
    # 先计算命宫天干
    yin_gan_index = calculate_wuhu_index(year_gan)
    ming_gong_dizhi_index = DI_ZHI.index(ming_gong_dizhi)
    gan_offset = (ming_gong_dizhi_index - 2) % 12
    ming_gong_gan_index = (yin_gan_index + gan_offset) % 10
    ming_gong_gan = TIAN_GAN[ming_gong_gan_index]
    
    # 纳音五行简化表（60甲子纳音）
    # 这里用简化规则
    nayin_table = {
        ("甲", "子"): "金", ("乙", "丑"): "金",
        ("丙", "寅"): "火", ("丁", "卯"): "火",
        ("戊", "辰"): "木", ("己", "巳"): "木",
        ("庚", "午"): "土", ("辛", "未"): "土",
        ("壬", "申"): "金", ("癸", "酉"): "金",
        ("甲", "戌"): "火", ("乙", "亥"): "火",
    }
    
    # 五行局对应
    ju_mapping = {
        "水": ("水二局", 2),
        "木": ("木三局", 3),
        "金": ("金四局", 4),
        "土": ("土五局", 5),
        "火": ("火六局", 6)
    }
    
    # 简化：根据命宫地支确定
    dizhi_wuxing = {
        "子": "水", "丑": "土", "寅": "木", "卯": "木",
        "辰": "土", "巳": "火", "午": "火", "未": "土",
        "申": "金", "酉": "金", "戌": "土", "亥": "水"
    }
    
    wuxing = dizhi_wuxing.get(ming_gong_dizhi, "水")
    return ju_mapping.get(wuxing, ("水二局", 2))


def arrange_main_stars(palaces: List[Palace], ziwei_position: int) -> None:
    """
    排列十四主星
    
    Args:
        palaces: 十二宫列表
        ziwei_position: 紫微星地支索引
    """
    # 主星相对紫微的位置关系（简化版）
    # 紫微星系列
    ziwei_group = {
        "紫微": 0,
        "天机": -1,  # 紫微逆1
        "太阳": -3,  # 紫微逆3
        "武曲": -4,  # 紫微逆4
        "天同": -5,  # 紫微逆5
        "廉贞": -8   # 紫微逆8
    }
    
    # 天府星系列（天府与紫微对宫）
    tianfu_position = (12 - ziwei_position) % 12
    tianfu_group = {
        "天府": 0,
        "太阴": 1,
        "贪狼": 2,
        "巨门": 3,
        "天相": 4,
        "天梁": 5,
        "七杀": 6,
        "破军": 10
    }
    
    # 安排紫微星系
    for star_name, offset in ziwei_group.items():
        position = (ziwei_position + offset) % 12
        # 找到对应地支的宫位
        for palace in palaces:
            if DI_ZHI.index(palace.dizhi) == position:
                star = Star(
                    name=star_name,
                    star_type=StarType.ZHUXING,
                    description=MAIN_STAR_TRAITS.get(star_name, {}).get("positive", "")
                )
                palace.stars.append(star)
                break
    
    # 安排天府星系
    for star_name, offset in tianfu_group.items():
        position = (tianfu_position + offset) % 12
        for palace in palaces:
            if DI_ZHI.index(palace.dizhi) == position:
                star = Star(
                    name=star_name,
                    star_type=StarType.ZHUXING,
                    description=MAIN_STAR_TRAITS.get(star_name, {}).get("positive", "")
                )
                palace.stars.append(star)
                break


def arrange_auxiliary_stars(palaces: List[Palace], year_gan: str, year_zhi: str,
                           lunar_month: int, birth_hour_zhi_index: int) -> None:
    """
    排列辅佐吉星
    
    Args:
        palaces: 十二宫列表
        year_gan: 年干
        year_zhi: 年支
        lunar_month: 农历月份
        birth_hour_zhi_index: 出生时辰地支索引
    """
    # 左辅：辰上起正月，顺数至生月
    zuofu_position = (4 + lunar_month - 1) % 12  # 辰=4
    
    # 右弼：戌上起正月，逆数至生月
    youbi_position = (10 - lunar_month + 1) % 12  # 戌=10
    
    # 文昌：以生时起巳，逆数至生时
    wenchang_position = (5 - birth_hour_zhi_index) % 12  # 巳=5
    
    # 文曲：以生时起酉，顺数至生时
    wenqu_position = (9 + birth_hour_zhi_index) % 12  # 酉=9
    
    aux_positions = {
        "左辅": zuofu_position,
        "右弼": youbi_position,
        "文昌": wenchang_position,
        "文曲": wenqu_position
    }
    
    for star_name, position in aux_positions.items():
        for palace in palaces:
            if DI_ZHI.index(palace.dizhi) == position:
                star = Star(
                    name=star_name,
                    star_type=StarType.JIXING,
                    description=AUXILIARY_STARS.get(star_name, {}).get("description", "")
                )
                palace.stars.append(star)
                break


def arrange_sha_stars(palaces: List[Palace], year_zhi: str, birth_hour_zhi_index: int) -> None:
    """
    排列六煞星
    
    Args:
        palaces: 十二宫列表
        year_zhi: 年支
        birth_hour_zhi_index: 出生时辰地支索引
    """
    year_zhi_index = DI_ZHI.index(year_zhi)
    
    # 擎羊、陀罗：以年干定位（简化处理）
    # 火星、铃星：以年支定位
    
    # 火星安星表（简化）
    huoxing_table = {
        "寅": 1, "午": 1, "戌": 1,  # 丑
        "申": 3, "子": 3, "辰": 3,  # 卯
        "巳": 4, "酉": 4, "丑": 4,  # 辰
        "亥": 9, "卯": 9, "未": 9   # 酉
    }
    
    huoxing_base = huoxing_table.get(year_zhi, 0)
    huoxing_position = (huoxing_base + birth_hour_zhi_index) % 12
    
    # 铃星安星表（简化）
    lingxing_table = {
        "寅": 3, "午": 3, "戌": 3,  # 卯
        "申": 10, "子": 10, "辰": 10,  # 戌
        "巳": 10, "酉": 10, "丑": 10,  # 戌
        "亥": 10, "卯": 10, "未": 10   # 戌
    }
    
    lingxing_base = lingxing_table.get(year_zhi, 0)
    lingxing_position = (lingxing_base + birth_hour_zhi_index) % 12
    
    sha_positions = {
        "火星": huoxing_position,
        "铃星": lingxing_position
    }
    
    for star_name, position in sha_positions.items():
        for palace in palaces:
            if DI_ZHI.index(palace.dizhi) == position:
                star = Star(
                    name=star_name,
                    star_type=StarType.SHAXING,
                    description=SHA_STARS.get(star_name, {}).get("description", "")
                )
                palace.stars.append(star)
                break


@dataclass
class ZiWeiChart:
    """紫微斗数命盘"""
    palaces: List[Palace]               # 十二宫
    ming_gong_index: int                # 命宫索引
    shen_gong_index: int                # 身宫索引
    wuxing_ju: str                      # 五行局
    ju_number: int                      # 局数
    birth_info: Dict                    # 出生信息
    
    def get_palace_by_name(self, name: str) -> Optional[Palace]:
        """根据名称获取宫位"""
        for palace in self.palaces:
            if palace.name == name:
                return palace
        return None
    
    def get_ming_gong(self) -> Palace:
        """获取命宫"""
        return self.get_palace_by_name("命宫")
    
    def get_career_palace(self) -> Palace:
        """获取官禄宫（事业宫）"""
        return self.get_palace_by_name("官禄宫")
    
    def get_wealth_palace(self) -> Palace:
        """获取财帛宫"""
        return self.get_palace_by_name("财帛宫")
    
    def get_marriage_palace(self) -> Palace:
        """获取夫妻宫"""
        return self.get_palace_by_name("夫妻宫")


def create_ziwei_chart(year_gan: str, year_zhi: str, 
                       lunar_month: int, lunar_day: int,
                       birth_hour_zhi: str) -> ZiWeiChart:
    """
    创建紫微斗数命盘
    
    Args:
        year_gan: 年干
        year_zhi: 年支
        lunar_month: 农历月份 (1-12)
        lunar_day: 农历日 (1-30)
        birth_hour_zhi: 出生时辰地支
    
    Returns:
        紫微斗数命盘
    """
    birth_hour_zhi_index = DI_ZHI.index(birth_hour_zhi)
    
    # 1. 计算命宫位置
    ming_gong_index = calculate_ming_gong(lunar_month, birth_hour_zhi_index)
    
    # 2. 计算身宫位置
    shen_gong_index = calculate_shen_gong(lunar_month, birth_hour_zhi_index)
    
    # 3. 排列十二宫
    palaces = arrange_twelve_palaces(ming_gong_index)
    
    # 4. 设置宫干
    set_palace_tiangan(palaces, year_gan)
    
    # 5. 计算五行局
    ming_gong_dizhi = DI_ZHI[ming_gong_index]
    wuxing_ju, ju_number = calculate_wuxing_ju(ming_gong_dizhi, year_gan)
    
    # 6. 计算紫微星位置
    ziwei_position = calculate_ziwei_position(ju_number, lunar_day)
    
    # 7. 排列主星
    arrange_main_stars(palaces, ziwei_position)
    
    # 8. 排列辅佐吉星
    arrange_auxiliary_stars(palaces, year_gan, year_zhi, lunar_month, birth_hour_zhi_index)
    
    # 9. 排列煞星
    arrange_sha_stars(palaces, year_zhi, birth_hour_zhi_index)
    
    return ZiWeiChart(
        palaces=palaces,
        ming_gong_index=ming_gong_index,
        shen_gong_index=shen_gong_index,
        wuxing_ju=wuxing_ju,
        ju_number=ju_number,
        birth_info={
            "year_gan": year_gan,
            "year_zhi": year_zhi,
            "lunar_month": lunar_month,
            "lunar_day": lunar_day,
            "birth_hour": birth_hour_zhi
        }
    )


def analyze_ziwei_chart(chart: ZiWeiChart) -> Dict:
    """
    分析紫微斗数命盘
    
    Args:
        chart: 紫微斗数命盘
    
    Returns:
        分析结果
    """
    ming_gong = chart.get_ming_gong()
    career_palace = chart.get_career_palace()
    wealth_palace = chart.get_wealth_palace()
    marriage_palace = chart.get_marriage_palace()
    
    # 命宫主星分析
    ming_main_stars = ming_gong.get_main_stars() if ming_gong else []
    ming_analysis = _analyze_palace_stars(ming_main_stars, "命宫")
    
    # 事业分析
    career_stars = career_palace.get_main_stars() if career_palace else []
    career_analysis = _analyze_palace_stars(career_stars, "官禄宫")
    
    # 财运分析
    wealth_stars = wealth_palace.get_main_stars() if wealth_palace else []
    wealth_analysis = _analyze_palace_stars(wealth_stars, "财帛宫")
    
    # 婚姻分析
    marriage_stars = marriage_palace.get_main_stars() if marriage_palace else []
    marriage_analysis = _analyze_palace_stars(marriage_stars, "夫妻宫")
    
    # 格局判断
    pattern = _analyze_pattern(chart)
    
    return {
        "basic_info": {
            "ming_gong": f"{ming_gong.dizhi}宫" if ming_gong else "",
            "shen_gong": f"{DI_ZHI[chart.shen_gong_index]}宫",
            "wuxing_ju": chart.wuxing_ju
        },
        "ming_analysis": ming_analysis,
        "career_analysis": career_analysis,
        "wealth_analysis": wealth_analysis,
        "marriage_analysis": marriage_analysis,
        "pattern": pattern,
        "palaces_detail": [
            {
                "name": p.name,
                "dizhi": p.dizhi,
                "tiangan": p.tiangan,
                "main_stars": [str(s) for s in p.get_main_stars()],
                "aux_stars": [str(s) for s in p.get_auxiliary_stars()],
                "sha_stars": [str(s) for s in p.get_sha_stars()]
            }
            for p in chart.palaces
        ]
    }


def _analyze_palace_stars(stars: List[Star], palace_name: str) -> Dict:
    """分析宫位星曜"""
    if not stars:
        return {
            "main_star": None,
            "description": f"{palace_name}无主星，需看对宫借星",
            "keywords": [],
            "career_hint": ""
        }
    
    main_star = stars[0]
    traits = MAIN_STAR_TRAITS.get(main_star.name, {})
    
    return {
        "main_star": main_star.name,
        "description": traits.get("positive", ""),
        "keywords": traits.get("keywords", []),
        "career_hint": traits.get("career", ""),
        "negative_hint": traits.get("negative", "")
    }


def _analyze_pattern(chart: ZiWeiChart) -> Dict:
    """分析命盘格局"""
    ming_gong = chart.get_ming_gong()
    if not ming_gong:
        return {"name": "普通格局", "description": ""}
    
    main_stars = ming_gong.get_main_stars()
    aux_stars = ming_gong.get_auxiliary_stars()
    sha_stars = ming_gong.get_sha_stars()
    
    star_names = [s.name for s in main_stars]
    aux_names = [s.name for s in aux_stars]
    
    patterns = []
    
    # 紫府同宫
    if "紫微" in star_names and "天府" in star_names:
        patterns.append(("紫府同宫", "帝王之相，大富大贵，领导才能出众"))
    
    # 机月同梁
    if any(s in star_names for s in ["天机", "太阴", "天同", "天梁"]):
        count = sum(1 for s in ["天机", "太阴", "天同", "天梁"] if s in star_names)
        if count >= 2:
            patterns.append(("机月同梁", "适合公职、技术、幕僚工作"))
    
    # 日月同明
    if "太阳" in star_names and "太阴" in star_names:
        patterns.append(("日月同明", "聪明才智，事业财运两全"))
    
    # 杀破狼
    if any(s in star_names for s in ["七杀", "破军", "贪狼"]):
        patterns.append(("杀破狼格", "变动开创，适合冒险创业"))
    
    # 府相朝垣
    if "天府" in star_names or "天相" in star_names:
        patterns.append(("府相朝垣", "财官双美，稳定发展"))
    
    # 辅弼夹命
    if "左辅" in aux_names and "右弼" in aux_names:
        patterns.append(("辅弼夹命", "贵人环绕，事业有成"))
    
    if patterns:
        return {
            "name": patterns[0][0],
            "description": patterns[0][1],
            "all_patterns": patterns
        }
    
    return {"name": "普通格局", "description": "格局中和，稳步发展", "all_patterns": []}


if __name__ == "__main__":
    # 测试示例
    chart = create_ziwei_chart(
        year_gan="庚",
        year_zhi="午",
        lunar_month=5,
        lunar_day=15,
        birth_hour_zhi="巳"
    )
    
    print(f"五行局: {chart.wuxing_ju}")
    print(f"命宫: {DI_ZHI[chart.ming_gong_index]}")
    print(f"身宫: {DI_ZHI[chart.shen_gong_index]}")
    
    print("\n十二宫:")
    for palace in chart.palaces:
        stars = [str(s) for s in palace.stars]
        print(f"  {palace.name}({palace.tiangan}{palace.dizhi}): {', '.join(stars) if stars else '空'}")
    
    print("\n命盘分析:")
    analysis = analyze_ziwei_chart(chart)
    print(f"  命宫主星: {analysis['ming_analysis']['main_star']}")
    print(f"  格局: {analysis['pattern']['name']}")
    print(f"  格局描述: {analysis['pattern']['description']}")
