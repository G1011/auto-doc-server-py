# 注释标记功能

Auto Doc Server 现在支持通过注释标记来识别需要生成文档的函数和类，这对于现有项目特别有用，因为不需要修改代码结构或添加装饰器。

## 标记含义说明

### 支持的标记类型

| 标记 | 含义 | 用途 | 示例 |
|------|------|------|------|
| `@doc` | 基础文档标记 | 标记需要生成基础文档的函数或类 | `@doc` |
| `@doc_util` | 工具函数标记 | 标记需要生成详细文档的工具函数或类，包含更多信息 | `@doc_util(description="...", category="...")` |
| `@doc_component` | 组件标记 | 标记需要生成完整文档的核心组件，包含所有详细信息 | `@doc_component(description="...", category="...", priority=1)` |
| `@doc_api` | API接口标记 | 标记公共API接口，通常用于外部调用的函数或类 | `@doc_api(description="...", category="API")` |
| `@doc_public` | 公共接口标记 | 标记公共接口，通常用于模块间调用的函数或类 | `@doc_public(description="...", category="公共接口")` |

### 标记详细说明

#### @doc - 基础文档标记
- **含义**: 基础文档标记，表示该函数或类需要生成基础文档
- **用途**: 适用于简单的内部函数或工具类
- **特点**: 生成基本的函数签名、参数和返回值信息
- **示例**:
```python
def helper_function():
    """
    辅助函数
    
    @doc
    """
    pass
```

#### @doc_util - 工具函数标记
- **含义**: 工具函数标记，表示该函数或类需要生成详细文档
- **用途**: 适用于重要的业务逻辑函数或核心类
- **特点**: 生成详细的文档，包含描述、分类、优先级等信息
- **示例**:
```python
def process_user_data(user_data: dict) -> dict:
    """
    处理用户数据
    
    @doc_util(description="用户数据处理函数", category="用户管理", priority=1)
    """
    pass
```

#### @doc_component - 组件标记
- **含义**: 组件标记，表示该函数或类需要生成最完整的文档
- **用途**: 适用于核心功能、复杂算法或重要的公共接口
- **特点**: 生成最完整的文档，包含所有可能的详细信息
- **示例**:
```python
def complex_algorithm(data: list) -> dict:
    """
    复杂算法实现
    
    @doc_component(description="核心算法实现", category="算法", priority=2)
    """
    pass
```

#### @doc_api - API接口标记
- **含义**: API接口标记，表示该函数或类是公共API接口
- **用途**: 适用于对外提供的API接口，通常用于Web API、库接口等
- **特点**: 强调这是一个API接口，可能包含API相关的特殊信息
- **示例**:
```python
def get_user_info(user_id: str) -> dict:
    """
    获取用户信息API
    
    @doc_api(description="用户信息查询接口", category="用户API", priority=3)
    """
    pass
```

#### @doc_public - 公共接口标记
- **含义**: 公共接口标记，表示该函数或类是公共接口
- **用途**: 适用于模块间调用的公共接口，但不一定是外部API
- **特点**: 强调这是一个公共接口，供其他模块使用
- **示例**:
```python
def validate_input(data: dict) -> bool:
    """
    输入验证函数
    
    @doc_public(description="输入验证接口", category="验证工具")
    """
    pass
```

## 支持的注释标记

### 1. 函数/类上方的注释标记

在函数或类定义前的注释中使用以下标记：

```python
# @doc
def my_function():
    pass

# @doc_util
class MyClass:
    pass

# @doc_component
def another_function():
    pass

# @doc_api
def public_api():
    pass

# @doc_public
def public_function():
    pass
```

### 2. Docstring内部的标记（推荐）

在函数或类的docstring内部使用标记，这种方式更加简洁：

```python
def my_function():
    """
    这是一个函数
    
    @doc
    """
    pass

class MyClass:
    """
    这是一个类
    
    @doc_util(description="我的类", category="工具类")
    """
    pass
```

### 带参数的标记

你还可以在注释中添加参数来提供更多信息：

#### 上方注释方式
```python
# @doc(description="自定义描述", category="核心功能", priority=1)
def my_function():
    pass

# @doc_util(description="用户管理类", category="用户管理", priority=2)
class UserManager:
    pass
```

#### Docstring内部方式（推荐）
```python
def my_function():
    """
    这是一个函数
    
    @doc(description="自定义描述", category="核心功能", priority=1)
    """
    pass

class UserManager:
    """
    用户管理类
    
    @doc_util(description="用户管理类", category="用户管理", priority=2)
    """
    pass
```

## 参数说明

- `description`: 自定义描述，会覆盖docstring中的描述
- `category`: 分类，用于组织文档结构
- `priority`: 优先级（数字越大优先级越高），用于排序

## 使用建议

### 根据用途选择合适的标记

1. **内部工具函数**: 使用 `@doc`
   ```python
   def format_date(date: str) -> str:
       """
       格式化日期
       
       @doc
       """
       pass
   ```

2. **业务逻辑函数**: 使用 `@doc_util`
   ```python
   def calculate_tax(income: float) -> float:
       """
       计算税费
       
       @doc_util(description="税费计算", category="财务", priority=1)
       """
       pass
   ```

3. **核心功能**: 使用 `@doc_component`
   ```python
   def process_order(order_data: dict) -> dict:
       """
       处理订单
       
       @doc_component(description="订单处理核心逻辑", category="订单管理", priority=2)
       """
       pass
   ```

4. **对外API**: 使用 `@doc_api`
   ```python
   def create_user(user_data: dict) -> dict:
       """
       创建用户API
       
       @doc_api(description="用户创建接口", category="用户API", priority=3)
       """
       pass
   ```

5. **模块间接口**: 使用 `@doc_public`
   ```python
   def validate_config(config: dict) -> bool:
       """
       配置验证
       
       @doc_public(description="配置验证接口", category="配置管理")
       """
       pass
   ```

## 使用方法

### 命令行使用

```bash
# 启用注释标记功能（默认启用）
auto-doc generate ./my_project

# 禁用注释标记功能
auto-doc generate ./my_project --disable-comment-markers

# 同时使用装饰器和注释标记
auto-doc generate ./my_project --include-all
```

### 代码中使用

```python
from auto_doc_server import AutoDocGenerator

# 启用注释标记功能
generator = AutoDocGenerator(
    project_path="./my_project",
    enable_comment_markers=True  # 默认启用
)

# 禁用注释标记功能
generator = AutoDocGenerator(
    project_path="./my_project",
    enable_comment_markers=False
)
```

## 示例

查看以下示例文件，了解完整的使用示例：
- `example_project/comment_example.py` - 上方注释标记示例
- `example_project/docstring_example.py` - docstring内部标记示例
- `example_project/marker_examples.py` - 不同标记使用场景示例

## 标记优先级

当同时使用多种标记方式时，优先级如下（从高到低）：

1. **Docstring内部标记** - 最高优先级
2. **函数/类上方注释标记** - 中等优先级
3. **装饰器标记** - 基础优先级

例如：
```python
# @doc_util(description="上方注释", category="上方", priority=1)
def mixed_markers():
    """
    这个函数同时使用了上方注释标记和docstring标记
    
    @doc_api(description="docstring中的标记", category="docstring", priority=2)
    
    注意：docstring中的标记会覆盖上方注释的标记
    """
    return "Mixed markers example"
```

在这个例子中，最终会使用docstring中的`@doc_api`标记。

## 注意事项

1. 注释标记必须紧邻函数或类定义
2. Docstring内部标记可以放在docstring的任何位置
3. 支持多行注释，解析器会查找连续的注释行
4. 注释标记不区分大小写
5. 如果同时使用了装饰器和注释标记，两者都会被识别
6. Docstring内部标记的优先级高于上方注释标记

## 与装饰器的对比

| 特性 | 装饰器 | 上方注释标记 | Docstring内部标记 |
|------|--------|-------------|------------------|
| 需要修改代码 | 是 | 否 | 否 |
| 语法简洁性 | 高 | 中 | 高 |
| 现有项目适用性 | 低 | 高 | 高 |
| 参数支持 | 完整 | 基本 | 基本 |
| IDE支持 | 好 | 一般 | 好 |
| 文档位置 | 分离 | 分离 | 统一 |

## 最佳实践

1. **现有项目**: 优先使用docstring内部标记，避免修改现有代码
2. **新项目**: 可以同时使用装饰器和注释标记
3. **团队协作**: 在项目文档中说明使用的标记方式
4. **一致性**: 在同一个项目中保持标记方式的一致性
5. **推荐方式**: 优先使用docstring内部标记，因为它更加简洁和直观
6. **语义化**: 根据函数或类的用途选择合适的标记类型 