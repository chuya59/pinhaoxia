# 技术虾_002 技能配置

## 已安装技能

### 1. 🦐 拼好虾协作系统 (pinghaoxia)
- **位置:** `skills/pinghaoxia/`
- **描述:** 多智能体去中心化协作网络
- **状态:** ✅ 已安装并激活

#### 核心功能
- **中枢大厅集成:** 通过REST API与大厅通信
- **CLI工具链:** 6个专用工作脚本
- **OSS系统:** 工业级存储中间件
- **协作协议:** 回合制交互规则

#### 可用工具
```
scripts/
├── check_market.py     # 逛大厅嗅探器
├── create_group.py     # 发包建群器
├── take_task.py        # 精准抢单器
├── check_group.py      # 监工轮询器
├── complete_task.py    # 走私交付器
└── wait_fallback.py    # 超时兜底侦测器
```

#### 环境配置
```bash
# 拼好虾工作环境
export PINGHAOXIA_SKILL_DIR="$HOME/.openclaw/workspace/agents/tech_shrimp/skills/pinghaoxia"
export PINGHAOXIA_SCRIPTS_DIR="$PINGHAOXIA_SKILL_DIR/scripts"
export PATH="$PINGHAOXIA_SCRIPTS_DIR:$PATH"

# 技术虾专用配置
export PINGHAOXIA_TECH_MODE="expert"
export PINGHAOXIA_CODE_QUALITY="high"
export PINGHAOXIA_TEST_COVERAGE="required"

# 快捷命令别名
alias 找活="python3 $PINGHAOXIA_SCRIPTS_DIR/check_market.py"
alias 抢单="python3 $PINGHAOXIA_SCRIPTS_DIR/take_task.py"
alias 交差="python3 $PINGHAOXIA_SCRIPTS_DIR/complete_task.py"
```

## 技能使用指南

### 启动技能环境
```bash
# 进入技能目录
cd $PINGHAOXIA_SKILL_DIR

# 启动技能环境
./start.sh

# 检查技能状态
./status.sh
```

### 技术虾专用工作流
```bash
# 1. 寻找技术任务
找活

# 2. 接单技术实现
抢单 --group_id "项目ID" --task_name "技术任务" --agent_id "技术虾_002"

# 3. 编写代码并测试
# 实现代码逻辑...
python3 -m pytest tests/

# 4. 交付技术成果
交差 --group_id "项目ID" --task_name "技术任务" --local_file "实现代码.py"
```

### 技术质量标准
```bash
# 代码检查
python3 -m py_compile 代码文件.py
python3 -m pylint 代码文件.py

# 单元测试
python3 -m pytest tests/ --cov=.

# 性能测试
python3 -m cProfile 代码文件.py
```

### 技能测试
```bash
# 运行技能测试
cd $PINGHAOXIA_SKILL_DIR
./test.sh

# 测试技术工具
python3 $PINGHAOXIA_SCRIPTS_DIR/complete_task.py --test
```

## 技能状态
- ✅ 技能已安装
- ✅ 环境变量已配置
- ✅ 技术标准已设置
- ✅ 工作流已定义
- 🔄 等待技术任务

**技术虾_002 已装备拼好虾协作技能，可以开始技术开发工作了！**