"""
图书元数据模型
存储图书的基本信息
"""
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class BookMetadata:
    """
    图书元数据
    
    存储图书的所有基本信息，用于生成封面设计
    """
    
    # 必填字段
    title: str  # 中文书名
    
    # 可选基本信息
    subtitle: Optional[str] = None  # 副标题
    author: str = ""  # 作者
    translator: Optional[str] = None  # 译者
    editor: Optional[str] = None  # 编者
    
    # 出版信息
    publisher: str = ""  # 出版社
    isbn: str = ""  # ISBN编号
    price: float = 0.0  # 定价
    
    # 书籍规格
    page_count: int = 200  # 页数
    
    # 内容信息
    synopsis: str = ""  # 内容简介
    recommendations: List[str] = field(default_factory=list)  # 推荐语列表
    genre: str = ""  # 类型/流派（如：科幻、文学、历史等）
    
    # 作者信息
    author_bio: str = ""  # 作者简介
    author_image: Optional[str] = None  # 作者照片路径
    is_famous_author: bool = False  # 是否知名作者（影响名字字号）
    
    # 系列信息
    series_name: Optional[str] = None  # 系列名称
    series_number: Optional[int] = None  # 系列编号
    
    # 其他图书信息
    keywords: List[str] = field(default_factory=list)  # 关键词
    target_audience: str = ""  # 目标读者
    publication_date: Optional[str] = None  # 出版日期
    edition: str = "第1版"  # 版次
    
    def __post_init__(self):
        """后处理：数据验证"""
        if not self.title:
            raise ValueError("书名不能为空")
        
        # 清理ISBN（移除连字符）
        if self.isbn:
            self.isbn = self.isbn.replace("-", "").replace(" ", "")
    
    def get_display_title(self) -> str:
        """
        获取显示标题（包含副标题）
        
        Returns:
            完整标题字符串
        """
        if self.subtitle:
            return f"{self.title}：{self.subtitle}"
        return self.title
    
    def get_author_info(self) -> str:
        """
        获取作者信息文本
        
        Returns:
            作者信息字符串
        """
        parts = []
        
        if self.author:
            parts.append(f"{self.author} 著")
        
        if self.translator:
            parts.append(f"{self.translator} 译")
        
        if self.editor:
            parts.append(f"{self.editor} 编")
        
        return " / ".join(parts)
    
    def get_price_text(self) -> str:
        """
        获取价格文本
        
        Returns:
            格式化的价格字符串
        """
        if self.price > 0:
            return f"定价：{self.price:.2f}元"
        return ""
    
    def has_series(self) -> bool:
        """
        是否属于系列图书
        
        Returns:
            布尔值
        """
        return self.series_name is not None
    
    def to_dict(self) -> dict:
        """
        转换为字典
        
        Returns:
            字典格式的数据
        """
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "author": self.author,
            "translator": self.translator,
            "editor": self.editor,
            "publisher": self.publisher,
            "isbn": self.isbn,
            "price": self.price,
            "page_count": self.page_count,
            "synopsis": self.synopsis,
            "recommendations": self.recommendations,
            "genre": self.genre,
            "author_bio": self.author_bio,
            "author_image": self.author_image,
            "is_famous_author": self.is_famous_author,
            "series_name": self.series_name,
            "series_number": self.series_number,
            "keywords": self.keywords,
            "target_audience": self.target_audience,
            "publication_date": self.publication_date,
            "edition": self.edition,
        }
