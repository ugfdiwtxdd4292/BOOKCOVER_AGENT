# 图书封面制作智能体系统

<div align="center">

**工业级图书封面设计AI智能体**

基于硅基流动API的完整封面制作解决方案

[功能特性](#功能特性) • [快速开始](#快速开始) • [使用指南](#使用指南) • [项目架构](#项目架构)

</div>

---

## 项目简介

本项目是一个**完整的、工业级别的、可落地的图书封面制作智能体系统**，使用硅基流动(SiliconFlow) API提供AI能力，实现从图书信息输入到印刷级PDF输出的全流程自动化。

### 核心特点

- ✅ **完全基于硅基流动API** - 所有AI能力通过硅基流动统一接口实现
- 📐 **符合印刷标准** - 支持出血、裁切标记、CMYK色彩空间
- 🎨 **多种设计风格** - 摄影、插画、3D渲染、抽象、几何等
- 📚 **完整的工作流** - 从创意到印刷文件的全链路支持
- 🔧 **高度可配置** - 支持自定义纸张、装订、特殊工艺
- 🧪 **生产级质量** - 完整的错误处理、测试覆盖、文档齐全

## 功能特性

### 第一部分：视觉与信息层
- **AI封面图像生成** - 使用硅基流动图像生成API，支持多种风格
- **智能配色引擎** - AI分析图书类型推荐色彩方案
- **中文排版系统** - 专业的中文书名和作者名排版
- **封底文案生成** - AI自动生成吸引人的封底文案

### 第二部分：结构设计要素
- **精确书脊计算** - 根据页数、纸张、装订方式自动计算
- **展开图布局** - 完整的封面+书脊+封底+勒口布局
- **ISBN条码生成** - 标准EAN-13条码，含校验码验证
- **勒口设计器** - 作者简介和系列书目排版
- **出版社品牌** - Logo定位和品牌规范

### 第三部分：制作与工艺要素
- **印刷文件处理** - RGB→CMYK转换，300dpi检查
- **出血裁切管理** - 标准3mm出血和裁切标记
- **特殊工艺支持** - UV上光、烫金烫银、压印等
- **PDF导出** - 符合印刷厂标准的PDF/X格式
- **审稿校对系统** - AI辅助文字校对和规范检查

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/ugfdiwtxdd4292/BOOKCOVER_AGENT.git
cd BOOKCOVER_AGENT

# 安装依赖
pip install -r requirements.txt

# 或使用setup.py安装
pip install -e .
```

### 配置API密钥

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，设置您的API密钥
# SILICON_KEY=your-api-key-here
```

### 命令行快速生成

```bash
# 基础用法
python cli.py generate \
    --title "时间简史" \
    --author "霍金" \
    --isbn "978-7-5357-1234-5" \
    --pages 256 \
    --price 59.80 \
    --genre "科普" \
    --style "photography" \
    --output ./output/

# 查看所有可用风格
python cli.py list-styles

# 查看支持的图书类型
python cli.py list-genres

# 验证ISBN
python cli.py validate-isbn --isbn "978-7-5357-1234-5"

# 计算书脊厚度
python cli.py calculate-spine --pages 256 --paper "胶版纸" --weight 80
```

### Web界面（Streamlit）

```bash
# 启动Web应用
streamlit run app.py

# 在浏览器中打开 http://localhost:8501
```

## 项目架构

```
BOOKCOVER_AGENT/
├── config/                    # 配置模块
│   ├── settings.py           # 全局配置（含API配置）
│   ├── paper_specs.py        # 纸张规格数据库
│   └── printing_standards.py # 印刷标准
├── core/                      # 核心模块
│   └── silicon_client.py     # 硅基流动API客户端
├── models/                    # 数据模型
│   ├── book_metadata.py      # 图书元数据
│   ├── cover_spec.py         # 封面规格
│   ├── print_spec.py         # 印刷规格
│   └── design_brief.py       # 设计简报
├── modules/                   # 功能模块
│   ├── visual/               # 视觉层
│   │   ├── cover_image_generator.py  # 封面图生成
│   │   └── ...
│   ├── structure/            # 结构层
│   │   ├── spine_calculator.py       # 书脊计算
│   │   ├── barcode_isbn_generator.py # 条码生成
│   │   └── spread_layout_engine.py   # 展开图引擎
│   └── production/           # 生产层
│       └── ...
├── templates/                 # 模板库
│   └── prompt_templates.py   # AI提示词模板
├── tests/                     # 测试
├── cli.py                     # 命令行接口
├── app.py                     # Web界面（TODO）
└── README.md                  # 本文档
```

## 使用指南

### API配置

本系统使用硅基流动API提供AI能力：

```python
# API端点
BASE_URL = "https://api.siliconflow.cn/v1"
IMAGE_GENERATION_URL = f"{BASE_URL}/images/generations"
CHAT_COMPLETION_URL = f"{BASE_URL}/chat/completions"

# 认证
Authorization: Bearer {SILICON_KEY}

# 图像生成模型
"Kwai-Kolors/Kolors" 或 "stabilityai/stable-diffusion-3-5-large"

# 文字生成模型
"Qwen/Qwen2.5-7B-Instruct" 或 "deepseek-ai/DeepSeek-V2.5"
```

### 视觉风格

支持以下视觉风格：

- `photography` - 专业摄影（适合纪实、传记类）
- `illustration` - 手绘插画（适合文学、儿童类）
- `3d_render` - 3D渲染（适合科幻、现代类）
- `abstract` - 抽象艺术（适合哲学、艺术类）
- `geometric` - 几何图形（适合商业、设计类）
- `minimalist` - 极简主义（适合现代文学）
- `vintage` - 复古风格（适合历史、经典类）
- `watercolor` - 水彩画（适合诗歌、散文类）

### 纸张规格

支持的纸张类型：

- **胶版纸** (60-120g/m²) - 最常用的书刊用纸
- **轻型纸** (60-80g/m²) - 轻薄且不透
- **铜版纸** (105-350g/m²) - 适合彩色印刷
- **特种纸** (80-300g/m²) - 艺术纸、压纹纸等

### 装订方式

- **平装** (胶装) - 最常见，适合大多数书籍
- **精装** - 硬壳精装，高档书籍
- **骑马订** - 薄册子、杂志
- **螺旋装** - 工具书、笔记本
- **线装** - 传统中式装帧

### 印刷知识科普

#### 为什么需要出血？
出血（Bleed）是印刷品边缘外延3mm的额外区域。印刷后裁切时，即使有微小偏差，也不会在成品边缘出现白边。

#### CMYK vs RGB
- **RGB** - 用于屏幕显示（红、绿、蓝）
- **CMYK** - 用于印刷（青、品红、黄、黑）
- 印刷文件必须使用CMYK色彩空间

#### 什么是书脊？
书脊是封面、封底之间的部分，宽度由书籍厚度决定。计算公式：
```
书脊宽度 = (页数 ÷ 2) × 单张纸厚度 + 装订附加
```

#### 什么是勒口？
勒口是封面两侧向内折叠的部分（通常100mm宽），用于放置作者简介、系列书目等信息。

## 开发

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_spine_calculator.py

# 查看覆盖率
pytest --cov=modules --cov=core
```

### 代码风格

本项目遵循PEP 8规范，所有代码包含完整的中文docstring。

## API使用示例

### Python API

```python
from models import BookMetadata, CoverSpec, DesignBrief
from modules.structure import SpineCalculator, BarcodeGenerator
from modules.visual import CoverImageGenerator

# 创建图书信息
book = BookMetadata(
    title="时间简史",
    author="霍金",
    isbn="9787535712345",
    page_count=256,
    price=59.80,
    genre="科普"
)

# 计算书脊
spine_width = SpineCalculator.calculate(
    page_count=256,
    paper_type="胶版纸",
    paper_weight=80
)

# 生成封面图像
generator = CoverImageGenerator()
image_path = generator.generate(
    theme="宇宙与时间",
    style="photography",
    genre="科普",
    output_path="output/cover.png"
)

# 生成ISBN条码
barcode = BarcodeGenerator()
barcode.generate(
    isbn="9787535712345",
    price=59.80,
    output_path="output/barcode.png"
)
```

## 常见问题

**Q: API密钥从哪里获取？**
A: 访问 https://siliconflow.cn 注册并获取API密钥。

**Q: 生成的图像包含文字怎么办？**
A: 在负面提示词中已经包含了"text, words, letters"，如果仍然出现，可以增加推理步数或调整引导强度。

**Q: 如何自定义字体？**
A: 将字体文件放入`fonts/`目录，然后在代码中指定字体路径。

**Q: 支持哪些输出格式？**
A: 支持PNG（带透明度）、JPEG、PDF（印刷级）、SVG（矢量图）。

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 致谢

- 硅基流动 API - 提供强大的AI能力
- python-barcode - ISBN条码生成
- Pillow - 图像处理
- ReportLab - PDF生成
- Streamlit - Web界面框架

---

<div align="center">
Made with ❤️ for Publishers and Designers
</div>