"""
示例模块 - 演示Auto Doc Server的功能
"""

import os
import sys
from typing import List, Dict, Optional, Union
from pathlib import Path

from auto_doc_server import doc_me

@doc_me(description="这是一个示例类", category="核心功能", priority=1)
class ExampleClass:
    """
    示例类 - 演示类的文档生成
    
    这个类展示了如何为类生成文档，包括方法、属性等。
    """
    
    def __init__(self, name: str, value: int = 0):
        """
        初始化示例类
        
        Args:
            name: 类实例的名称
            value: 初始值，默认为0
        """
        self.name = name
        self.value = value
    
    @doc_me(description="获取当前值", category="数据操作")
    def get_value(self) -> int:
        """
        获取当前值
        
        Returns:
            int: 当前存储的值
        """
        return self.value
    
    @doc_me(description="设置新值", category="数据操作")
    def set_value(self, new_value: int) -> None:
        """
        设置新的值
        
        Args:
            new_value: 要设置的新值
        """
        self.value = new_value
    
    @doc_me(description="增加值", category="数据操作")
    def increment(self, amount: int = 1) -> int:
        """
        增加当前值
        
        Args:
            amount: 要增加的数值，默认为1
            
        Returns:
            int: 增加后的新值
        """
        self.value += amount
        return self.value

@doc_me(description="数据处理工具函数", category="工具函数")
def process_data(data: List[Dict[str, any]], filter_key: Optional[str] = None) -> List[Dict[str, any]]:
    """
    处理数据列表
    
    这个函数可以处理包含字典的列表，支持可选的过滤功能。
    
    Args:
        data: 要处理的数据列表
        filter_key: 可选的过滤键，如果提供则只返回包含该键的字典
        
    Returns:
        List[Dict[str, any]]: 处理后的数据列表
        
    Raises:
        ValueError: 当数据格式不正确时抛出
        KeyError: 当过滤键不存在时抛出
        
    Example:
        >>> data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
        >>> result = process_data(data, 'age')
        >>> print(result)
        [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
    """
    if not isinstance(data, list):
        raise ValueError("数据必须是列表格式")
    
    if filter_key:
        return [item for item in data if filter_key in item]
    
    return data

@doc_me(description="计算平均值", category="数学计算")
def calculate_average(numbers: List[Union[int, float]]) -> float:
    """
    计算数字列表的平均值
    
    Args:
        numbers: 数字列表
        
    Returns:
        float: 平均值
        
    Raises:
        ValueError: 当列表为空时抛出
    """
    if not numbers:
        raise ValueError("数字列表不能为空")
    
    return sum(numbers) / len(numbers)

@doc_class(description="文件操作工具类", category="文件操作")
class FileHandler:
    """
    文件操作工具类
    
    提供文件读写、路径处理等功能。
    """
    
    def __init__(self, base_path: str = "."):
        """
        初始化文件处理器
        
        Args:
            base_path: 基础路径，默认为当前目录
        """
        self.base_path = Path(base_path)
    
    @doc_me(description="读取文件内容", category="文件操作")
    def read_file(self, filename: str, encoding: str = "utf-8") -> str:
        """
        读取指定文件的内容
        
        Args:
            filename: 文件名
            encoding: 文件编码，默认为utf-8
            
        Returns:
            str: 文件内容
            
        Raises:
            FileNotFoundError: 当文件不存在时抛出
            UnicodeDecodeError: 当编码错误时抛出
        """
        file_path = self.base_path / filename
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    
    @doc_me(description="写入文件内容", category="文件操作")
    def write_file(self, filename: str, content: str, encoding: str = "utf-8") -> None:
        """
        写入内容到指定文件
        
        Args:
            filename: 文件名
            content: 要写入的内容
            encoding: 文件编码，默认为utf-8
        """
        file_path = self.base_path / filename
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)

# 这个函数没有装饰器，默认不会被包含在文档中（除非设置include_all=True）
def internal_helper():
    """内部辅助函数，通常不会被包含在文档中"""
    pass 