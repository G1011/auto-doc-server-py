# example_module 模块

## 📖 模块概览


示例模块 - 演示Auto Doc Server的功能


## 📦 导入

```python
import os
import sys
from typing import typing.List, typing.Dict, typing.Optional, typing.Union
from pathlib import pathlib.Path
from auto_doc_server import auto_doc_server.doc_me

```


## 🏗️ 类

### ExampleClass

**类签名**:
```python
class ExampleClass
```

**文档字符串**:
```
示例类 - 演示类的文档生成

这个类展示了如何为类生成文档，包括方法、属性等。
```

**方法**:

#### get_value

**方法签名**:
```python
def get_value(self) -> int
```

**参数**:
| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| self | None | None |  |

**返回值**:
- **类型**: `int`
- **描述**: 

**文档字符串**:
```
获取当前值

Returns:
    int: 当前存储的值
```

**源代码**:
```python
    def get_value(self) -> int:
        """
        获取当前值
        
        Returns:
            int: 当前存储的值
        """
        return self.value
```


#### set_value

**方法签名**:
```python
def set_value(self, new_value: int) -> None
```

**参数**:
| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| self | None | None |  |
| new_value | int | None |  |

**返回值**:
- **类型**: `None`
- **描述**: 

**文档字符串**:
```
设置新的值

Args:
    new_value: 要设置的新值
```

**源代码**:
```python
    def set_value(self, new_value: int) -> None:
        """
        设置新的值
        
        Args:
            new_value: 要设置的新值
        """
        self.value = new_value
```


#### increment

**方法签名**:
```python
def increment(self, amount: int) -> int
```

**参数**:
| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| self | None | None |  |
| amount | int | 1 |  |

**返回值**:
- **类型**: `int`
- **描述**: 

**文档字符串**:
```
增加当前值

Args:
    amount: 要增加的数值，默认为1
    
Returns:
    int: 增加后的新值
```

**源代码**:
```python
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
```


#### 源代码

```python
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
```


---

### FileHandler

**类签名**:
```python
class FileHandler
```

**文档字符串**:
```
文件操作工具类

提供文件读写、路径处理等功能。
```

**方法**:

#### read_file

**方法签名**:
```python
def read_file(self, filename: str, encoding: str) -> str
```

**参数**:
| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| self | None | None |  |
| filename | str | None |  |
| encoding | str | utf-8 |  |

**返回值**:
- **类型**: `str`
- **描述**: 

**文档字符串**:
```
读取指定文件的内容

Args:
    filename: 文件名
    encoding: 文件编码，默认为utf-8
    
Returns:
    str: 文件内容
    
Raises:
    FileNotFoundError: 当文件不存在时抛出
    UnicodeDecodeError: 当编码错误时抛出
```

**源代码**:
```python
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
```


#### write_file

**方法签名**:
```python
def write_file(self, filename: str, content: str, encoding: str) -> None
```

**参数**:
| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| self | None | None |  |
| filename | str | None |  |
| content | str | None |  |
| encoding | str | utf-8 |  |

**返回值**:
- **类型**: `None`
- **描述**: 

**文档字符串**:
```
写入内容到指定文件

Args:
    filename: 文件名
    content: 要写入的内容
    encoding: 文件编码，默认为utf-8
```

**源代码**:
```python
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
```


#### 源代码

```python
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
```


## 未文档化的函数

### process_data

**函数签名**:
```python
def process_data(data: List[Dict[(str, any)]], filter_key: Optional[str]) -> List[Dict[(str, any)]]
```

**参数**:
| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| data | List[Dict[(str, any)]] | None |  |
| filter_key | Optional[str] | None |  |

**返回值**:
- **类型**: `List[Dict[(str, any)]]`
- **描述**: 

**文档字符串**:
```
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
```

**源代码**:
```python
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


---

### calculate_average

**函数签名**:
```python
def calculate_average(numbers: List[Union[(int, float)]]) -> float
```

**参数**:
| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| numbers | List[Union[(int, float)]] | None |  |

**返回值**:
- **类型**: `float`
- **描述**: 

**文档字符串**:
```
计算数字列表的平均值

Args:
    numbers: 数字列表
    
Returns:
    float: 平均值
    
Raises:
    ValueError: 当列表为空时抛出
```

**源代码**:
```python
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
```


---

### internal_helper

**函数签名**:
```python
def internal_helper()
```

**文档字符串**:
```
内部辅助函数，通常不会被包含在文档中
```

**源代码**:
```python
def internal_helper():
    """内部辅助函数，通常不会被包含在文档中"""
    pass 
```


---

*本文档由 Auto Doc Server 自动生成*
 