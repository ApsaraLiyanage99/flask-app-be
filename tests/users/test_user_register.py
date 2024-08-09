import pytest
from unittest.mock import AsyncMock, patch
from app.services.user_service import UserService


# check that the registration fails if the username and password are the same
@pytest.mark.asyncio
async def test_register_user_username_password_same():
    
    mock_db_handler = AsyncMock()

    data = {"username": "testuser", "password": "testuser"}

    response, status = await UserService.register_user(data, mock_db_handler)

    assert response == {"error": "Username and password cannot be the same"}
    assert status == 400


# check that registration fails if the password is not alphanumeric
@pytest.mark.asyncio
async def test_register_user_password_not_alphanumeric():

    mock_db_handler = AsyncMock()

    data = {"username": "testuser", "password": "pass@123"}

    response, status = await UserService.register_user(data, mock_db_handler)

    assert response == {"error": "Password must be alphanumeric"}
    assert status == 400


# check that user is successfully registered when valid data is provided
@pytest.mark.asyncio
async def test_register_user_success():
    # Arrange
    mock_db_handler = AsyncMock()
    mock_db_handler.execute = AsyncMock(return_value=[])

    # Mock the UserService.create_user method to return True
    with patch('app.services.user_service.User.create_user', new=AsyncMock(return_value=True)):
        data = {"username": "testuser", "password": "validpass123"}
        
        # Act
        response, status = await UserService.register_user(data, mock_db_handler)
        
        # Assert
        assert response == {"message": "User registered successfully"}
        assert status == 201


# check that the registration fails if the user already exists
@pytest.mark.asyncio
async def test_register_user_already_exists():
    mock_db_handler = AsyncMock()
    mock_db_handler.execute = AsyncMock(return_value=[{'id': 1, 'password': 'hashed'}])

    data = {"username": "existinguser", "password": "valid123"}

    # Act
    response, status = await UserService.register_user(data, mock_db_handler)

    # Assert
    assert response == {"error": "User already exists"}
    assert status == 400

