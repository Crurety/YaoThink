"""
玄心理命 - 个性化报告生成器
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json


# ==================== 报告模板 ====================

REPORT_TEMPLATES = {
    "personality_intro": """
## 🌟 你的人格画像

根据东方命理与西方心理学的综合分析，我们为你绘制了一幅独特的人格画像。

{personality_description}

### 核心特质
{core_traits}

### 你的优势
{strengths}

### 成长空间
{growth_areas}
""",

    "east_west_comparison": """
## ☯️ 东西方视角对照

### 东方命理视角
{eastern_view}

### 西方心理学视角
{western_view}

### 融合洞察
{fusion_insight}
""",

    "life_guidance": """
## 🧭 人生发展指南

### 💼 事业发展
{career_guidance}

### 💕 人际关系
{relationship_guidance}

### 🌱 个人成长
{growth_guidance}

### ⚠️ 注意事项
{caution_notes}
""",

    "compatibility_section": """
## 💞 关系兼容分析

### 与{partner_type}的相处

**兼容度**: {compatibility_score}/100

**优势互补**:
{complementary_points}

**潜在挑战**:
{challenge_points}

**相处建议**:
{relationship_advice}
""",

    "summary": """
## 📋 总结

{summary_text}

---
*分析时间: {analysis_time}*
*置信度: {confidence}%*
*数据来源: {data_sources}*
"""
}


# ==================== 报告生成器 ====================

@dataclass
class ReportSection:
    """报告章节"""
    title: str
    content: str
    order: int


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self):
        self.templates = REPORT_TEMPLATES
    
    def generate_full_report(
        self,
        fusion_result: Dict,
        user_info: Optional[Dict] = None
    ) -> str:
        """
        生成完整分析报告
        
        Args:
            fusion_result: 融合分析结果
            user_info: 用户信息 (可选)
        
        Returns:
            Markdown格式的完整报告
        """
        sections = []
        
        # 1. 标题
        title = self._generate_title(user_info)
        sections.append(title)
        
        # 2. 人格画像
        personality_section = self._generate_personality_section(fusion_result)
        sections.append(personality_section)
        
        # 3. 东西方对照
        comparison_section = self._generate_comparison_section(fusion_result)
        sections.append(comparison_section)
        
        # 4. 人生指导
        guidance_section = self._generate_guidance_section(fusion_result)
        sections.append(guidance_section)
        
        # 5. 总结
        summary_section = self._generate_summary_section(fusion_result)
        sections.append(summary_section)
        
        return "\n\n".join(sections)
    
    def _generate_title(self, user_info: Optional[Dict]) -> str:
        """生成报告标题"""
        name = user_info.get("name", "您") if user_info else "您"
        date = datetime.now().strftime("%Y年%m月%d日")
        
        return f"""# 🔮 {name}的命理心理融合分析报告

*生成日期: {date}*

---"""
    
    def _generate_personality_section(self, fusion_result: Dict) -> str:
        """生成人格画像章节"""
        personality = fusion_result.get("personality_fusion", {})
        
        core_traits = personality.get("core_traits", [])
        strengths = personality.get("strengths", [])
        challenges = personality.get("challenges", [])
        description = personality.get("description", "")
        
        traits_text = "\n".join([f"- {t}" for t in core_traits]) if core_traits else "- 待分析"
        strengths_text = "\n".join([f"- ✅ {s}" for s in strengths]) if strengths else "- 待分析"
        growth_text = "\n".join([f"- 🎯 {c}" for c in challenges]) if challenges else "- 持续关注"
        
        return self.templates["personality_intro"].format(
            personality_description=description or "根据您的命理和心理测试结果，您具有独特的人格特质。",
            core_traits=traits_text,
            strengths=strengths_text,
            growth_areas=growth_text
        )
    
    def _generate_comparison_section(self, fusion_result: Dict) -> str:
        """生成东西方对照章节"""
        consistency = fusion_result.get("consistency_analysis", {})
        
        # 东方视角
        bazi = fusion_result.get("bazi_analysis", {})
        ziwei = fusion_result.get("ziwei_analysis", {})
        
        eastern_points = []
        if bazi:
            wuxing = bazi.get("wuxing", {})
            if wuxing:
                strongest = max(wuxing, key=wuxing.get) if wuxing else "平衡"
                eastern_points.append(f"- 五行偏{strongest}，{self._get_wuxing_meaning(strongest)}")
        
        if not eastern_points:
            eastern_points.append("- 需要提供出生信息进行分析")
        
        eastern_view = "\n".join(eastern_points)
        
        # 西方视角
        mbti = fusion_result.get("mbti_result", {})
        big5 = fusion_result.get("big5_result", {})
        archetype = fusion_result.get("archetype_result", {})
        
        western_points = []
        if mbti:
            western_points.append(f"- MBTI类型: {mbti.get('type', '待测')}")
        if archetype:
            western_points.append(f"- 荣格原型: {archetype.get('primary', '待测')}")
        
        if not western_points:
            western_points.append("- 需要完成心理测试进行分析")
        
        western_view = "\n".join(western_points)
        
        # 融合洞察
        matches = consistency.get("matches", [])
        conflicts = consistency.get("conflicts", [])
        
        fusion_points = []
        for match in matches:
            fusion_points.append(f"✅ {match.get('description', '')}")
        for conflict in conflicts:
            fusion_points.append(f"🔄 {conflict.get('insight', conflict.get('description', ''))}")
        
        if not fusion_points:
            score = consistency.get("score", 50)
            fusion_points.append(f"综合一致性: {score}%")
        
        fusion_insight = "\n".join(fusion_points)
        
        return self.templates["east_west_comparison"].format(
            eastern_view=eastern_view,
            western_view=western_view,
            fusion_insight=fusion_insight
        )
    
    def _generate_guidance_section(self, fusion_result: Dict) -> str:
        """生成人生指导章节"""
        guidance = fusion_result.get("life_guidance", {})
        
        career = guidance.get("career", [])
        relationship = guidance.get("relationship", [])
        growth = guidance.get("growth", [])
        caution = guidance.get("caution", [])
        
        career_text = "\n".join([f"- {c}" for c in career]) if career else "- 发挥个人优势，寻找适合的发展方向"
        relationship_text = "\n".join([f"- {r}" for r in relationship]) if relationship else "- 真诚待人，建立深度连接"
        growth_text = "\n".join([f"- {g}" for g in growth]) if growth else "- 持续学习，保持开放心态"
        caution_text = "\n".join([f"- {c}" for c in caution]) if caution else "- 平衡发展，避免过度"
        
        return self.templates["life_guidance"].format(
            career_guidance=career_text,
            relationship_guidance=relationship_text,
            growth_guidance=growth_text,
            caution_notes=caution_text
        )
    
    def _generate_summary_section(self, fusion_result: Dict) -> str:
        """生成总结章节"""
        confidence = fusion_result.get("confidence", 50)
        analysis_time = fusion_result.get("analysis_time", datetime.now().isoformat())
        
        # 数据来源统计
        sources = []
        if fusion_result.get("bazi_analysis"):
            sources.append("八字命理")
        if fusion_result.get("ziwei_analysis"):
            sources.append("紫微斗数")
        if fusion_result.get("mbti_result"):
            sources.append("MBTI")
        if fusion_result.get("big5_result"):
            sources.append("大五人格")
        if fusion_result.get("archetype_result"):
            sources.append("荣格原型")
        if fusion_result.get("enneagram_result"):
            sources.append("九型人格")
        
        sources_text = "、".join(sources) if sources else "基础分析"
        
        # 生成总结文本
        personality = fusion_result.get("personality_fusion", {})
        core_traits = personality.get("core_traits", [])
        
        summary = f"您具有{'、'.join(core_traits[:3]) if core_traits else '独特'}的人格特质。"
        summary += f"本报告基于{len(sources)}个数据源的综合分析，置信度为{confidence}%。"
        summary += "建议定期回顾本报告，并在人生重要决策时参考相关建议。"
        
        return self.templates["summary"].format(
            summary_text=summary,
            analysis_time=analysis_time[:10] if len(analysis_time) > 10 else analysis_time,
            confidence=confidence,
            data_sources=sources_text
        )
    
    def _get_wuxing_meaning(self, wuxing: str) -> str:
        """获取五行含义"""
        meanings = {
            "木": "富有生机和创造力",
            "火": "热情洋溢，善于表达",
            "土": "稳重踏实，值得信赖",
            "金": "果断明快，追求效率",
            "水": "智慧深沉，善于洞察"
        }
        return meanings.get(wuxing, "性格平衡")
    
    def generate_mini_report(self, fusion_result: Dict) -> Dict:
        """
        生成简化版报告 (用于API返回)
        
        Returns:
            字典格式的简化报告
        """
        personality = fusion_result.get("personality_fusion", {})
        consistency = fusion_result.get("consistency_analysis", {})
        guidance = fusion_result.get("life_guidance", {})
        
        return {
            "summary": personality.get("description", ""),
            "core_traits": personality.get("core_traits", [])[:5],
            "strengths": personality.get("strengths", [])[:3],
            "challenges": personality.get("challenges", [])[:3],
            "consistency_score": consistency.get("score", 50),
            "top_career": guidance.get("career", [])[:3],
            "key_advice": guidance.get("growth", [])[:2],
            "confidence": fusion_result.get("confidence", 50)
        }


# 快捷函数
def generate_report(fusion_result: Dict, format: str = "markdown") -> str:
    """
    生成分析报告
    
    Args:
        fusion_result: 融合分析结果
        format: 输出格式 (markdown/json)
    
    Returns:
        报告内容
    """
    generator = ReportGenerator()
    
    if format == "json":
        return json.dumps(generator.generate_mini_report(fusion_result), ensure_ascii=False, indent=2)
    else:
        return generator.generate_full_report(fusion_result)
