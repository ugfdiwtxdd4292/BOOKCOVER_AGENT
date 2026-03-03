# 使用示例集合

本文档提供了各种实际使用场景的示例。

## 场景1: 科幻小说封面

### 图书信息
- 书名: 《三体》
- 作者: 刘慈欣
- 类型: 科幻

### CLI命令
```bash
python cli.py generate \
    --title "三体" \
    --author "刘慈欣" \
    --isbn "978-7-5366-9293-0" \
    --pages 396 \
    --price 23.00 \
    --genre "科幻" \
    --style "3d_render" \
    --output ./output/three_body/
```

### Python代码
```python
from models import BookMetadata, DesignBrief
from modules.visual import CoverImageGenerator

book = BookMetadata(
    title="三体",
    author="刘慈欣",
    genre="科幻",
    page_count=396,
    price=23.00
)

brief = DesignBrief(
    visual_style="3d_render",
    mood="mysterious",
    keywords=["space", "alien", "dark"]
)

generator = CoverImageGenerator()
image = generator.generate(
    theme="外星文明与地球的第一次接触",
    style="3d_render",
    genre="科幻",
    mood="mysterious",
    keywords=["cosmos", "alien civilization", "dark"],
    output_path="output/three_body_cover.png"
)
```

## 场景2: 文学作品封面

### 图书信息
- 书名: 《活着》
- 作者: 余华
- 类型: 文学

### CLI命令
```bash
python cli.py generate \
    --title "活着" \
    --author "余华" \
    --isbn "978-7-5302-0608-4" \
    --pages 192 \
    --price 18.00 \
    --genre "文学" \
    --style "illustration" \
    --output ./output/alive/
```

### 配色推荐
```python
from modules.visual import ColorMoodEngine

engine = ColorMoodEngine()
colors = engine.generate_color_scheme(
    genre="文学",
    mood="sad"
)
print(colors)
```

## 场景3: 儿童绘本封面

### 图书信息
- 书名: 《小王子》
- 作者: 安东尼·德·圣埃克苏佩里
- 类型: 儿童

### CLI命令
```bash
python cli.py generate \
    --title "小王子" \
    --author "安东尼·德·圣埃克苏佩里" \
    --isbn "978-7-5442-3845-4" \
    --pages 96 \
    --price 28.00 \
    --genre "儿童" \
    --style "watercolor" \
    --output ./output/little_prince/
```

## 场景4: 商业书籍封面

### 图书信息
- 书名: 《从0到1》
- 作者: 彼得·蒂尔
- 类型: 商业

### CLI命令
```bash
python cli.py generate \
    --title "从0到1" \
    --author "彼得·蒂尔" \
    --isbn "978-7-5086-4804-0" \
    --pages 208 \
    --price 45.00 \
    --genre "商业" \
    --style "minimalist" \
    --output ./output/zero_to_one/
```

## 场景5: 历史传记封面

### 图书信息
- 书名: 《史记》
- 作者: 司马迁
- 类型: 历史

### CLI命令
```bash
python cli.py generate \
    --title "史记" \
    --author "司马迁" \
    --isbn "978-7-1010-8872-7" \
    --pages 3300 \
    --price 200.00 \
    --genre "历史" \
    --style "vintage" \
    --output ./output/shiji/
```

## 场景6: 批量生成

### 准备CSV文件 (books.csv)
```csv
title,author,isbn,pages,price,genre,style
时间简史,霍金,978-7-5357-1234-5,256,59.80,科普,photography
人类简史,尤瓦尔·赫拉利,978-7-5086-5902-2,448,68.00,历史,illustration
未来简史,尤瓦尔·赫拉利,978-7-5086-6841-3,396,68.00,哲学,abstract
```

### 批量生成脚本
```bash
#!/bin/bash
while IFS=, read -r title author isbn pages price genre style; do
    # 跳过标题行
    if [ "$title" = "title" ]; then
        continue
    fi
    
    echo "生成 $title 的封面..."
    python cli.py generate \
        --title "$title" \
        --author "$author" \
        --isbn "$isbn" \
        --pages "$pages" \
        --price "$price" \
        --genre "$genre" \
        --style "$style" \
        --output "./output/$title/"
    
    echo "✓ $title 完成"
    echo "---"
done < books.csv

echo "所有封面生成完成！"
```

## 场景7: 计算不同纸张的书脊

```bash
# 计算200页图书在不同纸张上的书脊厚度
python cli.py calculate-spine --pages 200 --paper "胶版纸" --weight 80
# 输出: 6.5mm

python cli.py calculate-spine --pages 200 --paper "轻型纸" --weight 70
# 输出: 9.8mm

python cli.py calculate-spine --pages 200 --paper "铜版纸" --weight 128
# 输出: 5.3mm
```

## 场景8: ISBN批量验证

```python
from modules.structure import BarcodeGenerator

isbns = [
    "978-7-5357-1234-5",
    "978-7-5086-4804-0",
    "978-7-1010-8872-7",
    "978-7-5366-9293-0"
]

generator = BarcodeGenerator()

for isbn in isbns:
    is_valid = generator.validate_isbn(isbn)
    status = "✓" if is_valid else "✗"
    print(f"{status} {isbn}: {'有效' if is_valid else '无效'}")
```

## 场景9: 自定义配色方案

```python
from models import DesignBrief

# 创建自定义配色方案
brief = DesignBrief(
    visual_style="photography",
    mood="dramatic"
)

# 手动设置配色
brief.set_color_scheme({
    "primary": {
        "hex": "#1a1a2e",
        "cmyk": [100, 100, 0, 70],
        "description": "深蓝黑"
    },
    "secondary": {
        "hex": "#00d4ff",
        "cmyk": [60, 0, 0, 0],
        "description": "科技蓝"
    },
    "accent": {
        "hex": "#ff6b6b",
        "cmyk": [0, 80, 60, 0],
        "description": "珊瑚红"
    }
})

print(brief.to_dict())
```

## 场景10: 完整的封面制作流程

```python
from pathlib import Path
from models import BookMetadata, CoverSpec, DesignBrief
from modules.structure import SpineCalculator, BarcodeGenerator
from modules.visual import CoverImageGenerator, ColorMoodEngine
from core import SiliconFlowClient

# 1. 创建图书信息
book = BookMetadata(
    title="时间简史",
    author="霍金",
    isbn="9787535712345",
    page_count=256,
    price=59.80,
    genre="科普",
    synopsis="探索宇宙的起源、时间的本质和黑洞的奥秘。"
)

# 2. 创建输出目录
output_dir = Path("output/time_brief")
output_dir.mkdir(parents=True, exist_ok=True)

# 3. 计算书脊
spine_width = SpineCalculator.calculate(
    page_count=256,
    paper_type="胶版纸",
    paper_weight=80
)
print(f"✓ 书脊宽度: {spine_width}mm")

# 4. 创建封面规格
spec = CoverSpec(
    trim_width=170,
    trim_height=240,
    spine_width=spine_width,
    paper_type="胶版纸",
    paper_weight=80
)

# 5. 生成配色方案
color_engine = ColorMoodEngine()
colors = color_engine.generate_color_scheme("科普", "mysterious")
print(f"✓ 配色方案已生成")

# 6. 创建设计简报
brief = DesignBrief(
    visual_style="photography",
    mood="mysterious",
    keywords=["cosmos", "time", "physics"]
)
brief.set_color_scheme(colors)

# 7. 生成封面图像
generator = CoverImageGenerator()
cover_image = generator.generate(
    theme="宇宙与时间的奥秘",
    style="photography",
    genre="科普",
    mood="mysterious",
    keywords=["space", "time", "black hole"],
    output_path=str(output_dir / "cover.png")
)
print(f"✓ 封面图像: {cover_image}")

# 8. 生成ISBN条码
barcode_gen = BarcodeGenerator()
barcode = barcode_gen.generate(
    isbn="9787535712345",
    price=59.80,
    output_path=str(output_dir / "barcode.png")
)
print(f"✓ 条码: {barcode}")

# 9. 生成封底文案
client = SiliconFlowClient()
back_text = client.generate_back_cover_text(book.to_dict())
(output_dir / "back_text.txt").write_text(back_text, encoding='utf-8')
print(f"✓ 封底文案已生成")

print(f"\n🎉 所有文件已生成到: {output_dir}")
```

---

更多示例和用法请参考 [README.md](README.md) 和 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
