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

### 1. 在代码中使用装饰器

```python
from auto_doc_server import doc_me

@doc_me(description="数据处理函数", category="核心功能")
def process_data(data: list) -> dict:
    """处理数据并返回结果"""
    return {"result": data}
```

### 2. 生成文档

```bash
python3 start.py
```

### 3. 查看文档

访问 http://localhost:3000

## 🎯 核心特性

- 🐍 **Python原生支持**: 专为Python项目设计
- 📝 **智能解析**: 自动识别代码结构和注释
- 🎯 **装饰器控制**: 精确控制文档生成范围
- 🌐 **现代化界面**: 基于VitePress的美观界面
- ⚡ **一键启动**: 简化部署流程

## 📁 项目结构

```
auto-doc-server-py/
├── auto_doc_server/          # 核心模块
├── example_project/          # 示例项目
├── web/                      # VitePress界面
├── start.py                  # 启动脚本
├── requirements.txt          # Python依赖
└── README.md                 # 说明文档
```

## 🔧 装饰器说明

### @doc_me

标记函数或类需要生成文档：

```python
@doc_me(description="描述", category="分类", priority=1)
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

## 📋 支持的功能

- ✅ 自动解析Python代码
- ✅ 装饰器标记的文档化
- ✅ 参数表格和类型注解
- ✅ 代码语法高亮
- ✅ 完整的源代码展示
- ✅ 多种注释格式支持

## 🛠️ 技术栈

- **后端**: Python 3.8+, AST解析
- **前端**: VitePress, Vue 3
- **构建**: Vite
- **样式**: 内置主题

## �� 许可证

MIT License 