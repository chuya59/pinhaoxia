#!/usr/bin/env python3
"""
拼好虾 (PingHaoXia) - 全局配置模块
多智能体去中心化协作网络的核心配置
"""

import os
import json
from typing import Dict, Any, Optional

class PingHaoXiaConfig:
    """拼好虾系统全局配置"""
    
    # 中枢大厅 API 端点
    HUB_SERVER_URL = os.environ.get("PINGHAOXIA_HUB_URL", "http://localhost:5000")
    
    # API 端点路径
    ENDPOINTS = {
        "create_group": "/create_group",
        "list_tasks": "/list_tasks", 
        "take_task": "/take_task",
        "check_group": "/check_group",
        "complete_task": "/complete_task"
    }
    
    # 任务状态常量
    TASK_STATUS = {
        "PENDING": "pending",
        "PROCESSING": "processing", 
        "COMPLETED": "completed"
    }
    
    # 任务组状态常量
    GROUP_STATUS = {
        "RECRUITING": "recruiting",
        "ALL_TAKEN": "all_taken",
        "COMPLETED": "completed"
    }
    
    # 超时配置（秒）
    TIMEOUTS = {
        "API_REQUEST": 30,
        "FALLBACK_WAIT": 20,  # 兜底等待时间
        "TASK_PROCESSING": 300  # 任务处理超时
    }
    
    # 文件路径配置
    PATHS = {
        "WORKSPACE": os.path.expanduser("~/.pinghaoxia/workspace"),
        "LOGS": os.path.expanduser("~/.pinghaoxia/logs"),
        "CACHE": os.path.expanduser("~/.pinghaoxia/cache")
    }
    
    # 身份配置
    AGENT_ID = os.environ.get("PINGHAOXIA_AGENT_ID", "anonymous_agent")
    
    @classmethod
    def get_full_url(cls, endpoint: str) -> str:
        """获取完整的 API URL"""
        if endpoint not in cls.ENDPOINTS:
            raise ValueError(f"未知的端点: {endpoint}")
        return f"{cls.HUB_SERVER_URL}{cls.ENDPOINTS[endpoint]}"
    
    @classmethod
    def ensure_directories(cls):
        """确保必要的目录存在"""
        for path in cls.PATHS.values():
            os.makedirs(path, exist_ok=True)
    
    @classmethod
    def load_agent_config(cls) -> Dict[str, Any]:
        """加载 Agent 配置"""
        config_path = os.path.join(cls.PATHS["CACHE"], "agent_config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "agent_id": cls.AGENT_ID,
            "capabilities": [],
            "reputation": 0,
            "completed_tasks": 0
        }
    
    @classmethod
    def save_agent_config(cls, config: Dict[str, Any]):
        """保存 Agent 配置"""
        config_path = os.path.join(cls.PATHS["CACHE"], "agent_config.json")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

# 初始化配置
config = PingHaoXiaConfig()
config.ensure_directories()

if __name__ == "__main__":
    print("拼好虾配置模块")
    print(f"中枢大厅: {config.HUB_SERVER_URL}")
    print(f"Agent ID: {config.AGENT_ID}")
    print(f"工作空间: {config.PATHS['WORKSPACE']}")