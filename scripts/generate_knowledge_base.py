
import json
import os
import random

# ==================== 基础数据 ====================

TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 五行映射
GAN_ELEMENT = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
    "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"
}

ZHI_ELEMENT = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
    "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

# 季节映射 (月令)
ZHI_SEASON = {
    "寅": "春", "卯": "春", "辰": "春",
    "巳": "夏", "午": "夏", "未": "夏",
    "申": "秋", "酉": "秋", "戌": "秋",
    "亥": "冬", "子": "冬", "丑": "冬"
}

# 十神生克关系 (Simplified for generation)
SHISHEN_MAP = {
    ("木", "木"): "比劫", ("木", "火"): "食伤", ("木", "土"): "财星", ("木", "金"): "官杀", ("木", "水"): "印袅",
    ("火", "火"): "比劫", ("火", "土"): "食伤", ("火", "金"): "财星", ("火", "水"): "官杀", ("火", "木"): "印袅",
    ("土", "土"): "比劫", ("土", "金"): "食伤", ("土", "水"): "财星", ("土", "木"): "官杀", ("土", "火"): "印袅",
    ("金", "金"): "比劫", ("金", "水"): "食伤", ("金", "木"): "财星", ("金", "火"): "官杀", ("金", "土"): "印袅",
    ("水", "水"): "比劫", ("水", "木"): "食伤", ("水", "火"): "财星", ("水", "土"): "官杀", ("水", "金"): "印袅",
}

# ==================== 专业评语模板 ====================

# 1. 日主 x 月令 (格局与强弱)
PATTERN_COMMENTS = {
    "Wang": {  # 得令而旺 (如甲木生于寅卯月)
        "summary": "【建禄格/羊刃格】 身旺之造",
        "character": "个性坚强，自主性高，有领袖气质，但也容易固执己见。",
        "career": "适合独立创业、管理职或专业技术领域，能独当一面。",
        "wealth": "财运需靠个人努力，只有身旺才能任财，中晚年财运更佳。",
        "advice": "宜修身养性，听取他人意见，切勿刚愎自用。"
    },
    "Weak": {  # 失令而弱 (如甲木生于申酉月)
        "summary": "【正官格/七杀格】 身弱需印",
        "character": "为人谦和，行事谨慎，重视原则，但有时缺乏魄力。",
        "career": "适合公职、行政、教育或在大企业任职，寻求稳定发展。",
        "wealth": "财运平稳，不宜从事高风险投资，适合储蓄。",
        "advice": "宜增强自信，多学习技能（印星），寻找贵人（比劫）相助。"
    },
    "Balance": { # 其他情况
        "summary": "【杂气格】 五行调候",
        "character": "性格多面，适应力强，处世圆滑。",
        "career": "多才多艺，行业广泛，视大运流年而定。",
        "wealth": "财源多路，起伏不定。",
        "advice": "需专注某一领域深耕，避免博而不精。"
    }
}

# 2. 日主 x 元素 (十神特性)
SHISHEN_COMMENTS = {
    "比劫": "命带比劫，重义气，喜交友。但需防财来财去，宜与人合作。",
    "食伤": "命带食伤，才华横溢，思维敏捷。适合创意、演艺或技术行业。",
    "财星": "命带财星，讲究实际，理财有道。男命异性缘佳，利于经商。",
    "官杀": "命带官杀，责任感强，重视名誉。利于仕途或管理，但压力较大。",
    "印袅": "命带印袅，聪明好学，心地善良。利于学术研究，有长辈缘。"
}


def get_pattern_type(dm_element, month_zhi):
    """判断日主强弱类型"""
    month_element = ZHI_ELEMENT[month_zhi]
    
    # 简单逻辑：月令五行生日主或与日主相同 -> 旺
    # (Real Bazi needs more complex logic, but this is enough for "Logic-Driven Demo")
    
    if dm_element == month_element:
        return "Wang" # 比助
    
    # 生我者为印 (Check "Sheng" relationship is simplified here roughly)
    # Using simple map checking
    relation = SHISHEN_MAP.get((dm_element, month_element))
    
    # If month element generates Day Master (Inverse of SHISHEN_MAP logic above which is DM generates X)
    # Let's just use manual check for simplicity
    sheng_map = {"水": "木", "木": "火", "火": "土", "土": "金", "金": "水"}
    if sheng_map.get(month_element) == dm_element:
        return "Wang" # 印生
        
    return "Weak" # 克泄耗 -> 弱 (Simplified)


def generate_professional_data():
    """生成专业命理数据"""
    data = {}
    
    print("Generating Logic-Driven BaZi data...")
    
    # 1. 生成 [日主:月令] 规则
    for gan in TIAN_GAN:
        for zhi in DI_ZHI:
            key = f"bazi:day_master:{gan}:month:{zhi}"
            
            dm_element = GAN_ELEMENT[gan]
            pattern_type = get_pattern_type(dm_element, zhi)
            template = PATTERN_COMMENTS.get(pattern_type, PATTERN_COMMENTS["Balance"])
            
            # 动态生成具体内容
            content = {
                "summary": f"{gan}木生于{zhi}月（{ZHI_SEASON[zhi]}季），{template['summary']}",
                "character": f"日主为{gan}{dm_element}，{template['character']}",
                "career": template['career'],
                "wealth": template['wealth'],
                "advice": template['advice']
            }
            
            # Serialize to string for the Rule Engine (it expects string values currently, 
            # but we will upgrade Engine to parse JSON substring if needed, 
            # OR just store markdown formatted string)
            
            # Let's store as Markdown formatted string for direct display
            md_content = f"""
### 全局格局
{content['summary']}

### 性格特征
{content['character']}

### 事业方向
{content['career']}

### 财运分析
{content['wealth']}

### 建议
{content['advice']}
            """.strip()
            
            data[key] = md_content

    # 2. 生成 [日主:十神] 规则
    # key structure: bazi:dm:{gan}:shishen:{god}
    # But wait, ten gods are relative.
    # Engine calculates Ten Gods. 
    # Let's simply generate "Day Master x Element" rules which implies Ten God.
    
    for gan in TIAN_GAN:
        for element in ["木", "火", "土", "金", "水"]:
            if element == GAN_ELEMENT[gan]: continue # Skip self for now
            
            key = f"bazi:dm:{gan}:see:{element}"
            relation = SHISHEN_MAP.get((GAN_ELEMENT[gan], element), "其它")
            comment = SHISHEN_COMMENTS.get(relation, "运势平平。")
            
            data[key] = f"**{relation}运**：{comment}"

    # 3. 补充一些大数据的"填充"规则，模拟数据量
    # We repeat the structure but with slight variations or specialized combinations to fill size
    # For a real system, you'd add actual book content here.
    # For now, we focus on the QUALITY of the core rules we just generated.
    # We won't generate 50MB of junk anymore, quality over quantity. 
    # The user asked for "Professional and Precise", not "Huge".
    
    return data


def main():
    output_dir = "backend/app/data/rules"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "large_corpus.json")
    
    data = generate_professional_data()
    
    print(f"Writing {len(data)} high-quality rules to {file_path}...")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print("Done!")

if __name__ == "__main__":
    main()
