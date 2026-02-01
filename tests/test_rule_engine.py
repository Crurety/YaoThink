
import time
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.core.analysis.rule_engine import engine

def test_engine_performance():
    print("Testing Rule Engine Performance...")
    
    start_time = time.time()
    engine.load_rules()
    duration = time.time() - start_time
    
    print(f"Loaded {len(engine._rules)} rules in {duration:.4f} seconds.")
    
    # Test Match
    test_key = "bazi:day_master:甲:month:寅"
    print(f"Testing match for '{test_key}'...")
    result = engine.match(test_key)
    
    if result:
        print("Match Success!")
        print(f"Content length: {len(result)}")
        print(f"Snippet: {result[:50]}...")
    else:
        print(f"Match Failed for {test_key}")
        # Try a random key from rules
        if engine._rules:
            first_key = list(engine._rules.keys())[0]
            print(f"Trying existing key: {first_key}")
            print(f"Result: {engine.match(first_key)[:50]}...")

if __name__ == "__main__":
    test_engine_performance()
