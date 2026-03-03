"""
纸张规格数据库
包含各种纸张类型的厚度系数和特性
"""
from typing import Dict


class PaperType:
    """纸张类型"""
    
    def __init__(self, name: str, weight_range: tuple, thickness_factor: float, description: str):
        """
        初始化纸张类型
        
        Args:
            name: 纸张名称
            weight_range: 克重范围 (最小, 最大) 单位：g/m²
            thickness_factor: 厚度系数 (mm/张)
            description: 描述
        """
        self.name = name
        self.weight_range = weight_range
        self.thickness_factor = thickness_factor
        self.description = description
    
    def calculate_thickness(self, weight: int, pages: int) -> float:
        """
        计算纸张厚度
        
        Args:
            weight: 纸张克重 (g/m²)
            pages: 页数
            
        Returns:
            厚度 (mm)
        """
        # 根据克重调整系数
        min_weight, max_weight = self.weight_range
        if weight < min_weight or weight > max_weight:
            raise ValueError(f"克重 {weight} 超出纸张 {self.name} 的范围 {self.weight_range}")
        
        # 线性插值调整系数
        weight_ratio = (weight - min_weight) / (max_weight - min_weight) if max_weight > min_weight else 0.5
        adjusted_factor = self.thickness_factor * (0.8 + 0.4 * weight_ratio)
        
        return pages * adjusted_factor


# 纸张规格数据库
PAPER_SPECS: Dict[str, PaperType] = {
    "胶版纸": PaperType(
        name="胶版纸",
        weight_range=(60, 120),
        thickness_factor=0.06,  # 每张约0.06mm
        description="最常用的书刊用纸，适合黑白印刷"
    ),
    "轻型纸": PaperType(
        name="轻型纸",
        weight_range=(60, 80),
        thickness_factor=0.08,  # 比同克重胶版纸更厚
        description="轻薄且不透，适合较厚的书籍"
    ),
    "铜版纸": PaperType(
        name="铜版纸",
        weight_range=(105, 350),
        thickness_factor=0.05,  # 更致密，相对较薄
        description="表面光滑，适合彩色印刷和图册"
    ),
    "特种纸": PaperType(
        name="特种纸",
        weight_range=(80, 300),
        thickness_factor=0.07,
        description="包含多种艺术纸、压纹纸等"
    ),
}


def get_paper_type(paper_name: str) -> PaperType:
    """
    获取纸张类型
    
    Args:
        paper_name: 纸张名称
        
    Returns:
        PaperType对象
        
    Raises:
        ValueError: 纸张类型不存在
    """
    if paper_name not in PAPER_SPECS:
        raise ValueError(f"未知纸张类型: {paper_name}，可选: {list(PAPER_SPECS.keys())}")
    return PAPER_SPECS[paper_name]


def list_paper_types() -> list:
    """
    列出所有可用的纸张类型
    
    Returns:
        纸张名称列表
    """
    return list(PAPER_SPECS.keys())
