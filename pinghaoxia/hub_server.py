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
 "description": description, # 项目总纲
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
 "group_desc": group["description"], # 群总纲
 "task_name": t_name,
 "task_desc": t_info["desc"] # 重点！子任务的具体要求
 })
 
 return jsonify({"available_tasks": pending_tasks})

@app.route('/take_task', methods=['POST'])
def take_task():
 """接口 3：精准抢单 (加入兜底特权)"""
 data = request.json
 gid = data.get("group_id")
 t_name = data.get("task_name")
 agent_id = data.get("agent_id")
 
 # 🌟 核心：包工头超时兜底专用的特权开关
 bypass_monopoly = data.get("bypass_monopoly", False)
 
 if not agent_id:
 return jsonify({"error": "拒绝访问：必须提供工牌号 agent_id！"}), 403
 
 if gid not in task_groups or t_name not in task_groups[gid]["tasks"]:
 return jsonify({"error": "找不到该任务"}), 404
 
 # 🛡️ 反垄断拦截：如果没开特权，严格审查！
 if not bypass_monopoly:
 for existing_task, info in task_groups[gid]["tasks"].items():
 if info.get("worker") == agent_id:
 return jsonify({
 "error": f"反垄断拦截：{agent_id} 贪多嚼不烂！你已经拿了 '{existing_task}' 任务，把机会留给其他虾！"
 }), 403
 
 if task_groups[gid]["tasks"][t_name]["status"] == "pending":
 task_groups[gid]["tasks"][t_name]["status"] = "processing"
 task_groups[gid]["tasks"][t_name]["worker"] = agent_id
 return jsonify({
 "msg": "接单成功",
 "group_id": gid,
 "task_name": t_name,
 "worker": agent_id
 })
 
 return jsonify({"error": "手慢了，该任务已被抢走"}), 400

@app.route('/check_group', methods=['GET'])
def check_group():
 """接口 4：包工头监工 (查询整个任务组的进度)"""
 group_id = request.args.get("group_id")
 
 if group_id not in task_groups:
 return jsonify({"error": "404 Not Found"}), 404
 
 group = task_groups[group_id]
 
 # 判断是否全部接单，或者全部完工
 all_taken = all(t["status"] != "pending" for t in group["tasks"].values())
 all_completed = all(t["status"] == "completed" for t in group["tasks"].values())
 
 # 状态机流转
 if all_completed:
 group["status"] = "completed"
 elif all_taken:
 group["status"] = "all_taken"
 
 return jsonify(group)

@app.route('/complete_task', methods=['POST'])
def complete_task():
 """接口 5：走私交付 (记录干完活的 OSS 链接)"""
 data = request.json
 gid = data.get("group_id")
 t_name = data.get("task_name")
 oss_url = data.get("oss_url")
 
 if gid in task_groups and t_name in task_groups[gid]["tasks"]:
 task_groups[gid]["tasks"][t_name].update({
 "status": "completed",
 "oss_url": oss_url
 })
 return jsonify({"msg": "交付成功，感谢打工！"})
 
 return jsonify({"error": "交付失败，找不到该任务"}), 400

if __name__ == '__main__':
 # 监听所有网卡，5000 端口
 app.run(host='0.0.0.0', port=5000)