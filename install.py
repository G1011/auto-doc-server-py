#!/usr/bin/env python3
"""
Auto Doc Server 一键安装脚本
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """运行命令并处理错误"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        sys.exit(1)
    print(f"✅ Python版本: {sys.version}")

def check_node_version():
    """检查Node.js版本"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js版本: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ 未找到Node.js，请先安装Node.js")
    print("下载地址: https://nodejs.org/")
    return False

def install_python_dependencies():
    """安装Python依赖"""
    if not run_command("pip install -r requirements.txt", "安装Python依赖"):
        return False
    
    # 创建必要的目录
    os.makedirs("auto_doc_server", exist_ok=True)
    os.makedirs("web", exist_ok=True)
    os.makedirs("docs", exist_ok=True)
    return True

def install_node_dependencies():
    """安装Node.js依赖"""
    if not run_command("npm install", "安装Node.js依赖"):
        return False
    
    # 安装VitePress
    print("🔄 安装VitePress...")
    if not run_command("cd web && npm install", "安装VitePress"):
        return False
    
    return True

def create_config_file():
    """创建配置文件"""
    config_content = """# Auto Doc Server 配置文件
project_name: "Auto Doc Server"
output_path: "./docs"
include_all: false
exclude_patterns:
  - "__pycache__"
  - "*.pyc"
  - ".git"
  - "node_modules"
  - "venv"
  - ".env"

web:
  port: 3000
  host: "localhost"
  theme: "default"

markdown:
  template: "default"
  include_source: true
  include_toc: true
"""
    
    with open("config.yaml", "w", encoding="utf-8") as f:
        f.write(config_content)
    print("✅ 配置文件已创建: config.yaml")

def main():
    """主安装流程"""
    print("🚀 Auto Doc Server 安装程序")
    print("=" * 50)
    
    # 检查Python版本
    check_python_version()
    
    # 检查Node.js版本
    if not check_node_version():
        sys.exit(1)
    
    # 安装Python依赖
    if not install_python_dependencies():
        print("❌ Python依赖安装失败")
        sys.exit(1)
    
    # 安装Node.js依赖
    if not install_node_dependencies():
        print("❌ Node.js依赖安装失败")
        sys.exit(1)
    
    # 创建配置文件
    create_config_file()
    
    print("\n🎉 安装完成！")
    print("\n📖 使用说明:")
    print("1. 在Python项目中使用装饰器 @doc_me 标记需要文档化的函数/类")
    print("2. 运行: python -m auto_doc_server.generate --project ./your_project")
    print("3. 启动Web服务: cd web && npm run dev")
    print("4. 访问: http://localhost:3000")
    
    print("\n📚 更多信息请查看 README.md")

if __name__ == "__main__":
    main() 