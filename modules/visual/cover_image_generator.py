"""
封面主图AI生成器
使用硅基流动API生成封面图像
"""
import logging
from typing import Optional, Dict
from pathlib import Path

from core.silicon_client import SiliconFlowClient
from templates.prompt_templates import PromptTemplates
from PIL import Image

logger = logging.getLogger(__name__)


class CoverImageGenerator:
    """
    封面主图生成器
    
    使用AI生成封面背景图像
    """
    
    def __init__(self, client: Optional[SiliconFlowClient] = None):
        """
        初始化生成器
        
        Args:
            client: 硅基流动客户端（可选）
        """
        self.client = client or SiliconFlowClient()
    
    def generate(
        self,
        theme: str,
        style: str = "photography",
        genre: str = "",
        mood: str = "neutral",
        keywords: list = None,
        image_size: str = "1024x1024",
        output_path: str = "output/cover_image.png",
        dpi: int = 300
    ) -> str:
        """
        生成封面图像
        
        Args:
            theme: 主题描述
            style: 视觉风格
            genre: 图书类型
            mood: 情绪基调
            keywords: 额外关键词
            image_size: 图像尺寸
            output_path: 输出路径
            dpi: 目标DPI
            
        Returns:
            生成的图像文件路径
            
        Raises:
            Exception: 生成失败
        """
        logger.info(f"生成封面图像: 主题={theme}, 风格={style}, 类型={genre}")
        
        # 生成提示词
        prompt, negative_prompt = PromptTemplates.generate_cover_prompt(
            style=style,
            theme=theme,
            genre=genre,
            mood=mood,
            additional_keywords=keywords
        )
        
        logger.info(f"提示词: {prompt}")
        logger.info(f"负面提示词: {negative_prompt}")
        
        try:
            # 调用AI生成图像
            image_urls = self.client.generate_image(
                prompt=prompt,
                negative_prompt=negative_prompt,
                image_size=image_size,
                num_inference_steps=30,
                guidance_scale=7.5,
                batch_size=1
            )
            
            if not image_urls:
                raise Exception("未生成任何图像")
            
            # 下载第一张图像
            image_url = image_urls[0]
            logger.info(f"下载图像: {image_url}")
            
            # 确保输出目录存在
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # 下载图像
            downloaded_path = self.client.download_image(image_url, output_path)
            
            # 后处理：确保DPI正确
            self._post_process_image(downloaded_path, dpi)
            
            logger.info(f"封面图像已生成: {downloaded_path}")
            return downloaded_path
            
        except Exception as e:
            logger.error(f"生成封面图像失败: {str(e)}")
            raise
    
    def _post_process_image(self, image_path: str, target_dpi: int = 300):
        """
        后处理图像（调整DPI等）
        
        Args:
            image_path: 图像路径
            target_dpi: 目标DPI
        """
        try:
            img = Image.open(image_path)
            
            # 转换为CMYK（印刷色彩模式）
            if img.mode != 'CMYK':
                logger.info(f"转换色彩模式: {img.mode} -> CMYK")
                img = img.convert('CMYK')
            
            # 保存时设置DPI
            img.save(image_path, dpi=(target_dpi, target_dpi))
            
            logger.info(f"图像后处理完成: DPI={target_dpi}, 模式=CMYK")
            
        except Exception as e:
            logger.warning(f"图像后处理失败: {str(e)}")
    
    def generate_with_book_info(
        self,
        book_info: Dict,
        design_brief: Dict,
        output_path: str = "output/cover_image.png"
    ) -> str:
        """
        根据图书信息生成封面图像
        
        Args:
            book_info: 图书信息字典
            design_brief: 设计简报字典
            output_path: 输出路径
            
        Returns:
            生成的图像文件路径
        """
        # 先让AI生成描述
        cover_description = self.client.generate_cover_description(book_info)
        
        # 使用生成的描述作为主题
        return self.generate(
            theme=cover_description,
            style=design_brief.get('visual_style', 'photography'),
            genre=book_info.get('genre', ''),
            mood=design_brief.get('mood', 'neutral'),
            keywords=design_brief.get('keywords', []),
            output_path=output_path
        )


class ColorMoodEngine:
    """
    色调情绪引擎
    
    根据图书类型和情绪生成配色方案
    """
    
    def __init__(self, client: Optional[SiliconFlowClient] = None):
        """
        初始化引擎
        
        Args:
            client: 硅基流动客户端（可选）
        """
        self.client = client or SiliconFlowClient()
    
    def generate_color_scheme(
        self,
        genre: str,
        mood: str = "neutral",
        target_audience: str = "general"
    ) -> Dict:
        """
        生成配色方案
        
        Args:
            genre: 图书类型
            mood: 情绪基调
            target_audience: 目标读者
            
        Returns:
            配色方案字典
        """
        logger.info(f"生成配色方案: 类型={genre}, 情绪={mood}")
        
        try:
            # 使用AI生成配色方案
            color_scheme = self.client.generate_color_scheme(genre, mood)
            
            logger.info(f"配色方案已生成: {color_scheme}")
            return color_scheme
            
        except Exception as e:
            logger.error(f"生成配色方案失败: {str(e)}")
            # 返回默认方案
            return self.client._get_default_color_scheme(genre)
    
    @staticmethod
    def get_mood_description(mood: str) -> str:
        """
        获取情绪描述
        
        Args:
            mood: 情绪代码
            
        Returns:
            情绪描述
        """
        moods = {
            "happy": "欢快、积极、明亮",
            "sad": "忧郁、感伤、灰暗",
            "mysterious": "神秘、悬疑、深邃",
            "exciting": "激动、活力、动感",
            "calm": "平静、安详、舒缓",
            "dramatic": "戏剧性、强烈、冲突",
            "romantic": "浪漫、温柔、感性",
            "dark": "黑暗、沉重、压抑",
            "neutral": "中性、平衡、稳定",
        }
        return moods.get(mood, "中性")
