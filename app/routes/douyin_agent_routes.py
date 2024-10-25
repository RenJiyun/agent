from flask import Blueprint, jsonify, request
from app.services.douyin_agent_service import DouyinAgentService

douyin_agent_routes = Blueprint('douyin_agent_routes', __name__, url_prefix="/douyin/agents/")


@douyin_agent_routes.route('create', methods=['POST'])
def create():
    return jsonify(DouyinAgentService.create()), 200

@douyin_agent_routes.route('get_agent_info', methods=['GET'])
def get_agent_info():
    agent_id = request.json.get('agent_id')
    return jsonify(DouyinAgentService.get_agent_info(agent_id)), 200

@douyin_agent_routes.route('login', methods=['POST'])
def login():
    agent_id = request.json.get('agent_id')
    if agent_id is None:
        raise ValueError("agent_id is required")
    timeout = request.json.get('timeout', 120)
    return jsonify(DouyinAgentService.login(agent_id, timeout)), 200

@douyin_agent_routes.route('enter_live_room', methods=['POST'])
def enter_live_room():
    agent_id = request.json.get('agent_id')
    if agent_id is None:
        raise ValueError("agent_id is required")
    live_room_id = request.json.get('live_room_id')
    if live_room_id is None:
        raise ValueError("live_room_id is required")
    timeout = request.json.get('timeout', 120)
    return jsonify(DouyinAgentService.enter_live_room(agent_id, live_room_id, timeout)), 200

@douyin_agent_routes.route('leave_live_room', methods=['POST'])
def leave_live_room():
    agent_id = request.json.get('agent_id')
    if agent_id is None:
        raise ValueError("agent_id is required")
    return jsonify(DouyinAgentService.leave_live_room(agent_id)), 200


# 以下两个方法用来辅助调试获得登录状态
@douyin_agent_routes.route('debug1', methods=['GET'])
def debug1():
    DouyinAgentService.debug1()
    return jsonify({"status": 0, "msg": "success"}), 200

@douyin_agent_routes.route('debug2', methods=['GET'])
def debug2():
    DouyinAgentService.debug2()
    return jsonify({"status": 0, "msg": "success"}), 200

@douyin_agent_routes.route('debug3', methods=['GET'])
def debug3():
    DouyinAgentService.debug3()
    return jsonify({"status": 0, "msg": "success"}), 200
