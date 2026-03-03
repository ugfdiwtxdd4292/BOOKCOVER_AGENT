"""
数据模型模块初始化
"""
from .book_metadata import BookMetadata
from .cover_spec import CoverSpec
from .print_spec import PrintSpec
from .design_brief import DesignBrief

__all__ = ["BookMetadata", "CoverSpec", "PrintSpec", "DesignBrief"]
