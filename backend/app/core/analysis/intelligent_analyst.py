
import logging
from typing import Dict, List, Optional, Any
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
        
        # 尝试从字符串解析更多信息
        # 假设 data 包含 'wuxing_scores' 或 'strength' 等预计算结果
        # 这里进行更深度的逻辑推演
        
        # 1. 日主与月令关系 (权重: 10)
        relation = self._check_month_relation(day_master, month_zhi)
        if relation:
            items.append(AnalyticItem(content=relation, weight=10.0, category="core"))
            
        # 2. 五行平衡分析 (权重: 8)
        # 模拟分析，实际应基于分数判断
        # 这里作为一个演示逻辑
        items.append(AnalyticItem(
            content=f"日主{day_master}生于{month_zhi}月，气候与五行流转决定了命局的基础底色", 
            weight=5.0, 
            category="core"
        ))
        
        # 3. 建议生成
        # 基于简单的五行生克建议
        wuxing_career = {
            "木": "适合发展文化、教育、园艺等具有生发性质的行业",
            "火": "适合互联网、能源、餐饮等具有发散性质的行业",
            "土": "适合房地产、农业、仓储等具有承载性质的行业",
            "金": "适合金融、法律、机械等具有肃杀/规则性质的行业",
            "水": "适合航运、贸易、流动性强的行业"
        }
        # 假设我们无法确切知道喜用神，但可以给出一个基于日主五行的通用建议
        # 实际应传入喜用神
        dm_wuxing = self._get_wuxing(day_master)
        if dm_wuxing:
            items.append(AnalyticItem(
                content=wuxing_career.get(dm_wuxing, ""), 
                weight=6.0, 
                category="advice"
            ))

        return self.generate_narrative(items)
    
    def _check_month_relation(self, dm: str, month: str) -> Optional[str]:
        # 简化版：仅判定是否得令
        # 实际应包含十二长生和十神格
        # 五行对应：寅卯木，巳午火，申酉金，亥子水，辰戌丑未土
        season_map = {
            "寅": "木", "卯": "木",
            "巳": "火", "午": "火",
            "申": "金", "酉": "金",
            "亥": "水", "子": "水",
            "辰": "土", "戌": "土", "丑": "土", "未": "土"
        }
        dm_wx = self._get_wuxing(dm)
        month_wx = season_map.get(month)
        
        if not dm_wx or not month_wx:
            return None
            
        if dm_wx == month_wx:
            return f"日主得令，生于{month}月，自身能量强旺，个性坚定，但也易固执"
        elif self._is_generating(month_wx, dm_wx):
            return f"日主得月令相生，如{month}月滋养，得长辈或环境助力"
        elif self._is_controlling(dm_wx, month_wx):
            return f"日主克月令，属于掌控型人格，具备开拓精神，但也较为辛苦"
        elif self._is_controlling(month_wx, dm_wx):
            return f"月令克身，环境压力较大，但也更能磨练意志，成大器者多出于此"
        else: # 我生月令
            return f"日主生月令，才华发泄于外，聪明秀气，但也易劳心劳力"

    def _get_wuxing(self, stems: str) -> Optional[str]:
        mapping = {
            "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
            "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"
        }
        return mapping.get(stems)
        
    def _is_generating(self, w1, w2):
        # w1 生 w2
        cycle = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
        return cycle.get(w1) == w2

    def _is_controlling(self, w1, w2):
        # w1 克 w2
        cycle = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
        return cycle.get(w1) == w2

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
        items.append(AnalyticItem(
            content=f"命宫主星为{star_str}，这是你性格的核心底色", 
            weight=10.0, 
            category="core"
        ))
        
        # 2. 组合逻辑 (双星组合)
        if "紫微" in ming_stars and "天府" in ming_stars:
            items.append(AnalyticItem(
                content="【紫府同宫】格：南斗北斗帝星汇聚，气度恢弘，具备极强的领导力与财富管理能力，但也容易过分保守或自视甚高", 
                weight=9.5, 
                category="core"
            ))
            
        elif "紫微" in ming_stars and "贪狼" in ming_stars:
            items.append(AnalyticItem(
                content="【紫贪同宫】格：也就是所谓的'桃花犯主'，这并非贬义，而是指人缘极佳，长袖善舞，极具交际手腕，适合公关、演艺或营销行业", 
                weight=9.0, 
                category="personality"
            ))
            
        # 3. 单星逻辑
        elif "紫微" in ming_stars:
            items.append(AnalyticItem(
                content="具备帝王之气，耳软心活，但也容易因为缺乏辅佐而感到孤独（孤君）", 
                weight=8.0, 
                category="personality"
            ))
            
        if "天机" in ming_stars:
            items.append(AnalyticItem(
                content="心思缜密，擅长筹划，是天生的军师型人才，但容易思多行少，神经紧张", 
                weight=7.5, 
                category="personality"
            ))
            
        if "太阳" in ming_stars:
            items.append(AnalyticItem(
                content="性格光明磊落，乐于助人，所谓'贵'气所在。但往往只顾付出不求回报，容易劳碌", 
                weight=7.5, 
                category="personality"
            ))
            
        if "武曲" in ming_stars:
            items.append(AnalyticItem(
                content="刚毅果决，执行力强，对金钱敏感，适合经商或金融，但略显不解风情", 
                weight=7.5, 
                category="advice"
            ))

        if "天同" in ming_stars:
            items.append(AnalyticItem(
                content="福星坐命，心态平和，知足常乐，但这在竞争激烈的环境中可能表现为缺乏进取心", 
                weight=7.0, 
                category="personality"
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
        items.append(AnalyticItem(
            content=f"得卦【{gua_name}】，此卦为您当前的主要处境", 
            weight=10.0, 
            category="core"
        ))
        
        # 特殊卦象判定
        if gua_name == "乾为天":
            items.append(AnalyticItem(content="乾卦象征天道刚健，不仅要自强不息，更要审时度势（潜见惕跃飞亢）", weight=9.0, category="advice"))
        elif gua_name == "坤为地":
            items.append(AnalyticItem(content="坤卦象征地道柔顺，厚德载物，此时不宜通过激进手段强取，而应顺势而为，以静制动", weight=9.0, category="advice"))
        elif gua_name == "水火既济":
            items.append(AnalyticItem(content="事情处于完美或完成的阶段，但也预示着盛极而衰的可能，需防微杜渐", weight=8.5, category="core"))
        elif gua_name == "火水未济":
            items.append(AnalyticItem(content="虽然目前看似混乱或未成功，但蕴含着无限生机，是新的开始", weight=8.5, category="core"))
            
        # 2. 动爻具体分析
        if dong_yao:
            items.append(AnalyticItem(
                content=f"变爻在第{dong_yao}爻，这是事情发展的关键转折点", 
                weight=8.0, 
                category="core"
            ))
            
            # 简单的爻位逻辑
            if dong_yao == 1:
                items.append(AnalyticItem(content="初爻代表事物萌芽阶段，根基未稳，宜潜藏勿用", weight=7.0, category="advice"))
            elif dong_yao == 2:
                items.append(AnalyticItem(content="二爻居中得位，通常代表良机出现，利于进取", weight=7.0, category="advice"))
            elif dong_yao == 3:
                items.append(AnalyticItem(content="三爻位置尴尬（不中不正），常伴随危机，需格外谨慎", weight=7.0, category="advice"))
            elif dong_yao == 4:
                items.append(AnalyticItem(content="四爻近君（五爻），如伴虎侧，需柔顺以待，避免功高盖主", weight=7.0, category="advice"))
            elif dong_yao == 5:
                items.append(AnalyticItem(content="五爻为尊位，代表事物发展到顶峰，此时最为强盛", weight=7.0, category="advice"))
            elif dong_yao == 6:
                items.append(AnalyticItem(content="上爻往往代表物极必反，需考虑退路或新的循环", weight=7.0, category="advice"))
        else:
            items.append(AnalyticItem(
                content="此卦无动爻，更加强调本卦特质的稳定性，事情短期内变数较小", 
                weight=7.0, 
                category="core"
            ))

        return self.generate_narrative(items)
