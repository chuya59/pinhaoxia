#!/bin/bash

echo "🦐 虾队长_001 启动工作"
echo "========================"

# 加载拼好虾Skill环境
export PINGHAOXIA_SKILL_DIR="/home/admin/.openclaw/workspace/agents/shrimp_leader/skills/pinghaoxia"
export PINGHAOXIA_SCRIPTS_DIR="$PINGHAOXIA_SKILL_DIR/scripts"
export PINGHAOXIA_HUB_URL="http://localhost:5000"
export PINGHAOXIA_AGENT_ID="虾队长_001"
export PINGHAOXIA_OSS_MODE="mock"

# 添加到PATH
export PATH="$PINGHAOXIA_SCRIPTS_DIR:$PATH"

echo "✅ 拼好虾Skill环境加载完成"
echo "   Skill目录: $PINGHAOXIA_SKILL_DIR"
echo "   脚本目录: $PINGHAOXIA_SCRIPTS_DIR"
echo "   中枢大厅: $PINGHAOXIA_HUB_URL"
echo "   Agent ID: $PINGHAOXIA_AGENT_ID"
echo "   OSS模式: $PINGHAOXIA_OSS_MODE"
echo ""

# 检查Skill状态
if [ -f "$PINGHAOXIA_SKILL_DIR/status.sh" ]; then
    echo "🔧 检查拼好虾Skill状态..."
    "$PINGHAOXIA_SKILL_DIR/status.sh"
    echo ""
fi

echo "📋 虾队长_001 工作清单 (使用拼好虾Skill):"
echo "   1. 逛大厅嗅探器: 查看任务大厅"
echo "   2. 发包建群器: 创建新项目"
echo "   3. 监工轮询器: 监控项目进度"
echo "   4. 超时兜底侦测器: 启用兜底机制"
echo ""

echo "🚀 开始工作..."
echo ""

# 进入Skill目录
cd "$PINGHAOXIA_SKILL_DIR"

echo "🔍 正在使用逛大厅嗅探器查看任务大厅..."
python3 "$PINGHAOXIA_SCRIPTS_DIR/check_market.py"

echo ""
echo "💡 快捷命令 (已配置别名):"
echo "   逛大厅: python3 $PINGHAOXIA_SCRIPTS_DIR/check_market.py"
echo "   发包: python3 $PINGHAOXIA_SCRIPTS_DIR/create_group.py --description '项目' --tasks '任务:要求'"
echo "   监工: python3 $PINGHAOXIA_SCRIPTS_DIR/check_group.py --group_id '项目ID'"
echo "   兜底: python3 $PINGHAOXIA_SCRIPTS_DIR/wait_fallback.py --group_id '项目ID' --timeout 3600"
echo ""
echo "📚 查看技能配置: cat $PINGHAOXIA_SKILL_DIR/SKILL.md | head -50"
echo "📄 查看工作配置: cat $(dirname "$0")/PINGHAOXIA_CONFIG.md"
echo ""
echo "🦐 虾队长_001 已装备拼好虾Skill，就绪等待指令..."