"""
玄心理命 - 大运流年模块
大运计算、流年分析、运势预测
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import date
from enum import Enum

from .calendar import (
    SiZhu, GanZhi, TIAN_GAN, DI_ZHI,
    TIAN_GAN_WUXING, DI_ZHI_WUXING,
    TIAN_GAN_YINYANG, get_year_ganzhi
)
from .wuxing import (
    calculate_wuxing_score, get_xi_yong_shen,
    WUXING_SHENG, WUXING_KE
)
from .shishen import get_shishen, SHISHEN_TRAITS


class Gender(Enum):
    """性别"""
    MALE = "男"
    FEMALE = "女"


@dataclass
class DaYun:
    """大运"""
    order: int          # 顺序（第几步大运）
    start_age: int      # 起运年龄
    end_age: int        # 结束年龄
    ganzhi: GanZhi      # 大运干支
    shishen_gan: str    # 天干十神
    shishen_zhi: str    # 地支藏干主气十神
    
    def __str__(self) -> str:
        return f"{self.order}运({self.start_age}-{self.end_age}岁): {self.ganzhi}"


@dataclass
class LiuNian:
    """流年"""
    year: int           # 公历年份
    age: int            # 虚岁
    ganzhi: GanZhi      # 流年干支
    shishen_gan: str    # 天干十神
    shishen_zhi: str    # 地支藏干主气十神
    rating: str         # 运势评级
    
    def __str__(self) -> str:
        return f"{self.year}年({self.age}岁): {self.ganzhi} [{self.rating}]"


def calculate_qiyun_age(sizhu: SiZhu, gender: Gender, birth_year: int, birth_month: int, birth_day: int) -> int:
    """
    计算起运年龄
    
    规则：
    - 阳年男命、阴年女命：顺行大运
    - 阴年男命、阳年女命：逆行大运
    - 从出生日起数到下一个（或上一个）节气的天数，三天为一岁
    
    Args:
        sizhu: 四柱八字
        gender: 性别
        birth_year, birth_month, birth_day: 出生日期
    
    Returns:
        起运年龄
    """
    year_gan = sizhu.year.gan
    year_yinyang = TIAN_GAN_YINYANG[year_gan]
    
    # 判断顺逆
    if (year_yinyang == "阳" and gender == Gender.MALE) or \
       (year_yinyang == "阴" and gender == Gender.FEMALE):
        is_forward = True   # 顺行
    else:
        is_forward = False  # 逆行
    
    # 简化计算：使用固定节气日期估算
    # 实际应精确计算到下一个/上一个节气的天数
    jie_dates = {
        1: 6, 2: 4, 3: 6, 4: 5, 5: 6, 6: 6,
        7: 7, 8: 8, 9: 8, 10: 8, 11: 7, 12: 7
    }
    
    if is_forward:
        # 顺行：数到下一个节气
        if birth_month == 12:
            next_jie_day = jie_dates[1]
            days_to_jie = (31 - birth_day) + next_jie_day
        else:
            next_jie_day = jie_dates[birth_month + 1]
            days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            days_to_jie = (days_in_month[birth_month] - birth_day) + next_jie_day
    else:
        # 逆行：数到上一个节气
        current_jie_day = jie_dates[birth_month]
        if birth_day >= current_jie_day:
            days_to_jie = birth_day - current_jie_day
        else:
            if birth_month == 1:
                prev_jie_day = jie_dates[12]
                days_to_jie = birth_day + (31 - prev_jie_day)
            else:
                prev_jie_day = jie_dates[birth_month - 1]
                days_in_prev = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                days_to_jie = birth_day + (days_in_prev[birth_month - 1] - prev_jie_day)
    
    # 三天为一岁，不足三天按四舍五入
    qiyun_age = round(days_to_jie / 3)
    if qiyun_age < 1:
        qiyun_age = 1
    if qiyun_age > 10:
        qiyun_age = 10
    
    return qiyun_age, is_forward


def calculate_dayun(sizhu: SiZhu, gender: Gender, birth_year: int, birth_month: int, birth_day: int, count: int = 8) -> List[DaYun]:
    """
    计算大运
    
    Args:
        sizhu: 四柱八字
        gender: 性别
        birth_year, birth_month, birth_day: 出生日期
        count: 计算多少步大运
    
    Returns:
        大运列表
    """
    qiyun_age, is_forward = calculate_qiyun_age(sizhu, gender, birth_year, birth_month, birth_day)
    
    day_master = sizhu.day_master
    month_gan_idx = TIAN_GAN.index(sizhu.month.gan)
    month_zhi_idx = DI_ZHI.index(sizhu.month.zhi)
    
    dayun_list = []
    
    for i in range(count):
        if is_forward:
            # 顺行：月柱往后推
            gan_idx = (month_gan_idx + i + 1) % 10
            zhi_idx = (month_zhi_idx + i + 1) % 12
        else:
            # 逆行：月柱往前推
            gan_idx = (month_gan_idx - i - 1) % 10
            zhi_idx = (month_zhi_idx - i - 1) % 12
        
        ganzhi = GanZhi(TIAN_GAN[gan_idx], DI_ZHI[zhi_idx])
        
        # 计算十神
        shishen_gan = get_shishen(day_master, ganzhi.gan)
        from .calendar import DI_ZHI_CANG_GAN
        main_canggan = DI_ZHI_CANG_GAN[ganzhi.zhi][0]
        shishen_zhi = get_shishen(day_master, main_canggan)
        
        start_age = qiyun_age + i * 10
        end_age = start_age + 9
        
        dayun_list.append(DaYun(
            order=i + 1,
            start_age=start_age,
            end_age=end_age,
            ganzhi=ganzhi,
            shishen_gan=shishen_gan,
            shishen_zhi=shishen_zhi
        ))
    
    return dayun_list


def calculate_liunian(sizhu: SiZhu, birth_year: int, start_year: int, count: int = 10) -> List[LiuNian]:
    """
    计算流年
    
    Args:
        sizhu: 四柱八字
        birth_year: 出生年份
        start_year: 起始年份
        count: 计算多少年
    
    Returns:
        流年列表
    """
    day_master = sizhu.day_master
    xi_yong = get_xi_yong_shen(sizhu)
    yong_shen = xi_yong.get("yong_shen", [])
    xi_shen = xi_yong.get("xi_shen", [])
    ji_shen = xi_yong.get("ji_shen", [])
    
    liunian_list = []
    
    for i in range(count):
        year = start_year + i
        age = year - birth_year + 1  # 虚岁
        
        ganzhi = get_year_ganzhi(year)
        
        # 计算十神
        shishen_gan = get_shishen(day_master, ganzhi.gan)
        from .calendar import DI_ZHI_CANG_GAN
        main_canggan = DI_ZHI_CANG_GAN[ganzhi.zhi][0]
        shishen_zhi = get_shishen(day_master, main_canggan)
        
        # 评估流年运势
        rating = _rate_liunian(ganzhi, yong_shen, xi_shen, ji_shen)
        
        liunian_list.append(LiuNian(
            year=year,
            age=age,
            ganzhi=ganzhi,
            shishen_gan=shishen_gan,
            shishen_zhi=shishen_zhi,
            rating=rating
        ))
    
    return liunian_list


def _rate_liunian(ganzhi: GanZhi, yong_shen: List[str], xi_shen: List[str], ji_shen: List[str]) -> str:
    """评估流年运势"""
    gan_wuxing = TIAN_GAN_WUXING[ganzhi.gan]
    zhi_wuxing = DI_ZHI_WUXING[ganzhi.zhi]
    
    score = 0
    
    # 天干评分
    if gan_wuxing in yong_shen:
        score += 3
    elif gan_wuxing in xi_shen:
        score += 2
    elif gan_wuxing in ji_shen:
        score -= 2
    
    # 地支评分
    if zhi_wuxing in yong_shen:
        score += 2
    elif zhi_wuxing in xi_shen:
        score += 1
    elif zhi_wuxing in ji_shen:
        score -= 1
    
    if score >= 4:
        return "大吉"
    elif score >= 2:
        return "吉"
    elif score >= 0:
        return "平"
    elif score >= -2:
        return "凶"
    else:
        return "大凶"


def get_current_dayun(dayun_list: List[DaYun], current_age: int) -> DaYun:
    """获取当前所在大运"""
    for dayun in dayun_list:
        if dayun.start_age <= current_age <= dayun.end_age:
            return dayun
    return dayun_list[-1] if dayun_list else None


def analyze_dayun_liunian(sizhu: SiZhu, gender: Gender, 
                          birth_year: int, birth_month: int, birth_day: int,
                          target_year: int = None) -> Dict:
    """
    综合分析大运流年
    
    Args:
        sizhu: 四柱八字
        gender: 性别
        birth_year, birth_month, birth_day: 出生日期
        target_year: 目标年份（默认当年）
    
    Returns:
        大运流年分析结果
    """
    if target_year is None:
        target_year = date.today().year
    
    current_age = target_year - birth_year + 1
    
    # 计算大运
    dayun_list = calculate_dayun(sizhu, gender, birth_year, birth_month, birth_day)
    current_dayun = get_current_dayun(dayun_list, current_age)
    
    # 计算流年（前后5年）
    liunian_list = calculate_liunian(sizhu, birth_year, target_year - 2, 10)
    current_liunian = next((ln for ln in liunian_list if ln.year == target_year), None)
    
    # 大运流年组合分析
    combined_analysis = None
    if current_dayun and current_liunian:
        combined_analysis = _analyze_dayun_liunian_combination(
            sizhu, current_dayun, current_liunian
        )
    
    return {
        "birth_info": {
            "year": birth_year,
            "month": birth_month,
            "day": birth_day,
            "gender": gender.value
        },
        "current_age": current_age,
        "dayun_list": [
            {
                "order": dy.order,
                "range": f"{dy.start_age}-{dy.end_age}岁",
                "ganzhi": str(dy.ganzhi),
                "shishen": f"{dy.shishen_gan}/{dy.shishen_zhi}",
                "is_current": dy == current_dayun
            }
            for dy in dayun_list
        ],
        "current_dayun": {
            "ganzhi": str(current_dayun.ganzhi) if current_dayun else None,
            "shishen": f"{current_dayun.shishen_gan}/{current_dayun.shishen_zhi}" if current_dayun else None,
            "interpretation": _interpret_dayun(current_dayun) if current_dayun else None
        },
        "liunian_list": [
            {
                "year": ln.year,
                "age": ln.age,
                "ganzhi": str(ln.ganzhi),
                "shishen": f"{ln.shishen_gan}/{ln.shishen_zhi}",
                "rating": ln.rating,
                "is_current": ln.year == target_year
            }
            for ln in liunian_list
        ],
        "current_liunian": {
            "year": current_liunian.year if current_liunian else None,
            "ganzhi": str(current_liunian.ganzhi) if current_liunian else None,
            "rating": current_liunian.rating if current_liunian else None,
            "interpretation": _interpret_liunian(current_liunian) if current_liunian else None
        },
        "combined_analysis": combined_analysis
    }


def _interpret_dayun(dayun: DaYun) -> str:
    """解读大运"""
    traits = SHISHEN_TRAITS.get(dayun.shishen_gan, {})
    keywords = traits.get("keywords", [])
    positive = traits.get("positive", "")
    
    return f"此步大运{dayun.ganzhi}，天干透出{dayun.shishen_gan}星。" \
           f"关键词：{'、'.join(keywords)}。{positive[:30]}..."


def _interpret_liunian(liunian: LiuNian) -> str:
    """解读流年"""
    rating_desc = {
        "大吉": "运势极佳，宜积极进取",
        "吉": "运势良好，稳中求进",
        "平": "运势平稳，宜守不宜攻",
        "凶": "运势欠佳，宜谨慎行事",
        "大凶": "运势不佳，宜韬光养晦"
    }
    
    traits = SHISHEN_TRAITS.get(liunian.shishen_gan, {})
    keywords = traits.get("keywords", [])
    
    return f"{liunian.year}年{liunian.ganzhi}年，{liunian.shishen_gan}星当值。" \
           f"运势评级：{liunian.rating}。{rating_desc.get(liunian.rating, '')}。" \
           f"关键词：{'、'.join(keywords[:3])}。"


def _analyze_dayun_liunian_combination(sizhu: SiZhu, dayun: DaYun, liunian: LiuNian) -> Dict:
    """分析大运流年组合"""
    # 大运流年天干关系
    dy_gan_wx = TIAN_GAN_WUXING[dayun.ganzhi.gan]
    ln_gan_wx = TIAN_GAN_WUXING[liunian.ganzhi.gan]
    
    if dy_gan_wx == ln_gan_wx:
        gan_relation = "比和"
        gan_desc = "大运流年天干比和，力量加强"
    elif WUXING_SHENG.get(dy_gan_wx) == ln_gan_wx:
        gan_relation = "大运生流年"
        gan_desc = "大运生流年，有贵人相助"
    elif WUXING_SHENG.get(ln_gan_wx) == dy_gan_wx:
        gan_relation = "流年生大运"
        gan_desc = "流年生大运，顺势而为"
    elif WUXING_KE.get(dy_gan_wx) == ln_gan_wx:
        gan_relation = "大运克流年"
        gan_desc = "大运克流年，主动出击"
    elif WUXING_KE.get(ln_gan_wx) == dy_gan_wx:
        gan_relation = "流年克大运"
        gan_desc = "流年克大运，有压力挑战"
    else:
        gan_relation = "其他"
        gan_desc = ""
    
    # 综合评价
    if liunian.rating in ["大吉", "吉"] and gan_relation in ["比和", "大运生流年", "流年生大运"]:
        overall = "上上"
        advice = "此年运势绝佳，宜大展宏图，把握机会"
    elif liunian.rating in ["大吉", "吉"]:
        overall = "上"
        advice = "此年运势良好，积极进取可有所成"
    elif liunian.rating == "平":
        overall = "中"
        advice = "此年运势平稳，宜稳扎稳打，不宜冒进"
    else:
        overall = "下"
        advice = "此年运势欠佳，宜韬光养晦，等待时机"
    
    return {
        "dayun_ganzhi": str(dayun.ganzhi),
        "liunian_ganzhi": str(liunian.ganzhi),
        "gan_relation": gan_relation,
        "gan_description": gan_desc,
        "overall_rating": overall,
        "advice": advice
    }


if __name__ == "__main__":
    from .calendar import calculate_sizhu
    
    # 测试示例
    birth_year, birth_month, birth_day = 1990, 5, 15
    sizhu = calculate_sizhu(birth_year, birth_month, birth_day, 10)
    gender = Gender.MALE
    
    print(f"八字: {sizhu.bazi}")
    print(f"性别: {gender.value}")
    
    # 大运流年分析
    result = analyze_dayun_liunian(sizhu, gender, birth_year, birth_month, birth_day)
    
    print(f"\n当前年龄: {result['current_age']}岁")
    print(f"\n大运列表:")
    for dy in result['dayun_list']:
        mark = "◆" if dy['is_current'] else " "
        print(f"  {mark} {dy['order']}运 {dy['range']}: {dy['ganzhi']} ({dy['shishen']})")
    
    print(f"\n当前大运解读:")
    print(f"  {result['current_dayun']['interpretation']}")
    
    print(f"\n流年列表:")
    for ln in result['liunian_list']:
        mark = "◆" if ln['is_current'] else " "
        print(f"  {mark} {ln['year']}年({ln['age']}岁): {ln['ganzhi']} [{ln['rating']}]")
    
    print(f"\n当前流年解读:")
    print(f"  {result['current_liunian']['interpretation']}")
    
    print(f"\n大运流年组合分析:")
    if result['combined_analysis']:
        print(f"  {result['combined_analysis']['gan_description']}")
        print(f"  综合评级: {result['combined_analysis']['overall_rating']}")
        print(f"  建议: {result['combined_analysis']['advice']}")
