"""
硅基流动API统一客户端
实现图像生成和文字生成的完整接口
"""
import os
import time
import json
import requests
from typing import List, Dict, Optional, Any
from pathlib import Path
import logging

from config.settings import SiliconFlowConfig

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SiliconFlowClient:
    """
    硅基流动API客户端
    
    提供图像生成、文字生成等AI能力的统一接口
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化客户端
        
        Args:
            api_key: API密钥，如果不提供则从配置中读取
        """
        self.api_key = api_key or SiliconFlowConfig.SILICON_KEY
        self.base_url = SiliconFlowConfig.BASE_URL
        self.image_url = SiliconFlowConfig.IMAGE_GENERATION_URL
        self.chat_url = SiliconFlowConfig.CHAT_COMPLETION_URL
        
        # 超时和重试配置
        self.timeout = SiliconFlowConfig.REQUEST_TIMEOUT
        self.max_retries = SiliconFlowConfig.MAX_RETRIES
        self.retry_delay = SiliconFlowConfig.RETRY_DELAY
        
        # 会话
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
    
    def _make_request(self, url: str, payload: dict, method: str = "POST") -> dict:
        """
        发起HTTP请求（带重试机制）
        
        Args:
            url: 请求URL
            payload: 请求体
            method: HTTP方法
            
        Returns:
            响应JSON
            
        Raises:
            Exception: 请求失败
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                if method.upper() == "POST":
                    response = self.session.post(
                        url,
                        json=payload,
                        timeout=self.timeout
                    )
                else:
                    response = self.session.get(
                        url,
                        params=payload,
                        timeout=self.timeout
                    )
                
                # 检查状态码
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    # 速率限制，等待后重试
                    logger.warning(f"速率限制，等待 {self.retry_delay * (attempt + 1)} 秒后重试...")
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                else:
                    error_msg = f"请求失败: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    last_error = Exception(error_msg)
                    
            except requests.exceptions.Timeout:
                logger.warning(f"请求超时，尝试 {attempt + 1}/{self.max_retries}")
                last_error = Exception("请求超时")
                
            except requests.exceptions.RequestException as e:
                logger.error(f"请求异常: {str(e)}")
                last_error = e
            
            # 重试延迟
            if attempt < self.max_retries - 1:
                time.sleep(self.retry_delay)
        
        # 所有重试都失败
        raise last_error or Exception("请求失败")
    
    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        image_size: str = None,
        num_inference_steps: int = None,
        guidance_scale: float = None,
        seed: Optional[int] = None,
        batch_size: int = 1,
        model: str = None
    ) -> List[str]:
        """
        生成图像
        
        Args:
            prompt: 图像描述提示词
            negative_prompt: 负面提示词（不想要的元素）
            image_size: 图像尺寸（如 "1024x1024"）
            num_inference_steps: 推理步数
            guidance_scale: 引导强度
            seed: 随机种子（可选）
            batch_size: 生成图像数量
            model: 模型名称（可选，默认使用配置中的模型）
            
        Returns:
            图像URL列表
            
        Raises:
            Exception: 生成失败
        """
        # 使用默认值
        image_size = image_size or SiliconFlowConfig.DEFAULT_IMAGE_SIZE
        num_inference_steps = num_inference_steps or SiliconFlowConfig.DEFAULT_INFERENCE_STEPS
        guidance_scale = guidance_scale or SiliconFlowConfig.DEFAULT_GUIDANCE_SCALE
        model = model or SiliconFlowConfig.IMAGE_MODEL
        
        # 构建请求体
        payload = {
            "model": model,
            "prompt": prompt,
            "image_size": image_size,
            "batch_size": batch_size,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
        }
        
        # 添加可选参数
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        
        if seed is not None:
            payload["seed"] = seed
        
        logger.info(f"正在生成图像: {prompt[:50]}...")
        logger.debug(f"请求参数: {json.dumps(payload, ensure_ascii=False)}")
        
        try:
            # 发起请求
            response = self._make_request(self.image_url, payload)
            
            # 解析响应
            if "images" in response:
                images = response["images"]
                image_urls = []
                
                for img in images:
                    if "url" in img:
                        image_urls.append(img["url"])
                    elif "b64_json" in img:
                        # 如果返回base64编码，也添加（虽然硅基流动主要返回URL）
                        image_urls.append(f"data:image/png;base64,{img['b64_json']}")
                
                logger.info(f"成功生成 {len(image_urls)} 张图像")
                return image_urls
            else:
                raise Exception("响应中没有图像数据")
                
        except Exception as e:
            logger.error(f"图像生成失败: {str(e)}")
            raise
    
    def download_image(self, image_url: str, save_path: str) -> str:
        """
        下载图像到本地
        
        Args:
            image_url: 图像URL
            save_path: 保存路径
            
        Returns:
            保存的文件路径
            
        Raises:
            Exception: 下载失败
        """
        try:
            logger.info(f"正在下载图像: {image_url}")
            
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()
            
            # 确保目录存在
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            
            # 保存文件
            with open(save_path, "wb") as f:
                f.write(response.content)
            
            logger.info(f"图像已保存: {save_path}")
            return save_path
            
        except Exception as e:
            logger.error(f"图像下载失败: {str(e)}")
            raise
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        max_tokens: int = None,
        temperature: float = None,
        stream: bool = False
    ) -> str:
        """
        文字生成（聊天补全）
        
        Args:
            messages: 消息列表，格式: [{"role": "user", "content": "..."}]
            model: 模型名称（可选）
            max_tokens: 最大token数
            temperature: 温度参数
            stream: 是否流式输出
            
        Returns:
            生成的文本内容
            
        Raises:
            Exception: 生成失败
        """
        # 使用默认值
        model = model or SiliconFlowConfig.CHAT_MODEL
        max_tokens = max_tokens or SiliconFlowConfig.MAX_TOKENS
        temperature = temperature or SiliconFlowConfig.TEMPERATURE
        
        # 构建请求体
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": stream
        }
        
        logger.info(f"正在生成文本，消息数: {len(messages)}")
        logger.debug(f"请求参数: {json.dumps(payload, ensure_ascii=False)}")
        
        try:
            if stream:
                # 流式输出（暂时不实现，返回非流式结果）
                logger.warning("流式输出暂不支持，使用非流式模式")
                payload["stream"] = False
            
            # 发起请求
            response = self._make_request(self.chat_url, payload)
            
            # 解析响应
            if "choices" in response and len(response["choices"]) > 0:
                content = response["choices"][0]["message"]["content"]
                logger.info(f"成功生成文本，长度: {len(content)}")
                return content
            else:
                raise Exception("响应中没有生成的文本")
                
        except Exception as e:
            logger.error(f"文本生成失败: {str(e)}")
            raise
    
    def generate_cover_description(self, book_info: dict) -> str:
        """
        生成封面描述提示词
        
        Args:
            book_info: 图书信息字典
            
        Returns:
            封面描述提示词
        """
        # 构建系统提示
        system_prompt = """你是一位专业的图书封面设计师和AI提示词工程师。
请根据图书信息，生成一个详细的、适合AI图像生成的封面描述提示词。
提示词应该：
1. 描述视觉风格（摄影、插画、3D渲染等）
2. 描述主要元素和构图
3. 描述色调和氛围
4. 使用英文，简洁明了
5. 避免包含文字内容（书名等会单独排版）"""
        
        # 构建用户消息
        user_message = f"""请为以下图书生成封面描述提示词：

书名：{book_info.get('title', '')}
作者：{book_info.get('author', '')}
类型：{book_info.get('genre', '')}
简介：{book_info.get('synopsis', '')[:200]}

请生成一个适合AI图像生成的英文提示词。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        try:
            prompt = self.chat_completion(messages, temperature=0.8)
            logger.info(f"生成的封面描述: {prompt[:100]}...")
            return prompt.strip()
        except Exception as e:
            logger.error(f"生成封面描述失败: {str(e)}")
            # 返回一个简单的默认提示词
            return f"book cover design, {book_info.get('genre', 'literature')}, professional, clean composition"
    
    def generate_back_cover_text(self, book_info: dict) -> str:
        """
        生成封底文案
        
        Args:
            book_info: 图书信息字典
            
        Returns:
            封底文案
        """
        system_prompt = """你是一位专业的图书文案撰写专家。
请根据图书信息，生成简洁有力的封底文案。
封底文案应该：
1. 简短精练（200-300字）
2. 吸引读者兴趣
3. 体现图书核心价值
4. 使用中文"""
        
        user_message = f"""请为以下图书撰写封底文案：

书名：{book_info.get('title', '')}
作者：{book_info.get('author', '')}
类型：{book_info.get('genre', '')}
简介：{book_info.get('synopsis', '')}

请生成一段吸引人的封底文案（200-300字）。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        try:
            text = self.chat_completion(messages, temperature=0.7)
            logger.info(f"生成的封底文案: {text[:50]}...")
            return text.strip()
        except Exception as e:
            logger.error(f"生成封底文案失败: {str(e)}")
            # 返回简介作为后备
            return book_info.get('synopsis', '')[:300]
    
    def generate_color_scheme(self, genre: str, mood: str = "neutral") -> dict:
        """
        生成配色方案
        
        Args:
            genre: 图书类型
            mood: 情绪基调
            
        Returns:
            配色方案字典
        """
        system_prompt = """你是一位专业的色彩设计师。
请根据图书类型和情绪基调，推荐一个专业的配色方案。
配色方案应该包含：
1. 主色（primary）：主导色调
2. 辅色（secondary）：辅助色调
3. 强调色（accent）：突出重点
4. 文字色（text）：文字颜色
5. 背景色（background）：背景色

请以JSON格式返回，每个颜色包含：
- hex: 十六进制色值
- cmyk: CMYK色值数组 [C, M, Y, K]
- description: 色彩描述"""
        
        user_message = f"""图书类型：{genre}
情绪基调：{mood}

请推荐一个配色方案（JSON格式）。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        try:
            response = self.chat_completion(messages, temperature=0.7)
            
            # 尝试解析JSON
            try:
                # 提取JSON部分（可能包含在代码块中）
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    color_scheme = json.loads(json_str)
                    logger.info(f"生成的配色方案: {color_scheme}")
                    return color_scheme
            except json.JSONDecodeError:
                logger.warning("无法解析配色方案JSON，使用默认方案")
            
        except Exception as e:
            logger.error(f"生成配色方案失败: {str(e)}")
        
        # 返回默认配色方案
        return self._get_default_color_scheme(genre)
    
    def _get_default_color_scheme(self, genre: str) -> dict:
        """
        获取默认配色方案
        
        Args:
            genre: 图书类型
            
        Returns:
            配色方案字典
        """
        # 预设的配色方案
        schemes = {
            "科幻": {
                "primary": {"hex": "#1a1a2e", "cmyk": [100, 100, 0, 70], "description": "深蓝黑"},
                "secondary": {"hex": "#16213e", "cmyk": [100, 80, 0, 60], "description": "深蓝"},
                "accent": {"hex": "#00d4ff", "cmyk": [60, 0, 0, 0], "description": "科技蓝"},
                "text": {"hex": "#ffffff", "cmyk": [0, 0, 0, 0], "description": "白色"},
                "background": {"hex": "#0f3460", "cmyk": [100, 60, 0, 50], "description": "深蓝背景"}
            },
            "文学": {
                "primary": {"hex": "#2c3e50", "cmyk": [80, 60, 40, 30], "description": "深灰蓝"},
                "secondary": {"hex": "#95a5a6", "cmyk": [40, 30, 30, 0], "description": "浅灰"},
                "accent": {"hex": "#e74c3c", "cmyk": [0, 80, 80, 0], "description": "砖红"},
                "text": {"hex": "#2c3e50", "cmyk": [80, 60, 40, 30], "description": "深灰蓝"},
                "background": {"hex": "#ecf0f1", "cmyk": [10, 5, 5, 0], "description": "浅灰白"}
            },
            "历史": {
                "primary": {"hex": "#8b4513", "cmyk": [0, 60, 90, 40], "description": "褐色"},
                "secondary": {"hex": "#d4af37", "cmyk": [0, 20, 80, 10], "description": "金色"},
                "accent": {"hex": "#cd853f", "cmyk": [0, 40, 70, 20], "description": "古铜色"},
                "text": {"hex": "#3e2723", "cmyk": [0, 60, 70, 80], "description": "深褐"},
                "background": {"hex": "#f5e6d3", "cmyk": [0, 10, 20, 5], "description": "米色"}
            },
        }
        
        # 返回对应类型的配色，或默认配色
        return schemes.get(genre, schemes["文学"])
