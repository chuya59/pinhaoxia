import os
import shutil
import json
import argparse

# ================= 配置读取区 =================
# 通过环境变量控制行为，默认走 "mock" 模拟路线
OSS_MODE = os.getenv("PINGHAOXIA_OSS_MODE", "mock").lower()  # 可选: 'mock', 's3'

# 如果是真实 OSS，需要读取以下凭证
OSS_BUCKET = os.getenv("PINGHAOXIA_OSS_BUCKET", "my-shrimp-bucket")
OSS_AK = os.getenv("PINGHAOXIA_OSS_AK", "")
OSS_SK = os.getenv("PINGHAOXIA_OSS_SK", "")
OSS_ENDPOINT = os.getenv("PINGHAOXIA_OSS_ENDPOINT", "")

def upload_to_mock(local_file, remote_name):
    """【模拟模式】将文件复制到本地专门的 fake_oss_bucket 目录中"""
    # 找到 skills/pinhaoxia 根目录，在里面建个假 bucket
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    oss_dir = os.path.join(base_dir, "fake_oss_bucket")
    os.makedirs(oss_dir, exist_ok=True)
    
    target_path = os.path.join(oss_dir, remote_name)
    shutil.copy(local_file, target_path)
    
    # 返回 file:// 协议的伪造云端链接
    return f"file://{target_path}"

def upload_to_s3(local_file, remote_name):
    """【真实模式】使用 AWS S3 / MinIO 或兼容 S3 协议的真实云存储"""
    try:
        import boto3
    except ImportError:
        raise ImportError("检测到配置为 S3 模式，但缺少 boto3 库。请执行: pip install boto3")

    try:
        s3 = boto3.client('s3', 
                         aws_access_key_id=OSS_AK, 
                         aws_secret_access_key=OSS_SK,
                         endpoint_url=OSS_ENDPOINT if OSS_ENDPOINT else None)
        
        # 执行真实物理上传
        s3.upload_file(local_file, OSS_BUCKET, remote_name)
        
        # 拼接下载链接 (假设 Bucket 策略为公共读)
        if OSS_ENDPOINT:
            url = f"{OSS_ENDPOINT}/{OSS_BUCKET}/{remote_name}"
        else:
            url = f"https://{OSS_BUCKET}.s3.amazonaws.com/{remote_name}"
        return url
    except Exception as e:
        raise Exception(f"云端 S3 上传崩溃: {str(e)}")

def upload_file(local_file, remote_name):
    """统一上传路由入口"""
    if not os.path.exists(local_file):
        raise FileNotFoundError(f"本地待上传文件不存在: {local_file}")
    
    if OSS_MODE == "s3":
        return upload_to_s3(local_file, remote_name)
    else:
        # 默认全部走 Mock 兜底
        return upload_to_mock(local_file, remote_name)

if __name__ == "__main__":
    # 提供 CLI 测试入口
    parser = argparse.ArgumentParser(description="拼好虾 OSS 上传中间件 (支持 Mock 与 S3)")
    parser.add_argument("--local_file", required=True, help="本地文件路径")
    parser.add_argument("--remote_name", required=True, help="云端保存的文件名")
    args = parser.parse_args()
    
    try:
        result_url = upload_file(args.local_file, args.remote_name)
        print(json.dumps({"status": "success", "mode": OSS_MODE, "url": result_url}, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))