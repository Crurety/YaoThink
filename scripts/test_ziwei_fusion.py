# -*- coding: utf-8 -*-
"""
紫微斗数融合分析测试脚本
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.fusion import (
    FusionAnalyzer,
    get_star_psychology,
    get_palace_stars_psychology,
    ZIWEI_STAR_PSYCHOLOGY_MAP
)


def test_star_mapping():
    """测试星曜心理学映射"""
    print("=" * 50)
    print("测试1: 星曜心理学映射")
    print("=" * 50)
    
    # 测试映射表存在
    assert "紫微" in ZIWEI_STAR_PSYCHOLOGY_MAP, "紫微星应该存在于映射表"
    assert "天机" in ZIWEI_STAR_PSYCHOLOGY_MAP, "天机星应该存在于映射表"
    assert len(ZIWEI_STAR_PSYCHOLOGY_MAP) == 14, f"应该有14颗主星，实际 {len(ZIWEI_STAR_PSYCHOLOGY_MAP)}"
    
    # 测试单星映射
    ziwei_psychology = get_star_psychology("紫微")
    assert "keywords" in ziwei_psychology, "应该包含 keywords"
    assert "archetypes" in ziwei_psychology, "应该包含 archetypes"
    assert "RULER" in ziwei_psychology["archetypes"], "紫微应该对应 RULER 原型"
    
    print(f"  ✓ 紫微星映射: {ziwei_psychology}")
    
    # 测试不存在的星
    unknown = get_star_psychology("不存在的星")
    assert unknown == {}, "不存在的星应该返回空字典"
    
    print("  ✓ 星曜映射测试通过!")
    return True


def test_palace_stars_psychology():
    """测试宫位星曜综合分析"""
    print("\n" + "=" * 50)
    print("测试2: 宫位星曜综合分析")
    print("=" * 50)
    
    # 模拟命宫有紫微、天机双星
    stars = [{"name": "紫微"}, {"name": "天机"}]
    combined = get_palace_stars_psychology(stars)
    
    assert "keywords" in combined, "应该包含 keywords"
    assert "archetypes" in combined, "应该包含 archetypes"
    assert "primary_archetype" in combined, "应该包含 primary_archetype"
    assert len(combined["keywords"]) >= 4, "应该至少有4个关键词"
    
    print(f"  ✓ 双星综合分析:")
    print(f"    - 关键词: {combined['keywords'][:6]}")
    print(f"    - 主原型: {combined['primary_archetype']}")
    print(f"    - MBTI倾向: {combined.get('primary_mbti_tendencies', [])}")
    
    print("  ✓ 宫位星曜分析测试通过!")
    return True


def test_fusion_analyzer():
    """测试融合分析器"""
    print("\n" + "=" * 50)
    print("测试3: FusionAnalyzer 融合分析")
    print("=" * 50)
    
    analyzer = FusionAnalyzer()
    
    # 模拟紫微数据
    ziwei_data = {
        "chart_data": {
            "palaces": [
                {
                    "name": "命宫",
                    "stars": {"main": [{"name": "紫微"}, {"name": "天府"}]}
                },
                {
                    "name": "官禄宫",
                    "stars": {"main": [{"name": "武曲"}, {"name": "天相"}]}
                },
                {
                    "name": "财帛宫",
                    "stars": {"main": [{"name": "太阳"}]}
                },
                {
                    "name": "夫妻宫",
                    "stars": {"main": [{"name": "贪狼"}]}
                }
            ]
        }
    }
    
    # 测试仅紫微数据
    result = analyzer.analyze(ziwei_data=ziwei_data)
    
    assert result.personality_fusion, "应该有人格融合结果"
    assert result.ziwei_analysis == ziwei_data, "应该保存原始紫微数据"
    
    fusion = result.personality_fusion
    print(f"  ✓ 核心特质: {fusion.get('core_traits', [])[:5]}")
    print(f"  ✓ 紫微洞察: {list(fusion.get('ziwei_insights', {}).keys())}")
    print(f"  ✓ 置信度: {result.confidence}%")
    
    # 测试紫微+MBTI融合
    result_with_mbti = analyzer.analyze(
        ziwei_data=ziwei_data,
        mbti_type="ENTJ"
    )
    
    fusion_mbti = result_with_mbti.personality_fusion
    print(f"\n  ✓ 紫微+MBTI融合:")
    print(f"    - 核心特质: {fusion_mbti.get('core_traits', [])[:6]}")
    print(f"    - 优势: {fusion_mbti.get('strengths', [])}")
    
    # 检查人生指导
    guidance = result_with_mbti.life_guidance
    print(f"  ✓ 人生指导:")
    print(f"    - 事业: {guidance.get('career', [])[:2]}")
    print(f"    - 关系: {guidance.get('relationship', [])[:2]}")
    
    print("  ✓ 融合分析器测试通过!")
    return True


def test_ziwei_palace_analysis():
    """测试宫位分析方法"""
    print("\n" + "=" * 50)
    print("测试4: 宫位分析方法")
    print("=" * 50)
    
    analyzer = FusionAnalyzer()
    
    ziwei_data = {
        "palaces": [
            {
                "name": "命宫",
                "stars": {"main": [{"name": "七杀"}]}
            },
            {
                "name": "官禄宫",
                "major_stars": [{"name": "破军"}]  # 测试另一种数据结构
            }
        ]
    }
    
    palace_insights = analyzer._analyze_ziwei_palaces(ziwei_data)
    
    assert "命宫" in palace_insights, "应该分析命宫"
    ming_gong = palace_insights["命宫"]
    
    print(f"  ✓ 命宫分析:")
    print(f"    - 星曜: {ming_gong.get('stars', [])}")
    print(f"    - 关键词: {ming_gong.get('star_keywords', [])}")
    print(f"    - 原型: {ming_gong.get('primary_archetype')}")
    print(f"    - 生活领域: {ming_gong.get('life_domains', [])}")
    
    print("  ✓ 宫位分析测试通过!")
    return True


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  紫微斗数融合分析集成测试")
    print("=" * 60)
    
    all_passed = True
    
    try:
        all_passed &= test_star_mapping()
        all_passed &= test_palace_stars_psychology()
        all_passed &= test_fusion_analyzer()
        all_passed &= test_ziwei_palace_analysis()
        
        print("\n" + "=" * 60)
        if all_passed:
            print("  ✅ 所有测试通过!")
        else:
            print("  ❌ 部分测试失败")
        print("=" * 60 + "\n")
            
    except Exception as e:
        print(f"\n  ❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
