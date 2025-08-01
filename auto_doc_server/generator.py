"""
主要的文档生成器类
"""

import os
import yaml
from pathlib import Path
from typing import List, Optional, Dict, Any
from .parser import PythonParser, ModuleInfo
from .template_markdown_generator import TemplateMarkdownGenerator

class AutoDocGenerator:
    """自动文档生成器"""
    
    def __init__(
        self,
        project_path: str,
        output_path: str = "./docs",
        config_path: Optional[str] = None,
        include_all: bool = False,
        exclude_patterns: Optional[List[str]] = None
    ):
        self.project_path = Path(project_path)
        self.output_path = Path(output_path)
        self.config_path = Path(config_path) if config_path else None
        self.include_all = include_all
        self.exclude_patterns = exclude_patterns or []
        
        # 加载配置
        self.config = self._load_config()
        
        # 初始化组件
        self.parser = PythonParser(include_all=self.include_all)
        self.markdown_generator = TemplateMarkdownGenerator(
            output_path=str(self.output_path)
        )
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        config = {
            'project_name': 'Auto Doc Server',
            'output_path': str(self.output_path),
            'include_all': self.include_all,
            'exclude_patterns': self.exclude_patterns,
            'web': {
                'port': 3000,
                'host': 'localhost',
                'theme': 'default'
            },
            'markdown': {
                'template': 'default',
                'include_source': True,
                'include_toc': True
            }
        }
        
        if self.config_path and self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    file_config = yaml.safe_load(f)
                    config.update(file_config)
            except Exception as e:
                print(f"警告: 无法加载配置文件 {self.config_path}: {e}")
        
        return config
    
    def generate(self) -> None:
        """生成文档"""
        print("🚀 开始生成文档...")
        
        # 验证项目路径
        if not self.project_path.exists():
            raise FileNotFoundError(f"项目路径不存在: {self.project_path}")
        
        # 创建输出目录
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # 查找Python文件
        python_files = self._find_python_files()
        print(f"📁 找到 {len(python_files)} 个Python文件")
        
        # 解析所有文件
        modules = []
        for file_path in python_files:
            try:
                module_info = self.parser.parse_file(file_path)
                if module_info.functions or module_info.classes:
                    modules.append(module_info)
                    print(f"✅ 解析文件: {file_path.name}")
            except Exception as e:
                print(f"❌ 解析文件失败 {file_path.name}: {e}")
        
        print(f"📊 解析完成: {len(modules)} 个模块")
        
        # 生成文档
        project_name = self.config.get('project_name', 'Project')
        self.markdown_generator.generate_documentation(modules, project_name)
        
        print(f"📝 文档生成完成: {self.output_path}")
        
        # 生成统计信息
        self._generate_stats(modules)
    
    def _find_python_files(self) -> List[Path]:
        """查找Python文件"""
        python_files = []
        
        for root, dirs, files in os.walk(self.project_path):
            # 排除不需要的目录
            dirs[:] = [d for d in dirs if not self._should_exclude(d)]
            
            for file in files:
                if file.endswith('.py') and not self._should_exclude(file):
                    file_path = Path(root) / file
                    python_files.append(file_path)
        
        return python_files
    
    def _should_exclude(self, name: str) -> bool:
        """判断是否应该排除"""
        exclude_patterns = self.config.get('exclude_patterns', [])
        
        for pattern in exclude_patterns:
            if pattern in name or name.startswith(pattern):
                return True
        
        return False
    
    def _generate_stats(self, modules: List[ModuleInfo]) -> None:
        """生成统计信息"""
        total_functions = sum(len(m.functions) for m in modules)
        total_classes = sum(len(m.classes) for m in modules)
        
        stats = {
            'modules': len(modules),
            'functions': total_functions,
            'classes': total_classes,
            'generated_at': str(Path.cwd()),
            'output_path': str(self.output_path)
        }
        
        stats_file = self.output_path / "stats.json"
        import json
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"📈 统计信息: {total_functions} 个函数, {total_classes} 个类")
    
    def watch_and_generate(self) -> None:
        """监听文件变化并自动重新生成"""
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        
        class DocGeneratorHandler(FileSystemEventHandler):
            def __init__(self, generator):
                self.generator = generator
                self.last_generated = 0
            
            def on_modified(self, event):
                if event.is_directory:
                    return
                
                if event.src_path.endswith('.py'):
                    import time
                    current_time = time.time()
                    if current_time - self.last_generated > 2:  # 防抖
                        print(f"🔄 检测到文件变化: {event.src_path}")
                        self.generator.generate()
                        self.last_generated = current_time
        
        event_handler = DocGeneratorHandler(self)
        observer = Observer()
        observer.schedule(event_handler, str(self.project_path), recursive=True)
        observer.start()
        
        print(f"👀 开始监听文件变化: {self.project_path}")
        print("按 Ctrl+C 停止监听")
        
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
            print("🛑 停止监听") 