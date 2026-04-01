#!/bin/bash
echo "🦐 停止拼好虾系统..."

if [ -f /tmp/pinghaoxia_hub.pid ]; then
    PID=$(cat /tmp/pinghaoxia_hub.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        echo "✅ 停止中枢大厅 (PID: $PID)"
    fi
    rm -f /tmp/pinghaoxia_hub.pid
fi

# 停止Agent进程
for i in 1 2 3; do
    if [ -f /tmp/pinghaoxia_agent${i}.pid ]; then
        PID=$(cat /tmp/pinghaoxia_agent${i}.pid)
        if kill -0 $PID 2>/dev/null; then
            kill $PID
            echo "✅ 停止Agent $i (PID: $PID)"
        fi
        rm -f /tmp/pinghaoxia_agent${i}.pid
    fi
done

echo "✅ 系统已停止"
