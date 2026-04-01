#!/bin/bash
echo "🦐 启动拼好虾系统..."

# 设置环境变量
export PINGHAOXIA_HUB_URL="http://localhost:5000"

# 启动中枢大厅
cd "$(dirname "$0")/server"
if [ ! -f hub_server_fixed.py ]; then
    echo "❌ 错误: 找不到服务器文件"
    exit 1
fi

echo "启动中枢大厅..."
nohup python3 hub_server_fixed.py > hub_server.log 2>&1 &
HUB_PID=$!
echo $HUB_PID > /tmp/pinghaoxia_hub.pid

# 等待服务器启动
sleep 3

# 检查是否启动成功
if curl -s http://localhost:5000 > /dev/null; then
    echo "✅ 中枢大厅启动成功 (PID: $HUB_PID)"
    echo "📡 地址: http://localhost:5000"
else
    echo "❌ 中枢大厅启动失败"
    exit 1
fi

echo ""
echo "🎉 拼好虾系统启动完成！"
echo "使用以下命令管理:"
echo "  ./status.sh    # 查看状态"
echo "  ./stop.sh      # 停止系统"
echo "  ./test.sh      # 运行测试"
