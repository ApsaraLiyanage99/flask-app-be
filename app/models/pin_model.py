from dataclasses import dataclass
import logging

@dataclass
class Pin:
    title: str
    body: str
    image_link: str
    author: str

    @staticmethod
    async def create(db, title, body, image_link, author_name, user_id):
        query = """ INSERT INTO pins (title, body, image_link, author, author_id)
                    VALUES (%s, %s, %s, %s, %s) """
        await db.execute(query, title, body, image_link, author_name, user_id)
        return True

    @staticmethod
    async def get_all(db, title_filter=None, author_filter=None, order_by=None):
        query = "SELECT id, title, body, image_link, author, author_id FROM pins"
        if title_filter or author_filter:
            query += " WHERE"
            if title_filter:
                query += f" title LIKE '%{title_filter}%'"
            if title_filter and author_filter:
                query += " AND"
            if author_filter:
                query += f" author LIKE '%{author_filter}%'"
        if order_by:
            query += f" ORDER BY {order_by}"
        return await db.execute(query)
    
    @staticmethod
    async def get_one(db, pin_id):
        query = "SELECT title, body, image_link, author, author_id FROM pins WHERE id = %s"
        result = await db.execute(query, pin_id)
        return result[0] if result else None

    @staticmethod
    async def update(db, pin_id, title=None, body=None, image_link=None):
        fields = {}
        if title is not None: fields['title'] = title
        if body is not None: fields['body'] = body
        if image_link is not None: fields['image_link'] = image_link

        if not fields: return False

        clause = ', '.join([f"{key} = %s" for key in fields.keys()])
        values = list(fields.values())
        values.append(pin_id)

        query = f"UPDATE pins SET {clause} WHERE id = %s"

        try:
            await db.execute(query, *values)
            return True
        except Exception as e:
            logging.error(f"Error updating pin: {e}")
            return False

    @staticmethod
    async def delete(db, pin_id):
        query = "DELETE FROM pins WHERE id = %s"
        result = await db.execute(query, pin_id)
        return result is not None




