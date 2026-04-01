#!/bin/bash
echo "🦐 拼好虾系统状态"

# 检查中枢大厅
if curl -s http://localhost:5000 > /dev/null; then
    echo "✅ 中枢大厅: 运行中"
    
    # 获取任务数量
    TASKS=$(curl -s http://localhost:5000/list_tasks | python3 -c "import sys,json; data=json.load(sys.stdin); print(len(data.get('available_tasks', [])))")
    echo "📋 可用任务: $TASKS 个"
else
    echo "❌ 中枢大厅: 未运行"
fi

# 检查进程
if [ -f /tmp/pinghaoxia_hub.pid ]; then
    PID=$(cat /tmp/pinghaoxia_hub.pid)
    if kill -0 $PID 2>/dev/null; then
        echo "📊 服务器PID: $PID"
    fi
fi

echo ""
echo "📁 技能目录: $(dirname "$0")"
echo "🛠️  工具脚本:"
ls -la "$(dirname "$0")/scripts/" 2>/dev/null | grep "\.py$" | wc -l | xargs echo "   Python脚本:"
ls -la "$(dirname "$0")/agents/" 2>/dev/null | grep "\.md$" | wc -l | xargs echo "   Agent配置:"
