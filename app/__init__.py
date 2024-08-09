from flask import Flask
from app.routes.pin_routes import pin_bp
from app.routes.user_routes import user_bp
from app.core.database import AsyncDBHandler
from app.core.error_handler import init_error_handlers
from app.core.scheduler import start_scheduler
from flask_cors import CORS

async def create_app():
    app = Flask(__name__)
    CORS(app)

    db_handler = AsyncDBHandler()
    await db_handler.connect()

    app.register_blueprint(pin_bp)
    app.register_blueprint(user_bp)
    init_error_handlers(app)
    start_scheduler()

    return app
