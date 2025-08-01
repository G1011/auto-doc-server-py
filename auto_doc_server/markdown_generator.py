"""
Markdown文档生成器
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from .parser import ModuleInfo, FunctionInfo, ClassInfo

class MarkdownGenerator:
    """Markdown文档生成器"""
    
    def __init__(self, output_path: str = "./docs", template: str = "default"):
        self.output_path = Path(output_path)
        self.template = template
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def generate_documentation(self, modules: List[ModuleInfo], project_name: str = "Project") -> None:
        """生成完整的文档"""
        # 生成项目概览
        self._generate_overview(modules, project_name)
        
        # 生成每个模块的文档
        for module in modules:
            self._generate_module_doc(module)
        
        # 生成索引页面
        self._generate_index(modules, project_name)
    
    def _generate_overview(self, modules: List[ModuleInfo], project_name: str) -> None:
        """生成项目概览"""
        overview_content = f"""# {project_name} 项目文档

## 📋 项目概览

本项目包含以下模块：

"""
        
        # 统计信息
        total_functions = sum(len(m.functions) for m in modules)
        total_classes = sum(len(m.classes) for m in modules)
        
        overview_content += f"""
### 📊 统计信息

- **模块数量**: {len(modules)}
- **函数数量**: {total_functions}
- **类数量**: {total_classes}
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### 📁 模块列表

"""
        
        for module in modules:
            overview_content += f"- [{module.name}](./{module.name}.md) - {len(module.functions)} 个函数, {len(module.classes)} 个类\n"
        
        overview_content += """

## 🚀 快速开始

请查看各个模块的详细文档以了解具体功能。

## 📝 文档说明

- 所有公开的API都有详细的参数说明
- 包含完整的源代码示例
- 支持多种注释格式（Google、NumPy等）

---
*本文档由 Auto Doc Server 自动生成*
"""
        
        overview_file = self.output_path / "overview.md"
        with open(overview_file, 'w', encoding='utf-8') as f:
            f.write(overview_content)
    
    def _generate_module_doc(self, module: ModuleInfo) -> None:
        """生成模块文档"""
        content = f"""# {module.name} 模块

## 📖 模块概览

{module.docstring or "该模块暂无描述"}

## 📦 导入

```python
{self._format_imports(module.imports)}
```

"""
        
        # 函数部分
        if module.functions:
            content += "## 🔧 函数\n\n"
            for func in module.functions:
                content += self._format_function(func)
        
        # 类部分
        if module.classes:
            content += "## 🏗️ 类\n\n"
            for cls in module.classes:
                content += self._format_class(cls)
        
        content += f"""

---
*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        module_file = self.output_path / f"{module.name}.md"
        with open(module_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _format_function(self, func: FunctionInfo) -> str:
        """格式化函数文档"""
        content = f"""### {func.name}

{func.docstring or "该函数暂无描述"}

#### 函数签名

```python
{func.signature}
```

"""
        
        # 参数说明
        if func.parameters:
            content += "#### 参数\n\n"
            content += "| 参数名 | 类型 | 默认值 | 说明 |\n"
            content += "|--------|------|--------|------|\n"
            
            for param in func.parameters:
                param_name = param['name']
                param_type = param.get('type', 'Any')
                param_default = param.get('default', '无')
                param_desc = param.get('description', '')
                
                content += f"| {param_name} | {param_type} | {param_default} | {param_desc} |\n"
            
            content += "\n"
        
        # 返回值
        if func.return_type:
            content += f"#### 返回值\n\n类型: `{func.return_type}`\n\n"
        
        # 源代码
        content += "#### 源代码\n\n"
        content += f"```python\n{func.source_code}\n```\n\n"
        
        content += "---\n\n"
        return content
    
    def _format_class(self, cls: ClassInfo) -> str:
        """格式化类文档"""
        content = f"""### {cls.name}

{cls.docstring or "该类暂无描述"}

#### 类定义

```python
class {cls.name}{f'({", ".join(cls.bases)})' if cls.bases else ''}:
    pass
```

"""
        
        # 方法列表
        if cls.methods:
            content += "#### 方法\n\n"
            for method in cls.methods:
                content += f"- **{method.name}** - {method.docstring.split('.')[0] if method.docstring else '暂无描述'}\n"
            
            content += "\n"
            
            # 详细方法文档
            for method in cls.methods:
                content += f"##### {method.name}\n\n"
                content += f"{method.docstring or '该方法暂无描述'}\n\n"
                
                content += "**签名:**\n"
                content += f"```python\n{method.signature}\n```\n\n"
                
                # 参数说明
                if method.parameters:
                    content += "**参数:**\n"
                    content += "| 参数名 | 类型 | 默认值 | 说明 |\n"
                    content += "|--------|------|--------|------|\n"
                    
                    for param in method.parameters:
                        param_name = param['name']
                        param_type = param.get('type', 'Any')
                        param_default = param.get('default', '无')
                        param_desc = param.get('description', '')
                        
                        content += f"| {param_name} | {param_type} | {param_default} | {param_desc} |\n"
                    
                    content += "\n"
                
                # 返回值
                if method.return_type:
                    content += f"**返回值:** `{method.return_type}`\n\n"
                
                content += "---\n\n"
        
        # 源代码
        content += "#### 源代码\n\n"
        content += f"```python\n{cls.source_code}\n```\n\n"
        
        return content
    
    def _format_imports(self, imports: List[str]) -> str:
        """格式化导入语句"""
        if not imports:
            return "# 无导入语句"
        
        # 按模块分组
        import_groups = {}
        for imp in imports:
            if '.' in imp:
                module = imp.split('.')[0]
            else:
                module = imp
            
            if module not in import_groups:
                import_groups[module] = []
            import_groups[module].append(imp)
        
        # 生成导入语句
        content = ""
        for module, items in import_groups.items():
            if len(items) == 1 and items[0] == module:
                content += f"import {module}\n"
            else:
                content += f"from {module} import {', '.join(items)}\n"
        
        return content
    
    def _generate_index(self, modules: List[ModuleInfo], project_name: str) -> None:
        """生成索引页面"""
        index_content = f"""# {project_name} 文档索引

## 📚 文档导航

### 概览
- [项目概览](./overview.md)

### 模块文档

"""
        
        for module in modules:
            index_content += f"- [{module.name}](./{module.name}.md)\n"
        
        index_content += f"""

## 🔍 快速搜索

### 按功能分类

"""
        
        # 按分类组织
        categories = {}
        for module in modules:
            for func in module.functions:
                category = func.category or "其他"
                if category not in categories:
                    categories[category] = []
                categories[category].append((module.name, func.name, "function"))
            
            for cls in module.classes:
                category = cls.category or "其他"
                if category not in categories:
                    categories[category] = []
                categories[category].append((module.name, cls.name, "class"))
        
        for category, items in categories.items():
            index_content += f"#### {category}\n\n"
            for module_name, item_name, item_type in items:
                icon = "🔧" if item_type == "function" else "🏗️"
                index_content += f"- {icon} [{item_name}](./{module_name}.md#{item_name.lower()}) ({module_name})\n"
            index_content += "\n"
        
        index_content += f"""

---
*最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        index_file = self.output_path / "index.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content) 