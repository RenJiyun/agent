from flask import Blueprint, jsonify, request
from app.services.douyin_agent_service import DouyinAgentService

douyin_agent_routes = Blueprint('douyin_agent_routes', __name__, url_prefix="/douyin/agents/")


@douyin_agent_routes.route('create', methods=['POST'])
def create():
    return jsonify(DouyinAgentService.create()), 200

@douyin_agent_routes.route('login', methods=['POST'])
def login():
    return jsonify(DouyinAgentService.login()), 200


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
