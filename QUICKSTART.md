# 快速开始指南

## 安装步骤

### 1. 克隆仓库
```bash
git clone https://github.com/ugfdiwtxdd4292/BOOKCOVER_AGENT.git
cd BOOKCOVER_AGENT
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置API密钥
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，设置您的硅基流动API密钥
# SILICON_KEY=your-api-key-here
```

## 使用方式

### 方式一：命令行工具（推荐用于批量处理）

#### 生成完整封面
```bash
python cli.py generate \
    --title "时间简史" \
    --author "霍金" \
    --isbn "978-7-5357-1234-5" \
    --pages 256 \
    --price 59.80 \
    --genre "科普" \
    --style "photography" \
    --output ./output/
```

#### 计算书脊厚度
```bash
python cli.py calculate-spine --pages 256 --paper "胶版纸" --weight 80
```

#### 验证ISBN
```bash
python cli.py validate-isbn --isbn "978-7-5357-1234-5"
```

#### 查看可用选项
```bash
# 查看所有视觉风格
python cli.py list-styles

# 查看支持的图书类型
python cli.py list-genres

# 查看帮助
python cli.py --help
```

### 方式二：Web界面（推荐用于交互设计）

#### 启动Web应用
```bash
streamlit run app.py
```

然后在浏览器中打开 http://localhost:8501

#### Web界面功能
1. 📖 **图书信息输入** - 在左侧栏填写书名、作者、页数等
2. 🎨 **设计参数配置** - 选择视觉风格、情绪基调、纸张规格
3. 🚀 **一键生成** - 点击"生成封面"按钮开始
4. 👀 **实时预览** - 查看生成的封面图像和配色方案
5. 📥 **下载文件** - 下载封面图像、条码、文案

### 方式三：Python API（用于集成到其他系统）

```python
from models import BookMetadata, DesignBrief
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
print(f"书脊宽度: {spine_width}mm")

# 生成封面图像
generator = CoverImageGenerator()
image_path = generator.generate(
    theme="宇宙与时间的奥秘",
    style="photography",
    genre="科普",
    mood="mysterious",
    output_path="output/cover.png"
)

# 生成ISBN条码
barcode = BarcodeGenerator()
barcode_path = barcode.generate(
    isbn="9787535712345",
    price=59.80,
    output_path="output/barcode.png"
)

print(f"封面图像: {image_path}")
print(f"条码文件: {barcode_path}")
```

## 输出文件

生成的文件将保存在 `output/` 目录：

- `cover_image.png` - 封面主图（CMYK，300dpi）
- `barcode.png` - ISBN条码
- `back_cover_text.txt` - 封底文案

## 支持的选项

### 视觉风格
- `photography` - 专业摄影
- `illustration` - 手绘插画
- `3d_render` - 3D渲染
- `abstract` - 抽象艺术
- `geometric` - 几何图形
- `minimalist` - 极简主义
- `vintage` - 复古风格
- `watercolor` - 水彩画

### 图书类型
科幻、文学、历史、悬疑、爱情、儿童、商业、自传、哲学、科普

### 纸张类型
- 胶版纸 (60-120g/m²)
- 轻型纸 (60-80g/m²)
- 铜版纸 (105-350g/m²)
- 特种纸 (80-300g/m²)

### 装订方式
平装、精装、骑马订、螺旋装、线装

## 常见问题

### Q: 如何获取硅基流动API密钥？
A: 访问 https://siliconflow.cn 注册账号并获取API密钥。

### Q: 为什么生成的图像包含文字？
A: 系统已配置负面提示词来避免文字，如仍出现可以：
- 增加推理步数 (num_inference_steps)
- 调整引导强度 (guidance_scale)
- 尝试不同的视觉风格

### Q: 可以自定义字体吗？
A: 可以。将字体文件放入 `fonts/` 目录，然后在代码中指定路径。

### Q: 生成需要多长时间？
A: 根据网络速度和API负载，通常：
- 封面图像: 10-30秒
- 配色方案: 2-5秒
- 封底文案: 3-8秒
- ISBN条码: 即时

### Q: 如何批量生成多本书的封面？
A: 使用CLI工具配合shell脚本：
```bash
#!/bin/bash
while IFS=, read -r title author isbn pages price genre; do
    python cli.py generate \
        --title "$title" \
        --author "$author" \
        --isbn "$isbn" \
        --pages "$pages" \
        --price "$price" \
        --genre "$genre" \
        --output "./output/$title/"
done < books.csv
```

## 下一步

- 📖 阅读完整的 [README.md](README.md)
- 📋 查看 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- 🧪 运行测试: `pytest tests/`
- 💻 查看代码: 浏览 `modules/` 目录
- 🎨 自定义风格: 编辑 `templates/prompt_templates.py`

## 技术支持

遇到问题？
1. 检查 `.env` 文件中的API密钥是否正确
2. 确保已安装所有依赖: `pip install -r requirements.txt`
3. 查看日志输出定位问题
4. 提交Issue到GitHub仓库

---

祝您使用愉快！📚✨
