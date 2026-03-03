"""
AI提示词模板库
包含各种风格的封面生成提示词模板
"""
from typing import Dict, List


class PromptTemplates:
    """AI提示词模板"""
    
    # 封面图像生成提示词模板（按风格分类）
    COVER_IMAGE_PROMPTS = {
        "photography": {
            "template": "Professional book cover photography, {theme}, {mood} atmosphere, high quality, 8k, detailed, {keywords}, clean composition, centered subject",
            "negative": "text, words, letters, numbers, watermark, low quality, blurry, distorted",
            "description": "专业摄影风格",
        },
        "illustration": {
            "template": "Hand-drawn illustration for book cover, {theme}, {mood} mood, artistic, {keywords}, vibrant colors, detailed artwork, professional",
            "negative": "photo, realistic, text, words, watermark, low quality, messy",
            "description": "手绘插画风格",
        },
        "3d_render": {
            "template": "3D rendered book cover art, {theme}, {mood} feeling, cinema4d, octane render, {keywords}, professional lighting, high detail, modern",
            "negative": "flat, 2d, text, words, low poly, low quality, ugly",
            "description": "3D渲染风格",
        },
        "abstract": {
            "template": "Abstract art for book cover, {theme} concept, {mood} atmosphere, {keywords}, flowing shapes, modern design, professional",
            "negative": "realistic, photo, text, words, messy, chaotic",
            "description": "抽象艺术风格",
        },
        "geometric": {
            "template": "Geometric patterns for book cover, {theme}, {mood} style, {keywords}, clean lines, modern design, minimalist, professional",
            "negative": "cluttered, text, words, complex, messy, organic shapes",
            "description": "几何图形风格",
        },
        "minimalist": {
            "template": "Minimalist book cover design, {theme}, {mood} feeling, {keywords}, simple, clean, elegant, negative space, professional",
            "negative": "complex, detailed, busy, text, words, cluttered",
            "description": "极简主义风格",
        },
        "vintage": {
            "template": "Vintage book cover art, {theme}, {mood} atmosphere, {keywords}, retro style, aged texture, classic design, professional",
            "negative": "modern, digital, text, words, clean, pristine",
            "description": "复古风格",
        },
        "watercolor": {
            "template": "Watercolor painting for book cover, {theme}, {mood} feeling, {keywords}, soft colors, artistic, flowing, professional",
            "negative": "digital, hard edges, text, words, photo, realistic",
            "description": "水彩画风格",
        },
    }
    
    # 类型特定的关键词
    GENRE_KEYWORDS = {
        "科幻": ["futuristic", "space", "technology", "sci-fi", "cyber"],
        "文学": ["literary", "elegant", "classic", "sophisticated", "timeless"],
        "历史": ["historical", "ancient", "classic", "period", "traditional"],
        "悬疑": ["mysterious", "dark", "suspenseful", "noir", "shadowy"],
        "爱情": ["romantic", "emotional", "warm", "intimate", "heartfelt"],
        "儿童": ["playful", "colorful", "fun", "cheerful", "bright"],
        "商业": ["professional", "corporate", "modern", "sleek", "business"],
        "自传": ["personal", "intimate", "authentic", "genuine", "real"],
        "哲学": ["contemplative", "deep", "thoughtful", "abstract", "philosophical"],
        "科普": ["educational", "scientific", "informative", "clear", "diagram"],
    }
    
    # 情绪关键词
    MOOD_KEYWORDS = {
        "happy": ["bright", "cheerful", "joyful", "uplifting", "positive"],
        "sad": ["melancholic", "somber", "gray", "emotional", "touching"],
        "mysterious": ["enigmatic", "shadowy", "dark", "intriguing", "secretive"],
        "exciting": ["dynamic", "energetic", "vibrant", "thrilling", "action"],
        "calm": ["peaceful", "serene", "tranquil", "soothing", "quiet"],
        "dramatic": ["intense", "powerful", "bold", "striking", "impactful"],
        "romantic": ["tender", "warm", "passionate", "loving", "intimate"],
        "dark": ["noir", "gothic", "moody", "shadowy", "mysterious"],
    }
    
    # 负面提示词（通用）
    COMMON_NEGATIVE_PROMPTS = [
        "text", "words", "letters", "numbers", "title", "author name",
        "watermark", "logo", "signature",
        "low quality", "blurry", "distorted", "ugly", "bad art",
        "cropped", "out of frame", "poorly drawn",
    ]
    
    @classmethod
    def generate_cover_prompt(
        cls,
        style: str,
        theme: str,
        genre: str = "",
        mood: str = "neutral",
        additional_keywords: List[str] = None
    ) -> tuple:
        """
        生成封面提示词
        
        Args:
            style: 视觉风格
            theme: 主题
            genre: 图书类型
            mood: 情绪
            additional_keywords: 额外关键词
            
        Returns:
            (prompt, negative_prompt)
        """
        if style not in cls.COVER_IMAGE_PROMPTS:
            style = "photography"  # 默认风格
        
        template_data = cls.COVER_IMAGE_PROMPTS[style]
        template = template_data["template"]
        base_negative = template_data["negative"]
        
        # 收集关键词
        keywords = []
        
        # 添加类型关键词
        if genre in cls.GENRE_KEYWORDS:
            keywords.extend(cls.GENRE_KEYWORDS[genre][:3])
        
        # 添加情绪关键词
        if mood in cls.MOOD_KEYWORDS:
            keywords.extend(cls.MOOD_KEYWORDS[mood][:2])
        
        # 添加额外关键词
        if additional_keywords:
            keywords.extend(additional_keywords)
        
        # 构建提示词
        prompt = template.format(
            theme=theme,
            mood=mood,
            keywords=", ".join(keywords) if keywords else "professional"
        )
        
        # 构建负面提示词
        negative_prompt = base_negative + ", " + ", ".join(cls.COMMON_NEGATIVE_PROMPTS)
        
        return (prompt, negative_prompt)
    
    # 封底文案生成提示词
    BACK_COVER_PROMPT = """请为以下图书撰写吸引人的封底文案：

书名：{title}
作者：{author}
类型：{genre}
简介：{synopsis}

封底文案要求：
1. 简短精练（200-300字）
2. 引起读者兴趣和好奇心
3. 突出图书核心价值和亮点
4. 语言优美，富有感染力
5. 适合目标读者群体

请直接输出文案内容，不需要其他说明。"""
    
    # 配色推荐提示词
    COLOR_SCHEME_PROMPT = """作为专业色彩设计师，请为以下图书推荐配色方案：

图书类型：{genre}
情绪基调：{mood}
目标读者：{audience}

请以JSON格式返回配色方案，包含：
{{
  "primary": {{"hex": "#XXXXXX", "cmyk": [C, M, Y, K], "description": "主色描述"}},
  "secondary": {{"hex": "#XXXXXX", "cmyk": [C, M, Y, K], "description": "辅色描述"}},
  "accent": {{"hex": "#XXXXXX", "cmyk": [C, M, Y, K], "description": "强调色描述"}},
  "text": {{"hex": "#XXXXXX", "cmyk": [C, M, Y, K], "description": "文字色描述"}},
  "background": {{"hex": "#XXXXXX", "cmyk": [C, M, Y, K], "description": "背景色描述"}}
}}

要求：
1. 符合印刷标准（CMYK总值不超过320%）
2. 文字与背景对比度良好
3. 色彩搭配和谐，符合图书调性"""
    
    # 文字校对提示词
    PROOFREADING_PROMPT = """请校对以下图书封面文字信息，检查是否有错误：

书名：{title}
副标题：{subtitle}
作者：{author}
译者：{translator}
出版社：{publisher}
ISBN：{isbn}
价格：{price}

请检查：
1. 错别字
2. 标点符号使用
3. ISBN格式和校验码
4. 价格格式
5. 排版建议

如有问题，请列出并给出修正建议。如无问题，请回复"校对通过"。"""


class LayoutTemplates:
    """版式模板"""
    
    # 标题位置模板
    TITLE_LAYOUTS = {
        "center": {
            "horizontal": "center",
            "vertical": "center",
            "description": "居中布局",
        },
        "top": {
            "horizontal": "center",
            "vertical": "top",
            "margin_top": 0.15,  # 上边距占高度的比例
            "description": "顶部居中",
        },
        "bottom": {
            "horizontal": "center",
            "vertical": "bottom",
            "margin_bottom": 0.15,
            "description": "底部居中",
        },
        "top_left": {
            "horizontal": "left",
            "vertical": "top",
            "margin_top": 0.15,
            "margin_left": 0.1,
            "description": "左上角",
        },
        "top_right": {
            "horizontal": "right",
            "vertical": "top",
            "margin_top": 0.15,
            "margin_right": 0.1,
            "description": "右上角",
        },
    }
    
    # 文字分层模板
    TEXT_LAYERS = {
        "standard": {
            "title": {"size_ratio": 1.0, "weight": "bold", "layer": 3},
            "subtitle": {"size_ratio": 0.5, "weight": "normal", "layer": 2},
            "author": {"size_ratio": 0.6, "weight": "normal", "layer": 1},
        },
        "title_dominant": {
            "title": {"size_ratio": 1.2, "weight": "bold", "layer": 3},
            "subtitle": {"size_ratio": 0.4, "weight": "normal", "layer": 2},
            "author": {"size_ratio": 0.5, "weight": "normal", "layer": 1},
        },
        "author_prominent": {
            "title": {"size_ratio": 0.8, "weight": "bold", "layer": 2},
            "subtitle": {"size_ratio": 0.4, "weight": "normal", "layer": 1},
            "author": {"size_ratio": 0.9, "weight": "bold", "layer": 3},
        },
    }
    
    # 背景样式模板
    BACKGROUND_STYLES = {
        "solid": "纯色背景",
        "gradient": "渐变背景",
        "texture": "纹理背景",
        "image": "图像背景",
        "pattern": "图案背景",
    }
