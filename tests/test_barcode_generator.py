"""
测试条码生成器
"""
import pytest
import os
from pathlib import Path
from modules.structure.barcode_isbn_generator import BarcodeGenerator


def test_validate_isbn_valid():
    """测试有效ISBN验证"""
    gen = BarcodeGenerator()
    
    # 标准有效ISBN
    assert gen.validate_isbn("9787535712345") is True
    assert gen.validate_isbn("978-7-5357-1234-5") is True


def test_validate_isbn_invalid():
    """测试无效ISBN"""
    gen = BarcodeGenerator()
    
    # 校验码错误
    assert gen.validate_isbn("9787535712346") is False
    
    # 长度错误
    assert gen.validate_isbn("978753571234") is False
    assert gen.validate_isbn("97875357123456") is False


def test_calculate_check_digit():
    """测试校验码计算"""
    gen = BarcodeGenerator()
    
    # 前12位
    isbn12 = "978753571234"
    check_digit = gen.calculate_check_digit(isbn12)
    
    # 验证完整ISBN
    full_isbn = isbn12 + check_digit
    assert gen.validate_isbn(full_isbn) is True


def test_format_isbn():
    """测试ISBN格式化"""
    gen = BarcodeGenerator()
    
    isbn = "9787535712345"
    formatted = gen.format_isbn(isbn)
    
    # 应该包含连字符
    assert "-" in formatted
    assert formatted.startswith("978-7-")


def test_generate_barcode(tmp_path):
    """测试条码生成"""
    gen = BarcodeGenerator()
    
    output_file = tmp_path / "test_barcode.png"
    
    # 生成条码
    result = gen.generate(
        isbn="9787535712345",
        price=59.80,
        output_path=str(output_file)
    )
    
    # 检查文件是否存在
    # 注意：python-barcode可能会自动添加扩展名
    assert os.path.exists(result)


def test_generate_barcode_invalid_isbn():
    """测试无效ISBN生成"""
    gen = BarcodeGenerator()
    
    with pytest.raises(ValueError):
        gen.generate(
            isbn="invalid_isbn",
            output_path="output/test.png"
        )
