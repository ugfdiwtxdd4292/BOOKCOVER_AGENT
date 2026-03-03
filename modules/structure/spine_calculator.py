"""
书脊厚度精确计算引擎
根据页数、纸张类型和克重计算书脊宽度
"""
import logging
from typing import Optional

from config.paper_specs import get_paper_type, list_paper_types

logger = logging.getLogger(__name__)


class SpineCalculator:
    """
    书脊厚度计算器
    
    根据印刷标准精确计算书脊宽度
    """
    
    @staticmethod
    def calculate(
        page_count: int,
        paper_type: str = "胶版纸",
        paper_weight: int = 80,
        binding_type: str = "平装"
    ) -> float:
        """
        计算书脊厚度
        
        Args:
            page_count: 页数（必须是偶数，因为是对开页）
            paper_type: 纸张类型
            paper_weight: 纸张克重 (g/m²)
            binding_type: 装订方式
            
        Returns:
            书脊厚度（单位：毫米）
            
        Raises:
            ValueError: 参数无效
        """
        # 验证参数
        if page_count <= 0:
            raise ValueError("页数必须大于0")
        
        if page_count % 2 != 0:
            logger.warning(f"页数 {page_count} 不是偶数，将向上取整为 {page_count + 1}")
            page_count += 1
        
        # 获取纸张类型
        try:
            paper = get_paper_type(paper_type)
        except ValueError as e:
            logger.error(f"纸张类型错误: {str(e)}")
            raise
        
        # 计算纸张厚度（页数）
        # 注意：书籍是对开的，所以实际纸张数量是页数的一半
        sheet_count = page_count / 2
        
        # 使用纸张规格计算厚度
        paper_thickness = paper.calculate_thickness(paper_weight, int(sheet_count))
        
        # 装订附加厚度
        binding_extra = SpineCalculator._get_binding_extra(binding_type, page_count)
        
        # 总厚度
        total_thickness = paper_thickness + binding_extra
        
        # 确保最小厚度
        min_thickness = 3.0 if binding_type == "平装" else 5.0
        total_thickness = max(total_thickness, min_thickness)
        
        # 四舍五入到0.1mm
        total_thickness = round(total_thickness, 1)
        
        logger.info(
            f"书脊计算: {page_count}页 {paper_type}({paper_weight}g) "
            f"{binding_type} = {total_thickness}mm"
        )
        
        return total_thickness
    
    @staticmethod
    def _get_binding_extra(binding_type: str, page_count: int) -> float:
        """
        获取装订附加厚度
        
        Args:
            binding_type: 装订方式
            page_count: 页数
            
        Returns:
            附加厚度（毫米）
        """
        # 装订方式的附加厚度系数
        extras = {
            "平装": 0.5,  # 胶装有一定厚度
            "精装": 3.0,  # 精装封面和纸板较厚
            "骑马订": 0.0,  # 骑马订基本无附加
            "螺旋装": 2.0,  # 螺旋装有固定的附加
            "线装": 1.0,  # 线装有少量附加
        }
        
        base_extra = extras.get(binding_type, 0.5)
        
        # 页数越多，装订附加略微增加（因为胶层等会稍厚）
        if page_count > 400:
            base_extra += 0.5
        elif page_count > 200:
            base_extra += 0.3
        
        return base_extra
    
    @staticmethod
    def recommend_spine_width(page_count: int, paper_weight: int = 80) -> dict:
        """
        推荐书脊宽度（针对不同纸张类型）
        
        Args:
            page_count: 页数
            paper_weight: 纸张克重
            
        Returns:
            推荐结果字典
        """
        recommendations = {}
        
        for paper_type in list_paper_types():
            try:
                width = SpineCalculator.calculate(
                    page_count=page_count,
                    paper_type=paper_type,
                    paper_weight=paper_weight,
                    binding_type="平装"
                )
                recommendations[paper_type] = width
            except Exception as e:
                logger.warning(f"计算 {paper_type} 失败: {str(e)}")
                continue
        
        return recommendations
    
    @staticmethod
    def validate_spine_width(
        spine_width: float,
        page_count: int,
        paper_type: str = "胶版纸",
        paper_weight: int = 80
    ) -> tuple:
        """
        验证书脊宽度是否合理
        
        Args:
            spine_width: 指定的书脊宽度
            page_count: 页数
            paper_type: 纸张类型
            paper_weight: 纸张克重
            
        Returns:
            (是否合理, 推荐值, 差异)
        """
        recommended = SpineCalculator.calculate(
            page_count=page_count,
            paper_type=paper_type,
            paper_weight=paper_weight
        )
        
        difference = abs(spine_width - recommended)
        
        # 允许10%的误差
        tolerance = recommended * 0.1
        is_valid = difference <= tolerance
        
        return (is_valid, recommended, difference)
