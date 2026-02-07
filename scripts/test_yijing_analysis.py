"""
测试易经AI分析增强功能
"""
import sys
import os

# 确保可以导入 backend 模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.core.analysis.intelligent_analyst import analysis_service


def test_yijing_analysis():
    """测试易经分析"""
    print("=" * 60)
    print("易经AI分析增强功能测试")
    print("=" * 60)
    
    # 测试用例：乾卦，动爻在第6爻，变卦为泽天夬
    test_data = {
        "main_gua": {
            "name": "乾为天",
            "upper": {"name": "乾"},
            "lower": {"name": "乾"}
        },
        "dong_yao": 6,
        "changed_gua": {
            "name": "泽天夬"
        }
    }
    
    print("\n【测试用例1】乾为天，动爻第6爻")
    print("-" * 40)
    result = analysis_service.analyze_yijing(test_data)
    
    if result:
        print("\n[叙事分析]:")
        print(result.get("content", "无内容"))
        
        print("\n[结构化数据]:")
        structured = result.get("structured", {})
        for category, items in structured.items():
            print(f"  [{category}]: {len(items)} 条")
        
        # 验证维度
        expected_categories = ["core", "trigram", "relation", "moving", "advice"]
        found_categories = list(structured.keys())
        
        print("\n[维度检查]:")
        for cat in expected_categories:
            if cat in found_categories:
                print(f"  + {cat} 维度存在")
            else:
                print(f"  - {cat} 维度缺失")
    else:
        print("X 分析失败，返回空结果")
    
    print("\n" + "=" * 60)
    
    # 测试用例2：地天泰，动爻第3爻
    test_data2 = {
        "main_gua": {
            "name": "地天泰",
            "upper": {"name": "坤"},
            "lower": {"name": "乾"}
        },
        "dong_yao": 3,
        "changed_gua": {
            "name": "地泽临"
        }
    }
    
    print("\n【测试用例2】地天泰，动爻第3爻")
    print("-" * 40)
    result2 = analysis_service.analyze_yijing(test_data2)
    
    if result2:
        print("\n[叙事分析]:")
        print(result2.get("content", "无内容"))
        
        structured2 = result2.get("structured", {})
        print("\n[结构化数据]:")
        for category, items in structured2.items():
            print(f"  [{category}]: {len(items)} 条")
    else:
        print("X 分析失败，返回空结果")
    
    print("\n" + "=" * 60)
    
    # 测试用例3：无动爻情况
    test_data3 = {
        "main_gua": {
            "name": "水雷屯",
            "upper": {"name": "坎"},
            "lower": {"name": "震"}
        },
        "dong_yao": None,
        "changed_gua": {}
    }
    
    print("\n【测试用例3】水雷屯，无动爻")
    print("-" * 40)
    result3 = analysis_service.analyze_yijing(test_data3)
    
    if result3:
        print("\n[叙事分析]:")
        print(result3.get("content", "无内容"))
        
        structured3 = result3.get("structured", {})
        print("\n[结构化数据]:")
        for category, items in structured3.items():
            print(f"  [{category}]: {len(items)} 条")
    else:
        print("X 分析失败，返回空结果")
    
    print("\n" + "=" * 60)
    print("测试完成！")


if __name__ == "__main__":
    test_yijing_analysis()
