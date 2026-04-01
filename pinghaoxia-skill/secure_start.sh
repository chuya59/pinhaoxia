#!/bin/bash

echo "🔒 拼好虾 - 零信任安全模式启动"
echo "================================"

# 设置安全环境变量
export PINGHAOXIA_SECURITY_MODE="zero-trust"
export PYTHONSAFEEXEC="1"
export SAFE_COMMAND_EXECUTION="enabled"

# 检查安全组件
if [ ! -f "secure_skill_wrapper.py" ]; then
    echo "❌ 安全包装器不存在，请先安装零信任防御体系"
    exit 1
fi

if [ ! -f "scripts/secure_executor.py" ]; then
    echo "❌ 安全执行器不存在，请先安装零信任防御体系"
    exit 1
fi

# 启动安全技能
echo "🚀 启动安全技能包装器..."
python3 secure_skill_wrapper.py

echo ""
echo "✅ 零信任防御体系已启动"
echo ""
echo "📋 安全特性:"
echo "   • 命令白名单限制"
echo "   • 危险模式实时检测"
echo "   • 参数验证"
echo "   • 超时控制"
echo "   • 工作目录限制"
echo ""
echo "🔒 您的Agent现在受到全面保护！"
