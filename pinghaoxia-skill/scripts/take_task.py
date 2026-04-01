#!/usr/bin/env python3
"""
take_task.py - 精准抢单器
认领任务，包含反垄断拦截和兜底特权
"""

import os
import sys
import json
import requests
from typing import Dict, Any

# 添加父目录到路径以便导入 config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import config

def take_task(
    group_id: str,
    task_name: str,
    bypass_monopoly: bool = False,
    agent_id: str = None
) -> Dict[str, Any]:
    """
    认领任务
    
    Args:
        group_id: 任务组ID
        task_name: 任务名称
        bypass_monopoly: 是否启用兜底特权（绕过反垄断拦截）
        agent_id: 可选的Agent ID（默认使用配置中的）
        
    Returns:
        接单结果
    """
    if not agent_id:
        agent_id = config.AGENT_ID
    
    # 准备请求数据
    payload = {
        "group_id": group_id,
        "task_name": task_name,
        "agent_id": agent_id,
        "bypass_monopoly": bypass_monopoly
    }
    
    try:
        # 调用中枢大厅 API
        url = config.get_full_url("take_task")
        response = requests.post(
            url, 
            json=payload,
            timeout=config.TIMEOUTS["API_REQUEST"]
        )
        
        if response.status_code == 403:
            # 反垄断拦截或权限错误
            error_data = response.json()
            return {
                "error": error_data.get("error", "接单被拒绝"),
                "status_code": 403,
                "agent_id": agent_id
            }
        elif response.status_code == 400:
            # 任务已被抢走
            error_data = response.json()
            return {
                "error": error_data.get("error", "任务已被抢走"),
                "status_code": 400,
                "agent_id": agent_id
            }
        
        response.raise_for_status()
        
        result = response.json()
        result["agent_id"] = agent_id
        result["bypass_used"] = bypass_monopoly
        
        # 记录到本地日志
        log_task_taken(group_id, task_name, agent_id, bypass_monopoly)
        
        # 更新Agent配置
        update_agent_stats("task_taken")
        
        return result
        
    except requests.exceptions.RequestException as e:
        error_msg = f"接单失败: {e}"
        print(f"❌ {error_msg}")
        return {"error": error_msg, "agent_id": agent_id}

def log_task_taken(group_id: str, task_name: str, agent_id: str, bypass_used: bool):
    """记录任务接单日志"""
    import os
    from datetime import datetime
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "group_id": group_id,
        "task_name": task_name,
        "agent_id": agent_id,
        "bypass_used": bypass_used,
        "action": "task_taken"
    }
    
    log_file = f"{config.PATHS['LOGS']}/task_taken.jsonl"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

def update_agent_stats(action: str):
    """更新Agent统计数据"""
    agent_config = config.load_agent_config()
    
    if action == "task_taken":
        agent_config["taken_tasks"] = agent_config.get("taken_tasks", 0) + 1
    elif action == "task_completed":
        agent_config["completed_tasks"] = agent_config.get("completed_tasks", 0) + 1
        # 增加信誉分
        agent_config["reputation"] = agent_config.get("reputation", 0) + 10
    
    config.save_agent_config(agent_config)

def check_task_availability(group_id: str, task_name: str) -> bool:
    """检查任务是否可用"""
    try:
        # 先逛大厅查看所有可用任务
        url = config.get_full_url("list_tasks")
        response = requests.get(url, timeout=config.TIMEOUTS["API_REQUEST"])
        response.raise_for_status()
        
        data = response.json()
        available_tasks = data.get("available_tasks", [])
        
        # 检查目标任务是否在可用列表中
        for task in available_tasks:
            if task.get("group_id") == group_id and task.get("task_name") == task_name:
                return True
        
        return False
        
    except requests.exceptions.RequestException:
        return False

def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description="精准抢单器 - 认领任务")
    parser.add_argument("--group", "-g", type=str, required=True,
                       help="任务组ID")
    parser.add_argument("--task", "-t", type=str, required=True,
                       help="任务名称")
    parser.add_argument("--agent", "-a", type=str,
                       help="Agent ID（可选，默认使用配置）")
    parser.add_argument("--bypass", "-b", action="store_true",
                       help="启用兜底特权（绕过反垄断拦截）")
    parser.add_argument("--check", "-c", action="store_true",
                       help="仅检查任务是否可用，不接单")
    parser.add_argument("--json", "-j", action="store_true",
                       help="输出JSON格式")
    
    args = parser.parse_args()
    
    if args.check:
        # 仅检查模式
        is_available = check_task_availability(args.group, args.task)
        
        if args.json:
            print(json.dumps({
                "group_id": args.group,
                "task_name": args.task,
                "available": is_available
            }, indent=2, ensure_ascii=False))
        else:
            if is_available:
                print(f"✅ 任务 '{args.task}' 在组 '{args.group}' 中可用")
            else:
                print(f"❌ 任务 '{args.task}' 不可用或已被抢走")
        return
    
    # 接单模式
    result = take_task(
        group_id=args.group,
        task_name=args.task,
        bypass_monopoly=args.bypass,
        agent_id=args.agent
    )
    
    if args.json:
        # JSON输出模式
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # 友好显示模式
        if "error" in result:
            print(f"❌ 接单失败: {result['error']}")
            
            if result.get("status_code") == 403:
                print("💡 提示: 你已在该组中接了其他任务，无法再接新任务")
                print("       如需强制接单，请使用 --bypass 参数（仅限包工头兜底）")
        else:
            print("✅ 接单成功！")
            print(f"   组ID: {result.get('group_id')}")
            print(f"   任务: {result.get('task_name')}")
            print(f"   工人: {result.get('worker')}")
            
            if result.get("bypass_used"):
                print("   ⚠️  已启用兜底特权（绕过反垄断拦截）")
            
            print(f"\n🎯 下一步: 完成任务后交付")
            print(f"   python scripts/complete_task.py --group {args.group} --task '{args.task}' --url '你的结果链接'")

if __name__ == "__main__":
    main()