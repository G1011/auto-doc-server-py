"""
注释标记示例模块

这个模块展示了如何使用注释标记来生成文档，而不需要修改代码结构或添加装饰器。
这对于现有项目特别有用，因为只需要在注释中添加标记即可。
"""

# @doc
def simple_function():
    """这是一个简单的函数，通过注释标记来生成文档"""
    return "Hello, World!"

# @doc_me(description="计算两个数的和", category="数学运算", priority=1)
def add_numbers(a: int, b: int) -> int:
    """
    计算两个整数的和
    
    Args:
        a: 第一个整数
        b: 第二个整数
        
    Returns:
        两个整数的和
    """
    return a + b

# @document(description="字符串处理工具", category="文本处理")
def process_string(text: str, uppercase: bool = False) -> str:
    """
    处理字符串
    
    Args:
        text: 要处理的字符串
        uppercase: 是否转换为大写
        
    Returns:
        处理后的字符串
    """
    if uppercase:
        return text.upper()
    return text.lower()

# @api(description="用户管理类", category="用户管理", priority=2)
class UserManager:
    """用户管理类，用于处理用户相关的操作"""
    
    def __init__(self):
        self.users = {}
    
    # @doc
    def add_user(self, user_id: str, name: str) -> bool:
        """
        添加用户
        
        Args:
            user_id: 用户ID
            name: 用户姓名
            
        Returns:
            是否添加成功
        """
        if user_id not in self.users:
            self.users[user_id] = name
            return True
        return False
    
    # @public(description="获取用户信息", category="用户查询")
    def get_user(self, user_id: str) -> str:
        """
        获取用户信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户姓名，如果不存在则返回None
        """
        return self.users.get(user_id)

# @doc_me(description="配置管理类", category="系统配置")
class ConfigManager:
    """配置管理类"""
    
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = {}
    
    # @api
    def load_config(self) -> dict:
        """加载配置文件"""
        # 模拟加载配置
        self.config = {"debug": True, "port": 8080}
        return self.config
    
    # @document
    def get_config(self, key: str, default=None):
        """获取配置值"""
        return self.config.get(key, default)

# 这个函数没有注释标记，不会被包含在文档中（除非使用--include-all）
def internal_helper():
    """内部辅助函数，不会被生成文档"""
    pass

# @doc(description="数据验证工具", category="数据验证")
def validate_email(email: str) -> bool:
    """
    验证邮箱格式
    
    Args:
        email: 要验证的邮箱地址
        
    Returns:
        是否是有效的邮箱格式
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# @api(description="文件操作工具", category="文件处理", priority=3)
def read_file_content(file_path: str) -> str:
    """
    读取文件内容
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件内容
        
    Raises:
        FileNotFoundError: 文件不存在时抛出
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {file_path}") 