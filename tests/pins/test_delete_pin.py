import pytest
from unittest.mock import AsyncMock
from app.services.pin_service import PinService


# check that a pin is successfully deleted
@pytest.mark.asyncio
async def test_delete_pin_success():

    mock_db_handler = AsyncMock()
    test_pin_id = 1
    existing_pin = ('Title', 'Body', 'http://img.com/image.jpg', 'author', 1)

    mock_db_handler.execute.side_effect = [existing_pin, True]

    response, status = await PinService.delete_pin(test_pin_id, mock_db_handler)

    assert response == {'message': 'Pin deleted successfully'}
    assert status == 200


# check that the correct error response is returned when pin is not exist.
@pytest.mark.asyncio
async def test_delete_pin_not_found():
    mock_db_handler = AsyncMock()
    test_pin_id = 999 

    mock_db_handler.execute.side_effect = [[]]

    response, status = await PinService.delete_pin(test_pin_id, mock_db_handler)

    assert response == {'error': 'Pin not found'}
    assert status == 404


# check that correct error response is returned if there is an issue in deleting
# @pytest.mark.asyncio
# async def test_delete_pin_error_deleting():
#     mock_db_handler = AsyncMock()
#     test_pin_id = 1

#     existing_pin = ('Title', 'Body', 'http://img.com/image.jpg', 'author', 1)

#     mock_db_handler.execute.side_effect = [existing_pin, Exception("Database error")]

#     response, status = await PinService.delete_pin(test_pin_id, mock_db_handler)

#     assert response == {'error': 'Error deleting pin'}
#     assert status == 500