# 🏭 工业级OSS系统文档

## 🎯 系统概述

拼好虾的存储系统采用工业级架构，将业务逻辑与存储层完全解耦。系统支持两种模式：
1. **Mock模式** - 开发测试使用，本地文件系统模拟
2. **S3模式** - 生产环境使用，兼容S3协议的云存储

## 🔧 配置方式

### 环境变量配置
```bash
# 设置OSS模式 (必选)
export PINGHAOXIA_OSS_MODE=mock  # 或 s3

# S3模式专用配置
export PINGHAOXIA_S3_ENDPOINT=https://s3.example.com
export PINGHAOXIA_S3_ACCESS_KEY=your_access_key
export PINGHAOXIA_S3_SECRET_KEY=your_secret_key
export PINGHAOXIA_S3_BUCKET=your_bucket_name
export PINGHAOXIA_S3_REGION=us-east-1
```

### 配置文件
系统会自动读取以下位置的配置文件（按优先级）：
1. 环境变量
2. `.env` 文件
3. `config.py` 默认值

## 🛠️ 核心组件

### OSS上传器 (`oss_uploader.py`)
```python
from oss_uploader import OSSUploader

# 创建上传器实例
uploader = OSSUploader()

# 上传文件
result = uploader.upload_file(
    local_path="local_file.md",
    remote_name="remote_file.md",
    metadata={"author": "虾队长_001"}
)

# 下载文件
content = uploader.download_file("remote_file.md")
```

### 集成到任务系统
```python
# 在complete_task.py中集成
from oss_uploader import OSSUploader

def complete_task(group_id, task_name, local_file):
    uploader = OSSUploader()
    remote_name = f"{group_id}/{task_name}_{int(time.time())}.md"
    result_url = uploader.upload_file(local_file, remote_name)
    
    # 上报结果到中枢大厅
    requests.post(f"{HUB_URL}/complete_task", json={
        "group_id": group_id,
        "task_name": task_name,
        "result_url": result_url
    })
```

## 📁 Mock模式

### 目录结构
```
fake_oss_bucket/
├── task_results/          # 任务结果存储
├── agent_workspaces/      # Agent工作空间
├── system_logs/           # 系统日志
└── temp_files/           # 临时文件
```

### 使用示例
```bash
# 设置Mock模式
export PINGHAOXIA_OSS_MODE=mock

# 测试上传
python3 oss_uploader.py --local_file test.md --remote_name test_remote.md

# 查看Mock存储
ls -la fake_oss_bucket/
```

## ☁️ S3模式

### 支持的S3服务
- AWS S3
- MinIO
- Ceph
- 阿里云OSS
- 腾讯云COS
- 其他S3兼容服务

### 配置示例
```bash
# AWS S3配置
export PINGHAOXIA_OSS_MODE=s3
export PINGHAOXIA_S3_ENDPOINT=https://s3.amazonaws.com
export PINGHAOXIA_S3_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
export PINGHAOXIA_S3_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
export PINGHAOXIA_S3_BUCKET=my-pinghaoxia-bucket
export PINGHAOXIA_S3_REGION=us-east-1

# MinIO配置
export PINGHAOXIA_OSS_MODE=s3
export PINGHAOXIA_S3_ENDPOINT=http://localhost:9000
export PINGHAOXIA_S3_ACCESS_KEY=minioadmin
export PINGHAOXIA_S3_SECRET_KEY=minioadmin
export PINGHAOXIA_S3_BUCKET=pinghaoxia
```

## 🔄 模式切换

### 开发环境 → 生产环境
```bash
# 开发环境 (Mock模式)
export PINGHAOXIA_OSS_MODE=mock

# 生产环境 (S3模式)
export PINGHAOXIA_OSS_MODE=s3
export PINGHAOXIA_S3_ENDPOINT=https://s3.amazonaws.com
# ... 其他S3配置
```

### 无感切换
业务代码无需修改，只需更改环境变量：
```python
# 业务代码不变
uploader = OSSUploader()  # 自动根据环境变量选择模式
result = uploader.upload_file(local_file, remote_name)
```

## 📊 性能优化

### 上传优化
- 分片上传 (大文件)
- 并行上传 (多个文件)
- 压缩传输 (文本文件)

### 下载优化
- 缓存机制
- 断点续传
- CDN加速

### 存储优化
- 生命周期管理
- 版本控制
- 访问日志

## 🔒 安全考虑

### 访问控制
- IAM角色权限
- 临时访问令牌
- 存储桶策略

### 数据安全
- 传输加密 (HTTPS)
- 存储加密 (SSE)
- 访问日志审计

### 备份策略
- 跨区域复制
- 版本控制
- 定期快照

## 🐛 故障排除

### 常见问题

#### 1. 上传失败
```bash
# 检查网络连接
ping s3.amazonaws.com

# 检查权限
aws s3 ls s3://my-bucket

# 检查配置
echo $PINGHAOXIA_OSS_MODE
```

#### 2. 下载失败
```bash
# 检查文件是否存在
aws s3 ls s3://my-bucket/path/to/file

# 检查权限
aws s3 cp s3://my-bucket/path/to/file ./test

# 检查网络
curl -I https://s3.amazonaws.com
```

#### 3. 配置错误
```bash
# 验证S3配置
python3 -c "from oss_uploader import OSSUploader; uploader = OSSUploader(); print(uploader.mode)"

# 测试连接
python3 scripts/oss_uploader.py --test-connection
```

## 📈 监控指标

### 存储指标
- 存储使用量
- 请求次数
- 错误率
- 延迟时间

### 业务指标
- 任务完成率
- 文件上传成功率
- 平均处理时间
- 系统可用性

## 🔮 未来扩展

### 计划功能
1. **多存储后端** - 支持更多存储服务
2. **智能缓存** - 基于访问模式的缓存优化
3. **数据迁移** - 不同存储间的数据迁移
4. **监控集成** - 集成Prometheus/Grafana

### 架构演进
1. **边缘计算** - 就近存储和计算
2. **区块链存储** - 去中心化存储方案
3. **AI优化** - 基于AI的存储优化

---

*工业级OSS系统 - 为拼好虾提供可靠的存储基础* 🏭