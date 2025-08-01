"""
装饰器模块 - 用于标记需要文档化的函数和类
"""

import functools
import inspect
from typing import Any, Callable, Optional, Union

def doc_me(
    func_or_class: Optional[Union[Callable, type]] = None,
    *,
    description: Optional[str] = None,
    category: Optional[str] = None,
    priority: int = 0
):
    """
    装饰器：标记函数或类需要生成文档
    
    用法示例：
    @doc_me
    def my_function():
        pass
    
    @doc_me(description="自定义描述", category="核心功能", priority=1)
    def my_function():
        pass
    
    @doc_me(description="我的类", category="工具类")
    class MyClass:
        pass
    
    Args:
        func_or_class: 被装饰的函数或类（可选）
        description: 自定义描述
        category: 分类
        priority: 优先级（数字越大优先级越高）
    
    Returns:
        装饰后的函数或类
    """
    def decorator(obj: Union[Callable, type]) -> Union[Callable, type]:
        # 添加文档标记属性
        obj._doc_me = True
        obj._doc_description = description
        obj._doc_category = category
        obj._doc_priority = priority
        
        # 如果是类，为所有方法添加标记
        if inspect.isclass(obj):
            for name, member in inspect.getmembers(obj):
                if inspect.isfunction(member) and not name.startswith('_'):
                    member._doc_me = True
                    member._doc_category = category
                    member._doc_priority = priority
        
        return obj
    
    if func_or_class is None:
        return decorator
    else:
        return decorator(func_or_class)

def is_documented(obj: Any) -> bool:
    """
    检查对象是否被标记为需要文档化
    
    Args:
        obj: 要检查的对象
    
    Returns:
        bool: 是否被标记
    """
    return hasattr(obj, '_doc_me') and obj._doc_me

def get_doc_info(obj: Any) -> dict:
    """
    获取对象的文档信息
    
    Args:
        obj: 要检查的对象
    
    Returns:
        dict: 文档信息，包含description、category、priority
    """
    if not is_documented(obj):
        return {}
    
    return {
        'description': getattr(obj, '_doc_description', None),
        'category': getattr(obj, '_doc_category', None),
        'priority': getattr(obj, '_doc_priority', 0)
    } 