"""
Python代码解析器 - 支持多种注释格式解析
"""

import ast
import inspect
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

@dataclass
class FunctionInfo:
    """函数信息"""
    name: str
    docstring: str
    signature: str
    parameters: List[Dict[str, Any]]
    return_type: Optional[str]
    source_code: str
    line_number: int
    category: Optional[str] = None
    priority: int = 0
    comment_marked: bool = False  # 是否通过注释标记

@dataclass
class ClassInfo:
    """类信息"""
    name: str
    docstring: str
    bases: List[str]
    methods: List[FunctionInfo]
    source_code: str
    line_number: int
    category: Optional[str] = None
    priority: int = 0
    comment_marked: bool = False  # 是否通过注释标记

@dataclass
class ModuleInfo:
    """模块信息"""
    name: str
    docstring: str
    functions: List[FunctionInfo]
    classes: List[ClassInfo]
    imports: List[str]

class DocstringParser:
    """文档字符串解析器"""
    
    @staticmethod
    def parse_google_style(docstring: str) -> Dict[str, Any]:
        """解析Google风格的文档字符串"""
        if not docstring:
            return {}
        
        result = {
            'description': '',
            'args': [],
            'returns': None,
            'raises': [],
            'examples': []
        }
        
        lines = docstring.strip().split('\n')
        current_section = 'description'
        current_content = []
        
        for line in lines:
            line = line.strip()
            
            # 检查是否是新的部分
            if line.startswith('Args:'):
                if current_content:
                    result['description'] = '\n'.join(current_content).strip()
                current_section = 'args'
                current_content = []
            elif line.startswith('Returns:'):
                if current_content:
                    if current_section == 'args':
                        result['args'] = DocstringParser._parse_args_section(current_content)
                current_section = 'returns'
                current_content = []
            elif line.startswith('Raises:'):
                if current_content:
                    if current_section == 'returns':
                        result['returns'] = '\n'.join(current_content).strip()
                current_section = 'raises'
                current_content = []
            elif line.startswith('Example:') or line.startswith('Examples:'):
                if current_content:
                    if current_section == 'raises':
                        result['raises'] = DocstringParser._parse_raises_section(current_content)
                current_section = 'examples'
                current_content = []
            else:
                current_content.append(line)
        
        # 处理最后一个部分
        if current_content:
            if current_section == 'description':
                result['description'] = '\n'.join(current_content).strip()
            elif current_section == 'args':
                result['args'] = DocstringParser._parse_args_section(current_content)
            elif current_section == 'returns':
                result['returns'] = '\n'.join(current_content).strip()
            elif current_section == 'raises':
                result['raises'] = DocstringParser._parse_raises_section(current_content)
            elif current_section == 'examples':
                result['examples'] = current_content
        
        return result
    
    @staticmethod
    def parse_numpy_style(docstring: str) -> Dict[str, Any]:
        """解析NumPy风格的文档字符串"""
        if not docstring:
            return {}
        
        result = {
            'description': '',
            'parameters': [],
            'returns': None,
            'raises': []
        }
        
        # 简单的NumPy风格解析
        sections = re.split(r'\n\s*([A-Z][a-z]+)\s*\n', docstring)
        
        if len(sections) >= 2:
            result['description'] = sections[0].strip()
            
            for i in range(1, len(sections), 2):
                if i + 1 < len(sections):
                    section_name = sections[i].lower()
                    section_content = sections[i + 1].strip()
                    
                    if section_name == 'parameters':
                        result['parameters'] = DocstringParser._parse_numpy_parameters(section_content)
                    elif section_name == 'returns':
                        result['returns'] = section_content
                    elif section_name == 'raises':
                        result['raises'] = DocstringParser._parse_raises_section([section_content])
        
        return result
    
    @staticmethod
    def _parse_args_section(content: List[str]) -> List[Dict[str, str]]:
        """解析参数部分"""
        args = []
        current_arg = {}
        
        for line in content:
            line = line.strip()
            if not line:
                continue
            
            # 匹配参数定义: param_name (type): description
            match = re.match(r'(\w+)\s*(?:\(([^)]+)\))?\s*:\s*(.+)', line)
            if match:
                if current_arg:
                    args.append(current_arg)
                
                current_arg = {
                    'name': match.group(1),
                    'type': match.group(2) or '',
                    'description': match.group(3)
                }
            else:
                # 继续描述
                if current_arg and line:
                    current_arg['description'] += ' ' + line
        
        if current_arg:
            args.append(current_arg)
        
        return args
    
    @staticmethod
    def _parse_numpy_parameters(content: str) -> List[Dict[str, str]]:
        """解析NumPy风格的参数"""
        params = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # NumPy格式: param_name : type, optional
            match = re.match(r'(\w+)\s*:\s*([^,]+)(?:,\s*optional)?\s*(.+)', line)
            if match:
                params.append({
                    'name': match.group(1),
                    'type': match.group(2).strip(),
                    'description': match.group(3).strip()
                })
        
        return params
    
    @staticmethod
    def _parse_raises_section(content: List[str]) -> List[Dict[str, str]]:
        """解析异常部分"""
        raises = []
        
        for line in content:
            line = line.strip()
            if not line:
                continue
            
            # 匹配异常定义: ExceptionType: description
            match = re.match(r'(\w+(?:\.\w+)*)\s*:\s*(.+)', line)
            if match:
                raises.append({
                    'type': match.group(1),
                    'description': match.group(2)
                })
        
        return raises

class CommentParser:
    """注释解析器 - 用于解析注释中的文档标记"""
    
    # 支持的注释标记模式
    MARKERS = [
        r'@doc',           # @doc
        r'@doc_me',        # @doc_me
        r'@document',      # @document
        r'@api',           # @api
        r'@public',        # @public
    ]
    
    # 带参数的标记模式
    PARAM_MARKERS = [
        r'@doc\s*\(([^)]*)\)',           # @doc(description="xxx", category="xxx", priority=1)
        r'@doc_me\s*\(([^)]*)\)',        # @doc_me(description="xxx", category="xxx", priority=1)
        r'@document\s*\(([^)]*)\)',      # @document(description="xxx", category="xxx", priority=1)
        r'@api\s*\(([^)]*)\)',           # @api(description="xxx", category="xxx", priority=1)
    ]
    
    @classmethod
    def parse_comment_markers(cls, comment: str) -> Dict[str, Any]:
        """
        解析注释中的文档标记
        
        Args:
            comment: 注释内容
            
        Returns:
            包含标记信息的字典
        """
        if not comment:
            return {}
        
        comment = comment.strip()
        result = {
            'marked': False,
            'description': None,
            'category': None,
            'priority': 0
        }
        
        # 检查简单标记
        for marker in cls.MARKERS:
            if re.search(rf'\b{marker}\b', comment, re.IGNORECASE):
                result['marked'] = True
                break
        
        # 检查带参数的标记
        for pattern in cls.PARAM_MARKERS:
            match = re.search(pattern, comment, re.IGNORECASE)
            if match:
                result['marked'] = True
                params_str = match.group(1)
                params = cls._parse_params(params_str)
                result.update(params)
                break
        
        return result
    
    @classmethod
    def _parse_params(cls, params_str: str) -> Dict[str, Any]:
        """解析参数字符串"""
        params = {}
        
        # 匹配 key=value 格式的参数
        param_pattern = r'(\w+)\s*=\s*["\']([^"\']*)["\']'
        matches = re.findall(param_pattern, params_str)
        
        for key, value in matches:
            if key == 'priority':
                try:
                    params[key] = int(value)
                except ValueError:
                    params[key] = 0
            else:
                params[key] = value
        
        return params

class PythonParser:
    """Python代码解析器"""
    
    def __init__(self, include_all: bool = False, enable_comment_markers: bool = True):
        self.include_all = include_all
        self.enable_comment_markers = enable_comment_markers
        self.docstring_parser = DocstringParser()
        self.comment_parser = CommentParser()
    
    def parse_file(self, file_path: Path) -> ModuleInfo:
        """解析Python文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"警告: 无法解析文件 {file_path}: {e}")
            return ModuleInfo(
                name=file_path.stem,
                docstring="",
                functions=[],
                classes=[],
                imports=[]
            )
        
        return self._parse_ast_tree(tree, file_path, content)
    
    def _parse_ast_tree(self, tree: ast.AST, file_path: Path, content: str) -> ModuleInfo:
        """解析AST树"""
        module_info = ModuleInfo(
            name=file_path.stem,
            docstring="",
            functions=[],
            classes=[],
            imports=[]
        )
        
        # 获取模块文档字符串
        if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Str):
            module_info.docstring = tree.body[0].value.s
        
        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_info.imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module_name = node.module or ""
                for alias in node.names:
                    module_info.imports.append(f"{module_name}.{alias.name}")
            elif isinstance(node, ast.FunctionDef):
                func_info = self._parse_function(node, content)
                if self._should_include(func_info):
                    module_info.functions.append(func_info)
            elif isinstance(node, ast.ClassDef):
                class_info = self._parse_class(node, content)
                if self._should_include(class_info):
                    module_info.classes.append(class_info)
        
        return module_info
    
    def _parse_function(self, node: ast.FunctionDef, content: str) -> FunctionInfo:
        """解析函数定义"""
        # 获取源代码
        source_lines = content.split('\n')
        start_line = node.lineno - 1
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 1
        source_code = '\n'.join(source_lines[start_line:end_line])
        
        # 解析参数
        parameters = []
        for arg in node.args.args:
            param_info = {
                'name': arg.arg,
                'type': self._get_type_annotation(arg.annotation),
                'default': None
            }
            parameters.append(param_info)
        
        # 处理默认值
        defaults = node.args.defaults
        for i, default in enumerate(defaults):
            param_index = len(parameters) - len(defaults) + i
            if param_index < len(parameters):
                try:
                    parameters[param_index]['default'] = ast.unparse(default)
                except AttributeError:
                    parameters[param_index]['default'] = self._ast_to_string(default)
        
        # 获取返回类型
        return_type = self._get_type_annotation(node.returns)
        
        # 解析文档字符串
        docstring = ast.get_docstring(node) or ""
        
        # 检查装饰器标记
        category = None
        priority = 0
        comment_marked = False
        
        # 检查装饰器
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                if decorator.func.id == 'doc_me':
                    # 这里可以解析装饰器参数
                    pass
        
        # 检查注释标记
        if self.enable_comment_markers:
            comment_info = self._get_comment_info(node, source_lines)
            if comment_info['marked']:
                comment_marked = True
                category = comment_info.get('category', category)
                priority = comment_info.get('priority', priority)
        
        return FunctionInfo(
            name=node.name,
            docstring=docstring,
            signature=self._get_function_signature(node),
            parameters=parameters,
            return_type=return_type,
            source_code=source_code,
            line_number=node.lineno,
            category=category,
            priority=priority,
            comment_marked=comment_marked
        )
    
    def _parse_class(self, node: ast.ClassDef, content: str) -> ClassInfo:
        """解析类定义"""
        # 获取源代码
        source_lines = content.split('\n')
        start_line = node.lineno - 1
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 1
        source_code = '\n'.join(source_lines[start_line:end_line])
        
        # 解析基类
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                try:
                    bases.append(ast.unparse(base))
                except AttributeError:
                    bases.append(self._ast_to_string(base))
        
        # 解析方法
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._parse_function(item, content)
                if self._should_include(method_info):
                    methods.append(method_info)
        
        # 解析文档字符串
        docstring = ast.get_docstring(node) or ""
        
        # 检查注释标记
        category = None
        priority = 0
        comment_marked = False
        
        if self.enable_comment_markers:
            comment_info = self._get_comment_info(node, source_lines)
            if comment_info['marked']:
                comment_marked = True
                category = comment_info.get('category', category)
                priority = comment_info.get('priority', priority)
        
        return ClassInfo(
            name=node.name,
            docstring=docstring,
            bases=bases,
            methods=methods,
            source_code=source_code,
            line_number=node.lineno,
            category=category,
            priority=priority,
            comment_marked=comment_marked
        )
    
    def _get_comment_info(self, node: ast.AST, source_lines: List[str]) -> Dict[str, Any]:
        """获取节点前的注释信息"""
        line_number = node.lineno - 1  # 转换为0索引
        
        # 查找节点前的注释
        comments = []
        current_line = line_number - 1
        
        # 向上查找连续的注释行
        while current_line >= 0:
            line = source_lines[current_line].strip()
            
            # 跳过空行
            if not line:
                current_line -= 1
                continue
            
            # 检查是否是注释
            if line.startswith('#'):
                comments.insert(0, line[1:].strip())  # 移除#号
                current_line -= 1
            else:
                break
        
        # 解析所有注释
        for comment in comments:
            comment_info = self.comment_parser.parse_comment_markers(comment)
            if comment_info['marked']:
                return comment_info
        
        return {'marked': False}
    
    def _get_type_annotation(self, annotation) -> Optional[str]:
        """获取类型注解"""
        if annotation is None:
            return None
        try:
            return ast.unparse(annotation)
        except AttributeError:
            # Python 3.8 兼容性
            return self._ast_to_string(annotation)
    
    def _ast_to_string(self, node) -> str:
        """将AST节点转换为字符串（Python 3.8兼容）"""
        if node is None:
            return ""
        
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Attribute):
            return f"{self._ast_to_string(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return f"{self._ast_to_string(node.value)}[{self._ast_to_string(node.slice)}]"
        elif isinstance(node, ast.Index):
            return self._ast_to_string(node.value)
        elif isinstance(node, ast.Tuple):
            return f"({', '.join(self._ast_to_string(el) for el in node.elts)})"
        elif isinstance(node, ast.List):
            return f"[{', '.join(self._ast_to_string(el) for el in node.elts)}]"
        else:
            return str(node)
    
    def _get_function_signature(self, node: ast.FunctionDef) -> str:
        """获取函数签名"""
        args = []
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                try:
                    arg_str += f": {ast.unparse(arg.annotation)}"
                except AttributeError:
                    arg_str += f": {self._ast_to_string(arg.annotation)}"
            args.append(arg_str)
        
        signature = f"def {node.name}({', '.join(args)})"
        if node.returns:
            try:
                signature += f" -> {ast.unparse(node.returns)}"
            except AttributeError:
                signature += f" -> {self._ast_to_string(node.returns)}"
        
        return signature
    
    def _should_include(self, obj: Any) -> bool:
        """判断是否应该包含该对象"""
        if self.include_all:
            return True
        
        # 检查是否有装饰器标记
        if hasattr(obj, '_doc_me') and obj._doc_me:
            return True
        
        # 检查是否有注释标记
        if hasattr(obj, 'comment_marked') and obj.comment_marked:
            return True
        
        # 如果没有启用注释标记功能，则检查是否是公开的API（不以_开头）
        if not self.enable_comment_markers and hasattr(obj, 'name'):
            return not obj.name.startswith('_')
        
        return False 