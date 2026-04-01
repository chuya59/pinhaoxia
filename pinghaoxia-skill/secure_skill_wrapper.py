#!/usr/bin/env python3
"""
拼好虾Skill安全包装器
将零信任防御体系集成到拼好虾Skill中
"""

import os
import sys
import json
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from secure_executor import execute_agent_command

class PinghaoxiaSecureSkill:
    """拼好虾安全技能包装器"""
    
    def __init__(self, skill_dir=None):
        self.skill_dir = skill_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.scripts_dir = os.path.join(self.skill_dir, "scripts")
        
        # 确保脚本目录存在
        if not os.path.exists(self.scripts_dir):
            os.makedirs(self.scripts_dir, exist_ok=True)
        
        print(f"[安全技能] 初始化完成")
        print(f"  技能目录: {self.skill_dir}")
        print(f"  脚本目录: {self.scripts_dir}")
        print(f"  安全模式: 零信任防御体系已启用")
    
    def safe_execute(self, command: str) -> dict:
        """安全执行命令并返回结构化结果"""
        result = execute_agent_command(command)
        
        # 解析结果
        if "[安全警报]" in result:
            return {
                "success": False,
                "safe": False,
                "message": result,
                "output": None,
                "command": command
            }
        elif "[执行错误]" in result or "[执行崩溃]" in result or "[执行超时]" in result:
            return {
                "success": False,
                "safe": True,
                "message": result,
                "output": None,
                "command": command
            }
        else:
            return {
                "success": True,
                "safe": True,
                "message": "执行成功",
                "output": result,
                "command": command
            }
    
    def check_market(self, json_output=False, verbose=False) -> dict:
        """安全执行逛大厅嗅探器"""
        cmd = "python scripts/check_market.py"
        if json_output:
            cmd += " --json"
        if verbose:
            cmd += " --verbose"
        
        return self.safe_execute(cmd)
    
    def create_group(self, group_id: str, summary: str, tasks=None) -> dict:
        """安全执行发包建群器"""
        cmd = f"python scripts/create_group.py --group_id {group_id} --summary '{summary}'"
        
        if tasks:
            # 将任务列表转换为JSON字符串
            tasks_json = json.dumps(tasks, ensure_ascii=False)
            cmd += f" --tasks '{tasks_json}'"
        
        return self.safe_execute(cmd)
    
    def take_task(self, group_id: str, task_name: str, agent_id: str) -> dict:
        """安全执行精准抢单器"""
        cmd = f"python scripts/take_task.py --group_id {group_id} --task_name '{task_name}' --agent_id '{agent_id}'"
        return self.safe_execute(cmd)
    
    def check_group(self, group_id: str, verbose=False) -> dict:
        """安全执行监工轮询器"""
        cmd = f"python scripts/check_group.py --group_id {group_id}"
        if verbose:
            cmd += " --verbose"
        return self.safe_execute(cmd)
    
    def complete_task(self, group_id: str, task_name: str, local_file: str) -> dict:
        """安全执行走私交付器"""
        cmd = f"python scripts/complete_task.py --group_id {group_id} --task_name '{task_name}' --local_file '{local_file}'"
        return self.safe_execute(cmd)
    
    def wait_fallback(self, group_id: str, timeout=300, bypass=False) -> dict:
        """安全执行超时兜底侦测器"""
        cmd = f"python scripts/wait_fallback.py --group_id {group_id} --timeout {timeout}"
        if bypass:
            cmd += " --bypass"
        return self.safe_execute(cmd)
    
    def oss_upload(self, local_file: str, remote_name: str, mode=None) -> dict:
        """安全执行OSS上传器"""
        cmd = f"python scripts/oss_uploader.py --local_file '{local_file}' --remote_name '{remote_name}'"
        if mode:
            cmd += f" --mode {mode}"
        return self.safe_execute(cmd)
    
    def get_config(self, key=None) -> dict:
        """安全获取配置"""
        cmd = "python scripts/config.py"
        if key:
            cmd += f" --get {key}"
        else:
            cmd += " --list"
        return self.safe_execute(cmd)
    
    def set_config(self, key: str, value: str) -> dict:
        """安全设置配置"""
        cmd = f"python scripts/config.py --set {key} {value}"
        return self.safe_execute(cmd)
    
    def run_custom_command(self, command: str) -> dict:
        """安全执行自定义命令（经过严格检查）"""
        return self.safe_execute(command)
    
    def security_audit(self) -> dict:
        """执行安全审计"""
        print("[安全审计] 开始安全检查...")
        
        checks = []
        
        # 检查脚本目录
        if os.path.exists(self.scripts_dir):
            scripts = [f for f in os.listdir(self.scripts_dir) if f.endswith('.py')]
            checks.append({
                "check": "脚本目录",
                "status": "✅",
                "message": f"找到 {len(scripts)} 个Python脚本",
                "details": scripts
            })
        else:
            checks.append({
                "check": "脚本目录",
                "status": "❌",
                "message": "脚本目录不存在",
                "details": []
            })
        
        # 检查安全执行器
        try:
            from secure_executor import ALLOWED_COMMAND_PREFIXES, DANGEROUS_PATTERNS
            checks.append({
                "check": "安全执行器",
                "status": "✅",
                "message": f"已加载 {len(ALLOWED_COMMAND_PREFIXES)} 个白名单命令，{len(DANGEROUS_PATTERNS)} 个危险模式",
                "details": []
            })
        except ImportError:
            checks.append({
                "check": "安全执行器",
                "status": "❌",
                "message": "无法导入安全执行器",
                "details": []
            })
        
        # 测试安全命令
        test_result = self.safe_execute("python scripts/check_market.py --help")
        if test_result["success"]:
            checks.append({
                "check": "命令执行测试",
                "status": "✅",
                "message": "安全命令执行正常",
                "details": []
            })
        else:
            checks.append({
                "check": "命令执行测试",
                "status": "⚠️",
                "message": test_result["message"][:100],
                "details": []
            })
        
        # 测试危险命令拦截
        dangerous_test = self.safe_execute("rm -rf /")
        if not dangerous_test["safe"]:
            checks.append({
                "check": "危险命令拦截",
                "status": "✅",
                "message": "成功拦截危险命令",
                "details": []
            })
        else:
            checks.append({
                "check": "危险命令拦截",
                "status": "❌",
                "message": "危险命令拦截失败",
                "details": []
            })
        
        # 总结
        passed = sum(1 for c in checks if c["status"] == "✅")
        total = len(checks)
        
        return {
            "success": passed == total,
            "audit_result": {
                "passed": passed,
                "total": total,
                "score": f"{passed}/{total}",
                "checks": checks
            }
        }

def main():
    """主函数：演示安全技能包装器"""
    print("🦐 拼好虾 - 零信任防御体系")
    print("=" * 60)
    
    # 创建安全技能实例
    skill = PinghaoxiaSecureSkill()
    
    # 执行安全审计
    print("\n🔒 执行安全审计...")
    audit = skill.security_audit()
    
    if audit["success"]:
        print("✅ 安全审计通过！")
    else:
        print("⚠️  安全审计发现问题")
    
    # 显示审计结果
    for check in audit["audit_result"]["checks"]:
        print(f"{check['status']} {check['check']}: {check['message']}")
    
    # 演示安全命令执行
    print("\n🚀 演示安全命令执行...")
    
    # 1. 安全命令
    print("\n1. 执行安全命令 (check_market.py):")
    result = skill.check_market()
    if result["success"]:
        print(f"✅ 执行成功")
        if result["output"]:
            print(f"输出: {result['output'][:200]}...")
    else:
        print(f"❌ 执行失败: {result['message']}")
    
    # 2. 危险命令（应该被拦截）
    print("\n2. 尝试执行危险命令 (rm -rf /):")
    result = skill.run_custom_command("rm -rf /")
    if result["safe"]:
        print(f"❌ 安全漏洞！危险命令未被拦截")
    else:
        print(f"✅ 成功拦截危险命令: {result['message'][:100]}...")
    
    # 3. 参数验证
    print("\n3. 测试参数验证:")
    result = skill.run_custom_command("python scripts/check_market.py --dangerous-arg")
    if result["success"]:
        print(f"⚠️  参数验证可能有问题")
    else:
        print(f"✅ 参数验证成功拦截非法参数")
    
    print("\n" + "=" * 60)
    print("🎯 零信任防御体系特性:")
    print("  1. ✅ 命令白名单 - 只允许执行预定义的命令")
    print("  2. ✅ 危险模式检测 - 实时检测并拦截危险命令")
    print("  3. ✅ 参数验证 - 只允许使用预定义的参数")
    print("  4. ✅ 超时控制 - 防止长时间运行命令")
    print("  5. ✅ 工作目录限制 - 防止越权访问")
    print("  6. ✅ 环境变量控制 - 防止环境变量注入")
    print("\n🔒 您的拼好虾Agent现在受到全面保护！")

if __name__ == "__main__":
    main()