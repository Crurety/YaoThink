
import json
import os
from typing import Dict, List, Optional
import logging
from app.core.analysis.intelligent_analyst import BaziAnalyst, ZiweiAnalyst, YijingAnalyst

logger = logging.getLogger(__name__)

class RuleEngine:
    _instance = None
    _rules: Dict[str, str] = {}
    _is_loaded = False
    
    # Intelligent Analysts
    bazi_analyst = BaziAnalyst()
    ziwei_analyst = ZiweiAnalyst()
    yijing_analyst = YijingAnalyst()

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
        
        # Inject rule provider to analysts
        self.bazi_analyst.set_rule_provider(self.match)
        self.ziwei_analyst.set_rule_provider(self.match)
        self.yijing_analyst.set_rule_provider(self.match)

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
        分析八字 - 智能分析模式
        """
        # 优先使用智能分析
        try:
            return self.bazi_analyst.analyze(bazi_data)
        except Exception as e:
            logger.error(f"Intelligent Bazi Analysis failed: {e}")
            return "分析服务暂时忙碌，请稍后再试。"

        # Legacy logic removed
        return ""



    def analyze_ziwei(self, chart_data: Dict) -> str:
        """
        分析紫微斗数 - 智能分析模式
        """
        try:
            return self.ziwei_analyst.analyze(chart_data)
        except Exception as e:
            logger.error(f"Intelligent Ziwei Analysis failed: {e}")
            return "分析服务暂时忙碌，请稍后再试。"

    def analyze_yijing(self, hexagram_data: Dict) -> str:
        """
        分析易经 - 智能分析模式
        """
        try:
            return self.yijing_analyst.analyze(hexagram_data)
        except Exception as e:
            logger.error(f"Intelligent Yijing Analysis failed: {e}")
            return "分析服务暂时忙碌，请稍后再试。"

# Global instance
engine = RuleEngine()

