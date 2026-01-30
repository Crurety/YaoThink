"""
玄心理命 - 八字核心算法模块
农历/公历转换、干支计算
"""

from datetime import datetime, date
from typing import Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# 天干
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 地支
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 地支对应生肖
SHENGXIAO = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

# 天干五行属性
TIAN_GAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

# 地支五行属性
DI_ZHI_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

# 地支藏干
DI_ZHI_CANG_GAN = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"]
}

# 天干五行阴阳
TIAN_GAN_YINYANG = {
    "甲": "阳", "乙": "阴",
    "丙": "阳", "丁": "阴",
    "戊": "阳", "己": "阴",
    "庚": "阳", "辛": "阴",
    "壬": "阳", "癸": "阴"
}

# 地支五行阴阳
DI_ZHI_YINYANG = {
    "子": "阳", "丑": "阴", "寅": "阳", "卯": "阴",
    "辰": "阳", "巳": "阴", "午": "阳", "未": "阴",
    "申": "阳", "酉": "阴", "戌": "阳", "亥": "阴"
}

# 节气数据 (月份, 日期范围)
# 每月两个节气，前一个为节，后一个为气
JIE_QI = {
    1: [("小寒", 5, 7), ("大寒", 20, 21)],
    2: [("立春", 3, 5), ("雨水", 18, 20)],
    3: [("惊蛰", 5, 7), ("春分", 20, 22)],
    4: [("清明", 4, 6), ("谷雨", 19, 21)],
    5: [("立夏", 5, 7), ("小满", 20, 22)],
    6: [("芒种", 5, 7), ("夏至", 21, 22)],
    7: [("小暑", 6, 8), ("大暑", 22, 24)],
    8: [("立秋", 7, 9), ("处暑", 22, 24)],
    9: [("白露", 7, 9), ("秋分", 22, 24)],
    10: [("寒露", 8, 9), ("霜降", 23, 24)],
    11: [("立冬", 7, 8), ("小雪", 22, 23)],
    12: [("大雪", 6, 8), ("冬至", 21, 23)]
}

# 月份节气对应的月柱地支
# 以立春为正月（寅月）起点
JIE_QI_MONTH_ZHI = {
    "立春": "寅", "惊蛰": "卯", "清明": "辰", "立夏": "巳",
    "芒种": "午", "小暑": "未", "立秋": "申", "白露": "酉",
    "寒露": "戌", "立冬": "亥", "大雪": "子", "小寒": "丑"
}


class WuXing(Enum):
    """五行枚举"""
    MU = "木"
    HUO = "火"
    TU = "土"
    JIN = "金"
    SHUI = "水"


@dataclass
class GanZhi:
    """干支组合"""
    gan: str  # 天干
    zhi: str  # 地支
    
    def __str__(self) -> str:
        return f"{self.gan}{self.zhi}"
    
    @property
    def wuxing_gan(self) -> str:
        """天干五行"""
        return TIAN_GAN_WUXING[self.gan]
    
    @property
    def wuxing_zhi(self) -> str:
        """地支五行"""
        return DI_ZHI_WUXING[self.zhi]
    
    @property
    def cang_gan(self) -> list:
        """地支藏干"""
        return DI_ZHI_CANG_GAN[self.zhi]
    
    @property
    def nayin(self) -> str:
        """纳音五行"""
        return get_nayin(self.gan, self.zhi)


# 六十甲子纳音表
NAYIN_TABLE = {
    ("甲子", "乙丑"): "海中金", ("丙寅", "丁卯"): "炉中火",
    ("戊辰", "己巳"): "大林木", ("庚午", "辛未"): "路旁土",
    ("壬申", "癸酉"): "剑锋金", ("甲戌", "乙亥"): "山头火",
    ("丙子", "丁丑"): "涧下水", ("戊寅", "己卯"): "城头土",
    ("庚辰", "辛巳"): "白蜡金", ("壬午", "癸未"): "杨柳木",
    ("甲申", "乙酉"): "泉中水", ("丙戌", "丁亥"): "屋上土",
    ("戊子", "己丑"): "霹雳火", ("庚寅", "辛卯"): "松柏木",
    ("壬辰", "癸巳"): "长流水", ("甲午", "乙未"): "沙中金",
    ("丙申", "丁酉"): "山下火", ("戊戌", "己亥"): "平地木",
    ("庚子", "辛丑"): "壁上土", ("壬寅", "癸卯"): "金箔金",
    ("甲辰", "乙巳"): "覆灯火", ("丙午", "丁未"): "天河水",
    ("戊申", "己酉"): "大驿土", ("庚戌", "辛亥"): "钗钏金",
    ("壬子", "癸丑"): "桑柘木", ("甲寅", "乙卯"): "大溪水",
    ("丙辰", "丁巳"): "沙中土", ("戊午", "己未"): "天上火",
    ("庚申", "辛酉"): "石榴木", ("壬戌", "癸亥"): "大海水"
}


def get_nayin(gan: str, zhi: str) -> str:
    """获取纳音五行"""
    ganzhi = f"{gan}{zhi}"
    for pair, nayin in NAYIN_TABLE.items():
        if ganzhi in pair:
            return nayin
    return ""


def get_year_ganzhi(year: int) -> GanZhi:
    """
    计算年柱干支
    以立春为年的分界点
    
    Args:
        year: 公历年份
    
    Returns:
        年柱干支
    """
    # 天干：(年份-4) % 10
    gan_index = (year - 4) % 10
    # 地支：(年份-4) % 12
    zhi_index = (year - 4) % 12
    
    return GanZhi(TIAN_GAN[gan_index], DI_ZHI[zhi_index])


def get_month_ganzhi(year: int, month: int, day: int) -> GanZhi:
    """
    计算月柱干支
    根据节气确定月份
    
    Args:
        year: 公历年份
        month: 公历月份
        day: 公历日
    
    Returns:
        月柱干支
    """
    # 确定节气月份
    jie_qi_month = _get_jieqi_month(month, day)
    
    # 确定年干
    year_gan = get_year_ganzhi(year).gan
    year_gan_index = TIAN_GAN.index(year_gan)
    
    # 月干计算规则（五虎遁）:
    # 甲己之年丙作首，乙庚之岁戊为头
    # 丙辛必定寻庚起，丁壬壬位顺行流
    # 戊癸之年何方发，甲寅之上好追求
    month_gan_start = {
        0: 2,  # 甲年起丙寅
        5: 2,  # 己年起丙寅
        1: 4,  # 乙年起戊寅
        6: 4,  # 庚年起戊寅
        2: 6,  # 丙年起庚寅
        7: 6,  # 辛年起庚寅
        3: 8,  # 丁年起壬寅
        8: 8,  # 壬年起壬寅
        4: 0,  # 戊年起甲寅
        9: 0   # 癸年起甲寅
    }
    
    start_gan = month_gan_start[year_gan_index]
    # 月份从寅月(1)开始，到丑月(12)
    gan_index = (start_gan + jie_qi_month - 1) % 10
    zhi_index = (jie_qi_month + 1) % 12  # 寅月为index 2
    
    return GanZhi(TIAN_GAN[gan_index], DI_ZHI[zhi_index])


def _get_jieqi_month(month: int, day: int) -> int:
    """根据节气确定农历月份(1-12，1为寅月)"""
    # 简化版：使用固定节气日期
    jie_dates = {
        1: 6, 2: 4, 3: 6, 4: 5, 5: 6, 6: 6,
        7: 7, 8: 8, 9: 8, 10: 8, 11: 7, 12: 7
    }
    
    if month == 1:
        if day < jie_dates[1]:
            return 12  # 丑月
        else:
            return 12  # 还是丑月（小寒后）
    elif month == 2:
        if day < jie_dates[2]:
            return 12  # 丑月
        else:
            return 1   # 寅月（立春后）
    else:
        if day < jie_dates[month]:
            return month - 1
        else:
            return month
    
    return month


def get_day_ganzhi(year: int, month: int, day: int) -> GanZhi:
    """
    计算日柱干支
    使用基准日计算法
    
    Args:
        year: 公历年份
        month: 公历月份
        day: 公历日
    
    Returns:
        日柱干支
    """
    # 基准日：1900年1月1日为甲戌日（干0，支10）
    base_date = date(1900, 1, 1)
    target_date = date(year, month, day)
    
    delta = (target_date - base_date).days
    
    # 1900年1月1日的干支序号
    base_gan = 0   # 甲
    base_zhi = 10  # 戌
    
    gan_index = (base_gan + delta) % 10
    zhi_index = (base_zhi + delta) % 12
    
    return GanZhi(TIAN_GAN[gan_index], DI_ZHI[zhi_index])


def get_hour_ganzhi(day_gan: str, hour: int) -> GanZhi:
    """
    计算时柱干支
    
    Args:
        day_gan: 日干
        hour: 24小时制的小时数
    
    Returns:
        时柱干支
    """
    # 地支时辰对应（23-1点为子时）
    hour_zhi_map = {
        (23, 24): 0, (0, 1): 0,    # 子时
        (1, 3): 1,                  # 丑时
        (3, 5): 2,                  # 寅时
        (5, 7): 3,                  # 卯时
        (7, 9): 4,                  # 辰时
        (9, 11): 5,                 # 巳时
        (11, 13): 6,                # 午时
        (13, 15): 7,                # 未时
        (15, 17): 8,                # 申时
        (17, 19): 9,                # 酉时
        (19, 21): 10,               # 戌时
        (21, 23): 11                # 亥时
    }
    
    # 确定时辰地支
    zhi_index = 0
    for (start, end), idx in hour_zhi_map.items():
        if start <= hour < end or (start == 23 and hour >= 23):
            zhi_index = idx
            break
    
    # 时干计算规则（五鼠遁）:
    # 甲己还加甲，乙庚丙作初
    # 丙辛从戊起，丁壬庚子居
    # 戊癸何方发，壬子是真途
    day_gan_index = TIAN_GAN.index(day_gan)
    hour_gan_start = {
        0: 0,  # 甲日起甲子
        5: 0,  # 己日起甲子
        1: 2,  # 乙日起丙子
        6: 2,  # 庚日起丙子
        2: 4,  # 丙日起戊子
        7: 4,  # 辛日起戊子
        3: 6,  # 丁日起庚子
        8: 6,  # 壬日起庚子
        4: 8,  # 戊日起壬子
        9: 8   # 癸日起壬子
    }
    
    start_gan = hour_gan_start[day_gan_index]
    gan_index = (start_gan + zhi_index) % 10
    
    return GanZhi(TIAN_GAN[gan_index], DI_ZHI[zhi_index])


def get_shengxiao(year: int) -> str:
    """获取生肖"""
    year_zhi = get_year_ganzhi(year).zhi
    zhi_index = DI_ZHI.index(year_zhi)
    return SHENGXIAO[zhi_index]


@dataclass
class SiZhu:
    """四柱八字"""
    year: GanZhi    # 年柱
    month: GanZhi   # 月柱
    day: GanZhi     # 日柱
    hour: GanZhi    # 时柱
    
    @property
    def bazi(self) -> str:
        """八字字符串"""
        return f"{self.year} {self.month} {self.day} {self.hour}"
    
    @property
    def day_master(self) -> str:
        """日主（日干）"""
        return self.day.gan
    
    def get_all_gan(self) -> list:
        """获取四柱所有天干"""
        return [self.year.gan, self.month.gan, self.day.gan, self.hour.gan]
    
    def get_all_zhi(self) -> list:
        """获取四柱所有地支"""
        return [self.year.zhi, self.month.zhi, self.day.zhi, self.hour.zhi]
    
    def get_all_cang_gan(self) -> dict:
        """获取所有地支藏干"""
        return {
            "年支": self.year.cang_gan,
            "月支": self.month.cang_gan,
            "日支": self.day.cang_gan,
            "时支": self.hour.cang_gan
        }


def calculate_sizhu(year: int, month: int, day: int, hour: int) -> SiZhu:
    """
    计算四柱八字
    
    Args:
        year: 公历年份
        month: 公历月份
        day: 公历日
        hour: 24小时制的小时数
    
    Returns:
        四柱八字对象
    """
    year_gz = get_year_ganzhi(year)
    month_gz = get_month_ganzhi(year, month, day)
    day_gz = get_day_ganzhi(year, month, day)
    hour_gz = get_hour_ganzhi(day_gz.gan, hour)
    
    return SiZhu(year_gz, month_gz, day_gz, hour_gz)


# 农历转换相关
try:
    from lunarcalendar import Converter, Solar, Lunar
    
    def solar_to_lunar(year: int, month: int, day: int) -> Tuple[int, int, int, bool]:
        """
        公历转农历
        
        Returns:
            (农历年, 农历月, 农历日, 是否闰月)
        """
        solar = Solar(year, month, day)
        lunar = Converter.Solar2Lunar(solar)
        return (lunar.year, lunar.month, lunar.day, lunar.isleap)
    
    def lunar_to_solar(year: int, month: int, day: int, is_leap: bool = False) -> Tuple[int, int, int]:
        """
        农历转公历
        
        Returns:
            (公历年, 公历月, 公历日)
        """
        lunar = Lunar(year, month, day, is_leap)
        solar = Converter.Lunar2Solar(lunar)
        return (solar.year, solar.month, solar.day)

except ImportError:
    # 如果没有安装lunarcalendar，提供简化版本
    def solar_to_lunar(year: int, month: int, day: int) -> Tuple[int, int, int, bool]:
        """公历转农历（需要安装lunarcalendar）"""
        raise NotImplementedError("请安装lunarcalendar: pip install lunarcalendar")
    
    def lunar_to_solar(year: int, month: int, day: int, is_leap: bool = False) -> Tuple[int, int, int]:
        """农历转公历（需要安装lunarcalendar）"""
        raise NotImplementedError("请安装lunarcalendar: pip install lunarcalendar")


if __name__ == "__main__":
    # 测试示例
    test_year, test_month, test_day, test_hour = 1990, 5, 15, 10
    
    sizhu = calculate_sizhu(test_year, test_month, test_day, test_hour)
    print(f"出生时间: {test_year}年{test_month}月{test_day}日 {test_hour}时")
    print(f"八字: {sizhu.bazi}")
    print(f"日主: {sizhu.day_master}")
    print(f"生肖: {get_shengxiao(test_year)}")
    print(f"藏干: {sizhu.get_all_cang_gan()}")
