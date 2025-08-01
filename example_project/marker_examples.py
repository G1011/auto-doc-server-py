"""
标记使用示例模块

这个模块展示了不同标记的使用场景和含义，帮助开发者选择合适的标记。
"""

# ============================================================================
# @doc - 基础文档标记：适用于简单的内部函数或工具类
# ============================================================================

def format_date(date: str) -> str:
    """
    格式化日期字符串
    
    @doc
    """
    return date.replace('-', '/')

def calculate_percentage(value: float, total: float) -> float:
    """
    计算百分比
    
    @doc
    """
    return (value / total) * 100 if total > 0 else 0

# ============================================================================
# @doc_me - 详细文档标记：适用于重要的业务逻辑函数或核心类
# ============================================================================

def process_user_data(user_data: dict) -> dict:
    """
    处理用户数据，包括验证、清洗和格式化
    
    @doc_me(description="用户数据处理函数", category="用户管理", priority=1)
    """
    # 验证数据
    if not user_data.get('name'):
        raise ValueError("用户名不能为空")
    
    # 清洗数据
    user_data['name'] = user_data['name'].strip()
    user_data['email'] = user_data['email'].lower()
    
    return user_data

class DataProcessor:
    """
    数据处理类，提供各种数据处理功能
    
    @doc_me(description="数据处理核心类", category="数据处理", priority=2)
    """
    
    def __init__(self, config: dict):
        self.config = config
    
    def process_batch(self, data_list: list) -> list:
        """
        批量处理数据
        
        @doc_me(description="批量数据处理", category="批量操作", priority=1)
        """
        return [self.process_single(item) for item in data_list]
    
    def process_single(self, data: dict) -> dict:
        """
        处理单个数据项
        
        @doc
        """
        # 处理逻辑
        return data

# ============================================================================
# @document - 完整文档标记：适用于核心功能、复杂算法或重要接口
# ============================================================================

def complex_algorithm(data: list) -> dict:
    """
    复杂算法实现，包含多个步骤和优化策略
    
    @document(description="核心算法实现", category="算法", priority=3)
    """
    # 步骤1：数据预处理
    processed_data = preprocess_data(data)
    
    # 步骤2：特征提取
    features = extract_features(processed_data)
    
    # 步骤3：模型计算
    result = calculate_model(features)
    
    return result

class OrderProcessor:
    """
    订单处理系统，包含完整的订单生命周期管理
    
    @document(description="订单处理核心系统", category="订单管理", priority=3)
    """
    
    def __init__(self):
        self.order_queue = []
        self.processing_rules = {}
    
    def create_order(self, order_data: dict) -> dict:
        """
        创建新订单
        
        @document(description="订单创建核心逻辑", category="订单创建", priority=2)
        """
        # 验证订单数据
        self.validate_order_data(order_data)
        
        # 生成订单号
        order_id = self.generate_order_id()
        
        # 创建订单对象
        order = {
            'id': order_id,
            'data': order_data,
            'status': 'created',
            'created_at': self.get_current_time()
        }
        
        # 添加到队列
        self.order_queue.append(order)
        
        return order
    
    def process_order(self, order_id: str) -> dict:
        """
        处理订单
        
        @document(description="订单处理核心逻辑", category="订单处理", priority=2)
        """
        # 查找订单
        order = self.find_order(order_id)
        if not order:
            raise ValueError(f"订单不存在: {order_id}")
        
        # 更新状态
        order['status'] = 'processing'
        
        # 执行处理逻辑
        result = self.execute_processing(order)
        
        # 更新订单
        order['status'] = 'completed'
        order['result'] = result
        
        return order

# ============================================================================
# @api - API接口标记：适用于对外提供的API接口
# ============================================================================

def get_user_info(user_id: str) -> dict:
    """
    获取用户信息API
    
    @api(description="用户信息查询接口", category="用户API", priority=3)
    """
    # 验证用户ID
    if not user_id:
        raise ValueError("用户ID不能为空")
    
    # 查询数据库
    user = query_database(f"SELECT * FROM users WHERE id = '{user_id}'")
    
    if not user:
        raise ValueError(f"用户不存在: {user_id}")
    
    return {
        'id': user['id'],
        'name': user['name'],
        'email': user['email'],
        'status': user['status']
    }

def create_user(user_data: dict) -> dict:
    """
    创建用户API
    
    @api(description="用户创建接口", category="用户API", priority=3)
    """
    # 验证输入数据
    validate_user_data(user_data)
    
    # 检查用户是否已存在
    if user_exists(user_data['email']):
        raise ValueError("用户已存在")
    
    # 创建用户
    user_id = insert_user(user_data)
    
    return {
        'id': user_id,
        'message': '用户创建成功'
    }

class UserAPI:
    """
    用户API类，提供用户相关的所有API接口
    
    @api(description="用户API集合", category="用户API", priority=3)
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def update_user(self, user_id: str, update_data: dict) -> dict:
        """
        更新用户信息API
        
        @api(description="用户信息更新接口", category="用户API", priority=2)
        """
        # 验证用户存在
        if not self.user_exists(user_id):
            raise ValueError(f"用户不存在: {user_id}")
        
        # 更新用户信息
        self.db.update('users', user_id, update_data)
        
        return {'message': '用户信息更新成功'}

# ============================================================================
# @public - 公共接口标记：适用于模块间调用的公共接口
# ============================================================================

def validate_config(config: dict) -> bool:
    """
    配置验证函数
    
    @public(description="配置验证接口", category="配置管理")
    """
    required_fields = ['database_url', 'api_key', 'timeout']
    
    for field in required_fields:
        if field not in config:
            return False
    
    return True

def format_error_message(error: Exception) -> str:
    """
    格式化错误信息
    
    @public(description="错误信息格式化接口", category="错误处理")
    """
    return f"错误: {type(error).__name__} - {str(error)}"

class Logger:
    """
    日志记录器，提供统一的日志记录接口
    
    @public(description="日志记录接口", category="日志管理")
    """
    
    def __init__(self, log_level: str = 'INFO'):
        self.log_level = log_level
    
    def log(self, message: str, level: str = 'INFO'):
        """
        记录日志
        
        @public(description="日志记录方法", category="日志记录")
        """
        if self.should_log(level):
            print(f"[{level}] {message}")
    
    def should_log(self, level: str) -> bool:
        """
        判断是否应该记录日志
        
        @doc
        """
        levels = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3}
        return levels.get(level, 1) >= levels.get(self.log_level, 1)

# ============================================================================
# 辅助函数（不会被包含在文档中）
# ============================================================================

def preprocess_data(data: list) -> list:
    """数据预处理"""
    return data

def extract_features(data: list) -> dict:
    """特征提取"""
    return {'features': data}

def calculate_model(features: dict) -> dict:
    """模型计算"""
    return {'result': features}

def validate_order_data(data: dict):
    """验证订单数据"""
    pass

def generate_order_id() -> str:
    """生成订单ID"""
    return "ORDER_123"

def get_current_time() -> str:
    """获取当前时间"""
    return "2024-01-01 12:00:00"

def find_order(order_id: str) -> dict:
    """查找订单"""
    return {}

def execute_processing(order: dict) -> dict:
    """执行处理逻辑"""
    return {}

def query_database(query: str) -> dict:
    """查询数据库"""
    return {}

def validate_user_data(data: dict):
    """验证用户数据"""
    pass

def user_exists(email: str) -> bool:
    """检查用户是否存在"""
    return False

def insert_user(data: dict) -> str:
    """插入用户"""
    return "USER_123" 