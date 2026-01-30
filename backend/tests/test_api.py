"""
玄心理命 - API集成测试
"""

import pytest
from httpx import AsyncClient


class TestHealthEndpoints:
    """健康检查端点测试"""
    
    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """测试健康检查"""
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestBaziAPI:
    """八字API测试"""
    
    @pytest.mark.asyncio
    async def test_calculate_endpoint(self, client: AsyncClient, sample_birth_data):
        """测试八字计算端点"""
        response = await client.post("/api/bazi/calculate", json=sample_birth_data)
        assert response.status_code == 200
        data = response.json()
        assert "four_pillars" in data or "success" in data


class TestPsychologyAPI:
    """心理学API测试"""
    
    @pytest.mark.asyncio
    async def test_get_mbti_questions(self, client: AsyncClient):
        """测试获取MBTI题目"""
        response = await client.get("/api/psychology/mbti/questions")
        assert response.status_code == 200
        data = response.json()
        assert "questions" in data
        assert len(data["questions"]) == 32
    
    @pytest.mark.asyncio
    async def test_submit_mbti(self, client: AsyncClient, sample_mbti_answers):
        """测试提交MBTI答案"""
        response = await client.post(
            "/api/psychology/mbti/submit",
            json={"answers": sample_mbti_answers}
        )
        assert response.status_code == 200
        data = response.json()
        assert "type_code" in data or "result" in data
    
    @pytest.mark.asyncio
    async def test_get_big5_questions(self, client: AsyncClient):
        """测试获取大五题目"""
        response = await client.get("/api/psychology/big5/questions")
        assert response.status_code == 200
        data = response.json()
        assert "questions" in data
        assert len(data["questions"]) == 60


class TestYijingAPI:
    """易经API测试"""
    
    @pytest.mark.asyncio
    async def test_meihua_divination(self, client: AsyncClient, sample_yijing_question):
        """测试梅花起卦"""
        response = await client.post("/api/yijing/meihua", json=sample_yijing_question)
        assert response.status_code == 200
        data = response.json()
        assert "hexagram" in data or "success" in data


class TestFusionAPI:
    """融合分析API测试"""
    
    @pytest.mark.asyncio
    async def test_fusion_info(self, client: AsyncClient):
        """测试融合分析信息"""
        response = await client.get("/api/fusion/info")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "features" in data
    
    @pytest.mark.asyncio
    async def test_quick_fusion(self, client: AsyncClient):
        """测试快速融合分析"""
        response = await client.post("/api/fusion/quick", json={
            "mbti_type": "INTJ",
            "wuxing_scores": {"木": 25, "火": 15, "土": 20, "金": 30, "水": 40}
        })
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
    
    @pytest.mark.asyncio
    async def test_mapping_mbti(self, client: AsyncClient):
        """测试MBTI映射"""
        response = await client.get("/api/fusion/mapping/mbti/INTJ")
        assert response.status_code == 200
        data = response.json()
        assert "mbti_type" in data
        assert "mapping" in data
