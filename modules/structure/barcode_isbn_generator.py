"""
ISBN条码生成器
生成标准EAN-13条码并验证ISBN
"""
import logging
from typing import Optional
from pathlib import Path

try:
    import barcode
    from barcode.writer import ImageWriter
except ImportError:
    barcode = None
    ImageWriter = None

from config.printing_standards import ISBNStandard
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)


class BarcodeGenerator:
    """
    ISBN条码生成器
    
    生成标准EAN-13条码，并添加ISBN和定价信息
    """
    
    def __init__(self):
        """初始化生成器"""
        if barcode is None:
            logger.warning("python-barcode库未安装，条码生成功能受限")
    
    def generate(
        self,
        isbn: str,
        price: Optional[float] = None,
        output_path: Optional[str] = None,
        dpi: int = 300
    ) -> str:
        """
        生成ISBN条码
        
        Args:
            isbn: ISBN-13号码
            price: 价格（可选）
            output_path: 输出路径（可选）
            dpi: 分辨率
            
        Returns:
            生成的文件路径
            
        Raises:
            ValueError: ISBN无效
        """
        # 清理ISBN
        isbn_clean = isbn.replace("-", "").replace(" ", "")
        
        # 验证ISBN
        if not ISBNStandard.validate_isbn13(isbn_clean):
            raise ValueError(f"无效的ISBN-13: {isbn}")
        
        logger.info(f"生成ISBN条码: {isbn_clean}")
        
        # 设置输出路径
        if output_path is None:
            output_path = f"output/barcode_{isbn_clean}.png"
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        if barcode is not None:
            # 使用python-barcode库生成
            try:
                # 创建EAN13条码对象
                ean = barcode.get_barcode_class('ean13')
                
                # 生成条码（不包含校验位，库会自动计算）
                barcode_obj = ean(isbn_clean, writer=ImageWriter())
                
                # 保存（不含扩展名，库会自动添加）
                output_without_ext = output_path.rsplit('.', 1)[0]
                filename = barcode_obj.save(
                    output_without_ext,
                    options={
                        'dpi': dpi,
                        'module_width': 0.33,  # 模块宽度（mm）
                        'module_height': 15.0,  # 条码高度（mm）
                        'quiet_zone': 6.5,  # 静区宽度（mm）
                        'font_size': 10,
                        'text_distance': 2.0,
                        'background': 'white',
                        'foreground': 'black',
                    }
                )
                
                # 如果指定了价格，添加价格文字
                if price is not None:
                    self._add_price_text(filename, price)
                
                logger.info(f"条码已生成: {filename}")
                return filename
                
            except Exception as e:
                logger.error(f"使用barcode库生成失败: {str(e)}")
                # 降级到简单图像生成
                return self._generate_simple_barcode(isbn_clean, price, output_path, dpi)
        else:
            # 使用简单方法生成
            return self._generate_simple_barcode(isbn_clean, price, output_path, dpi)
    
    def _generate_simple_barcode(
        self,
        isbn: str,
        price: Optional[float],
        output_path: str,
        dpi: int
    ) -> str:
        """
        生成简单的条码图像（当python-barcode不可用时）
        
        Args:
            isbn: ISBN号
            price: 价格
            output_path: 输出路径
            dpi: 分辨率
            
        Returns:
            文件路径
        """
        # 计算尺寸（标准条码尺寸：37mm x 25mm）
        width_mm = 37
        height_mm = 25
        
        width_px = int(width_mm / 25.4 * dpi)
        height_px = int(height_mm / 25.4 * dpi)
        
        # 创建白色背景图像
        img = Image.new('RGB', (width_px, height_px), 'white')
        draw = ImageDraw.Draw(img)
        
        # 绘制黑色边框
        draw.rectangle([0, 0, width_px-1, height_px-1], outline='black', width=2)
        
        # 绘制ISBN文字
        try:
            # 尝试使用默认字体
            font_size = int(height_px * 0.15)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # ISBN文字
        isbn_text = f"ISBN: {isbn}"
        text_bbox = draw.textbbox((0, 0), isbn_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (width_px - text_width) // 2
        text_y = int(height_px * 0.7)
        draw.text((text_x, text_y), isbn_text, fill='black', font=font)
        
        # 价格文字
        if price is not None:
            price_text = f"定价：{price:.2f}元"
            price_bbox = draw.textbbox((0, 0), price_text, font=font)
            price_width = price_bbox[2] - price_bbox[0]
            price_x = (width_px - price_width) // 2
            price_y = int(height_px * 0.85)
            draw.text((price_x, price_y), price_text, fill='black', font=font)
        
        # 绘制模拟条纹（简化的条码效果）
        bar_top = int(height_px * 0.2)
        bar_bottom = int(height_px * 0.65)
        bar_width = width_px // 60
        
        for i in range(0, width_px - bar_width, bar_width * 2):
            x = i + int(width_px * 0.1)
            if x + bar_width < width_px * 0.9:
                draw.rectangle([x, bar_top, x + bar_width, bar_bottom], fill='black')
        
        # 保存图像
        img.save(output_path, dpi=(dpi, dpi))
        logger.info(f"简化条码已生成: {output_path}")
        
        return output_path
    
    def _add_price_text(self, image_path: str, price: float):
        """
        在条码图像上添加价格文字
        
        Args:
            image_path: 图像路径
            price: 价格
        """
        try:
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            
            # 加载字体
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
            except:
                font = ImageFont.load_default()
            
            # 价格文字
            price_text = f"定价：{price:.2f}元"
            
            # 获取图像尺寸
            width, height = img.size
            
            # 计算文字位置（右下角）
            text_bbox = draw.textbbox((0, 0), price_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            text_x = width - text_width - 10
            text_y = height - text_height - 5
            
            # 绘制白色背景
            draw.rectangle(
                [text_x - 5, text_y - 2, text_x + text_width + 5, text_y + text_height + 2],
                fill='white'
            )
            
            # 绘制文字
            draw.text((text_x, text_y), price_text, fill='black', font=font)
            
            # 保存
            img.save(image_path)
            
        except Exception as e:
            logger.error(f"添加价格文字失败: {str(e)}")
    
    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        """
        验证ISBN-13
        
        Args:
            isbn: ISBN字符串
            
        Returns:
            是否有效
        """
        return ISBNStandard.validate_isbn13(isbn)
    
    @staticmethod
    def calculate_check_digit(isbn12: str) -> str:
        """
        计算ISBN-13校验码
        
        Args:
            isbn12: 前12位ISBN
            
        Returns:
            校验码
        """
        return ISBNStandard.calculate_check_digit(isbn12)
    
    @staticmethod
    def format_isbn(isbn: str) -> str:
        """
        格式化ISBN（添加连字符）
        
        Args:
            isbn: ISBN字符串
            
        Returns:
            格式化的ISBN
        """
        isbn_clean = isbn.replace("-", "").replace(" ", "")
        
        if len(isbn_clean) != 13:
            return isbn
        
        # 标准格式：978-7-XXXX-XXXX-X
        if isbn_clean.startswith("978"):
            prefix = isbn_clean[:3]
            group = isbn_clean[3:4]
            publisher = isbn_clean[4:8]
            title = isbn_clean[8:12]
            check = isbn_clean[12]
            return f"{prefix}-{group}-{publisher}-{title}-{check}"
        
        return isbn
