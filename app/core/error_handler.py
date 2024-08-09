def handle_not_found_error(e):
    return {"error": "Resource not found"}, 404


def handle_internal_server_error(e):
    return {"error": "Internal server error"}, 500


def handle_database_error(e):
    return {"error": str(e)}, 500


def init_error_handlers(app):
    app.register_error_handler(404, handle_not_found_error)
    app.register_error_handler(500, handle_internal_server_error)
    app.register_error_handler(500, handle_database_error)
