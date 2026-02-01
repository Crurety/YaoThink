
import sys
import os
import json
import hashlib
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

from backend.app.core.bazi.calendar import calculate_sizhu
from backend.app.core.bazi.shensha import analyze_shensha, analyze_dizhi_relations
from backend.app.core.ziwei.palace import create_ziwei_chart, analyze_ziwei_chart
from backend.app.core.ziwei.advanced import analyze_advanced_patterns, calculate_palace_score
from backend.app.core.yijing.hexagram import meihua_by_time, analyze_hexagram

def generate_snapshot():
    results = {}
    
    # Test cases: (year, month, day, hour)
    test_cases = [
        (1990, 5, 15, 10),
        (2024, 2, 4, 16),  # Li Chun transition
        (1985, 11, 22, 23), # Late night
        (2000, 1, 1, 0)
    ]
    
    print("Generating baseline snapshot...")
    
    for tc in test_cases:
        key = f"{tc[0]}-{tc[1]}-{tc[2]}-{tc[3]}"
        case_data = {}
        
        # 1. BaZi
        sizhu = calculate_sizhu(*tc)
        case_data["bazi"] = sizhu.bazi
        case_data["shensha"] = analyze_shensha(sizhu)
        case_data["dizhi_rel"] = analyze_dizhi_relations(sizhu)
        
        # 2. ZiWei (Simplified Lunar calc since we might not have lunarcalendar installed in some envs, 
        # but here we assume the code handles it or we pass dummy lunar dates for consistency check)
        # For consistency check, we use fixed lunar dates mapping to solar if we can, 
        # but simplest is to just pass some consistent numbers close to reality or just raw numbers 
        # creating specific charts.
        # Let's verify logic by passing consistent inputs.
        lunar_month = (tc[1] + 2) % 12 + 1 
        lunar_day = (tc[2]) % 30 + 1
        
        ziwei_chart = create_ziwei_chart(
            sizhu.year.gan, sizhu.year.zhi,
            lunar_month, lunar_day, sizhu.hour.zhi
        )
        case_data["ziwei_basic"] = analyze_ziwei_chart(ziwei_chart)
        case_data["ziwei_advanced"] = analyze_advanced_patterns(ziwei_chart)
        scores = {}
        for p in ziwei_chart.palaces:
            scores[p.name] = calculate_palace_score(p)
        case_data["ziwei_scores"] = scores
        
        # 3. YiJing (Deterministic time)
        # Mock datetime for consistency
        dt = datetime(tc[0], tc[1], tc[2], tc[3])
        hex_data = meihua_by_time(dt)
        case_data["yijing"] = analyze_hexagram(hex_data)
        
        results[key] = case_data

    # Serialize to JSON string with sort_keys=True for deterministic output
    json_output = json.dumps(results, sort_keys=True, ensure_ascii=False, default=str)
    
    # Calculate hash
    snapshot_hash = hashlib.md5(json_output.encode("utf-8")).hexdigest()
    
    print(f"Snapshot Hash: {snapshot_hash}")
    return json_output, snapshot_hash

if __name__ == "__main__":
    content, h = generate_snapshot()
    with open("optimization_baseline.json", "w", encoding="utf-8") as f:
        f.write(content)
    print("Baseline saved to optimization_baseline.json")
