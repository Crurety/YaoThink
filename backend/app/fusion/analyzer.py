"""
玄心理命 - 融合分析引擎
综合东方玄学与西方心理学的分析
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

from .mapper import (
    get_wuxing_psychology,
    get_shishen_psychology,
    map_mbti_to_wuxing,
    map_palace_to_psychology,
    get_star_psychology,
    get_palace_stars_psychology,
    WUXING_MBTI_MAP,
    MBTI_WUXING_MAP,
    SHISHEN_ARCHETYPE_MAP,
    PALACE_LIFE_DOMAIN_MAP,
    ZIWEI_STAR_PSYCHOLOGY_MAP
)


# ==================== 融合分析结果 ====================

@dataclass
class FusionResult:
    """融合分析结果"""
    # 东方分析
    bazi_analysis: Optional[Dict] = None
    ziwei_analysis: Optional[Dict] = None
    yijing_analysis: Optional[Dict] = None
    
    # 西方分析
    mbti_result: Optional[Dict] = None
    big5_result: Optional[Dict] = None
    archetype_result: Optional[Dict] = None
    enneagram_result: Optional[Dict] = None
    
    # 融合分析
    personality_fusion: Dict = field(default_factory=dict)
    consistency_analysis: Dict = field(default_factory=dict)
    life_guidance: Dict = field(default_factory=dict)
    
    # 元数据
    analysis_time: str = ""
    confidence: float = 0.0


# ==================== 核心分析引擎 ====================

class FusionAnalyzer:
    """融合分析器"""
    
    def __init__(self):
        self.wuxing_map = WUXING_MBTI_MAP
        self.shishen_map = SHISHEN_ARCHETYPE_MAP
        self.palace_map = PALACE_LIFE_DOMAIN_MAP
    
    def analyze(
        self,
        bazi_data: Optional[Dict] = None,
        ziwei_data: Optional[Dict] = None,
        mbti_type: Optional[str] = None,
        big5_scores: Optional[Dict] = None,
        archetype: Optional[str] = None,
        enneagram_type: Optional[int] = None
    ) -> FusionResult:
        """
        执行综合分析
        
        Args:
            bazi_data: 八字分析结果
            ziwei_data: 紫微分析结果
            mbti_type: MBTI类型
            big5_scores: 大五人格分数
            archetype: 荣格原型
            enneagram_type: 九型人格类型
        
        Returns:
            融合分析结果
        """
        result = FusionResult()
        result.analysis_time = datetime.now().isoformat()
        
        # 存储原始数据
        result.bazi_analysis = bazi_data
        result.ziwei_analysis = ziwei_data
        result.mbti_result = {"type": mbti_type} if mbti_type else None
        result.big5_result = big5_scores
        result.archetype_result = {"primary": archetype} if archetype else None
        result.enneagram_result = {"type": enneagram_type} if enneagram_type else None
        
        # 执行融合分析
        result.personality_fusion = self._fuse_personality(
            bazi_data, ziwei_data, mbti_type, big5_scores, archetype, enneagram_type
        )
        
        # 一致性分析
        result.consistency_analysis = self._analyze_consistency(
            bazi_data, mbti_type, archetype, enneagram_type
        )
        
        # 人生指导
        result.life_guidance = self._generate_guidance(
            bazi_data, ziwei_data, mbti_type, big5_scores
        )
        
        # 计算置信度
        result.confidence = self._calculate_confidence(
            bazi_data, ziwei_data, mbti_type, big5_scores
        )
        
        return result
    
    def _fuse_personality(
        self,
        bazi: Optional[Dict],
        ziwei: Optional[Dict],
        mbti: Optional[str],
        big5: Optional[Dict],
        archetype: Optional[str],
        enneagram: Optional[int]
    ) -> Dict:
        """融合人格分析"""
        fusion = {
            "core_traits": [],
            "strengths": [],
            "challenges": [],
            "potential": [],
            "ziwei_insights": {},
            "description": ""
        }
        
        # 从八字提取五行人格
        if bazi and "wuxing" in bazi:
            wuxing_analysis = get_wuxing_psychology(bazi["wuxing"])
            fusion["core_traits"].extend(wuxing_analysis.get("primary_traits", []))
            fusion["potential"].extend(wuxing_analysis.get("development_areas", []))
            
            # 与MBTI对比
            if mbti:
                mbti_wuxing = map_mbti_to_wuxing(mbti)
                if mbti_wuxing.get("primary") == wuxing_analysis.get("strongest_wuxing"):
                    fusion["strengths"].append("东西方分析高度一致")
        
        # 从十神提取原型
        if bazi and "shishen" in bazi:
            shishen_analysis = get_shishen_psychology(bazi["shishen"])
            predicted_archetype = shishen_analysis.get("primary_archetype")
            
            if archetype and predicted_archetype == archetype:
                fusion["strengths"].append("十神与原型高度吻合")
            
            fusion["core_traits"].append(f"原型倾向: {predicted_archetype}")
        
        # ===== 从紫微斗数提取星曜人格 =====
        if ziwei:
            ziwei_palace_analysis = self._analyze_ziwei_palaces(ziwei)
            fusion["ziwei_insights"] = ziwei_palace_analysis
            
            # 提取命宫主星特质到核心特质
            ming_gong = ziwei_palace_analysis.get("命宫", {})
            if ming_gong:
                ming_keywords = ming_gong.get("star_keywords", [])
                if ming_keywords:
                    fusion["core_traits"].extend(ming_keywords[:4])
                
                ming_archetype = ming_gong.get("primary_archetype")
                if ming_archetype:
                    fusion["core_traits"].append(f"紫微原型: {ming_archetype}")
                    
                    # 与用户荣格测试结果对比
                    if archetype and ming_archetype == archetype:
                        fusion["strengths"].append("紫微星曜与荣格原型高度吻合")
                    
                    # 与MBTI对比
                    if mbti:
                        star_mbti_tendencies = ming_gong.get("mbti_tendencies", [])
                        mbti_match_count = sum(1 for t in star_mbti_tendencies if t in mbti)
                        if mbti_match_count >= 2:
                            fusion["strengths"].append("紫微星曜与MBTI特质一致")
        
        # MBTI与大五融合
        if mbti and big5:
            mbti_traits = self._get_mbti_traits(mbti)
            fusion["core_traits"].extend(mbti_traits[:3])
            
            # 分析大五突出维度
            if big5:
                high_dims = [k for k, v in big5.items() if v >= 70]
                low_dims = [k for k, v in big5.items() if v <= 30]
                fusion["strengths"].extend([f"高{d}" for d in high_dims])
                fusion["challenges"].extend([f"低{d}" for d in low_dims])
        
        # 生成综合描述
        fusion["description"] = self._generate_personality_description(fusion)
        
        return fusion
    
    def _analyze_ziwei_palaces(self, ziwei_data: Dict) -> Dict:
        """
        分析紫微宫位与心理领域
        
        Args:
            ziwei_data: 紫微分析结果，需包含 'palaces' 或 'chart_data.palaces' 字段
        
        Returns:
            每个宫位的星曜心理分析
        """
        palace_insights = {}
        
        # 兼容不同的数据结构
        palaces_list = []
        if "chart_data" in ziwei_data and "palaces" in ziwei_data["chart_data"]:
            palaces_list = ziwei_data["chart_data"]["palaces"]
        elif "palaces" in ziwei_data:
            palaces_list = ziwei_data["palaces"]
        
        # 关键宫位优先分析
        key_palaces = ["命宫", "官禄宫", "财帛宫", "夫妻宫", "福德宫", "迁移宫"]
        
        for palace in palaces_list:
            palace_name = palace.get("name", "")
            if not palace_name:
                continue
            
            # 获取宫位的心理学映射
            palace_mapping = map_palace_to_psychology(palace_name)
            
            # 提取主星列表
            stars_main = []
            stars_data = palace.get("stars", {})
            if isinstance(stars_data, dict):
                stars_main = stars_data.get("main", [])
            elif "major_stars" in palace:
                stars_main = palace.get("major_stars", [])
            
            if not stars_main:
                continue
            
            # 获取星曜综合心理分析
            star_psychology = get_palace_stars_psychology(stars_main)
            
            palace_insights[palace_name] = {
                "life_domains": palace_mapping.get("life_domains", []),
                "psychology_aspects": palace_mapping.get("psychology_aspects", []),
                "questions": palace_mapping.get("questions", []),
                "stars": [s.get("name") if isinstance(s, dict) else s for s in stars_main],
                "star_keywords": star_psychology.get("keywords", []),
                "primary_archetype": star_psychology.get("primary_archetype"),
                "mbti_tendencies": star_psychology.get("primary_mbti_tendencies", []),
                "big5_adjustments": star_psychology.get("big5", {}),
                "descriptions": star_psychology.get("descriptions", [])
            }
        
        return palace_insights
    
    def _analyze_consistency(
        self,
        bazi: Optional[Dict],
        mbti: Optional[str],
        archetype: Optional[str],
        enneagram: Optional[int]
    ) -> Dict:
        """分析东西方结果的一致性"""
        consistency = {
            "score": 0,
            "matches": [],
            "conflicts": [],
            "insights": []
        }
        
        matches = 0
        total_comparisons = 0
        
        # 五行与MBTI一致性
        if bazi and "wuxing" in bazi and mbti:
            total_comparisons += 1
            wuxing_analysis = get_wuxing_psychology(bazi["wuxing"])
            mbti_wuxing = map_mbti_to_wuxing(mbti)
            
            if wuxing_analysis.get("strongest_wuxing") == mbti_wuxing.get("primary"):
                matches += 1
                consistency["matches"].append({
                    "aspect": "五行与MBTI",
                    "description": f"命局五行{wuxing_analysis['strongest_wuxing']}与MBTI {mbti}的{mbti_wuxing['primary']}属性一致"
                })
            else:
                consistency["conflicts"].append({
                    "aspect": "五行与MBTI",
                    "description": f"命局五行偏{wuxing_analysis['strongest_wuxing']}，但MBTI显示{mbti_wuxing['primary']}特质",
                    "insight": "这可能表示你有未被发掘的潜力，或者正在经历人格成长"
                })
        
        # 十神与原型一致性
        if bazi and "shishen" in bazi and archetype:
            total_comparisons += 1
            shishen_analysis = get_shishen_psychology(bazi["shishen"])
            predicted = shishen_analysis.get("primary_archetype")
            
            if predicted == archetype:
                matches += 1
                consistency["matches"].append({
                    "aspect": "十神与原型",
                    "description": f"命局十神预测原型{predicted}与测试结果一致"
                })
            else:
                consistency["insights"].append(
                    f"命局暗示{predicted}原型，而测试显示{archetype}，说明你可能正在发展新的人格面向"
                )
        
        # 计算一致性分数
        if total_comparisons > 0:
            consistency["score"] = round((matches / total_comparisons) * 100)
        else:
            consistency["score"] = 50  # 默认中等一致性
        
        return consistency
    
    def _generate_guidance(
        self,
        bazi: Optional[Dict],
        ziwei: Optional[Dict],
        mbti: Optional[str],
        big5: Optional[Dict]
    ) -> Dict:
        """生成人生指导建议"""
        guidance = {
            "career": [],
            "relationship": [],
            "growth": [],
            "caution": []
        }
        
        # 基于MBTI的职业建议
        career_map = {
            "INTJ": ["战略顾问", "科学家", "系统架构师"],
            "INTP": ["研究员", "程序员", "分析师"],
            "ENTJ": ["CEO", "企业家", "项目经理"],
            "ENTP": ["创业者", "咨询师", "产品经理"],
            "INFJ": ["心理咨询师", "作家", "人力资源"],
            "INFP": ["艺术家", "作家", "心理学家"],
            "ENFJ": ["教师", "培训师", "公关经理"],
            "ENFP": ["营销", "创意总监", "记者"],
            "ISTJ": ["会计师", "审计员", "项目经理"],
            "ISFJ": ["护士", "行政", "客服经理"],
            "ESTJ": ["经理", "军官", "法官"],
            "ESFJ": ["人力资源", "社工", "销售经理"],
            "ISTP": ["工程师", "技术专家", "飞行员"],
            "ISFP": ["设计师", "艺术家", "美容师"],
            "ESTP": ["销售", "企业家", "运动员"],
            "ESFP": ["演员", "活动策划", "导游"]
        }
        
        if mbti and mbti in career_map:
            guidance["career"] = career_map[mbti]
        
        # 基于大五的成长建议
        if big5:
            if big5.get("N", 50) > 70:
                guidance["growth"].append("培养情绪调节能力，学习正念冥想")
                guidance["caution"].append("注意压力管理，避免焦虑积累")
            
            if big5.get("E", 50) < 30:
                guidance["growth"].append("适当扩展社交圈，但尊重自己的节奏")
            
            if big5.get("O", 50) < 30:
                guidance["growth"].append("尝试接受新事物，培养好奇心")
            
            if big5.get("C", 50) < 40:
                guidance["growth"].append("建立良好的时间管理和计划习惯")
            
            if big5.get("A", 50) < 40:
                guidance["relationship"].append("练习换位思考，提升共情能力")
        
        # 基于紫微宫位的建议
        if ziwei:
            ziwei_palace_analysis = self._analyze_ziwei_palaces(ziwei)
            
            # 官禄宫 - 事业建议
            guan_lu = ziwei_palace_analysis.get("官禄宫", {})
            if guan_lu:
                stars = guan_lu.get("stars", [])
                keywords = guan_lu.get("star_keywords", [])
                if stars:
                    star_str = "、".join(stars[:2])
                    guidance["career"].append(f"官禄宫坐{star_str}，适合发挥{','.join(keywords[:2])}的特质")
                guidance["career"].extend(guan_lu.get("questions", [])[:1])
            
            # 财帛宫 - 财运建议
            cai_bo = ziwei_palace_analysis.get("财帛宫", {})
            if cai_bo:
                archetype = cai_bo.get("primary_archetype")
                if archetype:
                    archetype_advice = {
                        "RULER": "适合管理型理财，可考虑投资管理岗位",
                        "SAGE": "适合知识变现，咨询类收入",
                        "HERO": "适合开拓性收入，创业或销售",
                        "EXPLORER": "适合多元化投资，不宜守成",
                        "CAREGIVER": "适合稳健理财，服务行业收入",
                        "CREATOR": "适合创意类收入，设计或内容创作"
                    }
                    if archetype in archetype_advice:
                        guidance["growth"].append(archetype_advice[archetype])
            
            # 夫妻宫 - 关系建议
            fu_qi = ziwei_palace_analysis.get("夫妻宫", {})
            if fu_qi:
                keywords = fu_qi.get("star_keywords", [])
                if keywords:
                    guidance["relationship"].append(f"感情上倾向{','.join(keywords[:2])}的伴侣类型")
        
        return guidance
    
    def _get_mbti_traits(self, mbti: str) -> List[str]:
        """获取MBTI核心特质"""
        trait_map = {
            "I": "内向沉稳", "E": "外向活跃",
            "S": "注重实际", "N": "直觉创新",
            "T": "理性分析", "F": "情感导向",
            "J": "计划条理", "P": "灵活适应"
        }
        return [trait_map.get(c, "") for c in mbti if c in trait_map]
    
    def _generate_personality_description(self, fusion: Dict) -> str:
        """生成人格描述文本"""
        traits = fusion.get("core_traits", [])
        strengths = fusion.get("strengths", [])
        
        if not traits:
            return "需要更多数据来生成完整分析"
        
        desc = f"你的核心特质包括{'、'.join(traits[:4])}。"
        
        if strengths:
            desc += f"你的优势在于{'、'.join(strengths[:3])}。"
        
        return desc
    
    def _calculate_confidence(
        self,
        bazi: Optional[Dict],
        ziwei: Optional[Dict],
        mbti: Optional[str],
        big5: Optional[Dict]
    ) -> float:
        """计算分析置信度"""
        data_sources = 0
        if bazi:
            data_sources += 1
        if ziwei:
            data_sources += 1
        if mbti:
            data_sources += 1
        if big5:
            data_sources += 1
        
        # 数据源越多，置信度越高
        return min(data_sources * 25, 100)


# 快捷分析函数
def quick_fusion_analysis(
    mbti_type: str = None,
    wuxing_scores: Dict[str, float] = None,
    shishen_pattern: Dict[str, int] = None
) -> Dict:
    """
    快速融合分析
    
    Args:
        mbti_type: MBTI类型
        wuxing_scores: 五行得分
        shishen_pattern: 十神格局
    
    Returns:
        融合分析结果
    """
    result = {
        "mbti_analysis": None,
        "wuxing_analysis": None,
        "fusion_insight": ""
    }
    
    if mbti_type:
        result["mbti_analysis"] = map_mbti_to_wuxing(mbti_type)
    
    if wuxing_scores:
        result["wuxing_analysis"] = get_wuxing_psychology(wuxing_scores)
    
    if shishen_pattern:
        result["shishen_analysis"] = get_shishen_psychology(shishen_pattern)
    
    # 生成融合洞察
    insights = []
    if result["mbti_analysis"] and result["wuxing_analysis"]:
        mbti_wuxing = result["mbti_analysis"].get("primary", "")
        actual_wuxing = result["wuxing_analysis"].get("strongest_wuxing", "")
        
        if mbti_wuxing == actual_wuxing:
            insights.append(f"你的MBTI类型与命局五行都指向{actual_wuxing}属性，说明你有着高度一致的人格特质")
        else:
            insights.append(f"你的MBTI显示{mbti_wuxing}特质，而命局偏{actual_wuxing}，这种差异可能代表成长和变化")
    
    result["fusion_insight"] = " ".join(insights)
    
    return result
