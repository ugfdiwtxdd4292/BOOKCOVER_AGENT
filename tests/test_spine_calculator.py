"""
测试书脊计算器
"""
import pytest
from modules.structure.spine_calculator import SpineCalculator


def test_basic_calculation():
    """测试基本计算"""
    # 200页胶版纸80g
    width = SpineCalculator.calculate(
        page_count=200,
        paper_type="胶版纸",
        paper_weight=80,
        binding_type="平装"
    )
    
    # 应该在合理范围内
    assert 5.0 <= width <= 15.0
    assert isinstance(width, float)


def test_odd_page_count():
    """测试奇数页数（应该自动向上取整）"""
    width = SpineCalculator.calculate(
        page_count=201,  # 奇数页
        paper_type="胶版纸",
        paper_weight=80
    )
    
    # 应该等于202页的厚度
    width_202 = SpineCalculator.calculate(
        page_count=202,
        paper_type="胶版纸",
        paper_weight=80
    )
    
    assert width == width_202


def test_invalid_page_count():
    """测试无效页数"""
    with pytest.raises(ValueError):
        SpineCalculator.calculate(
            page_count=0,
            paper_type="胶版纸",
            paper_weight=80
        )
    
    with pytest.raises(ValueError):
        SpineCalculator.calculate(
            page_count=-10,
            paper_type="胶版纸",
            paper_weight=80
        )


def test_invalid_paper_type():
    """测试无效纸张类型"""
    with pytest.raises(ValueError):
        SpineCalculator.calculate(
            page_count=200,
            paper_type="不存在的纸张",
            paper_weight=80
        )


def test_recommend_spine_width():
    """测试推荐功能"""
    recommendations = SpineCalculator.recommend_spine_width(
        page_count=200,
        paper_weight=80
    )
    
    # 应该有多个推荐
    assert len(recommendations) > 0
    
    # 每个推荐都应该是有效的
    for paper_type, width in recommendations.items():
        assert width > 0
        assert isinstance(width, float)


def test_validate_spine_width():
    """测试验证功能"""
    calculated = SpineCalculator.calculate(
        page_count=200,
        paper_type="胶版纸",
        paper_weight=80
    )
    
    # 测试准确值
    is_valid, recommended, diff = SpineCalculator.validate_spine_width(
        spine_width=calculated,
        page_count=200,
        paper_type="胶版纸",
        paper_weight=80
    )
    
    assert is_valid is True
    assert diff == 0.0
    
    # 测试偏差值
    is_valid, recommended, diff = SpineCalculator.validate_spine_width(
        spine_width=calculated * 2,  # 明显错误的值
        page_count=200,
        paper_type="胶版纸",
        paper_weight=80
    )
    
    assert is_valid is False
    assert diff > 0
