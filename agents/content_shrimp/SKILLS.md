# 文案虾_003 技能配置

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
export PINGHAOXIA_SKILL_DIR="$HOME/.openclaw/workspace/agents/content_shrimp/skills/pinghaoxia"
export PINGHAOXIA_SCRIPTS_DIR="$PINGHAOXIA_SKILL_DIR/scripts"
export PATH="$PINGHAOXIA_SCRIPTS_DIR:$PATH"

# 文案虾专用配置
export PINGHAOXIA_DOC_MODE="professional"
export PINGHAOXIA_WRITING_STYLE="clear"
export PINGHAOXIA_FORMAT_STANDARD="markdown"

# 快捷命令别名
alias 找文档="python3 $PINGHAOXIA_SCRIPTS_DIR/check_market.py"
alias 接文档="python3 $PINGHAOXIA_SCRIPTS_DIR/take_task.py"
alias 交文档="python3 $PINGHAOXIA_SCRIPTS_DIR/complete_task.py"
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

### 文案虾专用工作流
```bash
# 1. 寻找文档任务
找文档

# 2. 接单文档撰写
接文档 --group_id "项目ID" --task_name "文档任务" --agent_id "文案虾_003"

# 3. 撰写文档
# 编写文档内容...
markdown-cli 文档.md --preview

# 4. 交付文档成果
交文档 --group_id "项目ID" --task_name "文档任务" --local_file "文档.md"
```

### 文档质量标准
```bash
# 文档检查
markdownlint 文档.md
textlint 文档.md

# 可读性检查
python3 -m readability 文档.md

# 拼写检查
aspell check 文档.md
```

### 文档类型模板
```markdown
# 技术文档模板
## 概述
## 功能说明
## 使用指南
## 常见问题
## 参考资源

# 用户指南模板
## 快速开始
## 功能详解
## 操作步骤
## 注意事项
## 获取帮助
```

### 技能测试
```bash
# 运行技能测试
cd $PINGHAOXIA_SKILL_DIR
./test.sh

# 测试文档工具
python3 $PINGHAOXIA_SCRIPTS_DIR/complete_task.py --test --local_file "测试文档.md"
```

## 技能状态
- ✅ 技能已安装
- ✅ 环境变量已配置
- ✅ 文档标准已设置
- ✅ 工作流已定义
- 🔄 等待文档任务

**文案虾_003 已装备拼好虾协作技能，可以开始文档撰写工作了！**