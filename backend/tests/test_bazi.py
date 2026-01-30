"""
玄心理命 - 八字模块单元测试
"""

import pytest
from app.core.bazi.calculator import BaziCalculator
from app.core.bazi.calendar import LunarCalendar


class TestLunarCalendar:
    """农历转换测试"""
    
    def test_solar_to_lunar_basic(self):
        """测试公历转农历基本功能"""
        lunar = LunarCalendar.solar_to_lunar(1990, 6, 15)
        assert lunar is not None
        assert "year" in lunar
        assert "month" in lunar
        assert "day" in lunar
    
    def test_lunar_to_solar_basic(self):
        """测试农历转公历基本功能"""
        solar = LunarCalendar.lunar_to_solar(1990, 5, 23, False)
        assert solar is not None
    
    def test_get_jieqi(self):
        """测试获取节气"""
        jieqi = LunarCalendar.get_jieqi(1990)
        assert len(jieqi) == 24


class TestBaziCalculator:
    """八字计算测试"""
    
    def test_calculate_basic(self):
        """测试基本八字计算"""
        result = BaziCalculator.calculate(1990, 6, 15, 10, "男")
        
        assert result is not None
        assert "four_pillars" in result
        assert "year" in result["four_pillars"]
        assert "month" in result["four_pillars"]
        assert "day" in result["four_pillars"]
        assert "hour" in result["four_pillars"]
    
    def test_calculate_wuxing(self):
        """测试五行分析"""
        result = BaziCalculator.calculate(1990, 6, 15, 10, "男")
        
        assert "wuxing" in result
        wuxing = result["wuxing"]
        assert "木" in wuxing
        assert "火" in wuxing
        assert "土" in wuxing
        assert "金" in wuxing
        assert "水" in wuxing
    
    def test_calculate_shishen(self):
        """测试十神分析"""
        result = BaziCalculator.calculate(1990, 6, 15, 10, "男")
        
        assert "shishen" in result
    
    def test_different_hours(self):
        """测试不同时辰"""
        results = []
        for hour in [0, 6, 12, 18, 23]:
            result = BaziCalculator.calculate(1990, 6, 15, hour, "男")
            results.append(result["four_pillars"]["hour"])
        
        # 不同时辰应该有不同的时柱
        unique_hours = set(str(r) for r in results)
        assert len(unique_hours) >= 3
    
    def test_dayun_calculation(self):
        """测试大运计算"""
        result = BaziCalculator.calculate(1990, 6, 15, 10, "男")
        
        assert "dayun" in result
        dayun = result["dayun"]
        assert len(dayun) >= 8  # 至少8步大运
