# 注释标记功能

Auto Doc Server 现在支持通过注释标记来识别需要生成文档的函数和类，这对于现有项目特别有用，因为不需要修改代码结构或添加装饰器。

## 支持的注释标记

### 简单标记

在函数或类定义前的注释中使用以下标记：

```python
# @doc
def my_function():
    pass

# @doc_me
class MyClass:
    pass

# @document
def another_function():
    pass

# @api
def public_api():
    pass

# @public
def public_function():
    pass
```

### 带参数的标记

你还可以在注释中添加参数来提供更多信息：

```python
# @doc(description="自定义描述", category="核心功能", priority=1)
def my_function():
    pass

# @doc_me(description="用户管理类", category="用户管理", priority=2)
class UserManager:
    pass

# @document(description="数据处理工具", category="数据处理")
def process_data():
    pass

# @api(description="公共API接口", category="API", priority=3)
def api_endpoint():
    pass
```

## 参数说明

- `description`: 自定义描述，会覆盖docstring中的描述
- `category`: 分类，用于组织文档结构
- `priority`: 优先级（数字越大优先级越高），用于排序

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

查看 `example_project/comment_example.py` 文件，了解完整的使用示例。

## 注意事项

1. 注释标记必须紧邻函数或类定义
2. 支持多行注释，解析器会查找连续的注释行
3. 注释标记不区分大小写
4. 如果同时使用了装饰器和注释标记，两者都会被识别
5. 注释标记的优先级高于装饰器标记

## 与装饰器的对比

| 特性 | 装饰器 | 注释标记 |
|------|--------|----------|
| 需要修改代码 | 是 | 否 |
| 语法简洁性 | 高 | 中 |
| 现有项目适用性 | 低 | 高 |
| 参数支持 | 完整 | 基本 |
| IDE支持 | 好 | 一般 |

## 最佳实践

1. **现有项目**: 优先使用注释标记，避免修改现有代码
2. **新项目**: 可以同时使用装饰器和注释标记
3. **团队协作**: 在项目文档中说明使用的标记方式
4. **一致性**: 在同一个项目中保持标记方式的一致性 