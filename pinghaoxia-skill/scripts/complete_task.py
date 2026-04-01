#!/usr/bin/env python3
"""
complete_task.py - 走私交付器
完成任务并提交结果（模拟OSS直传）
"""

import sys
import json
import os
import uuid
import requests
from datetime import datetime
from typing import Dict, Any

# 添加父目录到路径以便导入 config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import config

def complete_task(
    group_id: str,
    task_name: str,
    result_content: str = None,
    result_file: str = None,
    oss_url: str = None,
    agent_id: str = None
) -> Dict[str, Any]:
    """
    完成任务并交付
    
    Args:
        group_id: 任务组ID
        task_name: 任务名称
        result_content: 结果内容（文本）
        result_file: 结果文件路径
        oss_url: 直接提供的OSS URL（如果已有）
        agent_id: 可选的Agent ID
        
    Returns:
        交付结果
    """
    if not agent_id:
        agent_id = config.AGENT_ID
    
    # 生成或获取OSS URL
    final_oss_url = oss_url
    if not final_oss_url:
        if result_file and os.path.exists(result_file):
            # 从文件生成模拟OSS URL
            final_oss_url = generate_mock_oss_url(result_file, result_content)
        elif result_content:
            # 从内容生成模拟OSS URL
            final_oss_url = generate_mock_oss_url(None, result_content)
        else:
            return {
                "error": "需要提供结果内容、文件或OSS URL",
                "agent_id": agent_id
            }
    
    # 准备请求数据
    payload = {
        "group_id": group_id,
        "task_name": task_name,
        "oss_url": final_oss_url
    }
    
    try:
        # 调用中枢大厅 API
        url = config.get_full_url("complete_task")
        response = requests.post(
            url, 
            json=payload,
            timeout=config.TIMEOUTS["API_REQUEST"]
        )
        
        if response.status_code == 400:
            error_data = response.json()
            return {
                "error": error_data.get("error", "交付失败"),
                "status_code": 400,
                "agent_id": agent_id
            }
        
        response.raise_for_status()
        
        result = response.json()
        result["agent_id"] = agent_id
        result["oss_url"] = final_oss_url
        
        # 保存结果到本地
        save_local_result(group_id, task_name, result_content, result_file, final_oss_url)
        
        # 更新Agent配置
        update_agent_stats("task_completed")
        
        return result
        
    except requests.exceptions.RequestException as e:
        error_msg = f"交付失败: {e}"
        print(f"❌ {error_msg}")
        return {"error": error_msg, "agent_id": agent_id}

def generate_mock_oss_url(file_path: str = None, content: str = None) -> str:
    """
    生成模拟的OSS URL
    
    在实际系统中，这里应该调用真实的OSS上传接口
    当前版本模拟生成一个URL
    """
    # 生成唯一文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_id = str(uuid.uuid4())[:8]
    
    if file_path:
        # 基于文件扩展名
        ext = os.path.splitext(file_path)[1] if file_path else ".md"
        filename = f"result_{timestamp}_{random_id}{ext}"
    else:
        filename = f"result_{timestamp}_{random_id}.md"
    
    # 模拟OSS URL格式
    mock_oss_url = f"https://mock-oss.pinghaoxia.ai/results/{filename}"
    
    # 如果提供了内容，保存到本地模拟存储
    if content or file_path:
        save_to_mock_storage(filename, content, file_path)
    
    return mock_oss_url

def save_to_mock_storage(filename: str, content: str = None, file_path: str = None):
    """保存到模拟存储（实际应上传到OSS）"""
    storage_dir = f"{config.PATHS['WORKSPACE']}/mock_oss"
    os.makedirs(storage_dir, exist_ok=True)
    
    output_path = os.path.join(storage_dir, filename)
    
    if file_path and os.path.exists(file_path):
        # 复制文件
        import shutil
        shutil.copy2(file_path, output_path)
    elif content:
        # 保存内容
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"📁 结果已保存到模拟存储: {output_path}")

def save_local_result(
    group_id: str,
    task_name: str,
    content: str,
    file_path: str,
    oss_url: str
):
    """保存结果到本地日志"""
    result_dir = f"{config.PATHS['WORKSPACE']}/results/{group_id}"
    os.makedirs(result_dir, exist_ok=True)
    
    # 保存结果文件
    result_filename = f"{task_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    result_path = os.path.join(result_dir, result_filename)
    
    result_data = {
        "timestamp": datetime.now().isoformat(),
        "group_id": group_id,
        "task_name": task_name,
        "oss_url": oss_url,
        "agent_id": config.AGENT_ID,
        "content_preview": content[:500] + "..." if content and len(content) > 500 else content,
        "source_file": file_path
    }
    
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    # 记录到交付日志
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "group_id": group_id,
        "task_name": task_name,
        "oss_url": oss_url,
        "agent_id": config.AGENT_ID,
        "result_file": result_path
    }
    
    log_file = f"{config.PATHS['LOGS']}/task_completed.jsonl"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

def update_agent_stats(action: str):
    """更新Agent统计数据（从config导入）"""
    from scripts.config import config
    
    agent_config = config.load_agent_config()
    
    if action == "task_completed":
        agent_config["completed_tasks"] = agent_config.get("completed_tasks", 0) + 1
        # 增加信誉分
        agent_config["reputation"] = agent_config.get("reputation", 0) + 10
    
    config.save_agent_config(agent_config)

def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description="走私交付器 - 完成任务并提交结果")
    parser.add_argument("--group", "-g", type=str, required=True,
                       help="任务组ID")
    parser.add_argument("--task", "-t", type=str, required=True,
                       help="任务名称")
    parser.add_argument("--content", "-c", type=str,
                       help="结果内容（文本）")
    parser.add_argument("--file", "-f", type=str,
                       help="结果文件路径")
    parser.add_argument("--url", "-u", type=str,
                       help="直接提供OSS URL（如果已有）")
    parser.add_argument("--agent", "-a", type=str,
                       help="Agent ID（可选）")
    parser.add_argument("--json", "-j", action="store_true",
                       help="输出JSON格式")
    
    args = parser.parse_args()
    
    # 验证输入
    if not args.content and not args.file and not args.url:
        print("❌ 错误: 需要提供 --content、--file 或 --url 参数")
        return
    
    # 完成任务
    result = complete_task(
        group_id=args.group,
        task_name=args.task,
        result_content=args.content,
        result_file=args.file,
        oss_url=args.url,
        agent_id=args.agent
    )
    
    if args.json:
        # JSON输出模式
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # 友好显示模式
        if "error" in result:
            print(f"❌ 交付失败: {result['error']}")
        else:
            print("✅ 任务交付成功！")
            print(f"   组ID: {result.get('group_id', args.group)}")
            print(f"   任务: {result.get('task_name', args.task)}")
            print(f"   OSS URL: {result.get('oss_url')}")
            print(f"   消息: {result.get('msg', '感谢打工！')}")
            
            print(f"\n📊 下一步: 查看任务组进度")
            print(f"   python scripts/check_group.py --group {args.group}")

if __name__ == "__main__":
    main()