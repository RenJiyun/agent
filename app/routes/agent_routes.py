from flask import Blueprint, jsonify, request
from app.services.agent_service import AgentService

agent_routes = Blueprint('agent_routes', __name__, url_prefix="/douyin/agents/deprecated")

# 获取所有代理
@agent_routes.route('list', methods=['GET'])
def list():
    result = AgentService.list()
    return jsonify(result), 200

# 获取单个代理
@agent_routes.route('detail', methods=['GET'])
def detail():
    agent_id = request.json.get('agent_id')
    result = AgentService.get_by_id(agent_id)
    return jsonify(result), 200

# 创建代理
@agent_routes.route('create', methods=['POST'])
def create():
    result = AgentService.create()
    return jsonify(result), 200

# 删除代理
@agent_routes.route('delete', methods=['POST'])
def delete():
    agent_id = request.json.get('agent_id')
    result = AgentService.delete(agent_id)
    return jsonify(result), 200

# 进入直播间
@agent_routes.route('enter_living_room', methods=['POST'])
def enter_living_room():
    agent_id = request.json.get('agent_id')
    room_id = request.json.get('room_id')
    result = AgentService.enter_living_room(agent_id, room_id)
    return jsonify(result), 200

# 离开直播间
@agent_routes.route('leave_living_room', methods=['POST'])
def leave_living_room():
    agent_id = request.json.get('agent_id')
    result = AgentService.leave_living_room(agent_id)
    return jsonify(result), 200

# 发送弹幕
@agent_routes.route('agents/<int:agent_id>/send_danmu', methods=['POST'])
def send_danmu(agent_id):
    content = request.json.get('content')
    result = AgentService.send_danmu(agent_id, content)
    return jsonify(result), 200

# 发送礼物
@agent_routes.route('agents/<int:agent_id>/send_gift', methods=['POST'])
def send_gift(agent_id):
    name = request.json.get('name')
    count = request.json.get('count')
    result = AgentService.send_gift(agent_id, name, count)
    return jsonify(result), 200

# 点赞
@agent_routes.route('agents/<int:agent_id>/like', methods=['POST'])
def like(agent_id):
    frequency = request.json.get('frequency')
    duration = request.json.get('duration')
    result = AgentService.like(agent_id, frequency, duration)
    return jsonify(result), 200
