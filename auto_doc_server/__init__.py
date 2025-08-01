"""
Auto Doc Server - 自动文档生成器
"""

from .generator import AutoDocGenerator
from .decorators import doc_me, is_documented, get_doc_info
from .parser import PythonParser
from .template_markdown_generator import TemplateMarkdownGenerator

__version__ = "1.0.0"
__author__ = "Auto Doc Server Team"

__all__ = [
    "AutoDocGenerator",
    "doc_me",
    "is_documented", 
    "get_doc_info",
    "PythonParser",
    "TemplateMarkdownGenerator"
] 