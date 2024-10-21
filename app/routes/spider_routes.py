from flask import Blueprint, jsonify, request
from app.services.spider_service import SpiderService

spider_routes = Blueprint('spider_routes', __name__)

# 获取所有爬虫
@spider_routes.route('/spiders', methods=['GET'])
def get_spiders():
    result = SpiderService.get_all()
    return jsonify(result), 200

# 获取单个爬虫
@spider_routes.route('/spiders/<int:spider_id>', methods=['GET'])
def get_spider(spider_id):
    result = SpiderService.get_by_id(spider_id)
    return jsonify(result), 200

# 创建爬虫
@spider_routes.route('/spiders', methods=['POST'])
def create_spider():
    name = request.json.get('name')
    keywords = request.json.get('keywords')
    result = SpiderService.create(name, keywords)
    return jsonify(result), 200

