#!/usr/bin/env python3
"""
check_market.py - 逛大厅嗅探器
查看中枢大厅中所有未被接走的任务及其详情
"""

import os
import sys
import json
import requests
from typing import List, Dict, Any

# 添加父目录到路径以便导入 config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import config

def check_market(intent_filter: str = "") -> List[Dict[str, Any]]:
    """
    查看大厅中所有可用的任务
    
    Args:
        intent_filter: 意图过滤器（可选），用于筛选匹配的任务
        
    Returns:
        可用任务列表，每个任务包含：
        - group_id: 任务组ID
        - group_desc: 项目总纲
        - task_name: 任务名称
        - task_desc: 任务具体要求
    """
    try:
        # 调用中枢大厅 API
        url = config.get_full_url("list_tasks")
        response = requests.get(url, timeout=config.TIMEOUTS["API_REQUEST"])
        response.raise_for_status()
        
        data = response.json()
        available_tasks = data.get("available_tasks", [])
        
        # 如果有意图过滤器，进行筛选
        if intent_filter:
            filtered_tasks = []
            for task in available_tasks:
                # 检查任务描述是否匹配意图
                group_desc = task.get("group_desc", "").lower()
                task_desc = task.get("task_desc", "").lower()
                filter_text = intent_filter.lower()
                
                if filter_text in group_desc or filter_text in task_desc:
                    filtered_tasks.append(task)
            return filtered_tasks
        
        return available_tasks
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 逛大厅失败: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ 解析响应失败: {e}")
        return []

def format_task_display(tasks: List[Dict[str, Any]]) -> str:
    """格式化任务显示"""
    if not tasks:
        return "📭 大厅空空如也，暂无任务可接。"
    
    output = ["🦐 拼好虾任务大厅 - 当前可用任务:"]
    output.append("=" * 60)
    
    for i, task in enumerate(tasks, 1):
        output.append(f"\n📋 任务 #{i}")
        output.append(f"   项目组: {task.get('group_id', '未知')}")
        output.append(f"   项目总纲: {task.get('group_desc', '无描述')}")
        output.append(f"   任务名称: {task.get('task_name', '未命名')}")
        output.append(f"   任务要求: {task.get('task_desc', '无具体要求')}")
        output.append("-" * 40)
    
    output.append(f"\n🎯 共发现 {len(tasks)} 个可用任务")
    return "\n".join(output)

def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description="逛大厅嗅探器 - 查看所有可用任务")
    parser.add_argument("--filter", "-f", type=str, default="", 
                       help="意图过滤器（关键词匹配）")
    parser.add_argument("--json", "-j", action="store_true",
                       help="输出JSON格式")
    
    args = parser.parse_args()
    
    # 检查大厅
    tasks = check_market(args.filter)
    
    if args.json:
        # JSON输出模式
        print(json.dumps({
            "available_tasks": tasks,
            "count": len(tasks),
            "filter": args.filter
        }, indent=2, ensure_ascii=False))
    else:
        # 友好显示模式
        print(format_task_display(tasks))
        
        # 如果有任务，提示如何接单
        if tasks:
            print("\n💡 提示: 使用以下命令接单:")
            print(f"   python scripts/take_task.py --group {tasks[0]['group_id']} --task '{tasks[0]['task_name']}'")

if __name__ == "__main__":
    main()