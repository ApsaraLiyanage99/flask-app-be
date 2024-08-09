import pytest
from unittest.mock import AsyncMock, patch
from app.services.pin_service import PinService
from app.models.user_model import User
from app.models.pin_model import Pin


# check that a pin is successfully created when valid data is provided and the user exists
@pytest.mark.asyncio
async def test_create_pin_success():
    mock_db_handler = AsyncMock()
    test_data = {
        'title': 'Sample Pin',
        'body': 'This is a sample pin.',
        'image_link': 'http://example.com/image.jpg'
    }
    test_user_id = 1
    test_author_name = 'testuser'

    mock_db_handler.execute.return_value = [test_author_name]

    with patch('app.models.pin_model.Pin.create', return_value=True) as mock_create:
        response, status = await PinService.create_pin(test_data, test_user_id, mock_db_handler)

        assert response == {'message': 'Pin created successfully'}
        assert status == 201


# check that fails if required fields missing.
@pytest.mark.asyncio
async def test_create_pin_missing_fields():
    mock_db_handler = AsyncMock()
    test_data = {
        'title': 'Sample Pin' 
    }
    test_user_id = 1

    response, status = await PinService.create_pin(test_data, test_user_id, mock_db_handler)

    assert response == {"error": "Missing required fields"}
    assert status == 400


# check that fails if the user does not exist
@pytest.mark.asyncio
async def test_create_pin_user_does_not_exist():
    mock_db_handler = AsyncMock()
    test_data = {
        'title': 'Sample Pin',
        'body': 'This is a sample pin.'
    }
    test_user_id = 1

    # simulate user not existing
    mock_db_handler.execute.return_value = []

    response, status = await PinService.create_pin(test_data, test_user_id, mock_db_handler)

    assert response == {"error": "User does not exist"}
    assert status == 401


# check that fails if there is an error in the process
@pytest.mark.asyncio
async def test_create_pin_error_creating_pin():
    mock_db_handler = AsyncMock()
    test_data = {
        'title': 'Sample Pin',
        'body': 'This is a sample pin.'
    }
    test_user_id = 1
    test_author_name = 'testuser'

    mock_db_handler.execute.return_value = [test_author_name]

    with patch('app.models.pin_model.Pin.create', return_value=False) as mock_create:
        response, status = await PinService.create_pin(test_data, test_user_id, mock_db_handler)

        assert response == {"error": "Error creating pin"}
        assert status == 500
