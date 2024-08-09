from flask import Blueprint, request, g
from app.core.middleware import authenticator
from app.core.database import AsyncDBHandler
from app.services.pin_service import PinService

pin_bp = Blueprint('pin', __name__, url_prefix='/pin')

db_handler = AsyncDBHandler()

@pin_bp.route('/create', methods=['POST'])
@authenticator()
async def create_pin():
    data = request.get_json()
    response, status = await PinService.create_pin(data, g.current_user_id, db_handler)
    return response, status


@pin_bp.route('/get-all', methods=['GET'])
@authenticator()
async def get_all_pins():
    filters = {
        "title_filter": request.args.get('title_filter'),
        "author_filter": request.args.get('author_filter'),
        "order_by": request.args.get('order_by')
    }
    response, status = await PinService.get_all_pins(filters, db_handler)
    return response, status


@pin_bp.route('/get', methods=['GET'])
@authenticator()
async def get_pin():
    pin_id = request.args['pin_id']
    response, status = await PinService.get_pin(pin_id, db_handler)
    return response, status


@pin_bp.route('/update', methods=['PUT'])
@authenticator()
async def update_pin():
    pin_id = request.args['pin_id']
    data = request.get_json()
    response, status = await PinService.update_pin(pin_id, data, db_handler)
    return response, status


@pin_bp.route('/delete', methods=['DELETE'])
@authenticator()
async def delete_pin():
    pin_id = request.args['pin_id']
    response, status = await PinService.delete_pin(pin_id, db_handler)
    return response, status
