#!/bin/bash
echo "🧪 测试拼好虾系统..."

cd "$(dirname "$0")"

# 检查服务器是否运行
if ! curl -s http://localhost:5000 > /dev/null; then
    echo "❌ 错误: 中枢大厅未运行"
    echo "请先运行: ./start.sh"
    exit 1
fi

# 运行Python测试
if [ -f "../test_pinghaoxia.py" ]; then
    python3 ../test_pinghaoxia.py
else
    echo "📋 手动测试步骤:"
    echo "1. 创建任务组:"
    echo '   curl -X POST http://localhost:5000/create_group -H "Content-Type: application/json" -d '\''{"group_id":"test_001","description":"测试项目","sub_tasks":[{"name":"任务1","desc":"测试任务1"}]}'\'''
    echo ""
    echo "2. 查看任务:"
    echo "   curl http://localhost:5000/list_tasks"
    echo ""
    echo "3. 接单任务:"
    echo '   curl -X POST http://localhost:5000/take_task -H "Content-Type: application/json" -d '\''{"group_id":"test_001","task_name":"任务1","agent_id":"测试虾"}'\'''
    echo ""
    echo "4. 完成任务:"
    echo '   curl -X POST http://localhost:5000/complete_task -H "Content-Type: application/json" -d '\''{"group_id":"test_001","task_name":"任务1","oss_url":"https://example.com/result"}'\'''
fi
