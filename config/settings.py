"""
全局配置文件
包含硅基流动API配置和图书默认参数
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class SiliconFlowConfig:
    """硅基流动API配置"""
    
    # API密钥
    SILICON_KEY = os.getenv("SILICON_KEY", "sk-ouyoyaxisndscgudrpdvgyzoondoufupjsokbyysguqmroip")
    
    # API端点
    BASE_URL = "https://api.siliconflow.cn/v1"
    IMAGE_GENERATION_URL = f"{BASE_URL}/images/generations"
    CHAT_COMPLETION_URL = f"{BASE_URL}/chat/completions"
    
    # 模型配置
    IMAGE_MODEL = "Kwai-Kolors/Kolors"  # 默认图像生成模型
    IMAGE_MODEL_ALT = "stabilityai/stable-diffusion-3-5-large"  # 备用模型
    CHAT_MODEL = "Qwen/Qwen2.5-7B-Instruct"  # 默认文字生成模型
    CHAT_MODEL_ALT = "deepseek-ai/DeepSeek-V2.5"  # 备用模型
    
    # 图像生成默认参数
    DEFAULT_IMAGE_SIZE = "1024x1024"
    DEFAULT_INFERENCE_STEPS = 30
    DEFAULT_GUIDANCE_SCALE = 7.5
    DEFAULT_BATCH_SIZE = 1
    
    # 文字生成默认参数
    MAX_TOKENS = 4096
    TEMPERATURE = 0.7
    
    # API请求配置
    REQUEST_TIMEOUT = 120  # 请求超时时间（秒）
    MAX_RETRIES = 3  # 最大重试次数
    RETRY_DELAY = 2  # 重试延迟（秒）


class BookDefaults:
    """图书默认参数"""
    
    # 成品尺寸（单位：毫米）
    DEFAULT_TRIM_WIDTH_MM = 170  # 成品宽度
    DEFAULT_TRIM_HEIGHT_MM = 240  # 成品高度
    
    # 出血参数
    BLEED_MM = 3  # 出血宽度（单位：毫米）
    
    # 分辨率
    DPI = 300  # 印刷级DPI
    
    # 书脊计算系数
    SPINE_FACTOR = 0.06  # 默认系数（可根据纸张类型调整）
    
    # 勒口宽度
    DEFAULT_FLAP_WIDTH_MM = 100  # 勒口宽度（单位：毫米）
    
    # 颜色模式
    COLOR_MODE = "CMYK"  # 印刷色彩模式
    
    # 安全区域
    SAFE_MARGIN_MM = 5  # 安全区域边距（单位：毫米）
    
    # 条码参数
    BARCODE_WIDTH_MM = 37  # 条码宽度
    BARCODE_HEIGHT_MM = 25  # 条码高度
    BARCODE_POSITION = "bottom_right"  # 条码位置：封底右下角
    
    # 默认字体大小（单位：磅）
    TITLE_FONT_SIZE = 48
    SUBTITLE_FONT_SIZE = 24
    AUTHOR_FONT_SIZE = 28
    PRICE_FONT_SIZE = 12


class PrintingConfig:
    """印刷配置"""
    
    # 色彩空间
    COLOR_SPACE = "CMYK"
    
    # PDF导出参数
    PDF_VERSION = "1.4"  # PDF版本
    EMBED_FONTS = True  # 嵌入字体
    COMPRESS = True  # 压缩
    
    # 特殊工艺
    SPECIAL_PROCESSES = [
        "uv_coating",  # UV上光
        "hot_stamping",  # 烫金/烫银
        "embossing",  # 压凹
        "debossing",  # 压凸
        "die_cutting",  # 模切
    ]
