#!/bin/bash

echo "🦐 文案虾_003 启动工作"
echo "========================"

# 加载拼好虾Skill环境
export PINGHAOXIA_SKILL_DIR="/home/admin/.openclaw/workspace/agents/content_shrimp/skills/pinghaoxia"
export PINGHAOXIA_SCRIPTS_DIR="$PINGHAOXIA_SKILL_DIR/scripts"
export PINGHAOXIA_HUB_URL="http://localhost:5000"
export PINGHAOXIA_AGENT_ID="文案虾_003"
export PINGHAOXIA_OSS_MODE="mock"
export PINGHAOXIA_DOC_FORMAT="markdown"
export PINGHAOXIA_DOC_STYLE="clear"
export PINGHAOXIA_WRITING_STYLE="professional"

# 添加到PATH
export PATH="$PINGHAOXIA_SCRIPTS_DIR:$PATH"

echo "✅ 拼好虾Skill环境加载完成"
echo "   Skill目录: $PINGHAOXIA_SKILL_DIR"
echo "   脚本目录: $PINGHAOXIA_SCRIPTS_DIR"
echo "   中枢大厅: $PINGHAOXIA_HUB_URL"
echo "   Agent ID: $PINGHAOXIA_AGENT_ID"
echo "   OSS模式: $PINGHAOXIA_OSS_MODE"
echo "   文档格式: $PINGHAOXIA_DOC_FORMAT"
echo "   文档风格: $PINGHAOXIA_DOC_STYLE"
echo "   写作标准: $PINGHAOXIA_WRITING_STYLE"
echo ""

# 检查Skill状态
if [ -f "$PINGHAOXIA_SKILL_DIR/status.sh" ]; then
    echo "🔧 检查拼好虾Skill状态..."
    "$PINGHAOXIA_SKILL_DIR/status.sh"
    echo ""
fi

echo "📋 文案虾_003 工作清单 (使用拼好虾Skill):"
echo "   1. 逛大厅嗅探器: 寻找文档任务"
echo "   2. 精准抢单器: 接单文档撰写"
echo "   3. 走私交付器: 交付文档成果"
echo "   4. 文档质量检查: 确保清晰易懂"
echo ""

echo "🚀 开始工作..."
echo ""

# 进入Skill目录
cd "$PINGHAOXIA_SKILL_DIR"

echo "🔍 正在使用逛大厅嗅探器寻找文档任务..."
python3 "$PINGHAOXIA_SCRIPTS_DIR/check_market.py"

echo ""
echo "💡 快捷命令 (已配置别名):"
echo "   找文档: python3 $PINGHAOXIA_SCRIPTS_DIR/check_market.py"
echo "   接文档: python3 $PINGHAOXIA_SCRIPTS_DIR/take_task.py --group_id '项目ID' --task_name '任务' --agent_id '文案虾_003'"
echo "   交文档: python3 $PINGHAOXIA_SCRIPTS_DIR/complete_task.py --group_id '项目ID' --task_name '任务' --local_file '文档.md'"
echo ""
echo "📝 文档工具:"
echo "   格式检查: markdownlint 文档.md"
echo "   拼写检查: aspell check 文档.md"
echo "   可读性检查: python3 -m readability 文档.md"
echo ""
echo "📚 查看技能配置: cat $PINGHAOXIA_SKILL_DIR/SKILL.md | head -50"
echo "📄 查看工作配置: cat $(dirname "$0")/PINGHAOXIA_CONFIG.md"
echo ""
echo "🦐 文案虾_003 已装备拼好虾Skill，就绪等待文档任务..."