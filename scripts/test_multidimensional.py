import sys
import os

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.analysis.intelligent_analyst import analysis_service
from app.core.analysis.rule_engine import engine

def test_ziwei_multidimensional():
    print("\n=== Testing Ziwei Multi-dimensional Analysis ===")
    
    mock_data = {
        "features": [
            {"palace": "命宫", "star": "紫微"},
            {"palace": "命宫", "star": "天府"},
            {"palace": "官禄宫", "star": "太阳"},  # Career
            {"palace": "财帛宫", "star": "武曲"},  # Wealth
            {"palace": "夫妻宫", "star": "天同"},  # Love
        ]
    }
    
    engine.load_rules()
    
    result = analysis_service.analyze_ziwei(mock_data)
    
    structured = result.get("structured", {})
    print("\n--- Structured Output Keys ---")
    print(list(structured.keys()))
    
    expected_categories = ["core", "career", "wealth", "love"]
    all_present = all(cat in structured for cat in expected_categories)
    
    if all_present:
        print("\n[PASS] All expected dimensions present.")
    else:
        print(f"\n[FAIL] Missing dimensions. Expected {expected_categories}, got {list(structured.keys())}")
        
    print("\n--- Content Preview ---")
    for cat, items in structured.items():
        print(f"\n[{cat.upper()}]:")
        for item in items:
            print(f"  - {item[:50]}...")

def test_bazi_multidimensional():
    print("\n=== Testing BaZi Multi-dimensional Analysis ===")
    
    # Mock data simulating what /api/bazi/analyze prepares
    mock_data = {
        "day_master": "甲",
        "month": {"zhi": "寅"},
        "geju": "正官格",
        "shishen_profile": {"dominant": ["偏财", "七杀"]},
        "wuxing_scores": {"火": 60, "木": 10}, # Excess Fire, Weak Wood
        "current_dayun": {"gan": "丙", "zhi": "午", "shishen": "食神"}
    }
    
    engine.load_rules()
    
    result = analysis_service.analyze_bazi(mock_data)
    structured = result.get("structured", {})
    
    print("\n--- Structured Output Keys ---")
    print(list(structured.keys()))
    
    # Expect: core (Day Master), career (Geju), personality (Shishen), advice (Wuxing), luck (Dayun)
    expected = ["core", "career", "personality", "advice", "luck"]
    present = [k for k in expected if k in structured]
    
    if len(present) == len(expected):
         print("\n[PASS] All expected dimensions present.")
    else:
         print(f"\n[FAIL] Missing dimensions. Expected {expected}, got {present}")
         
    print("\n--- Content Preview ---")
    for cat, items in structured.items():
        print(f"\n[{cat.upper()}]:")
        for item in items:
             # Clean newlines for preview
            text = item.replace('\n', ' ')
            print(f"  - {text[:60]}...")

if __name__ == "__main__":
    test_ziwei_multidimensional()
    test_bazi_multidimensional()
