"""
玄心理命 - 心理学模块单元测试
"""

import pytest
from app.core.psychology.mbti import calculate_mbti, get_mbti_questions, MBTI_TYPES
from app.core.psychology.big5 import calculate_big5, get_big5_questions
from app.core.psychology.archetype import calculate_archetype, get_archetype_questions
from app.core.psychology.enneagram import calculate_enneagram, get_enneagram_questions


class TestMBTI:
    """MBTI测试"""
    
    def test_get_questions(self):
        """测试获取题目"""
        questions = get_mbti_questions()
        assert len(questions) == 32
        for q in questions:
            assert "id" in q
            assert "question" in q
            assert "options" in q
    
    def test_calculate_all_a(self):
        """测试全选A"""
        answers = [{"question_id": i, "answer": "A"} for i in range(32)]
        result = calculate_mbti(answers)
        
        assert result is not None
        assert "type_code" in result
        assert len(result["type_code"]) == 4
        assert result["type_code"] in MBTI_TYPES
    
    def test_calculate_all_b(self):
        """测试全选B"""
        answers = [{"question_id": i, "answer": "B"} for i in range(32)]
        result = calculate_mbti(answers)
        
        assert result is not None
        assert "type_code" in result
    
    def test_calculate_mixed(self):
        """测试混合选择"""
        answers = [{"question_id": i, "answer": "A" if i % 2 == 0 else "B"} for i in range(32)]
        result = calculate_mbti(answers)
        
        assert result is not None
        assert "dimensions" in result
        assert "E" in result["dimensions"] or "I" in result["dimensions"]


class TestBig5:
    """大五人格测试"""
    
    def test_get_questions(self):
        """测试获取题目"""
        questions = get_big5_questions()
        assert len(questions) == 60
    
    def test_calculate_mid_scores(self):
        """测试中等分数"""
        answers = [{"question_id": i, "score": 3} for i in range(60)]
        result = calculate_big5(answers)
        
        assert result is not None
        assert "scores" in result
        scores = result["scores"]
        assert "O" in scores  # 开放性
        assert "C" in scores  # 尽责性
        assert "E" in scores  # 外向性
        assert "A" in scores  # 宜人性
        assert "N" in scores  # 神经质
    
    def test_calculate_high_scores(self):
        """测试高分"""
        answers = [{"question_id": i, "score": 5} for i in range(60)]
        result = calculate_big5(answers)
        
        assert result is not None
        for dim, score in result["scores"].items():
            assert score >= 60  # 高分应该 >= 60


class TestArchetype:
    """荣格原型测试"""
    
    def test_get_questions(self):
        """测试获取题目"""
        questions = get_archetype_questions()
        assert len(questions) == 36
    
    def test_calculate(self):
        """测试计算"""
        answers = [{"question_id": i, "score": 3 + (i % 3)} for i in range(36)]
        result = calculate_archetype(answers)
        
        assert result is not None
        assert "primary" in result
        assert "secondary" in result
        assert "scores" in result


class TestEnneagram:
    """九型人格测试"""
    
    def test_get_questions(self):
        """测试获取题目"""
        questions = get_enneagram_questions()
        assert len(questions) == 36
    
    def test_calculate(self):
        """测试计算"""
        answers = [{"question_id": i, "score": 3 + (i % 3)} for i in range(36)]
        result = calculate_enneagram(answers)
        
        assert result is not None
        assert "primary_type" in result
        assert 1 <= result["primary_type"] <= 9
        assert "wing" in result
        assert "scores" in result
