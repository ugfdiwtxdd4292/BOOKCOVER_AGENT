"""
封面规格模型
定义封面的物理尺寸和结构参数
"""
from dataclasses import dataclass
from typing import Optional
from config.settings import BookDefaults


@dataclass
class CoverSpec:
    """
    封面规格
    
    定义封面的所有尺寸参数（单位：毫米）
    """
    
    # 成品尺寸（裁切后的尺寸）
    trim_width: float = BookDefaults.DEFAULT_TRIM_WIDTH_MM  # 成品宽度
    trim_height: float = BookDefaults.DEFAULT_TRIM_HEIGHT_MM  # 成品高度
    
    # 书脊
    spine_width: float = 0.0  # 书脊宽度（需要计算）
    
    # 出血
    bleed: float = BookDefaults.BLEED_MM  # 出血宽度
    
    # 勒口
    flap_width: float = BookDefaults.DEFAULT_FLAP_WIDTH_MM  # 勒口宽度
    has_flaps: bool = True  # 是否有勒口
    
    # 安全区域
    safe_margin: float = BookDefaults.SAFE_MARGIN_MM  # 安全区域边距
    
    # 纸张和装订
    paper_type: str = "胶版纸"  # 纸张类型
    paper_weight: int = 80  # 纸张克重 (g/m²)
    binding_type: str = "平装"  # 装订方式
    
    # 分辨率
    dpi: int = BookDefaults.DPI  # 分辨率
    
    def __post_init__(self):
        """后处理：数据验证"""
        if self.trim_width <= 0 or self.trim_height <= 0:
            raise ValueError("成品尺寸必须大于0")
        
        if self.dpi < 300:
            raise ValueError("印刷级文件DPI不能低于300")
    
    def calculate_total_width(self) -> float:
        """
        计算展开图总宽度
        
        包含：左勒口 + 左出血 + 封底 + 书脊 + 封面 + 右出血 + 右勒口
        
        Returns:
            总宽度（毫米）
        """
        total = 0.0
        
        # 左侧勒口和出血
        if self.has_flaps:
            total += self.flap_width + self.bleed
        else:
            total += self.bleed
        
        # 封底
        total += self.trim_width
        
        # 书脊
        total += self.spine_width
        
        # 封面
        total += self.trim_width
        
        # 右侧勒口和出血
        if self.has_flaps:
            total += self.flap_width + self.bleed
        else:
            total += self.bleed
        
        return total
    
    def calculate_total_height(self) -> float:
        """
        计算展开图总高度
        
        包含：上出血 + 成品高度 + 下出血
        
        Returns:
            总高度（毫米）
        """
        return self.bleed + self.trim_height + self.bleed
    
    def get_cover_area(self) -> tuple:
        """
        获取封面区域的坐标和尺寸（相对于展开图）
        
        Returns:
            (x, y, width, height) 单位：毫米
        """
        # 封面起始位置
        x = 0.0
        if self.has_flaps:
            x += self.flap_width + self.bleed
        else:
            x += self.bleed
        
        x += self.trim_width + self.spine_width
        
        y = self.bleed
        
        return (x, y, self.trim_width, self.trim_height)
    
    def get_back_cover_area(self) -> tuple:
        """
        获取封底区域的坐标和尺寸（相对于展开图）
        
        Returns:
            (x, y, width, height) 单位：毫米
        """
        # 封底起始位置
        x = 0.0
        if self.has_flaps:
            x += self.flap_width + self.bleed
        else:
            x += self.bleed
        
        y = self.bleed
        
        return (x, y, self.trim_width, self.trim_height)
    
    def get_spine_area(self) -> tuple:
        """
        获取书脊区域的坐标和尺寸（相对于展开图）
        
        Returns:
            (x, y, width, height) 单位：毫米
        """
        # 书脊起始位置
        x = 0.0
        if self.has_flaps:
            x += self.flap_width + self.bleed
        else:
            x += self.bleed
        
        x += self.trim_width
        
        y = self.bleed
        
        return (x, y, self.spine_width, self.trim_height)
    
    def get_safe_area(self, area: str) -> tuple:
        """
        获取指定区域的安全区域
        
        Args:
            area: 区域名称 ("cover", "back_cover", "spine")
            
        Returns:
            (x, y, width, height) 单位：毫米
        """
        if area == "cover":
            x, y, w, h = self.get_cover_area()
        elif area == "back_cover":
            x, y, w, h = self.get_back_cover_area()
        elif area == "spine":
            x, y, w, h = self.get_spine_area()
        else:
            raise ValueError(f"未知区域: {area}")
        
        # 缩小安全边距
        return (
            x + self.safe_margin,
            y + self.safe_margin,
            w - 2 * self.safe_margin,
            h - 2 * self.safe_margin
        )
    
    def mm_to_pixels(self, mm: float) -> int:
        """
        将毫米转换为像素
        
        Args:
            mm: 毫米值
            
        Returns:
            像素值
        """
        inches = mm / 25.4
        return int(inches * self.dpi)
    
    def pixels_to_mm(self, pixels: int) -> float:
        """
        将像素转换为毫米
        
        Args:
            pixels: 像素值
            
        Returns:
            毫米值
        """
        inches = pixels / self.dpi
        return inches * 25.4
    
    def to_dict(self) -> dict:
        """
        转换为字典
        
        Returns:
            字典格式的数据
        """
        return {
            "trim_width": self.trim_width,
            "trim_height": self.trim_height,
            "spine_width": self.spine_width,
            "bleed": self.bleed,
            "flap_width": self.flap_width,
            "has_flaps": self.has_flaps,
            "safe_margin": self.safe_margin,
            "paper_type": self.paper_type,
            "paper_weight": self.paper_weight,
            "binding_type": self.binding_type,
            "dpi": self.dpi,
            "total_width": self.calculate_total_width(),
            "total_height": self.calculate_total_height(),
        }
