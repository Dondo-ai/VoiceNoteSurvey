from app import create_app
from config import config
import os
import db


config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config['default'])
app.config.from_object(config['default'])

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
