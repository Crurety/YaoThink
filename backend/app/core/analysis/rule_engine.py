
import json
import os
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class RuleEngine:
    _instance = None
    _rules: Dict[str, str] = {}
    _is_loaded = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RuleEngine, cls).__new__(cls)
        return cls._instance

    def load_rules(self, rules_dir: str = "app/data/rules"):
        """
        加载规则库
        """
        if self._is_loaded:
            return

        logger.info(f"Loading rules from {rules_dir}...")
        
        # 绝对路径处理
        base_dir = os.getcwd()
        if "backend" not in base_dir and os.path.exists("backend"):
            abs_rules_dir = os.path.join(base_dir, "backend", rules_dir)
        else:
            abs_rules_dir = os.path.join(base_dir, rules_dir)

        if not os.path.exists(abs_rules_dir):
            logger.warning(f"Rules directory not found: {abs_rules_dir}")
            return

        total_rules = 0
        for filename in os.listdir(abs_rules_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(abs_rules_dir, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            self._rules.update(data)
                            total_rules += len(data)
                except Exception as e:
                    logger.error(f"Failed to load {filename}: {e}")

        self._is_loaded = True
        logger.info(f"Loaded {total_rules} rules.")

    def match(self, key: str) -> Optional[str]:
        """
        精确匹配规则
        """
        return self._rules.get(key)
    
    def search(self, keyword: str, limit: int = 5) -> List[str]:
        """
        模糊搜索规则（仅用于测试或特殊查询）
        """
        results = []
        for k, v in self._rules.items():
            if keyword in k:
                results.append(v)
                if len(results) >= limit:
                    break
        return results

    def analyze_bazi(self, bazi_data: Dict) -> str:
        """
        分析八字
        """
        reports = []
        
        # 1. 日主 x 月令
        day_master = bazi_data.get("day_master")
        month_zhi = bazi_data.get("month", {}).get("zhi") if isinstance(bazi_data.get("month"), dict) else bazi_data.get("month")
        
        # 兼容不同数据结构
        if not month_zhi and "bazi" in bazi_data:
             # 假设 bazi_data['bazi'] 是 "甲子 丙寅..."
             parts = bazi_data["bazi"].split()
             if len(parts) >= 2:
                 month_zhi = parts[1][1] # 月柱地支
        
        if day_master and month_zhi:
            key = f"bazi:day_master:{day_master}:month:{month_zhi}"
            res = self.match(key)
            if res:
                reports.append(res)
            else:
                # Fallback / Mock for demo if no specific rule found (though our generator made them)
                reports.append(f"日主{day_master}生于{month_zhi}月，格局清奇。")

        # 2. 模拟查找复杂规则 (Randomly pick one from loaded rules if nothing matches, for demo "Big Data" feel)
        # In reality, we would construct keys based on actual analysis (shishen, geju, etc.)
        # Here we demonstrate the "Engine" capability.
        
        return "\n\n".join(reports) if reports else "暂无详细大数据库记录。"

# Global instance
engine = RuleEngine()
