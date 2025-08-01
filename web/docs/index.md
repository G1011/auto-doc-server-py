---
layout: home
hero:
  name: Auto Doc Server
  text: 自动为Python项目生成美观的文档
  tagline: 智能解析代码，生成结构化文档
  actions:
    - theme: brand
      text: 查看文档
      link: /generated/
    - theme: alt
      text: GitHub
      link: https://github.com/your-repo

features:
  - icon: 🚀
    title: 自动生成
    details: 自动解析Python代码，生成结构化的Markdown文档，支持多种注释格式
  - icon: 🎨
    title: 美观界面
    details: 基于VitePress的现代化Web界面，支持深色模式，响应式设计
  - icon: 🔧
    title: 灵活配置
    details: 支持装饰器标记，可配置包含规则，支持排除模式
  - icon: 📦
    title: 一键部署
    details: 提供完整的安装脚本，支持一键安装依赖和部署
  - icon: 🔍
    title: 智能解析
    details: 自动识别函数、类、方法，解析参数类型和默认值
  - icon: 📝
    title: 多种格式
    details: 支持Google、NumPy等主流注释格式，生成高质量文档
---

## 快速开始

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

访问 http://localhost:3000 查看文档。

## 项目统计

- **模块数量**: 1
- **函数数量**: 3
- **类数量**: 2
- **文档化函数**: 
- **文档化类**: 

## 生成的文档

- [项目概览](/generated/overview) - 项目整体概览和统计信息
- [示例模块](/generated/example_module) - example_module.py 的详细文档

## 核心特性

- 🐍 **Python原生支持**: 专为Python项目设计
- 📝 **智能解析**: 自动识别代码结构和注释
- 🎯 **装饰器控制**: 精确控制文档生成范围
- 🌐 **现代化界面**: 基于VitePress的美观界面
- ⚡ **快速部署**: 一键安装和启动
- 🔧 **灵活配置**: 丰富的配置选项

## 技术栈

- **后端**: Python 3.8+, AST解析, Click CLI
- **前端**: VitePress, Vue 3, Markdown
- **构建**: Vite, TypeScript
- **样式**: 内置主题, 响应式设计

---

Released under the MIT License.
 