
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

        # 神煞 (Missing in original logic but good to have)
        if "shensha" in categories:
             paragraphs.append("【神煞启示】" + "；".join(categories["shensha"]) + "。")
            
        return "\n\n".join(paragraphs)

    def generate_structured(self, items: List[AnalyticItem], threshold: float = 2.0) -> Dict[str, List[str]]:
        """
        生成结构化维度数据
        """
        # 1. 排序
        sorted_items = sorted(items, key=lambda x: x.weight, reverse=True)
        
        # 2. 过滤
        valid_items = [item for item in sorted_items if item.weight >= threshold]
        
        # 3. 分组
        structured = {}
        for item in valid_items:
            if item.category not in structured:
                structured[item.category] = []
            structured[item.category].append(item.content)
            
        return structured

class BaziAnalyst(BaseAnalyst):
    """八字智能分析器"""
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        items = []
        
        # 提取基础数据
        day_master = data.get("day_master", "未知")
        # 兼容不同数据结构：data['month'] 可能是 dict 或 str
        month_data = data.get("month", {})
        month_zhi = month_data.get("zhi", "未知") if isinstance(month_data, dict) else "未知"
        
        # 提取更多数据用于深入分析
        wuxing_scores = data.get("wuxing_scores", {})
        shishen_profile = data.get("shishen_profile", {}) # Expecting dict like {'dominant': [...]}
        geju = data.get("geju", "未知格局")
        dayun = data.get("current_dayun", {})  # Expecting {'gan': '...', 'zhi': '...'}
        shensha = data.get("shensha", []) # Expecting list of names
        
        # --- 1. 本命特质 (Day Master) ---
        dm_desc = self.get_rule([f"bazi:theory:day_master:{day_master}:general"])
        if dm_desc:
            items.append(AnalyticItem(
                content=f"**【本命特质】**\n{dm_desc}", 
                weight=10.0, 
                category="core"
            ))
        else:
             items.append(AnalyticItem(
                content=f"**【本命特质】**\n你是{day_master}日主的人。", 
                weight=5.0, 
                category="core"
            ))

        # --- 2. 当季得失 (Seasonal Effect) ---
        relation = self._check_month_relation(day_master, month_zhi)
        if relation:
            items.append(AnalyticItem(content=relation, weight=9.5, category="core"))
            
        # --- 3. 格局事业 (Structure/Geju) ---
        geju_desc = self.get_rule([f"bazi:theory:geju:{geju}"])
        if geju_desc:
            items.append(AnalyticItem(
                content=f"**【格局事业】**\n格局：{geju}。\n{geju_desc}",
                weight=9.0,
                category="career"
            ))
        elif geju != "未知格局":
             items.append(AnalyticItem(
                content=f"**【格局事业】**\n格局：{geju}。此格局定下了你事业的基本框架。",
                weight=6.0,
                category="career"
            ))

        # --- 4. 性格优劣 (Dominant Shishen) ---
        # 假设 shishen_profile 包含 prominent 列表
        dominant_shishens = shishen_profile.get("dominant", [])
        if dominant_shishens:
            traits = []
            for shishen in dominant_shishens:
                trait = self.get_rule([f"bazi:theory:shishen:dominant:{shishen}"])
                if trait:
                    traits.append(trait)
            
            if traits:
                items.append(AnalyticItem(
                    content="**【性格剖析】**\n" + "\n".join(traits),
                    weight=8.5,
                    category="personality"
                ))
        
        # --- 5. 五行平衡 (Wuxing Balance) ---
        # 简单的过旺/过弱检查
        # 假设 wuxing_scores 是 {'木': 10, '火': 50 ...}
        if wuxing_scores:
            advice = []
            sorted_wx = sorted(wuxing_scores.items(), key=lambda x: x[1], reverse=True)
            if sorted_wx:
                strongest = sorted_wx[0][0]
                weakest = sorted_wx[-1][0]
                
                excess_rule = self.get_rule([f"bazi:theory:wuxing:excess:{self._wuxing_cn_to_en(strongest)}"])
                deficiency_rule = self.get_rule([f"bazi:theory:wuxing:deficiency:{self._wuxing_cn_to_en(weakest)}"])
                
                if excess_rule: advice.append(excess_rule)
                if deficiency_rule: advice.append(deficiency_rule)
                
            if advice:
                items.append(AnalyticItem(
                    content="**【五行建议】**\n" + "\n".join(advice),
                    weight=8.0,
                    category="advice"
                ))

        # --- 6. 大运分析 (Da Yun) ---
        dy_info = dayun if dayun else {}
        dy_gan = dy_info.get("gan")
        dy_zhi = dy_info.get("zhi")
        dy_shishen = dy_info.get("shishen") # Computed in API

        if dy_gan and dy_zhi:
             content = f"**【当前大运】 ({dy_gan}{dy_zhi}运)**\n"
             
             # 1. 尝试查找具体的大运十神规则
             if dy_shishen:
                 dy_rule = self.get_rule([f"bazi:theory:shishen:dayun:{dy_shishen}"])
                 if dy_rule:
                     content += dy_rule + "\n"
                     
             # 2. 尝试查找具体的日主大运规则 (Fallback)
             if not dy_shishen or "bazi:theory" not in content:
                 dy_desc_gan = self.get_rule([f"bazi:theory:day_master:{day_master}:dayun_gan:{dy_gan}"])
                 if dy_desc_gan: content += f"{dy_desc_gan}\n"
             
             # 3. 地支规则 (Optional, if specific rules exist)
             dy_desc_zhi = self.get_rule([f"bazi:theory:day_master:{day_master}:dayun_zhi:{dy_zhi}"])
             if dy_desc_zhi: content += f"{dy_desc_zhi}\n"
             
             items.append(AnalyticItem(content=content, weight=9.2, category="luck"))

        # --- 7. 神煞解读 (Shen Sha) ---
        if shensha:
            ss_descs = []
            for ss in shensha:
                 # Map common names or use direct name
                 # Example: '天乙贵人' -> 'tian_yi_gui_ren' mapping might be needed or key uses CN
                 # Let's try direct CN key first for simplicity or pinyin
                 # 暂定使用中文key，如果为了规范可以转拼音，这里先假设 corpus 用中文key
                 desc = self.get_rule([f"bazi:theory:shensha:{ss}"])
                 if desc:
                     ss_descs.append(f"- **{ss}**：{desc}")
            
            if ss_descs:
                items.append(AnalyticItem(
                    content="**【神煞启示】**\n" + "\n".join(ss_descs),
                    weight=7.0,
                    category="shensha"
                ))

        # --- 8. 财运分析 (Wealth) ---
        wealth_shishens = ["正财", "偏财"]
        wealth_items = [s for s in dominant_shishens if s in wealth_shishens]
        if wealth_items:
            wealth_descs = []
            for ws in wealth_items:
                w_desc = self.get_rule([f"bazi:theory:shishen:wealth:{ws}"])
                if w_desc:
                    wealth_descs.append(w_desc)
                else:
                    # 使用通用十神描述作为降级
                    general = self.get_rule([f"bazi:theory:shishen:dominant:{ws}"])
                    if general:
                        wealth_descs.append(f"**{ws}**：{general}")
            
            if wealth_descs:
                items.append(AnalyticItem(
                    content="**【财运格局】**\n" + "\n".join(wealth_descs),
                    weight=7.5,
                    category="wealth"
                ))
        else:
            # 如果没有财星突出，给出通用建议
            items.append(AnalyticItem(
                content="**【财运格局】**\n命局中正偏财星不显，财运需要通过后天努力和机遇来拓展。建议注重技能提升，财从官来或财从技来。",
                weight=5.0,
                category="wealth"
            ))

        # --- 9. 人际关系 (Relationship) ---
        social_shishens = ["比肩", "劫财", "伤官", "食神"]
        social_items = [s for s in dominant_shishens if s in social_shishens]
        if social_items:
            social_descs = []
            for ss in social_items:
                s_desc = self.get_rule([f"bazi:theory:shishen:relationship:{ss}"])
                if s_desc:
                    social_descs.append(s_desc)
                else:
                    # 降级到通用十神
                    general = self.get_rule([f"bazi:theory:shishen:dominant:{ss}"])
                    if general:
                        social_descs.append(f"**{ss}**：{general}")
            
            if social_descs:
                items.append(AnalyticItem(
                    content="**【人际感情】**\n" + "\n".join(social_descs),
                    weight=7.0,
                    category="relationship"
                ))


        return {
            "content": self.generate_narrative(items),
            "structured": self.generate_structured(items)
        }
    
    def _check_month_relation(self, dm: str, month: str) -> Optional[str]:
        # --- SERVICE LAYER LOGIC: FALLBACK ---
        
        # 1. 尝试 L1 精确匹配 (Classic: Di Tian Sui)
        specific_key = f"bazi:theory:day_master:{dm}:month:{month}"
        theory = self.get_rule([specific_key])
        if theory:
            return f"**【当季得失】**\n{theory}"

        # 2. 尝试 L2 降级匹配 (General Season Theory)
        dm_wx = self._get_wuxing(dm)
        season_map = {
            "寅": "spring", "卯": "spring", "辰": "spring",
            "巳": "summer", "午": "summer", "未": "summer",
            "申": "autumn", "酉": "autumn", "戌": "autumn",
            "亥": "winter", "子": "winter", "丑": "winter"
        }
        
        season = season_map.get(month, "unknown")
        wx_en = self._wuxing_cn_to_en(dm_wx)
        
        if wx_en and season != "unknown":
            fallback_key = f"bazi:theory:season:{wx_en}_{season}"
            theory = self.get_rule([fallback_key])
            if theory:
                return f"**【五行季节论】**\n{theory}" 
                
        return None

    def _get_wuxing(self, stems: str) -> Optional[str]:
        mapping = {
            "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
            "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"
        }
        return mapping.get(stems)
        
    def _wuxing_cn_to_en(self, cn: str) -> Optional[str]:
        mapping = {"木":"wood", "火":"fire", "土":"earth", "金":"metal", "水":"water"}
        return mapping.get(cn)

class ZiweiAnalyst(BaseAnalyst):
    """紫微智能分析器"""
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        items = []
        features = data.get("features", [])
        
        # 宫位 -> 维度映射
        palace_map = {
            "命宫": "core",           # 核心/命宫
            "官禄宫": "career",       # 事业
            "财帛宫": "wealth",       # 财运
            "夫妻宫": "love",         # 婚姻
            "迁移宫": "travel",       # 出行/人际
            "福德宫": "spirit",       # 精神/福德
            "疾厄宫": "health"        # 健康
        }

        # 1. 遍历所有特征，按宫位归类
        palace_stars = {}
        for f in features:
            palace = f.get("palace")
            star = f.get("star")
            if palace and star:
                if palace not in palace_stars:
                    palace_stars[palace] = []
                palace_stars[palace].append(star)

        # 2. 针对关键宫位进行分析
        for palace, category in palace_map.items():
            stars = palace_stars.get(palace, [])
            if not stars:
                continue

            # 2.1 单星分析
            star_descs = []
            for star in stars:
                desc = self.get_rule([f"ziwei:theory:star:{star}"])
                if desc:
                    # 简单处理：如果是命宫，权重高；其他宫位稍低
                    weight = 10.0 if category == "core" else 8.5
                    
                    # 针对非命宫，尝试寻找特定宫位的星曜解释 (如果有的话)，否则通用解释
                    # fallback: ziwei:theory:star:{star}:{palace} -> ziwei:theory:star:{star}
                    specific_desc = self.get_rule([f"ziwei:theory:star:{star}:{palace}"])
                    final_desc = specific_desc if specific_desc else desc
                    
                    items.append(AnalyticItem(
                        content=f"**【{palace}】**\n{star}：{final_desc}",
                        weight=weight,
                        category=category
                    ))

            # 2.2 双星组合 (仅处理命宫，避免过于复杂)
            if category == "core" and len(stars) >= 2:
                # 简单的双星组合逻辑
                sorted_stars = sorted(stars)
                # 尝试查找前两颗主星的组合
                if len(sorted_stars) >= 2:
                    key = f"ziwei:theory:dual:{sorted_stars[0]}_{sorted_stars[1]}"
                    dual_desc = self.get_rule([key])
                    if dual_desc:
                        items.append(AnalyticItem(
                            content=f"**【双星格局】**\n{dual_desc}",
                            weight=9.5,
                            category="core"
                        ))

        # 若命宫无主星
        if "命宫" not in palace_stars or not palace_stars["命宫"]:
             items.append(AnalyticItem(
                content="**【特殊格局】**\n命宫无主星（命无正曜），不仅要看本宫，更要借对宫（迁移宫）星曜来分析。这类人通常可塑性极强，环境适应力好，但也易随波逐流。",
                weight=9.0,
                category="core"
            ))

        return {
            "content": self.generate_narrative(items),
            "structured": self.generate_structured(items)
        }

class YijingAnalyst(BaseAnalyst):
    """易经智能分析器"""
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
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

        return {
            "content": self.generate_narrative(items),
            "structured": self.generate_structured(items)
        }

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
        
    def analyze_bazi(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._bazi.analyze(data)
        
    def analyze_ziwei(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._ziwei.analyze(data)
        
    def analyze_yijing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._yijing.analyze(data)


# Global Service Instance
from app.core.analysis.rule_engine import engine
analysis_service = AnalysisService(engine)
