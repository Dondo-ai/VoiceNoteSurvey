from flask import Flask
import db,os
from dotenv import load_dotenv

#from app.blueprints.webhook import webhook_bp
# from app.extensions import db, migrate

def create_app(config_class=None):
    app = Flask(__name__)
    #app.config.from_object(config_class)
    # Load environment variables from .env file
    load_dotenv()

    # Load configuration from environment variables
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
    app.config['TWILIO_ID'] = os.getenv('TWILIO_ID')
    app.config['TWILIO_TOKEN'] = os.getenv('TWILIO_TOKEN')
    app.config['WHATSAPP_NUMBER'] = os.getenv('WHATSAPP_NUMBER')

    # Initialize extensions
    db.init_app(app)
    # Initialize extensions
    # db.init_app(app)
    # migrate.init_app(app, db)

    # Register Blueprints
    from app.blueprints.webhook import webhook_bp
    app.register_blueprint(webhook_bp, url_prefix='/webhook')

    from app.blueprints.home import home_bp
    app.register_blueprint(home_bp, url_prefix='/')

    return app
