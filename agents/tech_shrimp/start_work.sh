#!/bin/bash

echo "🦐 技术虾_002 启动工作"
echo "========================"

# 加载拼好虾Skill环境
export PINGHAOXIA_SKILL_DIR="/home/admin/.openclaw/workspace/agents/tech_shrimp/skills/pinghaoxia"
export PINGHAOXIA_SCRIPTS_DIR="$PINGHAOXIA_SKILL_DIR/scripts"
export PINGHAOXIA_HUB_URL="http://localhost:5000"
export PINGHAOXIA_AGENT_ID="技术虾_002"
export PINGHAOXIA_OSS_MODE="mock"
export PINGHAOXIA_TECH_STACK="python3"
export PINGHAOXIA_CODE_STYLE="pep8"
export PINGHAOXIA_CODE_QUALITY="high"

# 添加到PATH
export PATH="$PINGHAOXIA_SCRIPTS_DIR:$PATH"

echo "✅ 拼好虾Skill环境加载完成"
echo "   Skill目录: $PINGHAOXIA_SKILL_DIR"
echo "   脚本目录: $PINGHAOXIA_SCRIPTS_DIR"
echo "   中枢大厅: $PINGHAOXIA_HUB_URL"
echo "   Agent ID: $PINGHAOXIA_AGENT_ID"
echo "   OSS模式: $PINGHAOXIA_OSS_MODE"
echo "   技术栈: $PINGHAOXIA_TECH_STACK"
echo "   代码规范: $PINGHAOXIA_CODE_STYLE"
echo "   质量标准: $PINGHAOXIA_CODE_QUALITY"
echo ""

# 检查Skill状态
if [ -f "$PINGHAOXIA_SKILL_DIR/status.sh" ]; then
    echo "🔧 检查拼好虾Skill状态..."
    "$PINGHAOXIA_SKILL_DIR/status.sh"
    echo ""
fi

echo "📋 技术虾_002 工作清单 (使用拼好虾Skill):"
echo "   1. 逛大厅嗅探器: 寻找技术任务"
echo "   2. 精准抢单器: 接单代码实现"
echo "   3. 走私交付器: 交付技术成果"
echo "   4. 代码质量检查: 确保高质量交付"
echo ""

echo "🚀 开始工作..."
echo ""

# 进入Skill目录
cd "$PINGHAOXIA_SKILL_DIR"

echo "🔍 正在使用逛大厅嗅探器寻找技术任务..."
python3 "$PINGHAOXIA_SCRIPTS_DIR/check_market.py"

echo ""
echo "💡 快捷命令 (已配置别名):"
echo "   找活: python3 $PINGHAOXIA_SCRIPTS_DIR/check_market.py"
echo "   抢单: python3 $PINGHAOXIA_SCRIPTS_DIR/take_task.py --group_id '项目ID' --task_name '任务' --agent_id '技术虾_002'"
echo "   交差: python3 $PINGHAOXIA_SCRIPTS_DIR/complete_task.py --group_id '项目ID' --task_name '任务' --local_file '代码.py'"
echo ""
echo "🔧 技术工具:"
echo "   代码检查: python3 -m py_compile 代码文件.py"
echo "   单元测试: python3 -m pytest tests/"
echo "   性能分析: python3 -m cProfile 代码文件.py"
echo ""
echo "📚 查看技能配置: cat $PINGHAOXIA_SKILL_DIR/SKILL.md | head -50"
echo "📄 查看工作配置: cat $(dirname "$0")/PINGHAOXIA_CONFIG.md"
echo ""
echo "🦐 技术虾_002 已装备拼好虾Skill，就绪等待技术任务..."