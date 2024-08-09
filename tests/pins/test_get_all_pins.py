import pytest
from unittest.mock import AsyncMock, patch
from app.services.pin_service import PinService


# check that all pins are successfully retrieved when no filters are applied
@pytest.mark.asyncio
async def test_get_all_pins_success_no_filters():

    mock_db_handler = AsyncMock()
    test_pins = [
        (1, 'Sample Pin 1', 'This is a sample pin.', 'http://example.com/image1.jpg', 'author1', 1),
        (2, 'Sample Pin 2', 'This is another sample pin.', 'http://example.com/image2.jpg', 'author2', 2)
    ]

    mock_db_handler.execute.return_value = test_pins

    filters = {
        'title_filter': None,
        'author_filter': None,
        'order_by': None
    }

    response, status = await PinService.get_all_pins(filters, mock_db_handler)

    assert response == {'pins': test_pins}
    assert status == 200


# check that pins are filtered correctly by the title
@pytest.mark.asyncio
async def test_get_all_pins_title_filter():
    mock_db_handler = AsyncMock()
    test_pins = [
        (1, 'Sample Pin 1', 'This is a sample pin.', 'http://example.com/image1.jpg', 'author1', 1)
    ]

    mock_db_handler.execute.return_value = test_pins

    filters = {
        'title_filter': 'Sample Pin 1',
        'author_filter': None,
        'order_by': None
    }

    response, status = await PinService.get_all_pins(filters, mock_db_handler)

    assert response == {'pins': test_pins}
    assert status == 200


# check that pins are filtered correctly by the author
@pytest.mark.asyncio
async def test_get_all_pins_author_filter():
    mock_db_handler = AsyncMock()
    test_pins = [
        (1, 'Sample Pin 1', 'This is a sample pin.', 'http://example.com/image1.jpg', 'author1', 1)
    ]

    mock_db_handler.execute.return_value = test_pins

    filters = {
        'title_filter': None,
        'author_filter': 'author1',
        'order_by': None
    }

    response, status = await PinService.get_all_pins(filters, mock_db_handler)

    assert response == {'pins': test_pins}
    assert status == 200


# check that pins are ordered correctly
@pytest.mark.asyncio
async def test_get_all_pins_order_by():
    mock_db_handler = AsyncMock()
    test_pins = [
        (2, 'Sample Pin 2', 'This is another sample pin.', 'http://example.com/image2.jpg', 'author2', 2),
        (1, 'Sample Pin 1', 'This is a sample pin.', 'http://example.com/image1.jpg', 'author1', 1)
    ]

    mock_db_handler.execute.return_value = test_pins

    filters = {
        'title_filter': None,
        'author_filter': None,
        'order_by': 'ASC'
    }

    response, status = await PinService.get_all_pins(filters, mock_db_handler)

    assert response == {'pins': test_pins}
    assert status == 200


# check that an error response is returned if there is an issue in fetching 
@pytest.mark.asyncio
async def test_get_all_pins_error_fetching():
    mock_db_handler = AsyncMock()
    mock_db_handler.execute.side_effect = Exception("Database error")

    filters = {
        'title_filter': None,
        'author_filter': None,
        'order_by': None
    }

    response, status = await PinService.get_all_pins(filters, mock_db_handler)

    assert response == {"error": "Error fetching pins"}
    assert status == 500