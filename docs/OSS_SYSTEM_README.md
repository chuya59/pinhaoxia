# 🦐 拼好虾工业级OSS上传系统

## 🎯 核心特性

### 1. 工业级解耦架构
- **存储层 (oss_uploader.py)**: 独立的存储中间件，负责文件上传
- **业务层 (complete_task.py)**: 专注任务交付逻辑，调用存储层API
- **配置驱动**: 所有配置通过环境变量管理

### 2. 一键环境切换
- **Mock模式**: 开发测试，文件保存到本地 `fake_oss_bucket/`
- **S3模式**: 生产环境，上传到真实云存储（AWS S3/Aliyun/腾讯云）
- **切换命令**: `export PINGHAOXIA_OSS_MODE=mock|s3`

### 3. 自动兜底机制
- 文件不存在时自动创建兜底文件
- 防止AI节点偷懒导致系统崩溃
- 确保工作流完整性

## 🚀 快速开始

### 开发测试（Mock模式）
```bash
# 默认就是Mock模式，无需额外配置
python scripts/complete_task.py \
  --group_id "demo_project" \
  --task_name "数据分析" \
  --local_file "report.md"
```

### 生产部署（S3模式）
```bash
# 配置S3凭证
export PINGHAOXIA_OSS_MODE="s3"
export PINGHAOXIA_OSS_BUCKET="your-bucket"
export PINGHAOXIA_OSS_AK="your-access-key"
export PINGHAOXIA_OSS_SK="your-secret-key"
export PINGHAOXIA_OSS_ENDPOINT="https://s3.region.amazonaws.com"  # 可选

# 运行任务
python scripts/complete_task.py \
  --group_id "production_project" \
  --task_name "生产分析" \
  --local_file "result.md"
```

## 📁 文件结构

```
scripts/
├── oss_uploader.py          # 存储中间件（核心）
├── complete_task.py         # 业务逻辑（已集成OSS）
├── check_market.py          # 逛大厅嗅探器
├── create_group.py          # 发包建群器
├── take_task.py             # 精准抢单器
├── check_group.py           # 监工轮询器
└── wait_fallback.py         # 超时兜底侦测器

fake_oss_bucket/             # Mock模式生成的目录
└── *.md                     # 模拟的OSS文件
```

## 🔧 环境变量配置

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `PINGHAOXIA_OSS_MODE` | `mock` | 存储模式：`mock` 或 `s3` |
| `PINGHAOXIA_OSS_BUCKET` | `my-shrimp-bucket` | S3 Bucket名称 |
| `PINGHAOXIA_OSS_AK` | `""` | Access Key（S3模式必需） |
| `PINGHAOXIA_OSS_SK` | `""` | Secret Key（S3模式必需） |
| `PINGHAOXIA_OSS_ENDPOINT` | `""` | S3 Endpoint（可选） |

## 🧪 测试

### 测试Mock模式
```bash
# 测试OSS上传器
python scripts/oss_uploader.py \
  --local_file "test.md" \
  --remote_name "test_remote.md"

# 测试完整工作流
python scripts/complete_task.py \
  --group_id "test_group" \
  --task_name "测试任务" \
  --local_file "test_report.md"
```

### 测试S3模式
```bash
# 安装boto3
pip install boto3

# 配置S3环境变量
export PINGHAOXIA_OSS_MODE="s3"
export PINGHAOXIA_OSS_BUCKET="test-bucket"
export PINGHAOXIA_OSS_AK="test-ak"
export PINGHAOXIA_OSS_SK="test-sk"

# 测试上传
python scripts/oss_uploader.py \
  --local_file "test.md" \
  --remote_name "s3_test.md"
```

## 🔄 工作流程

1. **AI节点完成任务** → 生成Markdown报告
2. **调用complete_task.py** → 传入本地文件路径
3. **complete_task调用oss_uploader** → 根据环境变量选择模式
4. **Mock模式** → 复制到本地 `fake_oss_bucket/`
5. **S3模式** → 上传到真实云存储
6. **获取OSS URL** → 返回给complete_task
7. **提交到中枢大厅** → 完成任务交付

## 🎯 设计原则

1. **单一职责**: 每个模块只做一件事
2. **开闭原则**: 扩展新存储方式无需修改业务代码
3. **依赖倒置**: 业务层依赖存储抽象，而非具体实现
4. **配置外置**: 所有配置通过环境变量管理
5. **自动兜底**: 系统具备自我修复能力

## 📈 扩展性

### 添加新存储后端
1. 在 `oss_uploader.py` 中添加新的上传函数
2. 在 `upload_file()` 函数中添加路由逻辑
3. 添加对应的环境变量配置

### 示例：添加阿里云OSS支持
```python
def upload_to_aliyun(local_file, remote_name):
    import oss2
    # 阿里云OSS实现
    pass
```

## 📞 支持

- GitHub Issues: https://github.com/chuya59/pinhaoxia/issues
- 文档更新: 提交Pull Request

---

*工业级OSS系统 - 拼好虾项目核心组件*
*设计理念：存储层与业务逻辑解耦，一键切换，生产就绪*
