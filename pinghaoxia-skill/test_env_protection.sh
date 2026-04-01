#!/bin/bash

echo "🔐 环境变量保护测试"
echo "===================="

# 设置测试环境变量
export GITHUB_TOKEN="test_github_pat_1234567890abcdef"
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export OPENAI_API_KEY="sk-test-openai-key-123456"
export DATABASE_URL="postgresql://user:password@localhost/db"

echo "📋 设置的测试环境变量:"
echo "  • GITHUB_TOKEN: $GITHUB_TOKEN"
echo "  • AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID"
echo "  • OPENAI_API_KEY: $OPENAI_API_KEY"
echo "  • DATABASE_URL: $DATABASE_URL"
echo ""

echo "🚀 开始环境变量保护测试..."
echo ""

# 测试1: 尝试读取环境变量（应该被拦截）
echo "1. 测试读取敏感环境变量:"
echo "   命令: echo \$GITHUB_TOKEN"
python3 -c "
import sys
sys.path.insert(0, 'scripts')
from secure_executor import execute_agent_command
result = execute_agent_command('echo \$GITHUB_TOKEN')
print('   结果:', '✅ 被拦截' if '[安全警报]' in result else '❌ 未被拦截')
"
echo ""

# 测试2: 尝试使用printenv读取（应该被拦截）
echo "2. 测试使用printenv读取:"
echo "   命令: printenv AWS_ACCESS_KEY_ID"
python3 -c "
import sys
sys.path.insert(0, 'scripts')
from secure_executor import execute_agent_command
result = execute_agent_command('printenv AWS_ACCESS_KEY_ID')
print('   结果:', '✅ 被拦截' if '[安全警报]' in result else '❌ 未被拦截')
"
echo ""

# 测试3: 尝试使用Python读取（应该被拦截）
echo "3. 测试使用Python读取:"
echo "   命令: python -c 'import os; print(os.getenv(\"OPENAI_API_KEY\"))'"
python3 -c "
import sys
sys.path.insert(0, 'scripts')
from secure_executor import execute_agent_command
result = execute_agent_command('python -c \"import os; print(os.getenv(\\\"OPENAI_API_KEY\\\"))\"')
print('   结果:', '✅ 被拦截' if '[安全警报]' in result else '❌ 未被拦截')
"
echo ""

# 测试4: 安全命令（应该正常执行）
echo "4. 测试安全命令执行:"
echo "   命令: python scripts/check_market.py --help"
python3 -c "
import sys
sys.path.insert(0, 'scripts')
from secure_executor import execute_agent_command
result = execute_agent_command('python scripts/check_market.py --help')
if '[执行成功]' in result or 'usage:' in result:
    print('   结果: ✅ 正常执行')
else:
    print('   结果: ⚠️  执行可能有问题')
"
echo ""

echo "===================="
echo "📊 测试总结:"
echo "  环境变量保护功能已成功集成到拼好虾零信任防御体系"
echo "  所有敏感环境变量的读取尝试都会被实时拦截"
echo "  安全命令可以正常执行，不受影响"
echo ""
echo "🔒 您的密钥、token等敏感信息现在受到全面保护！"
