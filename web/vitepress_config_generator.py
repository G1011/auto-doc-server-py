#!/usr/bin/env python3
"""
VitePress配置生成器
使用Jinja2模板动态生成VitePress配置文件
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from jinja2 import Environment, FileSystemLoader

class VitePressConfigGenerator:
    """VitePress配置生成器"""
    
    def __init__(self, generated_docs_path: str = "../generated_docs", 
                 template_dir: str = "templates",
                 output_dir: str = "docs/.vitepress"):
        self.generated_docs_path = Path(generated_docs_path)
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        
        # 初始化Jinja2环境
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def parse_generated_docs(self) -> List[Dict[str, Any]]:
        """解析生成的文档，提取路由信息"""
        docs = []
        
        if not self.generated_docs_path.exists():
            print(f"⚠️ 生成的文档目录不存在: {self.generated_docs_path}")
            return docs
        
        # 解析Markdown文件
        for md_file in self.generated_docs_path.glob("*.md"):
            if md_file.name == "index.md":
                continue  # 跳过索引文件
                
            doc_info = self._parse_markdown_file(md_file)
            docs.append(doc_info)
        
        return docs
    
    def _parse_markdown_file(self, file_path: Path) -> Dict[str, Any]:
        """解析单个Markdown文件"""
        doc_info = {
            "filename": file_path.name,
            "route": file_path.stem,
            "title": file_path.stem.replace("_", " ").title(),
            "sections": [],
            "description": ""
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取标题
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match:
                doc_info["title"] = title_match.group(1).strip()
            
            # 提取章节信息
            sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
            doc_info["sections"] = sections
            
            # 提取描述（第一段非标题文本）
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('---'):
                    doc_info["description"] = line
                    break
            
            # 特殊处理某些文件
            if file_path.name == "overview.md":
                doc_info["title"] = "项目概览"
                doc_info["description"] = "项目整体概览和统计信息"
            elif file_path.name == "example_module.md":
                doc_info["title"] = "示例模块"
                doc_info["description"] = "example_module.py 的详细文档"
                
        except Exception as e:
            print(f"⚠️ 解析文件 {file_path.name} 失败: {e}")
        
        return doc_info
    
    def get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "title": "Auto Doc Server",
            "description": "自动为Python项目生成美观的文档",
            "tagline": "智能解析代码，生成结构化文档",
            "lang": "zh-CN",
            "site_title": "Auto Doc Server",
            "github_url": "https://github.com/your-repo",
            "social_links": [
                {"icon": "github", "url": "https://github.com/your-repo"}
            ],
            "footer": {
                "message": "Released under the MIT License.",
                "copyright": "Copyright © 2024 Auto Doc Server"
            },
            "markdown": {
                "theme": "material-theme-palenight",
                "line_numbers": True,
                "toc_levels": [1, 2, 3]
            },
            "vite": {
                "port": 3000,
                "host": "localhost"
            }
        }
    
    def generate_config(self, custom_config: Optional[Dict[str, Any]] = None) -> str:
        """生成VitePress配置文件内容"""
        # 解析生成的文档
        docs = self.parse_generated_docs()
        
        # 合并配置
        config = self.get_default_config()
        if custom_config:
            config.update(custom_config)
        
        # 渲染模板
        template = self.jinja_env.get_template('vitepress_config.j2')
        config_content = template.render(config=config, docs=docs)
        
        return config_content
    
    def save_config(self, config_content: str, output_file: str = "config.ts") -> bool:
        """保存配置文件"""
        try:
            # 确保输出目录存在
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # 写入配置文件
            config_file = self.output_dir / output_file
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(config_content)
            
            print(f"✅ VitePress配置已生成: {config_file}")
            return True
            
        except Exception as e:
            print(f"❌ 保存配置文件失败: {e}")
            return False
    
    def generate_index_page(self, custom_config: Optional[Dict[str, Any]] = None) -> str:
        """生成首页内容"""
        # 解析生成的文档
        docs = self.parse_generated_docs()
        
        # 获取统计信息
        stats = self._get_stats()
        
        # 合并配置
        config = self.get_default_config()
        if custom_config:
            config.update(custom_config)
        
        # 渲染首页模板
        template = self.jinja_env.get_template('index.j2')
        index_content = template.render(config=config, docs=docs, stats=stats)
        
        return index_content
    
    def _get_stats(self) -> Optional[Dict[str, Any]]:
        """获取统计信息"""
        try:
            stats_file = self.generated_docs_path / "stats.json"
            if stats_file.exists():
                with open(stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return None
    
    def save_index_page(self, index_content: str, output_file: str = "index.md") -> bool:
        """保存首页文件"""
        try:
            # 确保输出目录存在
            index_dir = self.output_dir.parent
            index_dir.mkdir(parents=True, exist_ok=True)
            
            # 写入首页文件
            index_file = index_dir / output_file
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            print(f"✅ 首页已生成: {index_file}")
            return True
            
        except Exception as e:
            print(f"❌ 保存首页失败: {e}")
            return False
    
    def generate_and_save(self, custom_config: Optional[Dict[str, Any]] = None) -> bool:
        """生成并保存配置文件"""
        try:
            # 生成VitePress配置
            config_content = self.generate_config(custom_config)
            if not self.save_config(config_content):
                return False
            
            # 生成首页
            index_content = self.generate_index_page(custom_config)
            if not self.save_index_page(index_content):
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ 生成配置文件失败: {e}")
            return False

def main():
    """主函数"""
    generator = VitePressConfigGenerator()
    
    # 自定义配置示例
    custom_config = {
        "title": "My Project Docs",
        "description": "我的项目文档",
        "github_url": "https://github.com/myuser/myproject",
        "vite": {
            "port": 3000,
            "host": "localhost"
        }
    }
    
    if generator.generate_and_save(custom_config):
        print("🎉 VitePress配置生成完成！")
    else:
        print("❌ 配置生成失败")

if __name__ == "__main__":
    main() 