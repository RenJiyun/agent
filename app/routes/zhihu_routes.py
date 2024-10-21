from flask import Blueprint, jsonify, request
from app.services.zhihu_service import ZhihuService

zhihu_routes = Blueprint('zhihu_routes', __name__, url_prefix='/zhihu')

# 登录
@zhihu_routes.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    result = ZhihuService.login(username, timeout=120)
    return jsonify(result), 200

# 登出
@zhihu_routes.route('/logout', methods=['POST'])
def logout():
    username = request.json.get('username')
    result = ZhihuService.logout(username)
    return jsonify(result), 200

# 获取用户信息
@zhihu_routes.route('/get_user_info', methods=['GET'])
def get_user_info():
    username = request.json.get('username')
    result = ZhihuService.get_user_info(username, timeout=10)
    return jsonify(result), 200
    
# 网络调试
@zhihu_routes.route('/debug', methods=['GET'])
def debug():
    result = {"status": 1, "msg": "success"}
    return jsonify(result), 200

