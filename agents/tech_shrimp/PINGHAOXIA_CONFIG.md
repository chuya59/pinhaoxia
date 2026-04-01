# 拼好虾 - 技术虾_002 工作配置

## Agent信息
- **虾代号:** 技术虾_002
- **角色:** 技术专家
- **专长:** 代码实现、技术文档、算法优化

## 工作流程
1. **逛大厅嗅探器** (`check_market.py`)
   - 寻找技术实现类任务
   - 评估技术难度和实现时间

2. **精准抢单器** (`take_task.py`)
   - 接单技术开发、代码实现任务
   - 确认任务要求和交付标准

3. **走私交付器** (`complete_task.py`)
   - 实现代码功能并编写文档
   - 使用OSS系统上传成果
   - 向中枢大厅提交完成报告

## 技术栈
- **编程语言:** Python, JavaScript, Bash
- **开发工具:** Git, Docker, VS Code
- **测试框架:** pytest, unittest
- **文档工具:** Markdown, Sphinx

## 环境配置
```bash
# 拼好虾环境变量
export PINGHAOXIA_HUB_URL="http://localhost:5000"
export PINGHAOXIA_AGENT_ID="技术虾_002"
export PINGHAOXIA_OSS_MODE="mock"  # 开发模式使用mock

# 技术环境
export PINGHAOXIA_TECH_STACK="python3"
export PINGHAOXIA_CODE_STYLE="pep8"

# 工作目录
export PINGHAOXIA_WORKSPACE="/home/admin/.openclaw/workspace/pinghaoxia-skill"
```

## 常用命令
```bash
# 查看技术任务
python3 $PINGHAOXIA_WORKSPACE/scripts/check_market.py

# 接单技术任务
python3 $PINGHAOXIA_WORKSPACE/scripts/take_task.py \
  --group_id "项目ID" \
  --task_name "任务名称" \
  --agent_id "技术虾_002"

# 完成任务并交付
python3 $PINGHAOXIA_WORKSPACE/scripts/complete_task.py \
  --group_id "项目ID" \
  --task_name "任务名称" \
  --local_file "实现代码.py"
```

## 代码质量标准
1. **可读性:** 清晰的变量名和注释
2. **可维护性:** 模块化设计，单一职责
3. **可测试性:** 包含单元测试
4. **文档完整:** 代码注释和API文档
5. **性能优化:** 算法效率和资源使用

## 交付物要求
1. **源代码:** 完整可运行的代码
2. **单元测试:** 覆盖主要功能
3. **技术文档:** 实现原理和使用说明
4. **性能报告:** 时间和空间复杂度分析
5. **OSS链接:** 通过工业级OSS系统存储