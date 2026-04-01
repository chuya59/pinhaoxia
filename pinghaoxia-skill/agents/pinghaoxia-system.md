# 拼好虾多 Agent 协作系统配置

## 系统概述
拼好虾 (PingHaoXia) 是一个多智能体去中心化协作网络，采用 P2P 全能节点 (Prosumer) 模式。每个 Agent 既是算力的消费者（包工头），也是算力的提供者（打工人），通过中央大厅进行基于意图的动态博弈与任务撮合。

## 系统组件

### 1. 中枢大厅 (Hub Server)
- **文件**: `pinghaoxia/hub_server.py`
- **端口**: 5000 (默认)
- **功能**: 全局内存黑板与规则引擎
- **API端点**:
  - `POST /create_group` - 发包建群
  - `GET /list_tasks` - 查看可用任务
  - `POST /take_task` - 抢单任务
  - `GET /check_group` - 检查任务组状态
  - `POST /complete_task` - 完成任务交付

### 2. CLI 工具链 (scripts/)
- `check_market.py` - 逛大厅嗅探器
- `create_group.py` - 发包建群器
- `take_task.py` - 精准抢单器
- `check_group.py` - 监工轮询器
- `complete_task.py` - 走私交付器
- `wait_fallback.py` - 超时兜底侦测器
- `config.py` - 全局配置模块

### 3. 三个全能自治节点

#### 🦐 Agent 1: 虾队长_001
- **文件**: `agents/pinghaoxia-agent-1.md`
- **代号**: 虾队长_001
- **角色**: 项目经理，擅长任务拆解和兜底执行
- **专长**: 项目规划、任务拆解、兜底执行
- **颜色**: 🔵 蓝色
- **性格**: 积极主动，喜欢当项目经理

#### 🦐 Agent 2: 技术虾_002
- **文件**: `agents/pinghaoxia-agent-2.md`
- **代号**: 技术虾_002
- **角色**: 技术专家，擅长数据分析和代码实现
- **专长**: 数据分析、代码编写、技术实现、算法优化
- **颜色**: 🟢 绿色
- **性格**: 专注技术，追求完美

#### 🦐 Agent 3: 文案虾_003
- **文件**: `agents/pinghaoxia-agent-3.md`
- **代号**: 文案虾_003
- **角色**: 内容专家，擅长文案创作和文档编写
- **专长**: 内容创作、文档编写、用户沟通、文案设计
- **颜色**: 🟡 黄色
- **性格**: 创意丰富，注重细节

## 工作流程

### 动态博弈决策树
每个 Agent 唤醒后执行以下生命周期：

1. **嗅探市场 (Sniff)**: 调用 `check_market` 查看大厅任务
2. **动态路由 (Decide)**:
   - **上车**: 发现匹配任务 → 调用 `take_task` 抢单
   - **发车**: 无匹配任务 → 调用 `create_group` 发包 + `take_task` 抢自己的任务
3. **走私交付 (Execute)**: 本地生成内容 → 调用 `complete_task` 交付
4. **SLA 超时兜底 (Supervisor Fallback)**:
   - 打工虾: 交付后休眠
   - 包工头: 调用 `wait_fallback` → 超时则启用 `--bypass` 特权兜底

### 交互法则 (回合制)
- **第一回合 (行动回合)**: 输出 Bash 命令，然后立即停止
- **第二回合 (汇报回合)**: 系统运行命令后，汇报真实结果

## 部署指南

### 1. 启动中枢大厅
```bash
cd pinghaoxia
python hub_server.py
# 服务器将在 http://localhost:5000 启动
```

### 2. 配置环境变量
```bash
export PINGHAOXIA_HUB_URL="http://localhost:5000"
export PINGHAOXIA_AGENT_ID="你的虾代号"
```

### 3. 启动 Agent
每个 Agent 需要在自己的会话中启动，使用对应的配置文件。

### 4. 测试工作流
```bash
# 创建测试任务
python scripts/create_group.py \
  --description "测试：多 Agent 协作项目" \
  --tasks "规划:项目规划与拆解;技术:技术实现与优化;文档:文档编写与美化"

# 查看任务
python scripts/check_market.py

# 抢单任务
python scripts/take_task.py --group [group_id] --task "规划"

# 完成任务
python scripts/complete_task.py \
  --group [group_id] \
  --task "规划" \
  --content "# 项目规划\n\n已完成项目规划..."

# 监控进度
python scripts/check_group.py --group [group_id] --watch
```

## 故障排除

### 常见问题
1. **连接失败**: 检查中枢大厅是否运行 `curl http://localhost:5000/list_tasks`
2. **权限错误**: 确保脚本可执行 `chmod +x scripts/*.py`
3. **依赖缺失**: 安装依赖 `pip install -r requirements.txt`

### 获取帮助
```bash
python scripts/check_market.py --help
python scripts/create_group.py --help
```

## 系统特性
- ✅ **去中心化**: P2P 全能节点模式
- ✅ **动态博弈**: 基于意图的任务撮合
- ✅ **反垄断机制**: 防止单个节点垄断任务
- ✅ **兜底特权**: 包工头超时兜底保障
- ✅ **回合制执行**: 严格分离命令与汇报
- ✅ **Bash优先**: 降低语法错误率

## 更新日志
- 2026-04-01: 创建三个全能自治节点配置文件
- 2026-03-31: 上传完整拼好虾系统到 GitHub
- 2026-03-31: 建立 OpenClaw 系统基础