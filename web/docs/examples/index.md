# 示例项目

这里展示了Auto Doc Server的完整功能示例。

## 项目结构

```
example_project/
└── example_module.py  # 示例模块
```

## 生成的文档

- [项目概览](../generated/overview.md)
- [示例模块](../generated/example_module.md)
- [索引页面](../generated/index.md)

## 示例代码

### 装饰器使用

```python
from auto_doc_server import doc_me, doc_class, doc_function

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
    
    @doc_function(description="获取当前值", category="数据操作")
    def get_value(self) -> int:
        """
        获取当前值
        
        Returns:
            int: 当前存储的值
        """
        return self.value
```

### 函数文档

```python
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
```

## 运行示例

### 1. 生成文档

```bash
python3 example_usage.py
```

### 2. 查看生成的文档

生成的文档位于 `generated_docs/` 目录：

- `overview.md` - 项目概览
- `example_module.md` - 示例模块详细文档
- `index.md` - 索引页面
- `stats.json` - 统计信息

### 3. 启动Web服务

```bash
cd web && npm run dev
```

访问 http://localhost:3000 查看文档。

## 文档特性

### 自动解析

- ✅ 函数签名和参数
- ✅ 类型注解
- ✅ 文档字符串
- ✅ 源代码展示
- ✅ 导入语句

### 格式化输出

- 📝 结构化的Markdown
- 📊 参数表格
- 💻 代码高亮
- 🔗 内部链接
- 📋 目录导航

### 分类组织

- 🏷️ 按装饰器分类
- 📁 按模块组织
- 🔍 搜索功能
- 📱 响应式设计

## 下一步

- 查看 [生成的文档](../generated/)
- 学习 [装饰器使用](../guide/decorators.md)
- 了解 [配置选项](../guide/configuration.md) 