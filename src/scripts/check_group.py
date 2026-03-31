#!/usr/bin/env python3
"""
check_group.py - 监工轮询器
查询整个任务组的进度和状态
"""

import sys
import json
import requests
from typing import Dict, Any, List

# 添加父目录到路径以便导入 config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import config

def check_group(group_id: str) -> Dict[str, Any]:
    """
    查询任务组状态
    
    Args:
        group_id: 任务组ID
        
    Returns:
        任务组完整状态信息
    """
    try:
        # 调用中枢大厅 API
        url = f"{config.get_full_url('check_group')}?group_id={group_id}"
        response = requests.get(url, timeout=config.TIMEOUTS["API_REQUEST"])
        
        if response.status_code == 404:
            return {
                "error": f"任务组 '{group_id}' 不存在",
                "status_code": 404,
                "group_id": group_id
            }
        
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        error_msg = f"查询任务组失败: {e}"
        print(f"❌ {error_msg}")
        return {"error": error_msg, "group_id": group_id}

def analyze_group_status(group_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析任务组状态
    
    Returns:
        分析结果，包含统计信息和建议
    """
    if "error" in group_data:
        return group_data
    
    tasks = group_data.get("tasks", {})
    total_tasks = len(tasks)
    
    # 统计任务状态
    status_counts = {"pending": 0, "processing": 0, "completed": 0}
    for task_info in tasks.values():
        status = task_info.get("status", "pending")
        if status in status_counts:
            status_counts[status] += 1
    
    # 计算进度
    completion_rate = 0
    if total_tasks > 0:
        completion_rate = (status_counts["completed"] / total_tasks) * 100
    
    # 分析建议
    suggestions = []
    if status_counts["pending"] > 0:
        suggestions.append(f"还有 {status_counts['pending']} 个任务待接单")
    if status_counts["processing"] > 0:
        suggestions.append(f"有 {status_counts['processing']} 个任务正在处理中")
    
    # 判断是否需要兜底
    needs_fallback = False
    if group_data.get("status") == "recruiting" and status_counts["pending"] > 0:
        # 检查是否有任务长时间未接单
        needs_fallback = True
    
    return {
        "group_id": group_data.get("group_id", "unknown"),
        "description": group_data.get("description", "无描述"),
        "group_status": group_data.get("status", "unknown"),
        "total_tasks": total_tasks,
        "status_counts": status_counts,
        "completion_rate": round(completion_rate, 1),
        "suggestions": suggestions,
        "needs_fallback": needs_fallback,
        "tasks": tasks
    }

def format_group_display(analysis: Dict[str, Any]) -> str:
    """格式化任务组显示"""
    if "error" in analysis:
        return f"❌ {analysis['error']}"
    
    output = [f"📊 任务组监控报告: {analysis['group_id']}"]
    output.append("=" * 60)
    output.append(f"项目总纲: {analysis['description']}")
    output.append(f"组状态: {analysis['group_status']}")
    output.append(f"完成度: {analysis['completion_rate']}%")
    output.append("")
    
    # 任务状态统计
    output.append("📈 任务状态统计:")
    counts = analysis['status_counts']
    output.append(f"   待接单: {counts['pending']} 个")
    output.append(f"   处理中: {counts['processing']} 个") 
    output.append(f"   已完成: {counts['completed']} 个")
    output.append(f"   总计: {analysis['total_tasks']} 个")
    output.append("")
    
    # 任务详情
    output.append("📋 任务详情:")
    tasks = analysis.get("tasks", {})
    for task_name, task_info in tasks.items():
        status = task_info.get("status", "pending")
        worker = task_info.get("worker", "未分配")
        desc = task_info.get("desc", "无描述")
        
        status_icon = {
            "pending": "⏳",
            "processing": "🔄", 
            "completed": "✅"
        }.get(status, "❓")
        
        output.append(f"   {status_icon} {task_name}")
        output.append(f"       状态: {status}")
        output.append(f"       工人: {worker}")
        output.append(f"       要求: {desc}")
        
        if task_info.get("oss_url"):
            output.append(f"       交付: {task_info['oss_url']}")
        
        output.append("")
    
    # 建议
    if analysis['suggestions']:
        output.append("💡 建议:")
        for suggestion in analysis['suggestions']:
            output.append(f"   • {suggestion}")
    
    # 兜底提示
    if analysis['needs_fallback']:
        output.append("")
        output.append("⚠️  注意: 有任务长时间未接单，可能需要兜底")
        output.append("   使用命令: python scripts/wait_fallback.py --group " + analysis['group_id'])
    
    return "\n".join(output)

def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description="监工轮询器 - 查询任务组进度")
    parser.add_argument("--group", "-g", type=str, required=True,
                       help="任务组ID")
    parser.add_argument("--json", "-j", action="store_true",
                       help="输出JSON格式")
    parser.add_argument("--watch", "-w", action="store_true",
                       help="监控模式，持续轮询")
    parser.add_argument("--interval", "-i", type=int, default=5,
                       help="监控间隔（秒，仅限监控模式）")
    
    args = parser.parse_args()
    
    if args.watch:
        # 监控模式
        import time
        print(f"👀 开始监控任务组: {args.group}")
        print("按 Ctrl+C 停止监控")
        print("-" * 40)
        
        try:
            while True:
                group_data = check_group(args.group)
                analysis = analyze_group_status(group_data)
                
                if not args.json:
                    print(f"\n🕐 {time.strftime('%H:%M:%S')}")
                    print(format_group_display(analysis))
                else:
                    print(json.dumps(analysis, indent=2, ensure_ascii=False))
                
                # 检查是否全部完成
                if analysis.get("completion_rate", 0) >= 100:
                    print("\n🎉 所有任务已完成！")
                    break
                
                time.sleep(args.interval)
                
        except KeyboardInterrupt:
            print("\n👋 监控已停止")
        return
    
    # 单次查询模式
    group_data = check_group(args.group)
    analysis = analyze_group_status(group_data)
    
    if args.json:
        # JSON输出模式
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
    else:
        # 友好显示模式
        print(format_group_display(analysis))

if __name__ == "__main__":
    main()