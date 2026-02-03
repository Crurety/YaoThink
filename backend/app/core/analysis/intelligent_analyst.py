
import logging
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class AnalyticItem:
    """分析条目"""
    content: str
    weight: float = 1.0  # 权重 0.0 - 10.0
    category: str = "general"

class BaseAnalyst:
    """分析器基类"""
    
    def __init__(self):
        self.rule_provider: Optional[Callable[[str], Optional[str]]] = None
        
    def set_rule_provider(self, provider: Callable[[str], Optional[str]]):
        """设置规则提供者 (通常是 RuleEngine.match)"""
        self.rule_provider = provider
        
    def get_rule(self, keys: Union[str, List[str]]) -> Optional[str]:
        """
        智能获取规则 (Support Retry/Fallback)
        If keys is a list, try each key in order until a match is found.
        """
        if isinstance(keys, str):
            keys = [keys]
            
        if self.rule_provider:
            for key in keys:
                val = self.rule_provider(key)
                if val:
                    return val
        return None
    
    def generate_narrative(self, items: List[AnalyticItem], threshold: float = 2.0) -> str:
        """
        生成叙事文本
        根据权重排序，过滤低权重项，并组合成自然段落
        """
        # 1. 排序
        sorted_items = sorted(items, key=lambda x: x.weight, reverse=True)
        
        # 2. 过滤
        valid_items = [item for item in sorted_items if item.weight >= threshold]
        
        if not valid_items:
            return "根据当前信息，暂无明显的特殊格局分析。"
            
        # 3. 组合
        # 简单策略：按类别分组，然后拼接
        categories = {}
        for item in valid_items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item.content)
            
        paragraphs = []
        
        # 核心格局优先
        if "core" in categories:
            paragraphs.append("【核心格局】" + "；".join(categories["core"]) + "。")
            
        # 性格分析
        if "personality" in categories:
            paragraphs.append("【性格特征】" + "，".join(categories["personality"]) + "。")
            
        # 运势/具体建议
        if "advice" in categories:
            paragraphs.append("【发展建议】" + "；".join(categories["advice"]) + "。")
            
        return "\n\n".join(paragraphs)

class BaziAnalyst(BaseAnalyst):
    """八字智能分析器"""
    
    def analyze(self, data: Dict[str, Any]) -> str:
        items = []
        
        day_master = data.get("day_master", "未知")
        month_zhi = data.get("month", {}).get("zhi", "未知") if isinstance(data.get("month"), dict) else "未知"
        
        # 1. 日主与月令关系 (权重: 10)
        relation = self._check_month_relation(day_master, month_zhi)
        if relation:
            items.append(AnalyticItem(content=relation, weight=10.0, category="core"))
            
        # 2. 五行平衡分析 (权重: 8)
        # Try specific rule first, then generic
        items.append(AnalyticItem(
            content=f"日主{day_master}生于{month_zhi}月，气候与五行流转决定了命局的基础底色", 
            weight=5.0, 
            category="core"
        ))
        
        # 3. 十神/五行建议
        dm_wuxing = self._get_wuxing(day_master)
        if dm_wuxing:
             # Example of future expansion
             pass

        return self.generate_narrative(items)
    
    def _check_month_relation(self, dm: str, month: str) -> Optional[str]:
        # --- SERVICE LAYER LOGIC: FALLBACK ---
        
        # 1. 尝试 L1 精确匹配 (Classic: Di Tian Sui)
        specific_key = f"bazi:theory:day_master:{dm}:month:{month}"
        theory = self.get_rule([specific_key])
        if theory:
            return f"【经典月令论】：{theory}"

        # 2. 尝试 L2 降级匹配 (General Season Theory)
        dm_wx = self._get_wuxing(dm)
        season_map = {
            "寅": "spring", "卯": "spring", "辰": "spring",
            "巳": "summer", "午": "summer", "未": "summer",
            "申": "autumn", "酉": "autumn", "戌": "autumn",
            "亥": "winter", "子": "winter", "丑": "winter"
        }
        wuxing_en = {"木":"wood", "火":"fire", "土":"earth", "金":"metal", "水":"water"}
        
        season = season_map.get(month, "unknown")
        wx_en = wuxing_en.get(dm_wx)
        
        if wx_en and season != "unknown":
            fallback_key = f"bazi:theory:season:{wx_en}_{season}"
            theory = self.get_rule([fallback_key])
            if theory:
                return f"【五行季节论】：{theory}" 
                
        return None

    def _get_wuxing(self, stems: str) -> Optional[str]:
        mapping = {
            "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
            "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"
        }
        return mapping.get(stems)

class ZiweiAnalyst(BaseAnalyst):
    """紫微智能分析器"""
    
    def analyze(self, data: Dict[str, Any]) -> str:
        items = []
        features = data.get("features", [])
        
        ming_stars = [f["star"] for f in features if f.get("palace") == "命宫"]
        
        if not ming_stars:
            return "命宫无主星（命无正曜），不仅要看本宫，更要借对宫（迁移宫）星曜来分析。这类人通常可塑性极强，环境适应力好，但也易随波逐流。"
            
        # 1. 主星格局分析
        star_str = "、".join(ming_stars)
        
        desc_list = []
        for star in ming_stars:
            # Fallsback: 1. Specific Star, 2. Maybe class if implemented
            desc = self.get_rule([f"ziwei:theory:star:{star}"])
            if desc:
                desc_list.append(desc)
            
        content = f"命宫主星为{star_str}。\n" + "\n".join(desc_list)
        items.append(AnalyticItem(
            content=content, 
            weight=10.0, 
            category="core"
        ))
        
        # 2. 组合逻辑 (双星组合)
        if len(ming_stars) == 2:
            sorted_stars = sorted(ming_stars)
            key = f"ziwei:theory:dual:{sorted_stars[0]}_{sorted_stars[1]}"
            dual_desc = self.get_rule([key])
            if dual_desc:
                items.append(AnalyticItem(
                    content=dual_desc, 
                    weight=9.5, 
                    category="core"
                ))

        return self.generate_narrative(items)

class YijingAnalyst(BaseAnalyst):
    """易经智能分析器"""
    
    def analyze(self, data: Dict[str, Any]) -> str:
        items = []
        
        main_gua = data.get("main_gua", {})
        dong_yao = data.get("dong_yao") # int 1-6 or None
        
        gua_name = main_gua.get("name", "未知")
        
        # 1. 本卦大象分析
        # Strategy: 1. Specific Gua Name
        gua_desc = self.get_rule([f"yijing:theory:gua:{gua_name}"])
        if not gua_desc:
            gua_desc = f"【{gua_name}】：此卦象征当前的处境。"
            
        items.append(AnalyticItem(
            content=gua_desc, 
            weight=10.0, 
            category="core"
        ))
        
        # 2. 动爻具体分析
        if dong_yao:
            items.append(AnalyticItem(
                content=f"变爻在第{dong_yao}爻，这是事情发展的关键转折点", 
                weight=8.0, 
                category="core"
            ))
            
            yao_theory = self.get_rule([f"yijing:theory:yao:{dong_yao}"])
            if yao_theory:
                 items.append(AnalyticItem(content=yao_theory, weight=7.0, category="advice"))
        else:
            items.append(AnalyticItem(
                content="此卦无动爻，更加强调本卦特质的稳定性，事情短期内变数较小", 
                weight=7.0, 
                category="core"
            ))

        return self.generate_narrative(items)

class AnalysisService:
    """
    智能分析服务入口
    Main Service Façade that orchestrates sub-analysts.
    """
    def __init__(self, rule_engine_instance):
        self._bazi = BaziAnalyst()
        self._ziwei = ZiweiAnalyst()
        self._yijing = YijingAnalyst()
        
        # Inject dependencies
        provider = rule_engine_instance.match
        self._bazi.set_rule_provider(provider)
        self._ziwei.set_rule_provider(provider)
        self._yijing.set_rule_provider(provider)
        
    def analyze_bazi(self, data: Dict[str, Any]) -> str:
        return self._bazi.analyze(data)
        
    def analyze_ziwei(self, data: Dict[str, Any]) -> str:
        return self._ziwei.analyze(data)
        
    def analyze_yijing(self, data: Dict[str, Any]) -> str:
        return self._yijing.analyze(data)


# Global Service Instance
from app.core.analysis.rule_engine import engine
analysis_service = AnalysisService(engine)
