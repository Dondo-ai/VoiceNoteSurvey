from flask import Blueprint

webhook_bp = Blueprint('webhook', __name__)

from app.blueprints.webhook import routes