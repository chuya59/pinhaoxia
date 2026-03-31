#!/usr/bin/env python3
"""
wait_fallback.py - 超时兜底侦测器
包工头专用：等待其他节点接单，超时后启用兜底特权
"""

import sys
import json
import time
import requests
from typing import Dict, Any, List

# 添加父目录到路径以便导入 config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import config

def wait_for_fallback(
    group_id: str,
    wait_time: int = 20,
    check_interval: int = 2
) -> Dict[str, Any]:
    """
    等待其他节点接单，超时后返回未接单任务列表
    
    Args:
        group_id: 任务组ID
        wait_time: 等待时间（秒）
        check_interval: 检查间隔（秒）
        
    Returns:
        等待结果，包含未接单任务列表和是否超时
    """
    print(f"⏳ 开始等待其他节点接单，超时时间: {wait_time}秒")
    print(f"   任务组: {group_id}")
    print("   按 Ctrl+C 提前结束等待")
    print("-" * 40)
    
    start_time = time.time()
    elapsed = 0
    last_status = None
    
    try:
        while elapsed < wait_time:
            # 检查任务组状态
            group_status = check_group_status(group_id)
            
            if "error" in group_status:
                return group_status
            
            # 分析未接单任务
            pending_tasks = get_pending_tasks(group_status)
            
            # 显示状态
            current_status = format_wait_status(group_status, pending_tasks, elapsed, wait_time)
            if current_status != last_status:
                print(current_status)
                last_status = current_status
            
            # 如果没有未接单任务，提前结束
            if not pending_tasks:
                print("🎉 所有任务已被接单，无需兜底")
                return {
                    "group_id": group_id,
                    "status": "all_taken",
                    "pending_tasks": [],
                    "elapsed_time": elapsed,
                    "timeout": False
                }
            
            # 等待下一次检查
            time.sleep(check_interval)
            elapsed = time.time() - start_time
        
        # 超时处理
        print(f"⏰ 等待超时 ({wait_time}秒)")
        
        # 获取最终的未接单任务列表
        final_status = check_group_status(group_id)
        if "error" in final_status:
            return final_status
        
        pending_tasks = get_pending_tasks(final_status)
        
        return {
            "group_id": group_id,
            "status": "timeout",
            "pending_tasks": pending_tasks,
            "elapsed_time": elapsed,
            "timeout": True,
            "message": f"等待超时，有 {len(pending_tasks)} 个任务未接单"
        }
        
    except KeyboardInterrupt:
        print("\n👋 等待被用户中断")
        elapsed = time.time() - start_time
        
        # 获取当前状态
        final_status = check_group_status(group_id)
        if "error" in final_status:
            return final_status
        
        pending_tasks = get_pending_tasks(final_status)
        
        return {
            "group_id": group_id,
            "status": "interrupted",
            "pending_tasks": pending_tasks,
            "elapsed_time": elapsed,
            "timeout": False,
            "message": "用户主动中断等待"
        }

def check_group_status(group_id: str) -> Dict[str, Any]:
    """检查任务组状态"""
    try:
        url = f"{config.get_full_url('check_group')}?group_id={group_id}"
        response = requests.get(url, timeout=config.TIMEOUTS["API_REQUEST"])
        
        if response.status_code == 404:
            return {"error": f"任务组 '{group_id}' 不存在"}
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        return {"error": f"检查任务组失败: {e}"}

def get_pending_tasks(group_status: Dict[str, Any]) -> List[Dict[str, str]]:
    """获取未接单任务列表"""
    pending_tasks = []
    
    tasks = group_status.get("tasks", {})
    for task_name, task_info in tasks.items():
        if task_info.get("status") == "pending":
            pending_tasks.append({
                "task_name": task_name,
                "task_desc": task_info.get("desc", "无描述"),
                "group_id": group_status.get("group_id", "unknown")
            })
    
    return pending_tasks

def format_wait_status(
    group_status: Dict[str, Any],
    pending_tasks: List[Dict[str, str]],
    elapsed: float,
    total_wait: int
) -> str:
    """格式化等待状态显示"""
    tasks = group_status.get("tasks", {})
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks.values() if t.get("status") == "completed")
    processing_tasks = sum(1 for t in tasks.values() if t.get("status") == "processing")
    
    progress = min(int((elapsed / total_wait) * 20), 20)
    progress_bar = "█" * progress + "░" * (20 - progress)
    percent = min(int((elapsed / total_wait) * 100), 100)
    
    lines = [
        f"🕐 已等待: {elapsed:.1f}s / {total_wait}s",
        f"   [{progress_bar}] {percent}%",
        f"📊 任务状态: 总计{total_tasks} | 待接{len(pending_tasks)} | 处理中{processing_tasks} | 完成{completed_tasks}"
    ]
    
    if pending_tasks:
        lines.append(f"⏳ 未接单任务: {len(pending_tasks)}个")
        for i, task in enumerate(pending_tasks[:3], 1):
            lines.append(f"   {i}. {task['task_name']}: {task['task_desc'][:50]}...")
        if len(pending_tasks) > 3:
            lines.append(f"   ... 还有 {len(pending_tasks) - 3} 个任务")
    
    return "\n".join(lines)

def execute_fallback(group_id: str, pending_tasks: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    执行兜底操作：使用特权接单所有未接任务
    
    Args:
        group_id: 任务组ID
        pending_tasks: 未接单任务列表
        
    Returns:
        兜底执行结果
    """
    if not pending_tasks:
        return {"message": "没有需要兜底的任务", "group_id": group_id}
    
    print(f"🚨 开始兜底执行，将接单 {len(pending_tasks)} 个任务")
    print("⚠️  启用兜底特权（--bypass）")
    
    results = []
    for task in pending_tasks:
        task_name = task["task_name"]
        print(f"   🔄 接单任务: {task_name}")
        
        # 使用特权接单
        try:
            # 这里需要调用 take_task.py 的逻辑，但为了简化，我们直接模拟
            # 实际应该导入并调用 take_task 函数
            payload = {
                "group_id": group_id,
                "task_name": task_name,
                "agent_id": config.AGENT_ID,
                "bypass_monopoly": True
            }
            
            url = config.get_full_url("take_task")
            response = requests.post(
                url, 
                json=payload,
                timeout=config.TIMEOUTS["API_REQUEST"]
            )
            
            if response.status_code == 200:
                result = response.json()
                results.append({
                    "task_name": task_name,
                    "status": "success",
                    "message": result.get("msg", "接单成功")
                })
                print(f"     ✅ 成功接单")
            else:
                results.append({
                    "task_name": task_name,
                    "status": "failed",
                    "message": f"HTTP {response.status_code}: {response.text}"
                })
                print(f"     ❌ 接单失败")
                
        except Exception as e:
            results.append({
                "task_name": task_name,
                "status": "error",
                "message": str(e)
            })
            print(f"     ❌ 错误: {e}")
    
    return {
        "group_id": group_id,
        "fallback_executed": True,
        "total_tasks": len(pending_tasks),
        "successful": sum(1 for r in results if r["status"] == "success"),
        "failed": sum(1 for r in results if r["status"] != "success"),
        "results": results,
        "message": f"兜底执行完成，成功接单 {sum(1 for r in results if r['status'] == 'success')}/{len(pending_tasks)} 个任务"
    }

def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description="超时兜底侦测器 - 包工头专用")
    parser.add_argument("--group", "-g", type=str, required=True,
                       help="任务组ID")
    parser.add_argument("--time", "-t", type=int, default=20,
                       help="等待时间（秒，默认20）")
    parser.add_argument("--interval", "-i", type=int, default=2,
                       help="检查间隔（秒，默认2）")
    parser.add_argument("--auto-fallback", "-a", action="store_true",
                       help="超时后自动执行兜底")
    parser.add_argument("--json", "-j", action="store_true",
                       help="输出JSON格式")
    
    args = parser.parse_args()
    
    # 等待其他节点接单
    wait_result = wait_for_fallback(
        group_id=args.group,
        wait_time=args.time,
        check_interval=args.interval
    )
    
    # 检查是否需要兜底
    if wait_result.get("timeout") and args.auto_fallback:
        print("\n" + "=" * 50)
        print("🚀 检测到超时，开始自动兜底执行")
        print("=" * 50)
        
        fallback_result = execute_fallback(
            group_id=args.group,
            pending_tasks=wait_result.get("pending_tasks", [])
        )
        
        # 合并结果
        final_result = {
            "wait_result": wait_result,
            "fallback_result": fallback_result,
            "final_status": "fallback_executed"
        }
    else:
        final_result = {
            "wait_result": wait_result,
            "fallback_result": None,
            "final_status": "wait_completed"
        }
        
        if wait_result.get("timeout"):
            print("\n⚠️  等待超时，但未启用自动兜底")
            print("   如需兜底，请使用 --auto-fallback 参数")
            print("   或手动接单:")
            for task in wait_result.get("pending_tasks", []):
                print(f"   python scripts/take_task.py --group {args.group} --task '{task['task_name']}' --bypass")
    
    if args.json:
        # JSON输出模式
        print(json.dumps(final_result, indent=2, ensure_ascii=False))
    else:
        # 总结显示
        print("\n" + "=" * 50)
        print("📋 等待结果总结")
        print("=" * 50)
        
        wr = wait_result
        print(f"任务组: {wr.get('group_id')}")
        print(f"状态: {wr.get('status')}")
        print(f"等待时间: {wr.get('elapsed_time', 0):.1f}秒")
        print(f"未接单任务: {len(wr.get('pending_tasks', []))}个")
        
        if final_result.get("fallback_result"):
            fr = final_result["fallback_result"]
            print(f"\n🚀 兜底执行结果:")
            print(f"   成功接单: {fr.get('successful', 0)}/{fr.get('total_tasks', 0)}")
            print(f"   消息: {fr.get('message')}")

if __name__ == "__main__":
    main()