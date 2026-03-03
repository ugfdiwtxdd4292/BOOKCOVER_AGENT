"""
完整展开图引擎
生成封面+书脊+封底+勒口的完整展开图布局
"""
import logging
from typing import Optional, Tuple
from PIL import Image, ImageDraw

from models.cover_spec import CoverSpec

logger = logging.getLogger(__name__)


class SpreadLayoutEngine:
    """
    展开图布局引擎
    
    生成完整的封面展开图，包含裁切标记和对位线
    """
    
    def __init__(self, cover_spec: CoverSpec):
        """
        初始化引擎
        
        Args:
            cover_spec: 封面规格
        """
        self.spec = cover_spec
    
    def create_spread_canvas(self) -> Image.Image:
        """
        创建展开图画布
        
        Returns:
            PIL图像对象
        """
        # 计算总尺寸（像素）
        total_width_mm = self.spec.calculate_total_width()
        total_height_mm = self.spec.calculate_total_height()
        
        width_px = self.spec.mm_to_pixels(total_width_mm)
        height_px = self.spec.mm_to_pixels(total_height_mm)
        
        logger.info(f"创建展开图画布: {width_px}x{height_px}px ({total_width_mm}x{total_height_mm}mm)")
        
        # 创建白色画布
        canvas = Image.new('CMYK', (width_px, height_px), (0, 0, 0, 0))
        
        return canvas
    
    def draw_guides(self, canvas: Image.Image, include_crop_marks: bool = True) -> Image.Image:
        """
        绘制辅助线和裁切标记
        
        Args:
            canvas: 画布图像
            include_crop_marks: 是否包含裁切标记
            
        Returns:
            添加了辅助线的图像
        """
        draw = ImageDraw.Draw(canvas)
        
        # 计算关键位置（像素）
        positions = self._calculate_guide_positions()
        
        # 绘制裁切线（红色）
        if include_crop_marks:
            self._draw_crop_marks(draw, positions)
        
        # 绘制折叠线（蓝色虚线）
        self._draw_fold_lines(draw, positions)
        
        # 绘制安全区域（绿色）
        self._draw_safe_areas(draw, positions)
        
        logger.info("辅助线绘制完成")
        
        return canvas
    
    def _calculate_guide_positions(self) -> dict:
        """
        计算辅助线位置
        
        Returns:
            位置字典（像素坐标）
        """
        positions = {}
        
        # 出血区域
        bleed_px = self.spec.mm_to_pixels(self.spec.bleed)
        positions['bleed'] = bleed_px
        
        # 左勒口边界
        if self.spec.has_flaps:
            left_flap = self.spec.flap_width + self.spec.bleed
            positions['left_flap_edge'] = self.spec.mm_to_pixels(left_flap)
        
        # 封底区域
        back_x, back_y, back_w, back_h = self.spec.get_back_cover_area()
        positions['back_cover_left'] = self.spec.mm_to_pixels(back_x)
        positions['back_cover_right'] = self.spec.mm_to_pixels(back_x + back_w)
        
        # 书脊区域
        spine_x, spine_y, spine_w, spine_h = self.spec.get_spine_area()
        positions['spine_left'] = self.spec.mm_to_pixels(spine_x)
        positions['spine_right'] = self.spec.mm_to_pixels(spine_x + spine_w)
        
        # 封面区域
        cover_x, cover_y, cover_w, cover_h = self.spec.get_cover_area()
        positions['cover_left'] = self.spec.mm_to_pixels(cover_x)
        positions['cover_right'] = self.spec.mm_to_pixels(cover_x + cover_w)
        
        # 右勒口边界
        if self.spec.has_flaps:
            right_flap = cover_x + cover_w
            positions['right_flap_edge'] = self.spec.mm_to_pixels(right_flap)
        
        # 画布尺寸
        positions['canvas_width'] = self.spec.mm_to_pixels(self.spec.calculate_total_width())
        positions['canvas_height'] = self.spec.mm_to_pixels(self.spec.calculate_total_height())
        
        return positions
    
    def _draw_crop_marks(self, draw: ImageDraw.Draw, positions: dict):
        """
        绘制裁切标记
        
        Args:
            draw: 绘图对象
            positions: 位置字典
        """
        # 裁切标记的颜色（CMYK: 洋红色）
        mark_color = (0, 100, 0, 0)
        mark_length = 20  # 标记长度（像素）
        
        height = positions['canvas_height']
        bleed = positions['bleed']
        
        # 四角的裁切标记
        corners = [
            # 左上角
            (bleed, bleed),
            # 右上角
            (positions['canvas_width'] - bleed, bleed),
            # 左下角
            (bleed, height - bleed),
            # 右下角
            (positions['canvas_width'] - bleed, height - bleed),
        ]
        
        for x, y in corners:
            # 水平线
            draw.line([(x - mark_length, y), (x + mark_length, y)], fill=mark_color, width=1)
            # 垂直线
            draw.line([(x, y - mark_length), (x, y + mark_length)], fill=mark_color, width=1)
    
    def _draw_fold_lines(self, draw: ImageDraw.Draw, positions: dict):
        """
        绘制折叠线（书脊位置）
        
        Args:
            draw: 绘图对象
            positions: 位置字典
        """
        # 折叠线颜色（CMYK: 青色）
        fold_color = (100, 0, 0, 0)
        
        height = positions['canvas_height']
        
        # 书脊左边缘
        x = positions['spine_left']
        draw.line([(x, 0), (x, height)], fill=fold_color, width=1)
        
        # 书脊右边缘
        x = positions['spine_right']
        draw.line([(x, 0), (x, height)], fill=fold_color, width=1)
    
    def _draw_safe_areas(self, draw: ImageDraw.Draw, positions: dict):
        """
        绘制安全区域边界
        
        Args:
            draw: 绘图对象
            positions: 位置字典
        """
        # 安全区域颜色（CMYK: 黄色）
        safe_color = (0, 0, 100, 0)
        
        safe_margin_px = self.spec.mm_to_pixels(self.spec.safe_margin)
        
        # 封面安全区域
        cover_left = positions['cover_left']
        cover_right = positions['cover_right']
        bleed = positions['bleed']
        height = positions['canvas_height']
        
        # 绘制矩形（虚线效果可通过多个短线实现）
        safe_rect = [
            cover_left + safe_margin_px,
            bleed + safe_margin_px,
            cover_right - safe_margin_px,
            height - bleed - safe_margin_px
        ]
        
        # 简化：绘制实线矩形
        draw.rectangle(safe_rect, outline=safe_color, width=1)
    
    def get_region_bbox(self, region: str) -> Tuple[int, int, int, int]:
        """
        获取指定区域的边界框（像素坐标）
        
        Args:
            region: 区域名称 ("cover", "back_cover", "spine", "left_flap", "right_flap")
            
        Returns:
            (x, y, width, height) 像素坐标
        """
        if region == "cover":
            x, y, w, h = self.spec.get_cover_area()
        elif region == "back_cover":
            x, y, w, h = self.spec.get_back_cover_area()
        elif region == "spine":
            x, y, w, h = self.spec.get_spine_area()
        elif region == "left_flap":
            if not self.spec.has_flaps:
                raise ValueError("封面没有勒口")
            x = self.spec.bleed
            y = self.spec.bleed
            w = self.spec.flap_width
            h = self.spec.trim_height
        elif region == "right_flap":
            if not self.spec.has_flaps:
                raise ValueError("封面没有勒口")
            cover_x, _, cover_w, _ = self.spec.get_cover_area()
            x = cover_x + cover_w
            y = self.spec.bleed
            w = self.spec.flap_width
            h = self.spec.trim_height
        else:
            raise ValueError(f"未知区域: {region}")
        
        # 转换为像素
        return (
            self.spec.mm_to_pixels(x),
            self.spec.mm_to_pixels(y),
            self.spec.mm_to_pixels(w),
            self.spec.mm_to_pixels(h)
        )
    
    def paste_image_to_region(
        self,
        canvas: Image.Image,
        image: Image.Image,
        region: str,
        fit_mode: str = "cover"
    ) -> Image.Image:
        """
        将图像粘贴到指定区域
        
        Args:
            canvas: 画布
            image: 要粘贴的图像
            region: 区域名称
            fit_mode: 适应模式 ("cover"填充, "contain"包含, "stretch"拉伸)
            
        Returns:
            处理后的画布
        """
        x, y, w, h = self.get_region_bbox(region)
        
        # 调整图像大小
        if fit_mode == "stretch":
            resized = image.resize((w, h), Image.Resampling.LANCZOS)
        elif fit_mode == "contain":
            resized = self._fit_contain(image, w, h)
        else:  # cover
            resized = self._fit_cover(image, w, h)
        
        # 粘贴到画布
        canvas.paste(resized, (x, y))
        
        logger.info(f"图像已粘贴到 {region} 区域")
        
        return canvas
    
    def _fit_cover(self, image: Image.Image, target_w: int, target_h: int) -> Image.Image:
        """
        调整图像大小以填充目标区域（裁剪溢出部分）
        
        Args:
            image: 原图像
            target_w: 目标宽度
            target_h: 目标高度
            
        Returns:
            调整后的图像
        """
        img_w, img_h = image.size
        
        # 计算缩放比例（取大的那个，确保填满）
        scale = max(target_w / img_w, target_h / img_h)
        
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        
        # 缩放
        resized = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # 居中裁剪
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        
        cropped = resized.crop((left, top, left + target_w, top + target_h))
        
        return cropped
    
    def _fit_contain(self, image: Image.Image, target_w: int, target_h: int) -> Image.Image:
        """
        调整图像大小以包含在目标区域内（不裁剪）
        
        Args:
            image: 原图像
            target_w: 目标宽度
            target_h: 目标高度
            
        Returns:
            调整后的图像（可能带边距）
        """
        img_w, img_h = image.size
        
        # 计算缩放比例（取小的那个，确保全部显示）
        scale = min(target_w / img_w, target_h / img_h)
        
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        
        # 缩放
        resized = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # 创建白色背景
        result = Image.new('CMYK', (target_w, target_h), (0, 0, 0, 0))
        
        # 居中粘贴
        x = (target_w - new_w) // 2
        y = (target_h - new_h) // 2
        
        result.paste(resized, (x, y))
        
        return result
