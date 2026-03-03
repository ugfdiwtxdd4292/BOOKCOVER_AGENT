"""
设计需求简报模型
汇总设计需求和AI生成参数
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass
class DesignBrief:
    """
    设计需求简报
    
    汇总所有设计需求，用于指导AI生成和人工设计
    """
    
    # 视觉风格
    visual_style: str = "photography"  # 视觉风格（photography/illustration/3d/abstract/geometric）
    
    # 色彩方案
    color_scheme: Optional[Dict[str, any]] = None  # 配色方案
    primary_color: Optional[str] = None  # 主色
    secondary_color: Optional[str] = None  # 辅色
    accent_color: Optional[str] = None  # 强调色
    
    # 情绪和氛围
    mood: str = "neutral"  # 情绪基调（happy/sad/mysterious/exciting/calm等）
    atmosphere: str = ""  # 氛围描述
    
    # 目标受众
    target_audience: str = "general"  # 目标读者群体
    
    # 封面主题
    theme: str = ""  # 主题关键词
    keywords: List[str] = field(default_factory=list)  # 设计关键词
    
    # AI提示词
    cover_prompt: str = ""  # 封面图生成提示词
    negative_prompt: str = ""  # 负面提示词（不想要的元素）
    
    # 排版偏好
    title_layout: str = "center"  # 标题布局（center/top/bottom/left/right）
    text_orientation: str = "horizontal"  # 文字方向（horizontal/vertical）
    
    # 字体选择
    title_font: Optional[str] = None  # 标题字体
    body_font: Optional[str] = None  # 正文字体
    
    # 参考图片
    reference_images: List[str] = field(default_factory=list)  # 参考图片路径
    
    # 品牌元素
    include_publisher_logo: bool = True  # 是否包含出版社Logo
    publisher_logo_path: Optional[str] = None  # 出版社Logo路径
    
    # 特殊要求
    special_requirements: str = ""  # 特殊要求说明
    
    # 审美偏好
    minimalist: bool = False  # 是否极简风格
    bold_typography: bool = False  # 是否使用粗体字
    image_dominant: bool = True  # 是否以图为主（否则以文字为主）
    
    def __post_init__(self):
        """后处理：设置默认值"""
        if not self.color_scheme:
            self.color_scheme = {}
    
    def add_keyword(self, keyword: str):
        """
        添加设计关键词
        
        Args:
            keyword: 关键词
        """
        if keyword and keyword not in self.keywords:
            self.keywords.append(keyword)
    
    def set_color_scheme(self, scheme: Dict[str, any]):
        """
        设置配色方案
        
        Args:
            scheme: 配色方案字典
        """
        self.color_scheme = scheme
        
        # 提取主要颜色
        if "primary" in scheme:
            self.primary_color = scheme["primary"]
        if "secondary" in scheme:
            self.secondary_color = scheme["secondary"]
        if "accent" in scheme:
            self.accent_color = scheme["accent"]
    
    def generate_prompt_summary(self) -> str:
        """
        生成提示词摘要
        
        Returns:
            提示词摘要文本
        """
        parts = []
        
        if self.visual_style:
            parts.append(f"风格: {self.visual_style}")
        
        if self.mood:
            parts.append(f"情绪: {self.mood}")
        
        if self.keywords:
            parts.append(f"关键词: {', '.join(self.keywords)}")
        
        if self.primary_color:
            parts.append(f"主色: {self.primary_color}")
        
        return " | ".join(parts)
    
    def get_layout_description(self) -> str:
        """
        获取版式描述
        
        Returns:
            版式描述文本
        """
        parts = []
        
        if self.title_layout:
            parts.append(f"标题位置: {self.title_layout}")
        
        if self.text_orientation:
            parts.append(f"文字方向: {self.text_orientation}")
        
        if self.minimalist:
            parts.append("极简风格")
        
        if self.bold_typography:
            parts.append("粗体字")
        
        if self.image_dominant:
            parts.append("以图为主")
        else:
            parts.append("以文字为主")
        
        return " | ".join(parts)
    
    def to_dict(self) -> dict:
        """
        转换为字典
        
        Returns:
            字典格式的数据
        """
        return {
            "visual_style": self.visual_style,
            "color_scheme": self.color_scheme,
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color,
            "accent_color": self.accent_color,
            "mood": self.mood,
            "atmosphere": self.atmosphere,
            "target_audience": self.target_audience,
            "theme": self.theme,
            "keywords": self.keywords,
            "cover_prompt": self.cover_prompt,
            "negative_prompt": self.negative_prompt,
            "title_layout": self.title_layout,
            "text_orientation": self.text_orientation,
            "title_font": self.title_font,
            "body_font": self.body_font,
            "reference_images": self.reference_images,
            "include_publisher_logo": self.include_publisher_logo,
            "publisher_logo_path": self.publisher_logo_path,
            "special_requirements": self.special_requirements,
            "minimalist": self.minimalist,
            "bold_typography": self.bold_typography,
            "image_dominant": self.image_dominant,
            "prompt_summary": self.generate_prompt_summary(),
            "layout_description": self.get_layout_description(),
        }
