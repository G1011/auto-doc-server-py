# 快速开始

## 安装

### 一键安装

```bash
python3 install.py
```

这个脚本会自动：
- 检查Python和Node.js版本
- 安装Python依赖
- 安装VitePress
- 创建配置文件

### 手动安装

```bash
# 安装Python依赖
pip3 install -r requirements.txt

# 安装VitePress
cd web && npm install
```

## 基本使用

### 1. 标记需要文档化的代码

```python
from auto_doc_server import doc_me, doc_class, doc_function

@doc_me(description="数据处理工具", category="核心功能")
def process_data(data: List[Dict], filter_key: str = None) -> List[Dict]:
    """
    处理数据列表
    
    Args:
        data: 要处理的数据
        filter_key: 过滤键
        
    Returns:
        处理后的数据
    """
    return data

@doc_class(description="文件操作类", category="工具类")
class FileHandler:
    """文件操作工具类"""
    
    @doc_function(description="读取文件")
    def read_file(self, path: str) -> str:
        """读取文件内容"""
        pass
```

### 2. 生成文档

```bash
# 使用示例
python3 example_usage.py

# 或者使用命令行
python3 -m auto_doc_server.cli generate ./your_project
```

### 3. 启动Web服务

```bash
cd web && npm run dev
```

访问 http://localhost:3000 查看文档。

## 配置选项

### 基本配置

```python
generator = AutoDocGenerator(
    project_path="./your_project",
    output_path="./docs",
    include_all=False,  # 只包含标记的函数/类
    exclude_patterns=["__pycache__", "*.pyc"]
)
```

### 配置文件 (config.yaml)

```yaml
project_name: "My Project"
output_path: "./docs"
include_all: false
exclude_patterns:
  - "__pycache__"
  - "*.pyc"
  - ".git"

web:
  port: 3000
  host: "localhost"
  theme: "default"

markdown:
  template: "default"
  include_source: true
  include_toc: true
```

## 装饰器说明

### @doc_me

标记函数或类需要生成文档：

```python
@doc_me(description="自定义描述", category="分类", priority=1)
def my_function():
    pass
```

### @doc_class

专门用于标记类：

```python
@doc_class(description="类描述", category="分类")
class MyClass:
    pass
```

### @doc_function

专门用于标记函数：

```python
@doc_function(description="函数描述", category="分类")
def my_function():
    pass
```

## 命令行工具

### 生成文档

```bash
python3 -m auto_doc_server.cli generate ./project_path
```

### 监听文件变化

```bash
python3 -m auto_doc_server.cli watch ./project_path
```

### 启动Web服务

```bash
python3 -m auto_doc_server.cli serve
```

### 初始化配置

```bash
python3 -m auto_doc_server.cli init
```

## 注释格式支持

### Google风格

```python
def function(param1: str, param2: int) -> bool:
    """
    函数描述
    
    Args:
        param1: 参数1描述
        param2: 参数2描述
        
    Returns:
        返回值描述
        
    Raises:
        ValueError: 异常描述
    """
    pass
```

### NumPy风格

```python
def function(param1: str, param2: int) -> bool:
    """
    函数描述
    
    Parameters
    ----------
    param1 : str
        参数1描述
    param2 : int
        参数2描述
        
    Returns
    -------
    bool
        返回值描述
    """
    pass
```

## 下一步

- 查看 [装饰器使用指南](./decorators.md)
- 了解 [配置选项](./configuration.md)
- 学习 [命令行工具](./cli.md)
- 查看 [示例项目](../examples/) 