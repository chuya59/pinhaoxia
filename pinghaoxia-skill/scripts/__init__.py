"""
拼好虾 (PingHaoXia) - 多智能体去中心化协作网络
脚本工具包
"""

__version__ = "6.0.0"
__author__ = "Lady W & 贾维斯"
__description__ = "为 AI Agent 打造的去中心化自由职业者市场 (Freelancer DAO)"

# 导出主要功能
from .config import PingHaoXiaConfig, config

__all__ = [
    "PingHaoXiaConfig",
    "config",
]