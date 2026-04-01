#!/usr/bin/env python3
"""
complete_task.py - 走私交付器（工业级版本）
完成任务并提交结果，使用独立的OSS上传中间件
"""

import argparse
import requests
import json
import os
import sys

# 添加父目录到路径以便导入 config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import HUB_URL
except ImportError:
    # 如果config.py不存在，使用默认值
    HUB_URL = "http://localhost:5000"

# 引入刚刚独立出来的存储中间件
try:
    import oss_uploader
except ImportError:
    print(json.dumps({"error": "缺少 oss_uploader 模块，请确保 scripts/oss_uploader.py 存在"}, ensure_ascii=False))
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="走私交付任务")
    parser.add_argument("--group_id", required=True, help="任务组ID")
    parser.add_argument("--task_name", required=True, help="子任务名")
    parser.add_argument("--local_file", required=True, help="本地生成的Markdown文件路径")
    args = parser.parse_args()

    # 1. 容错拦截：如果 AI 偷懒只敲了命令没建文件，系统帮它兜底建一个
    if not os.path.exists(args.local_file):
        try:
            # 自动提取目录并创建
            os.makedirs(os.path.dirname(os.path.abspath(args.local_file)), exist_ok=True)
            with open(args.local_file, "w", encoding="utf-8") as f:
                f.write(f"# {args.task_name} 报告\n⚠️ AI 节点未生成物理文件，触发系统强制兜底。")
            print(json.dumps({"warning": f"创建兜底文件: {args.local_file}"}, ensure_ascii=False))
        except Exception as e:
            print(json.dumps({"error": f"创建兜底文件失败: {str(e)}"}, ensure_ascii=False))
            return

    # 2. 调用独立的 OSS 模块上传文件
    remote_name = f"{args.group_id}_{args.task_name}_remote.md"
    try:
        # 这里它会自动根据你的环境变量决定是真传还是 mock
        oss_url = oss_uploader.upload_file(args.local_file, remote_name)
        print(json.dumps({"info": f"OSS上传成功，模式: {oss_uploader.OSS_MODE}"}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": f"OSS 上传层失败: {str(e)}"}, ensure_ascii=False))
        return

    # 3. 向云端大厅交差
    payload = {
        "group_id": args.group_id, 
        "task_name": args.task_name, 
        "oss_url": oss_url
    }
    try:
        resp = requests.post(f"{HUB_URL}/complete_task", json=payload, timeout=5)
        print(json.dumps({
            "upload_status": "success", 
            "oss_mode": oss_uploader.OSS_MODE, 
            "oss_url": oss_url, 
            "hub_response": resp.json()
        }, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": f"大厅交付接口失败: {str(e)}"}, ensure_ascii=False))

if __name__ == "__main__":
    main()