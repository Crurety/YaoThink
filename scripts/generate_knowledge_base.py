
import json
import os
import random
import itertools

# 基础数据
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
SHISHEN = ["比肩", "劫财", "食神", "伤官", "偏财", "正财", "七杀", "正官", "偏印", "正印"]
STARS = ["紫微", "天机", "太阳", "武曲", "天同", "廉贞", "天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军"]
PALACES = ["命宫", "兄弟", "夫妻", "子女", "财帛", "疾厄", "迁移", "交友", "官禄", "田宅", "福德", "父母"]

# 描述模板
TEMPLATES = [
    "此局{key}，意味着{trait}。在事业上表现为{career}，财运方面{wealth}，但需注意{caution}。",
    "{key}之象，{trait}。为人处世{attitude}，{career}是发展的良机，凡事{advice}。",
    "命带{key}，主{trait}。{wealth}，事业{career}，建议多{advice}，尤其在{season}。",
    "格局为{key}，{trait}之兆。{attitude}，利于{career}，{wealth}，切记{caution}。",
    "若逢{icon}，则{key}。{trait}，{advice}，可得{wealth}，需防{caution}。",
]

TRAITS = ["刚健中正", "柔顺利贞", "进取有为", "深谋远虑", "才华横溢", "贵人多助", "多劳多得", "财源广进", "运势亨通", "波折起伏"]
CAREERS = ["仕途顺利", "商场得意", "技艺超群", "学术有成", "创业艰难", "职场稳健", "名利双收", "默默耕耘"]
WEALTHS = ["正财稳健", "偏财意外", "积少成多", "财来财去", "富贵天成", "需勤俭持家"]
CAUTIONS = ["小人作祟", "口舌是非", "身体抱恙", "投资风险", "情感纠纷", "虽然由于", "虽有波折"]
ATTITUDES = ["谦虚谨慎", "乐观向上", "积极进取", "稳重踏实", "灵活变通"]
ADVICES = ["广结善缘", "谨言慎行", "把握机会", "修身养性", "顺其自然"]
SEASONS = ["春季", "夏季", "秋季", "冬季", "流年"]


def generate_large_bazi_data(target_size_mb=50):
    """
    生成大量八字规则数据
    """
    data = {}
    current_size = 0
    target_bytes = target_size_mb * 1024 * 1024

    print(f"Generating BaZi data, target: {target_size_mb}MB...")

    # 1. 日主 x 月令 (10 x 12 = 120 组合)
    for gan in TIAN_GAN:
        for zhi in DI_ZHI:
            key = f"bazi:day_master:{gan}:month:{zhi}"
            desc = random.choice(TEMPLATES).format(
                key=f"日主{gan}生于{zhi}月",
                trait=random.choice(TRAITS),
                career=random.choice(CAREERS),
                wealth=random.choice(WEALTHS),
                caution=random.choice(CAUTIONS),
                attitude=random.choice(ATTITUDES),
                advice=random.choice(ADVICES),
                season=random.choice(SEASONS),
                icon="流年"
            )
            data[key] = desc * 50 # Repeat content to simulate long text

    # 2. 十神组合 (10 x 10 = 100 组合)
    for s1 in SHISHEN:
        for s2 in SHISHEN:
            key = f"bazi:shishen:{s1}:meet:{s2}"
            desc = random.choice(TEMPLATES).format(
                key=f"{s1}见{s2}",
                trait=random.choice(TRAITS),
                career=random.choice(CAREERS),
                wealth=random.choice(WEALTHS),
                caution=random.choice(CAUTIONS),
                attitude=random.choice(ATTITUDES),
                advice=random.choice(ADVICES),
                season=random.choice(SEASONS),
                icon="大运"
            )
            data[key] = desc * 10

    # 3. 三柱组合 (生成大量随机组合 fill space)
    # 日干 x 月支 x 时支 (10 x 12 x 12 = 1440)
    # 扩展生成直到满足大小
    
    count = 0
    while True:
        # 生成一个随机复杂的组合键
        gan = random.choice(TIAN_GAN)
        zhi1 = random.choice(DI_ZHI)
        zhi2 = random.choice(DI_ZHI)
        star = random.choice(STARS)
        
        # 更加复杂的键，模拟细粒度规则
        key = f"bazi:complex:{gan}:{zhi1}:{zhi2}:{star}:{count}" 
        
        # 生成一段长文本
        paragraph = []
        for _ in range(5): # 5 sentences
            paragraph.append(random.choice(TEMPLATES).format(
                key=f"{gan}日{zhi1}月",
                trait=random.choice(TRAITS),
                career=random.choice(CAREERS),
                wealth=random.choice(WEALTHS),
                caution=random.choice(CAUTIONS),
                attitude=random.choice(ATTITUDES),
                advice=random.choice(ADVICES),
                season=random.choice(SEASONS),
                icon="岁运"
            ))
        
        content = "\\n".join(paragraph) * 20 # Make it verify large per entry (~2KB)
        data[key] = content
        
        count += 1
        
        # Check size every 1000 items
        if count % 1000 == 0:
            json_str = json.dumps(data, ensure_ascii=False)
            current_size = len(json_str.encode('utf-8'))
            print(f"Current size: {current_size / 1024 / 1024:.2f} MB, Items: {len(data)}")
            if current_size >= target_bytes:
                break
    
    return data

def main():
    output_dir = "backend/app/data/rules"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "large_corpus.json")
    
    data = generate_large_bazi_data(target_size_mb=50)
    
    print(f"Writing to {file_path}...")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print("Done!")

if __name__ == "__main__":
    main()
