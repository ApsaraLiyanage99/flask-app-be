import pytest
from unittest.mock import AsyncMock
from app.services.pin_service import PinService


# check that a pin is successfully updated when it exists
@pytest.mark.asyncio
async def test_update_pin_success():
    mock_db_handler = AsyncMock()
    test_pin_id = 1

    update_data = {
        'title': 'Updated Title',
        'body': 'Updated body',
        'image_link': 'http://new.com/updated_image.jpg'
    }
    existing_pin = ('Old Title', 'Old body', 'http://old.com/old_image.jpg', 'author', 1)

    mock_db_handler.execute.side_effect = [existing_pin, True]

    response, status = await PinService.update_pin(test_pin_id, update_data, mock_db_handler)

    assert response == {'message': 'Pin updated successfully'}
    assert status == 200


# check that correct error response is returned when pin does not exist
@pytest.mark.asyncio
async def test_update_pin_not_found():
    mock_db_handler = AsyncMock()
    test_pin_id = 999 

    update_data = {
        'title': 'Updated Title',
        'body': 'Updated body',
        'image_link': 'http://new.com/updated_image.jpg'
    }

    mock_db_handler.execute.side_effect = [[]]

    response, status = await PinService.update_pin(test_pin_id, update_data, mock_db_handler)

    assert response == {'error': 'Pin not found'}
    assert status == 404


# check that correct error response is returned if there is an issue in updating
@pytest.mark.asyncio
async def test_update_pin_error_updating():

    mock_db_handler = AsyncMock()
    test_pin_id = 1
    update_data = {
        'title': 'Updated Title',
        'body': 'Updated body',
        'image_link': 'http://new.com/updated_image.jpg'
    }

    mock_db_handler.execute.side_effect = [('Old Title', 'Old body', 'http://old.com/old_image.jpg', 'author', 1), Exception("Database error")]

    response, status = await PinService.update_pin(test_pin_id, update_data, mock_db_handler)

    assert response == {'error': 'Error updating pin'}
    assert status == 500