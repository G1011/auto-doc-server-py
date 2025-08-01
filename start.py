#!/usr/bin/env python3
"""
Auto Doc Server 简化启动脚本
一键完成文档生成和Web服务启动
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """检查环境"""
    print("🔍 检查环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    
    # 检查Node.js
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        print("✅ 环境检查通过")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 请先安装Node.js和npm")
        return False

def install_dependencies():
    """安装依赖"""
    print("📦 安装依赖...")
    
    try:
        # 安装Python依赖
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        
        # 安装VitePress
        web_dir = Path("web")
        web_dir.mkdir(exist_ok=True)
        
        # 创建package.json
        package_json = web_dir / "package.json"
        if not package_json.exists():
            import json
            package_data = {
                "name": "auto-doc-server-web",
                "version": "1.0.0",
                "type": "module",
                "scripts": {
                    "dev": "vitepress dev docs",
                    "build": "vitepress build docs"
                },
                "dependencies": {
                    "vitepress": "^1.0.0-rc.44"
                },
                "devDependencies": {
                    "vue": "^3.4.0"
                }
            }
            with open(package_json, 'w') as f:
                json.dump(package_data, f, indent=2)
        
        # 安装Node.js依赖
        subprocess.run(["npm", "install"], cwd=web_dir, check=True, capture_output=True)
        print("✅ 依赖安装完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def generate_docs():
    """生成文档"""
    print("📝 生成文档...")
    
    try:
        from auto_doc_server import AutoDocGenerator
        
        generator = AutoDocGenerator(
            project_path="./example_project",
            output_path="./generated_docs",
            include_all=False
        )
        generator.generate()
        print("✅ 文档生成完成")
        return True
        
    except Exception as e:
        print(f"❌ 文档生成失败: {e}")
        return False

def setup_vitepress():
    """设置VitePress"""
    print("🌐 设置VitePress...")
    
    try:
        # 创建目录结构
        docs_dir = Path("web/docs")
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        # 首页将通过Jinja2模板动态生成
        
        # 创建生成的文档目录
        generated_dir = docs_dir / "generated"
        generated_dir.mkdir(exist_ok=True)
        
        # 复制生成的文档
        import shutil
        for file in Path("generated_docs").glob("*.md"):
            shutil.copy2(file, generated_dir)
        
        # 使用Jinja2模板生成VitePress配置
        from web.vitepress_config_generator import VitePressConfigGenerator
        
        generator = VitePressConfigGenerator(
            generated_docs_path="generated_docs",
            template_dir="web/templates",
            output_dir="web/docs/.vitepress"
        )
        
        if not generator.generate_and_save():
            print("❌ VitePress配置生成失败")
            return False
        
        print("✅ VitePress设置完成")
        return True
        
    except Exception as e:
        print(f"❌ VitePress设置失败: {e}")
        return False

def start_server():
    """启动服务器"""
    print("🚀 启动服务器...")
    print("🌐 访问地址: http://localhost:3000")
    print("📖 按 Ctrl+C 停止服务器")
    
    try:
        subprocess.run(["npm", "run", "dev"], cwd="web")
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")

def main():
    """主函数"""
    print("🚀 Auto Doc Server 启动")
    print("=" * 40)
    
    # 检查环境
    if not check_environment():
        return 1
    
    # 安装依赖
    if not install_dependencies():
        return 1
    
    # 生成文档
    if not generate_docs():
        return 1
    
    # 设置VitePress
    if not setup_vitepress():
        return 1
    
    # 启动服务器
    start_server()
    return 0

if __name__ == "__main__":
    sys.exit(main()) 