"""
命令行接口
"""

import click
import sys
from pathlib import Path
from .generator import AutoDocGenerator

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Auto Doc Server - 自动文档生成器"""
    pass

@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='./docs', help='输出目录')
@click.option('--config', '-c', help='配置文件路径')
@click.option('--include-all', is_flag=True, help='包含所有函数和类')
@click.option('--exclude', multiple=True, help='排除的文件模式')
@click.option('--enable-comment-markers', is_flag=True, default=True, help='启用注释标记功能')
@click.option('--disable-comment-markers', is_flag=True, help='禁用注释标记功能')
def generate(project_path, output, config, include_all, exclude, enable_comment_markers, disable_comment_markers):
    """生成文档"""
    try:
        # 处理注释标记选项
        if disable_comment_markers:
            enable_comment_markers = False
        
        generator = AutoDocGenerator(
            project_path=project_path,
            output_path=output,
            config_path=config,
            include_all=include_all,
            exclude_patterns=list(exclude),
            enable_comment_markers=enable_comment_markers
        )
        generator.generate()
        click.echo("✅ 文档生成完成!")
    except Exception as e:
        click.echo(f"❌ 生成失败: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='./docs', help='输出目录')
@click.option('--config', '-c', help='配置文件路径')
@click.option('--enable-comment-markers', is_flag=True, default=True, help='启用注释标记功能')
@click.option('--disable-comment-markers', is_flag=True, help='禁用注释标记功能')
def watch(project_path, output, config, enable_comment_markers, disable_comment_markers):
    """监听文件变化并自动重新生成"""
    try:
        # 处理注释标记选项
        if disable_comment_markers:
            enable_comment_markers = False
        
        generator = AutoDocGenerator(
            project_path=project_path,
            output_path=output,
            config_path=config,
            enable_comment_markers=enable_comment_markers
        )
        generator.watch_and_generate()
    except KeyboardInterrupt:
        click.echo("\n👋 再见!")
    except Exception as e:
        click.echo(f"❌ 监听失败: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--port', default=3000, help='服务器端口')
@click.option('--host', default='localhost', help='服务器地址')
def serve(port, host):
    """启动Web服务器"""
    try:
        import subprocess
        import os
        
        # 检查是否有web目录
        web_dir = Path("web")
        if not web_dir.exists():
            click.echo("❌ web目录不存在，请先构建前端项目", err=True)
            sys.exit(1)
        
        # 同步文档到VitePress
        click.echo("🔄 同步文档到VitePress...")
        os.chdir(web_dir)
        subprocess.run(["python3", "sync_docs.py"], check=True)
        
        # 启动VitePress开发服务器
        click.echo(f"🌐 启动VitePress服务器 (http://{host}:{port})...")
        subprocess.run(["npm", "run", "dev"])
        
    except FileNotFoundError:
        click.echo("❌ 未找到npm，请先安装Node.js", err=True)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ 同步文档失败: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ 启动服务器失败: {e}", err=True)
        sys.exit(1)

@cli.command()
def init():
    """初始化项目配置"""
    config_content = """# Auto Doc Server 配置文件
project_name: "My Project"
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
    
    config_file = Path("config.yaml")
    if config_file.exists():
        if not click.confirm("配置文件已存在，是否覆盖?"):
            return
    
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    click.echo("✅ 配置文件已创建: config.yaml")

if __name__ == '__main__':
    cli() 