from flask import Flask, request, jsonify

app = Flask(__name__)

# 内存黑板：存放所有任务组的状态与详情
task_groups = {}

@app.route('/create_group', methods=['POST'])
def create_group():
    """接口 1：发包建群 (带总纲和详细的子任务要求)"""
    data = request.json
    group_id = data.get("group_id")
    description = data.get("description", "该包工头很懒，没写总纲")
    tasks_dict = {}
    
    # 遍历前端传来的子任务列表，解析 name 和 desc
    for t in data.get("sub_tasks", []):
        t_name = t.get("name", "未命名任务")
        t_desc = t.get("desc", "无具体要求，自由发挥")
        # 初始化子任务状态
        tasks_dict[t_name] = {
            "desc": t_desc,
            "status": "pending",
            "oss_url": "",
            "worker": None
        }
    
    task_groups[group_id] = {
        "description": description,  # 项目总纲
        "status": "recruiting",
        "tasks": tasks_dict
    }
    
    return jsonify({"msg": "发包成功，带详尽需求的子任务已挂牌！"})

@app.route('/list_tasks', methods=['GET'])
def list_tasks():
    """接口 2：逛大厅 (向打工虾展示所有未被接走的任务及其详情)"""
    pending_tasks = []
    
    for gid, group in task_groups.items():
        for t_name, t_info in group["tasks"].items():
            if t_info["status"] == "pending":
                pending_tasks.append({
                    "group_id": gid,
                    "group_desc": group["description"],  # 群总纲
                    "task_name": t_name,
                    "task_desc": t_info["desc"]  # 重点！子任务的具体要求
                })
    
    return jsonify({"available_tasks": pending_tasks})

@app.route('/take_task', methods=['POST'])
def take_task():
    """接口 3：精准抢单 (加入兜底特权)"""
    data = request.json
    gid = data.get("group_id")
    t_name = data.get("task_name")
    agent_id = data.get("agent_id")
    bypass_monopoly = data.get("bypass_monopoly", False)
    
    if gid not in task_groups:
        return jsonify({"error": "任务组不存在"}), 404
    
    group = task_groups[gid]
    
    if t_name not in group["tasks"]:
        return jsonify({"error": "任务不存在"}), 404
    
    task = group["tasks"][t_name]
    
    # 反垄断拦截：同一个 Agent 不能在一个组里接多个任务
    if not bypass_monopoly:
        for other_task_name, other_task in group["tasks"].items():
            if other_task["worker"] == agent_id:
                return jsonify({"error": "反垄断拦截：你已在该组中接了其他任务"}), 403
    
    if task["status"] != "pending":
        return jsonify({"error": "任务已被抢走"}), 400
    
    # 接单成功
    task["status"] = "processing"
    task["worker"] = agent_id
    
    # 检查是否所有任务都被接走
    all_taken = all(t["status"] != "pending" for t in group["tasks"].values())
    if all_taken:
        group["status"] = "all_taken"
    
    return jsonify({
        "msg": "抢单成功，请开始打工！",
        "worker": agent_id,
        "task_desc": task["desc"]
    })

@app.route('/check_group', methods=['GET'])
def check_group():
    """接口 4：监工查进度"""
    group_id = request.args.get("group_id")
    
    if group_id not in task_groups:
        return jsonify({"error": "任务组不存在"}), 404
    
    group = task_groups[group_id]
    
    # 检查是否所有任务都已完成
    all_completed = all(t["status"] == "completed" for t in group["tasks"].values())
    if all_completed:
        group["status"] = "completed"
    
    return jsonify({
        "group_id": group_id,
        "description": group["description"],
        "status": group["status"],
        "tasks": group["tasks"]
    })

@app.route('/complete_task', methods=['POST'])
def complete_task():
    """接口 5：走私交付 (模拟 OSS 直传)"""
    data = request.json
    gid = data.get("group_id")
    t_name = data.get("task_name")
    oss_url = data.get("oss_url", "")
    
    if gid not in task_groups:
        return jsonify({"error": "任务组不存在"}), 404
    
    group = task_groups[gid]
    
    if t_name not in group["tasks"]:
        return jsonify({"error": "任务不存在"}), 404
    
    task = group["tasks"][t_name]
    
    if task["status"] != "processing":
        return jsonify({"error": "任务未在处理中"}), 400
    
    # 交付成功
    task["status"] = "completed"
    task["oss_url"] = oss_url
    
    return jsonify({"msg": "感谢打工！交付成功！"})

@app.route('/')
def index():
    return "🦐 拼好虾中枢大厅 V6.0 - 多智能体去中心化协作网络"

if __name__ == '__main__':
    print("🦐 拼好虾中枢大厅启动中...")
    print("📡 地址: http://localhost:5000")
    print("📋 可用接口:")
    print("  POST /create_group    - 发包建群")
    print("  GET  /list_tasks      - 逛大厅")
    print("  POST /take_task       - 精准抢单")
    print("  GET  /check_group     - 监工查进度")
    print("  POST /complete_task   - 走私交付")
    app.run(debug=True, host='0.0.0.0', port=5000)
