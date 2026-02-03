import sys
import os

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.analysis.intelligent_analyst import analysis_service

def test_ziwei_multidimensional():
    print("Testing Ziwei Multi-dimensional Analysis...")
    
    mock_data = {
        "features": [
            {"palace": "命宫", "star": "紫微"},
            {"palace": "命宫", "star": "天府"},
            {"palace": "官禄宫", "star": "太阳"},  # Career
            {"palace": "财帛宫", "star": "武曲"},  # Wealth
            {"palace": "夫妻宫", "star": "天同"},  # Love
        ]
    }
    
    # Load rules (mocking the engine load if needed or relying on startup)
    # The intelligent_analyst imports 'engine' which auto-loads on first use if we trigger it or we can manually load
    from app.core.analysis.rule_engine import engine
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

if __name__ == "__main__":
    test_ziwei_multidimensional()
