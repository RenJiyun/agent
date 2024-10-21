from flask import Flask
from app.routes.agent_routes import agent_routes
from app.routes.spider_routes import spider_routes

app = Flask(__name__)
app.register_blueprint(agent_routes)
app.register_blueprint(spider_routes)