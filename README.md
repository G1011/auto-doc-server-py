# Auto Doc Server

自动为Python项目生成Markdown文档并提供美观的Web界面。

## 🚀 快速开始

### 一键启动

```bash
python3 start.py
```

这个命令会自动完成：
1. 环境检查
2. 依赖安装
3. 文档生成
4. Web服务启动

然后访问 http://localhost:3000 查看文档。

## 📝 使用方法

### 1. 使用装饰器（推荐用于新项目）

```python
from auto_doc_server import doc_me

@doc_me(description="数据处理函数", category="核心功能")
def process_data(data: list) -> dict:
    """处理数据并返回结果"""
    return {"result": data}
```

### 2. 使用注释标记（推荐用于现有项目）

```python
# @doc_me(description="数据处理函数", category="核心功能")
def process_data(data: list) -> dict:
    """处理数据并返回结果"""
    return {"result": data}

# @api(description="用户管理类", category="用户管理")
class UserManager:
    """用户管理类"""
    
    # @doc
    def add_user(self, user_id: str, name: str) -> bool:
        """添加用户"""
        pass
```

### 3. 生成文档

```bash
# 使用默认设置（启用注释标记）
python3 start.py

# 禁用注释标记
python3 -m auto_doc_server.cli generate ./my_project --disable-comment-markers

# 包含所有函数和类
python3 -m auto_doc_server.cli generate ./my_project --include-all
```

### 4. 查看文档

访问 http://localhost:3000

## 🎯 核心特性

- 🐍 **Python原生支持**: 专为Python项目设计
- 📝 **智能解析**: 自动识别代码结构和注释
- 🎯 **双重标记**: 支持装饰器和注释标记两种方式
- 🌐 **现代化界面**: 基于VitePress的美观界面
- ⚡ **一键启动**: 简化部署流程
- 🔧 **现有项目友好**: 无需修改代码结构即可生成文档

## 📁 项目结构

```
auto-doc-server-py/
├── auto_doc_server/          # 核心模块
├── example_project/          # 示例项目
├── web/                      # VitePress界面
├── start.py                  # 启动脚本
├── requirements.txt          # Python依赖
├── COMMENT_MARKERS.md        # 注释标记详细说明
└── README.md                 # 说明文档
```

## 🔧 标记方式说明

### 装饰器方式

#### @doc_me

标记函数或类需要生成文档：

```python
@doc_me(description="描述", category="分类", priority=1)
def my_function():
    pass
```

### 注释标记方式

#### 简单标记

```python
# @doc
def my_function():
    pass

# @doc_me
class MyClass:
    pass

# @document
def another_function():
    pass

# @api
def public_api():
    pass

# @public
def public_function():
    pass
```

#### 带参数的标记

```python
# @doc(description="自定义描述", category="核心功能", priority=1)
def my_function():
    pass

# @doc_me(description="用户管理类", category="用户管理", priority=2)
class UserManager:
    pass
```

## 📋 支持的功能

- ✅ 自动解析Python代码
- ✅ 装饰器标记的文档化
- ✅ 注释标记的文档化
- ✅ 参数表格和类型注解
- ✅ 多种文档风格支持
- ✅ 分类和优先级管理
- ✅ 现代化Web界面
- ✅ 实时文件监听 