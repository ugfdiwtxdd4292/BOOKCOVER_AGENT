"""
印刷规格模型
定义印刷相关的技术参数
"""
from dataclasses import dataclass, field
from typing import List, Optional
from config.settings import PrintingConfig


@dataclass
class PrintSpec:
    """
    印刷规格
    
    定义印刷过程中的技术参数和工艺选项
    """
    
    # 色彩模式
    color_mode: str = PrintingConfig.COLOR_SPACE  # CMYK或RGB
    
    # PDF导出参数
    pdf_version: str = PrintingConfig.PDF_VERSION  # PDF版本
    embed_fonts: bool = PrintingConfig.EMBED_FONTS  # 是否嵌入字体
    compress: bool = PrintingConfig.COMPRESS  # 是否压缩
    
    # 裁切和折叠标记
    include_crop_marks: bool = True  # 是否包含裁切标记
    include_bleed_marks: bool = True  # 是否包含出血标记
    include_registration_marks: bool = True  # 是否包含对位标记
    include_color_bars: bool = False  # 是否包含色标
    
    # 特殊工艺
    lamination: Optional[str] = None  # 覆膜类型（"亮膜"/"哑膜"/None）
    special_processes: List[str] = field(default_factory=list)  # 特殊工艺列表
    
    # UV工艺
    uv_areas: List[dict] = field(default_factory=list)  # UV区域列表
    
    # 烫金/烫银
    foil_areas: List[dict] = field(default_factory=list)  # 烫金区域列表
    
    # 压印
    emboss_areas: List[dict] = field(default_factory=list)  # 压印区域列表
    
    # 专色
    spot_colors: List[str] = field(default_factory=list)  # 专色列表
    
    # 印刷质量
    quality_level: str = "standard"  # 印刷质量级别 (standard/high/premium)
    
    # 纸张表面处理
    paper_finish: Optional[str] = None  # 纸张表面处理（"光面"/"哑面"/None）
    
    def __post_init__(self):
        """后处理：数据验证"""
        if self.color_mode not in ["CMYK", "RGB"]:
            raise ValueError("色彩模式必须是CMYK或RGB")
        
        if self.quality_level not in ["standard", "high", "premium"]:
            raise ValueError("质量级别必须是standard/high/premium之一")
    
    def has_special_processes(self) -> bool:
        """
        是否包含特殊工艺
        
        Returns:
            布尔值
        """
        return (
            len(self.special_processes) > 0 or
            len(self.uv_areas) > 0 or
            len(self.foil_areas) > 0 or
            len(self.emboss_areas) > 0
        )
    
    def add_uv_area(self, x: float, y: float, width: float, height: float, uv_type: str = "局部UV"):
        """
        添加UV区域
        
        Args:
            x: X坐标（毫米）
            y: Y坐标（毫米）
            width: 宽度（毫米）
            height: 高度（毫米）
            uv_type: UV类型
        """
        self.uv_areas.append({
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "type": uv_type
        })
        
        if "uv_coating" not in self.special_processes:
            self.special_processes.append("uv_coating")
    
    def add_foil_area(self, x: float, y: float, width: float, height: float, 
                      foil_type: str = "烫金"):
        """
        添加烫金区域
        
        Args:
            x: X坐标（毫米）
            y: Y坐标（毫米）
            width: 宽度（毫米）
            height: 高度（毫米）
            foil_type: 烫印类型（"烫金"/"烫银"等）
        """
        self.foil_areas.append({
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "type": foil_type
        })
        
        if "hot_stamping" not in self.special_processes:
            self.special_processes.append("hot_stamping")
    
    def add_emboss_area(self, x: float, y: float, width: float, height: float,
                        emboss_type: str = "凸印"):
        """
        添加压印区域
        
        Args:
            x: X坐标（毫米）
            y: Y坐标（毫米）
            width: 宽度（毫米）
            height: 高度（毫米）
            emboss_type: 压印类型（"凸印"/"凹印"等）
        """
        self.emboss_areas.append({
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "type": emboss_type
        })
        
        if "embossing" not in self.special_processes:
            self.special_processes.append("embossing")
    
    def get_process_summary(self) -> str:
        """
        获取工艺总结
        
        Returns:
            工艺描述文本
        """
        parts = []
        
        # 覆膜
        if self.lamination:
            parts.append(f"覆膜: {self.lamination}")
        
        # UV工艺
        if self.uv_areas:
            parts.append(f"UV工艺: {len(self.uv_areas)}处")
        
        # 烫金/烫银
        if self.foil_areas:
            parts.append(f"烫印工艺: {len(self.foil_areas)}处")
        
        # 压印
        if self.emboss_areas:
            parts.append(f"压印工艺: {len(self.emboss_areas)}处")
        
        # 专色
        if self.spot_colors:
            parts.append(f"专色: {len(self.spot_colors)}种")
        
        if not parts:
            return "无特殊工艺"
        
        return " | ".join(parts)
    
    def to_dict(self) -> dict:
        """
        转换为字典
        
        Returns:
            字典格式的数据
        """
        return {
            "color_mode": self.color_mode,
            "pdf_version": self.pdf_version,
            "embed_fonts": self.embed_fonts,
            "compress": self.compress,
            "include_crop_marks": self.include_crop_marks,
            "include_bleed_marks": self.include_bleed_marks,
            "include_registration_marks": self.include_registration_marks,
            "include_color_bars": self.include_color_bars,
            "lamination": self.lamination,
            "special_processes": self.special_processes,
            "uv_areas": self.uv_areas,
            "foil_areas": self.foil_areas,
            "emboss_areas": self.emboss_areas,
            "spot_colors": self.spot_colors,
            "quality_level": self.quality_level,
            "paper_finish": self.paper_finish,
            "has_special_processes": self.has_special_processes(),
            "process_summary": self.get_process_summary(),
        }
