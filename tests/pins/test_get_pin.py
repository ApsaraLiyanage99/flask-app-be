import pytest
from unittest.mock import AsyncMock, patch
from app.services.pin_service import PinService


# check that a pin is successfully retrieved
@pytest.mark.asyncio
async def test_get_pin_success():
    mock_db_handler = AsyncMock()
    test_pin_id = 1
    test_pin = ('Sample Pin', 'This is a sample pin.', 'http://example.com/image.jpg', 'author', 1)

    mock_db_handler.execute.return_value = [test_pin]

    response, status = await PinService.get_pin(test_pin_id, mock_db_handler)

    assert response == {'pin': test_pin}
    assert status == 200


# check that the correct error response is returned when the pin does not exist
@pytest.mark.asyncio
async def test_get_pin_not_found():
    mock_db_handler = AsyncMock()
    test_pin_id = 999  # this id is not in pins table

    mock_db_handler.execute.return_value = []

    response, status = await PinService.get_pin(test_pin_id, mock_db_handler)

    assert response == {'error': 'Pin not found'}
    assert status == 404


# check that an error response is returned if there is an issue fetching
# @pytest.mark.asyncio
# async def test_get_pin_error_fetching():
#     mock_db_handler = AsyncMock()
#     mock_db_handler.execute.side_effect = Exception("Database error")
#     test_pin_id = 1

#     response, status = await PinService.get_pin(test_pin_id, mock_db_handler)

#     assert response == {'error': 'Error fetching pin'}
#     assert status == 500