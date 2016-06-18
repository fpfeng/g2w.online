import os
from app import app
from app import views
from config import configs

if __name__ == '__main__':
    app.config.from_object(configs[os.environ.get('g2pconf', 'test')])
    app.run()
