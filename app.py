"""
Streamlit Web UI
图书封面制作智能体系统的Web界面
"""
import streamlit as st
import logging
from pathlib import Path

from models.book_metadata import BookMetadata
from models.cover_spec import CoverSpec
from models.design_brief import DesignBrief
from modules.structure.spine_calculator import SpineCalculator
from modules.structure.barcode_isbn_generator import BarcodeGenerator
from modules.visual.cover_image_generator import CoverImageGenerator, ColorMoodEngine
from core.silicon_client import SiliconFlowClient
from templates.prompt_templates import PromptTemplates
from config.paper_specs import list_paper_types

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 页面配置
st.set_page_config(
    page_title="图书封面制作智能体",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 标题
st.title("📚 图书封面制作智能体系统")
st.markdown("**基于硅基流动API的工业级封面设计工具**")

# 侧边栏 - 图书信息输入
st.sidebar.header("📖 图书基本信息")

with st.sidebar:
    title = st.text_input("书名 *", value="时间简史", help="必填项")
    author = st.text_input("作者", value="霍金")
    
    col1, col2 = st.columns(2)
    with col1:
        pages = st.number_input("页数", min_value=1, value=256, step=1)
    with col2:
        price = st.number_input("定价（元）", min_value=0.0, value=59.80, step=0.10)
    
    isbn = st.text_input("ISBN", value="978-7-5357-1234-5", help="13位ISBN号码")
    
    # 图书类型
    genres = list(PromptTemplates.GENRE_KEYWORDS.keys())
    genre = st.selectbox("图书类型", genres, index=genres.index("科普") if "科普" in genres else 0)
    
    synopsis = st.text_area(
        "内容简介",
        value="探索宇宙的起源、时间的本质和黑洞的奥秘。",
        height=100
    )

# 主内容区 - 设计参数
st.header("🎨 设计参数")

tab1, tab2, tab3 = st.tabs(["视觉风格", "封面规格", "印刷选项"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # 视觉风格选择
        styles = list(PromptTemplates.COVER_IMAGE_PROMPTS.keys())
        style_names = [PromptTemplates.COVER_IMAGE_PROMPTS[s]["description"] for s in styles]
        style_index = st.selectbox(
            "视觉风格",
            range(len(styles)),
            format_func=lambda i: f"{styles[i]} - {style_names[i]}"
        )
        visual_style = styles[style_index]
        
        # 情绪基调
        moods = list(PromptTemplates.MOOD_KEYWORDS.keys())
        mood = st.selectbox("情绪基调", moods, index=moods.index("neutral"))
        
    with col2:
        # 额外关键词
        keywords_input = st.text_input(
            "额外关键词",
            value="",
            help="用逗号分隔，如：科技,未来,深空"
        )
        keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
        
        # 主题描述
        theme = st.text_input(
            "主题描述",
            value=f"{genre}类图书关于宇宙和时间",
            help="用于AI生成提示词"
        )

with tab2:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        trim_width = st.number_input("成品宽度（mm）", value=170, step=1)
        trim_height = st.number_input("成品高度（mm）", value=240, step=1)
    
    with col2:
        paper_types = list_paper_types()
        paper_type = st.selectbox("纸张类型", paper_types, index=0)
        paper_weight = st.number_input("纸张克重（g/m²）", value=80, step=5)
    
    with col3:
        binding_types = ["平装", "精装", "骑马订", "螺旋装", "线装"]
        binding = st.selectbox("装订方式", binding_types, index=0)
        has_flaps = st.checkbox("包含勒口", value=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        include_barcode = st.checkbox("包含ISBN条码", value=True)
        generate_back_text = st.checkbox("AI生成封底文案", value=True)
    
    with col2:
        lamination = st.selectbox("覆膜", ["无", "亮膜", "哑膜"], index=0)
        lamination = None if lamination == "无" else lamination

# 生成按钮
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    generate_button = st.button("🚀 生成封面", type="primary", use_container_width=True)

# 生成流程
if generate_button:
    if not title:
        st.error("请输入书名！")
    else:
        try:
            # 创建输出目录
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            
            # 进度条
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 1. 创建数据模型
            status_text.text("📝 准备数据...")
            progress_bar.progress(10)
            
            book = BookMetadata(
                title=title,
                author=author,
                isbn=isbn,
                page_count=pages,
                price=price,
                genre=genre,
                synopsis=synopsis
            )
            
            brief = DesignBrief(
                visual_style=visual_style,
                theme=theme,
                mood=mood,
                keywords=keywords
            )
            
            # 2. 计算书脊
            status_text.text("📐 计算书脊厚度...")
            progress_bar.progress(20)
            
            try:
                spine_width = SpineCalculator.calculate(
                    page_count=pages,
                    paper_type=paper_type,
                    paper_weight=paper_weight,
                    binding_type=binding
                )
                st.success(f"✓ 书脊宽度：{spine_width}mm")
            except Exception as e:
                st.warning(f"⚠ 书脊计算失败：{str(e)}")
                spine_width = 8.0
            
            # 3. 生成配色方案
            status_text.text("🎨 生成配色方案...")
            progress_bar.progress(30)
            
            try:
                color_engine = ColorMoodEngine()
                color_scheme = color_engine.generate_color_scheme(genre, mood)
                st.success("✓ 配色方案已生成")
                
                # 显示配色方案
                if color_scheme and "primary" in color_scheme:
                    color_cols = st.columns(5)
                    for i, (name, color_data) in enumerate(color_scheme.items()):
                        if i < 5 and isinstance(color_data, dict) and "hex" in color_data:
                            with color_cols[i]:
                                st.markdown(
                                    f'<div style="background-color:{color_data["hex"]};'
                                    f'height:50px;border-radius:5px;margin:5px 0;"></div>'
                                    f'<small>{name}</small>',
                                    unsafe_allow_html=True
                                )
            except Exception as e:
                st.warning(f"⚠ 配色方案生成失败：{str(e)}")
            
            # 4. 生成封面图像
            status_text.text("🖼️ AI生成封面图像...")
            progress_bar.progress(50)
            
            try:
                cover_generator = CoverImageGenerator()
                image_path = cover_generator.generate(
                    theme=theme,
                    style=visual_style,
                    genre=genre,
                    mood=mood,
                    keywords=keywords,
                    output_path=str(output_dir / "cover_image.png")
                )
                st.success("✓ 封面图像已生成")
                
                # 显示图像
                st.image(image_path, caption="生成的封面图像", use_container_width=True)
                
            except Exception as e:
                st.error(f"✗ 封面图像生成失败：{str(e)}")
                logger.error(f"Image generation error: {str(e)}")
            
            # 5. 生成ISBN条码
            if include_barcode and isbn:
                status_text.text("📊 生成ISBN条码...")
                progress_bar.progress(70)
                
                try:
                    barcode_gen = BarcodeGenerator()
                    barcode_path = barcode_gen.generate(
                        isbn=isbn,
                        price=price if price > 0 else None,
                        output_path=str(output_dir / "barcode.png")
                    )
                    st.success(f"✓ 条码已生成：{barcode_path}")
                    
                    # 显示条码
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.image(barcode_path, caption="ISBN条码")
                        
                except Exception as e:
                    st.warning(f"⚠ 条码生成失败：{str(e)}")
            
            # 6. 生成封底文案
            if generate_back_text:
                status_text.text("📝 AI生成封底文案...")
                progress_bar.progress(85)
                
                try:
                    client = SiliconFlowClient()
                    back_text = client.generate_back_cover_text(book.to_dict())
                    
                    # 保存文案
                    back_text_path = output_dir / "back_cover_text.txt"
                    back_text_path.write_text(back_text, encoding='utf-8')
                    
                    st.success("✓ 封底文案已生成")
                    
                    # 显示文案
                    with st.expander("查看封底文案", expanded=True):
                        st.markdown(back_text)
                        
                except Exception as e:
                    st.warning(f"⚠ 封底文案生成失败：{str(e)}")
            
            # 完成
            progress_bar.progress(100)
            status_text.text("✨ 生成完成！")
            
            st.success("🎉 封面制作完成！所有文件已保存到 output/ 目录")
            
            # 下载按钮
            st.markdown("### 📥 下载文件")
            
            download_cols = st.columns(3)
            
            # 提供下载链接
            if (output_dir / "cover_image.png").exists():
                with download_cols[0]:
                    with open(output_dir / "cover_image.png", "rb") as f:
                        st.download_button(
                            "📷 下载封面图像",
                            f,
                            file_name=f"{title}_cover.png",
                            mime="image/png"
                        )
            
            if (output_dir / "barcode.png").exists():
                with download_cols[1]:
                    with open(output_dir / "barcode.png", "rb") as f:
                        st.download_button(
                            "📊 下载条码",
                            f,
                            file_name=f"{title}_barcode.png",
                            mime="image/png"
                        )
            
            if (output_dir / "back_cover_text.txt").exists():
                with download_cols[2]:
                    with open(output_dir / "back_cover_text.txt", "r", encoding='utf-8') as f:
                        st.download_button(
                            "📝 下载封底文案",
                            f,
                            file_name=f"{title}_back_text.txt",
                            mime="text/plain"
                        )
            
        except Exception as e:
            st.error(f"❌ 生成过程出错：{str(e)}")
            logger.error(f"Generation error: {str(e)}", exc_info=True)

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    📚 图书封面制作智能体系统 v1.0 | 基于硅基流动API | 
    <a href='https://github.com/ugfdiwtxdd4292/BOOKCOVER_AGENT'>GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)
