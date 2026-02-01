
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
        分析八字 - 多维模式匹配
        """
        reports = []
        
        # --- 1. 数据提取与预处理 ---
        day_master = bazi_data.get("day_master")
        month_zhi = None
        
        # 尝试从对象结构提取月支
        month = bazi_data.get("month")
        if isinstance(month, dict):
            month_zhi = month.get("zhi")
        elif isinstance(month, str):
            month_zhi = month
            
        # 尝试从字符串解析 (如 "甲子 丙寅...")
        full_chart = bazi_data.get("bazi", "")
        stems = []
        if isinstance(full_chart, str) and len(full_chart.split()) >= 4:
            parts = full_chart.split()
            # 假设格式：年柱 月柱 日柱 时柱 (每柱2字)
            # 例如: ["甲子", "丙寅", "戊辰", "庚申"]
            if len(parts) >= 2 and len(parts[1]) >= 2:
                month_zhi = month_zhi or parts[1][1]
            
            # 提取所有天干 (除了日主自己)
            for idx, part in enumerate(parts):
                if idx == 2: continue # 跳过日柱(日主)
                if len(part) > 0:
                    stems.append(part[0])

        if not day_master or not month_zhi:
            return "数据不足，无法进行详细的大数据分析。"

        # --- 2. 核心格局分析 [日主:月令] ---
        # 对应 generate_knowledge_base.py 中的 PATTERN_COMMENTS
        key_core = f"bazi:day_master:{day_master}:month:{month_zhi}"
        res_core = self.match(key_core)
        
        if res_core:
            reports.append(res_core)
        else:
            # 基础兜底
            reports.append(f"### 基础分析\n日主**{day_master}**生于**{month_zhi}**月，格局需结合全局判断。")

        # --- 3. 十神/五行配置分析 [日主:见:元素] ---
        # 简单五行映射
        gan_map = {
            "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
            "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"
        }
        
        seen_elements = set()
        supplementary_info = []
        
        for stem in stems:
            element = gan_map.get(stem)
            if element and element not in seen_elements:
                key_supp = f"bazi:dm:{day_master}:see:{element}"
                res_supp = self.match(key_supp)
                if res_supp:
                    supplementary_info.append(res_supp)
                seen_elements.add(element)
        
        if supplementary_info:
            reports.append("### 命局配置\n" + "\n".join(supplementary_info))

        # --- 4. 生成最终报告 ---
        final_report = "\n\n".join(reports)
        
        # 添加免责声明
        final_report += "\n\n---\n*注：以上内容基于经典命理古籍（如《滴天髓》）的大数据匹配生成，不做封建迷信解读，仅供心理参考。*"
        
        return final_report

# Global instance
engine = RuleEngine()
