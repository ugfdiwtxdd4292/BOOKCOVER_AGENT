"""
印刷标准配置
包含印刷行业标准参数和规范
"""
from enum import Enum
from typing import Dict, List


class BindingType(Enum):
    """装订方式"""
    PAPERBACK = "平装"  # 胶装
    HARDCOVER = "精装"  # 精装
    SADDLE_STITCH = "骑马订"  # 适用于薄册子
    SPIRAL = "螺旋装"  # 螺旋装订
    THREAD_SEWING = "线装"  # 传统线装


class PrintingStandard:
    """印刷标准"""
    
    # 标准开本尺寸（单位：毫米）
    STANDARD_SIZES = {
        "32开": (140, 203),
        "16开": (185, 260),
        "大32开": (144, 210),
        "正16开": (170, 240),
        "A4": (210, 297),
        "A5": (148, 210),
        "B5": (176, 250),
        "小16开": (184, 260),
    }
    
    # 出血标准
    BLEED_STANDARDS = {
        "国内标准": 3,  # 3mm
        "国际标准": 3,  # 3mm
        "精装书": 5,  # 精装书可能需要更大的出血
    }
    
    # 分辨率标准
    DPI_STANDARDS = {
        "印刷级": 300,  # 标准印刷
        "高品质": 350,  # 高品质印刷
        "艺术品": 600,  # 艺术品级别
        "网络用": 72,  # 仅供参考，不用于印刷
    }
    
    # 颜色模式
    COLOR_MODES = {
        "CMYK": "四色印刷",
        "RGB": "数字显示（不适合印刷）",
        "专色": "专色印刷",
    }
    
    # 安全区域标准（单位：毫米）
    SAFE_MARGINS = {
        "最小": 3,
        "标准": 5,
        "推荐": 8,
    }
    
    # 书脊最小宽度（单位：毫米）
    MIN_SPINE_WIDTH = {
        "平装": 3,  # 平装书脊最小3mm
        "精装": 5,  # 精装书脊最小5mm
    }


class ColorStandard:
    """色彩标准"""
    
    # CMYK安全色值范围（避免过度印刷）
    CMYK_MAX_TOTAL = 320  # C+M+Y+K总和不超过320%
    
    # 常用专色
    PANTONE_COLORS = {
        "金色": "PANTONE 871 C",
        "银色": "PANTONE 877 C",
        "红色": "PANTONE 186 C",
        "蓝色": "PANTONE 300 C",
    }
    
    # 黑色标准
    BLACK_STANDARDS = {
        "纯黑": (0, 0, 0, 100),  # 仅K版
        "四色黑": (60, 40, 40, 100),  # 更浓郁的黑色
        "富黑": (70, 50, 30, 100),  # 高品质黑色
    }
    
    # 白色（纸张本色）
    WHITE = (0, 0, 0, 0)


class FinishingProcess:
    """后期加工工艺"""
    
    # 覆膜类型
    LAMINATION_TYPES = {
        "亮膜": "增加光泽度，保护封面",
        "哑膜": "柔和质感，减少反光",
        "触感膜": "特殊触感效果",
    }
    
    # UV工艺
    UV_TYPES = {
        "局部UV": "在特定区域上光，产生对比效果",
        "全面UV": "整体上光，增加亮度",
        "磨砂UV": "磨砂质感的UV效果",
    }
    
    # 烫印工艺
    FOIL_STAMPING = {
        "烫金": "金属金色效果",
        "烫银": "金属银色效果",
        "彩色烫": "彩色金属效果",
        "镭射烫": "镭射彩虹效果",
    }
    
    # 压印工艺
    EMBOSSING = {
        "凸印": "图案凸起",
        "凹印": "图案凹陷",
        "击凸": "无油墨的凸起",
    }


class ISBNStandard:
    """ISBN标准"""
    
    # ISBN格式
    ISBN_13_FORMAT = "978-X-XXXX-XXXX-X"  # 13位ISBN
    ISBN_10_FORMAT = "X-XXXX-XXXX-X"  # 10位ISBN（已停用）
    
    # 中国出版社代码
    CHINA_PUBLISHER_PREFIX = "978-7"  # 中国区ISBN前缀
    
    # 条码类型
    BARCODE_TYPE = "EAN-13"  # 13位欧洲商品条码
    
    @staticmethod
    def validate_isbn13(isbn: str) -> bool:
        """
        验证13位ISBN校验码
        
        Args:
            isbn: ISBN字符串（可含连字符）
            
        Returns:
            是否有效
        """
        # 移除连字符和空格
        isbn_clean = isbn.replace("-", "").replace(" ", "")
        
        if len(isbn_clean) != 13:
            return False
        
        if not isbn_clean.isdigit():
            return False
        
        # 计算校验码
        checksum = 0
        for i, digit in enumerate(isbn_clean[:12]):
            weight = 1 if i % 2 == 0 else 3
            checksum += int(digit) * weight
        
        check_digit = (10 - (checksum % 10)) % 10
        
        return int(isbn_clean[12]) == check_digit
    
    @staticmethod
    def calculate_check_digit(isbn12: str) -> str:
        """
        计算ISBN-13校验码
        
        Args:
            isbn12: 前12位ISBN
            
        Returns:
            校验码（单个数字字符）
        """
        isbn_clean = isbn12.replace("-", "").replace(" ", "")
        
        if len(isbn_clean) != 12:
            raise ValueError("需要12位ISBN前缀")
        
        checksum = 0
        for i, digit in enumerate(isbn_clean):
            weight = 1 if i % 2 == 0 else 3
            checksum += int(digit) * weight
        
        check_digit = (10 - (checksum % 10)) % 10
        return str(check_digit)


# 导出所有标准
__all__ = [
    "BindingType",
    "PrintingStandard",
    "ColorStandard",
    "FinishingProcess",
    "ISBNStandard",
]
