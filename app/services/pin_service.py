from app.models.pin_model import Pin
from app.models.user_model import User
import logging


class PinService:
    @staticmethod
    async def create_pin(data, current_user_id, db_handler):
        title = data.get('title')
        body = data.get('body')
        image_link = data.get('image_link', '')

        if not title or not body:
            return {"error": "Missing required fields"}, 400

        author_name = await User.get_name_by_userid(db_handler, current_user_id)
        if author_name is None:
            return {"error": "User does not exist"}, 401

        success = await Pin.create(db_handler, title, body, image_link, author_name, current_user_id)
        if not success:
            return {"error": "Error creating pin"}, 500

        return {"message": "Pin created successfully"}, 201

    @staticmethod
    async def get_all_pins(filters, db_handler):
        try:
            title_filter = filters.get('title_filter')
            author_filter = filters.get('author_filter')
            order_by = filters.get('order_by')

            pins = await Pin.get_all(db_handler, title_filter, author_filter, order_by)
            return {"pins": pins}, 200
        except Exception as e:
            logging.error(f"Error fetching pins: {e}")
            return {"error": "Error fetching pins"}, 500

    @staticmethod
    async def get_pin(pin_id, db_handler):
        pin = await Pin.get_one(db_handler, pin_id)
        if pin:
            return {"pin": pin}, 200
        else:
            return {"error": "Pin not found"}, 404

    @staticmethod
    async def update_pin(pin_id, data, db_handler):
        title = data.get('title')
        body = data.get('body')
        image_link = data.get('image_link')

        pin = await Pin.get_one(db_handler, pin_id)
        if pin is None:
            return {"error": "Pin not found"}, 404

        success = await Pin.update(db_handler, pin_id, title=title, body=body, image_link=image_link)
        if not success:
            return {"error": "Error updating pin"}, 500

        return {"message": "Pin updated successfully"}, 200

    @staticmethod
    async def delete_pin(pin_id, db_handler):
        pin = await Pin.get_one(db_handler, pin_id)
        if pin is None:
            return {"error": "Pin not found"}, 404

        success = await Pin.delete(db_handler, pin_id)
        if not success:
            return {"error": "Error deleting pin"}, 500

        return {"message": "Pin deleted successfully"}, 200
