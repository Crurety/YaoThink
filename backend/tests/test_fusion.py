"""
玄心理命 - 融合分析模块单元测试
"""

import pytest
from app.fusion.mapper import (
    WUXING_MBTI_MAP,
    MBTI_WUXING_MAP,
    get_wuxing_psychology,
    get_shishen_psychology,
    map_mbti_to_wuxing
)
from app.fusion.analyzer import FusionAnalyzer, quick_fusion_analysis
from app.fusion.report import ReportGenerator, generate_report


class TestMapper:
    """映射模块测试"""
    
    def test_wuxing_mbti_map_complete(self):
        """测试五行映射完整性"""
        wuxing_list = ["木", "火", "土", "金", "水"]
        for wx in wuxing_list:
            assert wx in WUXING_MBTI_MAP
            assert "mbti_tendencies" in WUXING_MBTI_MAP[wx]
            assert "mbti_types" in WUXING_MBTI_MAP[wx]
    
    def test_mbti_wuxing_map_complete(self):
        """测试MBTI映射完整性"""
        mbti_types = [
            "INTJ", "INTP", "ENTJ", "ENTP",
            "INFJ", "INFP", "ENFJ", "ENFP",
            "ISTJ", "ISFJ", "ESTJ", "ESFJ",
            "ISTP", "ISFP", "ESTP", "ESFP"
        ]
        for mbti in mbti_types:
            assert mbti in MBTI_WUXING_MAP
    
    def test_get_wuxing_psychology(self):
        """测试五行心理分析"""
        wuxing_scores = {"木": 30, "火": 20, "土": 15, "金": 25, "水": 10}
        result = get_wuxing_psychology(wuxing_scores)
        
        assert result is not None
        assert "dominant" in result
        assert "traits" in result
    
    def test_map_mbti_to_wuxing(self):
        """测试MBTI到五行映射"""
        result = map_mbti_to_wuxing("INTJ")
        
        assert result is not None
        assert "primary" in result


class TestFusionAnalyzer:
    """融合分析器测试"""
    
    def test_quick_analysis(self):
        """测试快速分析"""
        result = quick_fusion_analysis(mbti_type="INTJ")
        
        assert result is not None
    
    def test_full_analysis(self):
        """测试完整分析"""
        analyzer = FusionAnalyzer()
        result = analyzer.analyze(
            mbti_type="INTJ",
            big5_scores={"O": 75, "C": 70, "E": 35, "A": 50, "N": 40}
        )
        
        assert result is not None
        assert result.personality_fusion is not None
        assert result.life_guidance is not None
    
    def test_consistency_analysis(self):
        """测试一致性分析"""
        analyzer = FusionAnalyzer()
        result = analyzer.analyze(
            mbti_type="INTJ",
            bazi_data={
                "wuxing": {"木": 20, "火": 15, "土": 20, "金": 30, "水": 40}
            }
        )
        
        assert result.consistency_analysis is not None
        assert "score" in result.consistency_analysis


class TestReportGenerator:
    """报告生成器测试"""
    
    def test_generate_markdown_report(self):
        """测试Markdown报告生成"""
        fusion_result = {
            "personality_fusion": {
                "core_traits": ["理性", "分析"],
                "strengths": ["逻辑思维"],
                "challenges": ["情感表达"],
                "description": "测试描述"
            },
            "consistency_analysis": {
                "score": 75,
                "matches": [],
                "insights": []
            },
            "life_guidance": {
                "career": ["技术"],
                "growth": ["沟通"]
            },
            "confidence": 80
        }
        
        report = generate_report(fusion_result, format="markdown")
        
        assert report is not None
        assert "人格画像" in report
        assert "东西方" in report
    
    def test_generate_mini_report(self):
        """测试简化报告"""
        generator = ReportGenerator()
        fusion_result = {
            "personality_fusion": {
                "core_traits": ["理性"],
                "strengths": ["逻辑"],
                "challenges": [],
                "description": "测试"
            },
            "consistency_analysis": {"score": 70},
            "life_guidance": {"career": ["分析"], "growth": []},
            "confidence": 75
        }
        
        mini = generator.generate_mini_report(fusion_result)
        
        assert "summary" in mini
        assert "core_traits" in mini
        assert "confidence" in mini
