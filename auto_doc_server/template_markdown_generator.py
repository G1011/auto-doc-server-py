"""
基于Jinja2模板的Markdown文档生成器
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from .parser import ModuleInfo, FunctionInfo, ClassInfo

class TemplateMarkdownGenerator:
    """基于Jinja2模板的Markdown文档生成器"""
    
    def __init__(self, output_path: str = "./docs", template_dir: str = "templates"):
        self.output_path = Path(output_path)
        self.template_dir = Path(__file__).parent / template_dir
        
        # 初始化Jinja2环境
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "footer": "本文档由 Auto Doc Server 自动生成",
            "generation_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def generate_documentation(self, modules: List[ModuleInfo], project_name: str = "Project", 
                             custom_config: Optional[Dict[str, Any]] = None) -> None:
        """生成完整的文档"""
        # 合并配置
        config = self.get_default_config()
        if custom_config:
            config.update(custom_config)
        
        # 计算统计信息
        stats = self._calculate_stats(modules)
        
        # 生成项目概览
        self._generate_overview(modules, project_name, stats, config)
        
        # 生成每个模块的文档
        for module in modules:
            self._generate_module_doc(module, config)
        
        # 生成索引页面
        self._generate_index(modules, project_name, config)
        
        # 保存统计信息
        self._save_stats(stats)
    
    def _calculate_stats(self, modules: List[ModuleInfo]) -> Dict[str, Any]:
        """计算统计信息"""
        total_functions = sum(len(m.functions) for m in modules)
        total_classes = sum(len(m.classes) for m in modules)
        documented_functions = sum(len([f for f in m.functions if hasattr(f, '_doc_me') and f._doc_me]) for m in modules)
        documented_classes = sum(len([c for c in m.classes if hasattr(c, '_doc_me') and c._doc_me]) for m in modules)
        
        return {
            "total_functions": total_functions,
            "total_classes": total_classes,
            "documented_functions": documented_functions,
            "documented_classes": documented_classes,
            "modules": len(modules)
        }
    
    def _generate_overview(self, modules: List[ModuleInfo], project_name: str, 
                          stats: Dict[str, Any], config: Dict[str, Any]) -> None:
        """生成项目概览"""
        try:
            template = self.jinja_env.get_template('overview.j2')
            overview_content = template.render(
                project_name=project_name,
                modules=modules,
                stats=stats,
                config=config,
                generation_time=config["generation_time"]
            )
            
            overview_file = self.output_path / "overview.md"
            with open(overview_file, 'w', encoding='utf-8') as f:
                f.write(overview_content)
                
            print(f"✅ 生成项目概览: {overview_file}")
            
        except Exception as e:
            print(f"❌ 生成项目概览失败: {e}")
    
    def _generate_module_doc(self, module: ModuleInfo, config: Dict[str, Any]) -> None:
        """生成模块文档"""
        try:
            # 准备模块数据
            module_data = self._prepare_module_data(module)
            
            template = self.jinja_env.get_template('module.j2')
            module_content = template.render(
                module=module_data,
                imports_formatted=self._format_imports(module.imports),
                config=config
            )
            
            module_file = self.output_path / f"{module.name}.md"
            with open(module_file, 'w', encoding='utf-8') as f:
                f.write(module_content)
                
            print(f"✅ 生成模块文档: {module_file}")
            
        except Exception as e:
            print(f"❌ 生成模块文档失败: {e}")
    
    def _prepare_module_data(self, module: ModuleInfo) -> Dict[str, Any]:
        """准备模块数据用于模板渲染"""
        # 分离文档化和未文档化的函数
        documented_functions = [f for f in module.functions if hasattr(f, '_doc_me') and f._doc_me]
        undocumented_functions = [f for f in module.functions if not hasattr(f, '_doc_me') or not f._doc_me]
        
        return {
            "name": module.name,
            "docstring": module.docstring,
            "imports": module.imports,
            "functions": documented_functions,
            "classes": module.classes,
            "undocumented_functions": undocumented_functions
        }
    
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
    
    def _generate_index(self, modules: List[ModuleInfo], project_name: str, 
                       config: Dict[str, Any]) -> None:
        """生成索引页面"""
        try:
            # 按分类组织
            categories = {}
            for module in modules:
                for func in module.functions:
                    category = getattr(func, 'category', '其他')
                    if category not in categories:
                        categories[category] = []
                    categories[category].append((module.name, func.name, "function"))
                
                for cls in module.classes:
                    category = getattr(cls, 'category', '其他')
                    if category not in categories:
                        categories[category] = []
                    categories[category].append((module.name, cls.name, "class"))
            
            template = self.jinja_env.get_template('index.j2')
            index_content = template.render(
                project_name=project_name,
                modules=modules,
                categories=categories,
                config=config
            )
            
            index_file = self.output_path / "index.md"
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)
                
            print(f"✅ 生成索引页面: {index_file}")
            
        except Exception as e:
            print(f"❌ 生成索引页面失败: {e}")
    
    def _save_stats(self, stats: Dict[str, Any]) -> None:
        """保存统计信息"""
        try:
            stats_file = self.output_path / "stats.json"
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
                
            print(f"✅ 保存统计信息: {stats_file}")
            
        except Exception as e:
            print(f"❌ 保存统计信息失败: {e}") 