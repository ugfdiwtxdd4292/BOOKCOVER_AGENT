#!/usr/bin/env python3
"""
命令行接口
提供图书封面生成的命令行工具
"""
import click
import logging
from pathlib import Path

from models.book_metadata import BookMetadata
from models.cover_spec import CoverSpec
from models.design_brief import DesignBrief
from modules.structure.spine_calculator import SpineCalculator
from modules.structure.barcode_isbn_generator import BarcodeGenerator
from modules.visual.cover_image_generator import CoverImageGenerator, ColorMoodEngine
from core.silicon_client import SiliconFlowClient

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    """图书封面制作智能体系统"""
    pass


@cli.command()
@click.option('--title', required=True, help='书名')
@click.option('--author', default='', help='作者')
@click.option('--isbn', default='', help='ISBN号')
@click.option('--pages', default=200, help='页数')
@click.option('--price', default=0.0, help='定价')
@click.option('--genre', default='文学', help='图书类型')
@click.option('--style', default='photography', help='视觉风格')
@click.option('--output', default='./output/', help='输出目录')
def generate(title, author, isbn, pages, price, genre, style, output):
    """生成图书封面"""
    click.echo(f"开始生成封面: {title}")
    
    try:
        # 创建图书元数据
        book = BookMetadata(
            title=title,
            author=author,
            isbn=isbn,
            page_count=pages,
            price=price,
            genre=genre
        )
        
        # 创建设计简报
        brief = DesignBrief(
            visual_style=style,
            theme=f"{genre}类图书 - {title}",
            mood="neutral"
        )
        
        # 创建输出目录
        output_dir = Path(output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. 计算书脊
        click.echo(f"\n1. 计算书脊厚度...")
        spine_width = SpineCalculator.calculate(
            page_count=pages,
            paper_type="胶版纸",
            paper_weight=80
        )
        click.echo(f"   书脊宽度: {spine_width}mm")
        
        # 2. 生成配色方案
        click.echo(f"\n2. 生成配色方案...")
        color_engine = ColorMoodEngine()
        color_scheme = color_engine.generate_color_scheme(genre, "neutral")
        click.echo(f"   配色方案已生成")
        
        # 3. 生成封面图像
        click.echo(f"\n3. 生成封面图像...")
        cover_generator = CoverImageGenerator()
        
        cover_image_path = output_dir / "cover_image.png"
        try:
            image_path = cover_generator.generate(
                theme=f"{genre} book about {title}",
                style=style,
                genre=genre,
                mood="neutral",
                output_path=str(cover_image_path)
            )
            click.echo(f"   封面图像: {image_path}")
        except Exception as e:
            click.echo(f"   警告: 封面图像生成失败: {str(e)}", err=True)
            click.echo(f"   将继续其他步骤...")
        
        # 4. 生成ISBN条码
        if isbn:
            click.echo(f"\n4. 生成ISBN条码...")
            barcode_gen = BarcodeGenerator()
            try:
                barcode_path = barcode_gen.generate(
                    isbn=isbn,
                    price=price if price > 0 else None,
                    output_path=str(output_dir / "barcode.png")
                )
                click.echo(f"   条码文件: {barcode_path}")
            except Exception as e:
                click.echo(f"   警告: 条码生成失败: {str(e)}", err=True)
        
        # 5. 生成封底文案
        click.echo(f"\n5. 生成封底文案...")
        client = SiliconFlowClient()
        try:
            back_text = client.generate_back_cover_text(book.to_dict())
            back_text_path = output_dir / "back_cover_text.txt"
            back_text_path.write_text(back_text, encoding='utf-8')
            click.echo(f"   封底文案: {back_text_path}")
            click.echo(f"   预览: {back_text[:100]}...")
        except Exception as e:
            click.echo(f"   警告: 封底文案生成失败: {str(e)}", err=True)
        
        click.echo(f"\n✓ 封面生成完成！")
        click.echo(f"  输出目录: {output_dir.absolute()}")
        
    except Exception as e:
        click.echo(f"\n✗ 生成失败: {str(e)}", err=True)
        raise


@cli.command()
@click.option('--isbn', required=True, help='ISBN号')
def validate_isbn(isbn):
    """验证ISBN号"""
    barcode_gen = BarcodeGenerator()
    
    is_valid = barcode_gen.validate_isbn(isbn)
    
    if is_valid:
        click.echo(f"✓ ISBN有效: {isbn}")
        formatted = barcode_gen.format_isbn(isbn)
        click.echo(f"  格式化: {formatted}")
    else:
        click.echo(f"✗ ISBN无效: {isbn}", err=True)
        
        # 尝试计算正确的校验码
        isbn_clean = isbn.replace("-", "").replace(" ", "")
        if len(isbn_clean) == 12:
            check_digit = barcode_gen.calculate_check_digit(isbn_clean)
            correct_isbn = isbn_clean + check_digit
            click.echo(f"  正确的ISBN应该是: {barcode_gen.format_isbn(correct_isbn)}")


@cli.command()
@click.option('--pages', required=True, type=int, help='页数')
@click.option('--paper', default='胶版纸', help='纸张类型')
@click.option('--weight', default=80, type=int, help='纸张克重')
def calculate_spine(pages, paper, weight):
    """计算书脊厚度"""
    try:
        width = SpineCalculator.calculate(
            page_count=pages,
            paper_type=paper,
            paper_weight=weight
        )
        
        click.echo(f"书脊厚度: {width}mm")
        click.echo(f"  页数: {pages}页")
        click.echo(f"  纸张: {paper} {weight}g/m²")
        
        # 显示其他纸张类型的推荐
        click.echo(f"\n其他纸张类型推荐:")
        recommendations = SpineCalculator.recommend_spine_width(pages, weight)
        for paper_type, width in recommendations.items():
            click.echo(f"  {paper_type}: {width}mm")
            
    except Exception as e:
        click.echo(f"✗ 计算失败: {str(e)}", err=True)


@cli.command()
def list_styles():
    """列出所有可用的视觉风格"""
    from templates.prompt_templates import PromptTemplates
    
    click.echo("可用的视觉风格:\n")
    for style, data in PromptTemplates.COVER_IMAGE_PROMPTS.items():
        click.echo(f"  {style:15s} - {data['description']}")


@cli.command()
def list_genres():
    """列出所有支持的图书类型"""
    from templates.prompt_templates import PromptTemplates
    
    click.echo("支持的图书类型:\n")
    for genre in PromptTemplates.GENRE_KEYWORDS.keys():
        click.echo(f"  - {genre}")


def main():
    """主入口"""
    cli()


if __name__ == '__main__':
    main()
