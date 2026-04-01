#!/usr/bin/env python3
"""
create_group.py - 发包建群器
创建新的任务组并拆解为详尽的子任务
"""

import os
import sys
import json
import uuid
import requests
from typing import List, Dict, Any
from datetime import datetime

# 添加父目录到路径以便导入 config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import config

def create_task_group(
    description: str,
    sub_tasks: List[Dict[str, str]],
    group_id: str = None
) -> Dict[str, Any]:
    """
    创建新的任务组
    
    Args:
        description: 项目总纲描述
        sub_tasks: 子任务列表，每个子任务需包含 name 和 desc
        group_id: 可选的组ID（如未提供则自动生成）
        
    Returns:
        创建结果，包含 group_id 和状态信息
    """
    if not group_id:
        # 生成唯一组ID：时间戳 + 随机后缀
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = str(uuid.uuid4())[:8]
        group_id = f"group_{timestamp}_{random_suffix}"
    
    # 准备请求数据
    payload = {
        "group_id": group_id,
        "description": description,
        "sub_tasks": sub_tasks
    }
    
    try:
        # 调用中枢大厅 API
        url = config.get_full_url("create_group")
        response = requests.post(
            url, 
            json=payload,
            timeout=config.TIMEOUTS["API_REQUEST"]
        )
        response.raise_for_status()
        
        result = response.json()
        result["group_id"] = group_id
        
        # 记录到本地日志
        log_create_group(group_id, description, sub_tasks)
        
        return result
        
    except requests.exceptions.RequestException as e:
        error_msg = f"发包建群失败: {e}"
        print(f"❌ {error_msg}")
        return {"error": error_msg, "group_id": group_id}

def parse_sub_tasks_from_input(task_input: str) -> List[Dict[str, str]]:
    """
    从输入字符串解析子任务
    
    Args:
        task_input: 格式为 "任务1:描述1;任务2:描述2" 或 JSON 字符串
        
    Returns:
        解析后的子任务列表
    """
    sub_tasks = []
    
    # 尝试解析为JSON
    try:
        tasks_data = json.loads(task_input)
        if isinstance(tasks_data, list):
            for task in tasks_data:
                if isinstance(task, dict):
                    sub_tasks.append({
                        "name": task.get("name", "未命名任务"),
                        "desc": task.get("desc", "无具体要求")
                    })
        return sub_tasks
    except json.JSONDecodeError:
        pass
    
    # 尝试解析为 "任务:描述;任务:描述" 格式
    if ":" in task_input and ";" in task_input:
        task_pairs = task_input.split(";")
        for pair in task_pairs:
            if ":" in pair:
                name, desc = pair.split(":", 1)
                sub_tasks.append({
                    "name": name.strip(),
                    "desc": desc.strip()
                })
    
    # 如果都没有匹配，创建单个任务
    if not sub_tasks:
        sub_tasks.append({
            "name": "main_task",
            "desc": task_input.strip()
        })
    
    return sub_tasks

def log_create_group(group_id: str, description: str, sub_tasks: List[Dict[str, str]]):
    """记录任务组创建日志"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "group_id": group_id,
        "description": description,
        "sub_tasks": sub_tasks,
        "agent_id": config.AGENT_ID
    }
    
    log_file = f"{config.PATHS['LOGS']}/create_groups.jsonl"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description="发包建群器 - 创建新任务组")
    parser.add_argument("--description", "-d", type=str, required=True,
                       help="项目总纲描述")
    parser.add_argument("--tasks", "-t", type=str, required=True,
                       help="子任务列表，格式：'任务1:描述1;任务2:描述2' 或 JSON 数组")
    parser.add_argument("--group-id", "-g", type=str,
                       help="指定组ID（可选，不指定则自动生成）")
    parser.add_argument("--json", "-j", action="store_true",
                       help="输出JSON格式")
    
    args = parser.parse_args()
    
    # 解析子任务
    sub_tasks = parse_sub_tasks_from_input(args.tasks)
    
    # 创建任务组
    result = create_task_group(
        description=args.description,
        sub_tasks=sub_tasks,
        group_id=args.group_id
    )
    
    if args.json:
        # JSON输出模式
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # 友好显示模式
        if "error" in result:
            print(f"❌ 发包失败: {result['error']}")
        else:
            print("✅ 发包建群成功！")
            print(f"   组ID: {result.get('group_id')}")
            print(f"   消息: {result.get('msg', '任务组已创建')}")
            print(f"\n📋 子任务详情:")
            for i, task in enumerate(sub_tasks, 1):
                print(f"   {i}. {task['name']}: {task['desc']}")
            
            print(f"\n🎯 下一步: 立即抢单自己的任务")
            print(f"   python scripts/take_task.py --group {result['group_id']} --task '{sub_tasks[0]['name']}'")

if __name__ == "__main__":
    main()