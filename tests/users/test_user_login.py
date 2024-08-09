import pytest
from unittest.mock import AsyncMock, patch
from app.services.user_service import UserService
import bcrypt


# check that login fails when the user does not exist 
@pytest.mark.asyncio
async def test_login_user_user_not_exist():
    mock_db_handler = AsyncMock()
    mock_db_handler.execute.return_value = []

    data = {'username': 'nonexistentuser', 'password': 'somepassword'}
    response, status = await UserService.login_user(data, mock_db_handler)
    
    assert response == {"error": "User does not exist"}
    assert status == 401


# check that login fails if either the username or password is missing
@pytest.mark.asyncio
async def test_login_user_missing_fields():
    mock_db_handler = AsyncMock()
    
    test_cases = [
        ({'password': 'somepassword'}, {"error": "Missing username or password"}, 400),
        ({'username': 'someuser'}, {"error": "Missing username or password"}, 400),
        ({}, {"error": "Missing username or password"}, 400)
    ]
    
    for data, expected_response, expected_status in test_cases:
        response, status = await UserService.login_user(data, mock_db_handler)
        
        assert response == expected_response
        assert status == expected_status


# check that password is not match
@pytest.mark.asyncio
async def test_login_user_password_mismatch():
    mock_db_handler = AsyncMock()
    test_username = 'testuser'
    test_password = 'validpassword123'
    test_hashed_password = bcrypt.hashpw('differentpassword'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    mock_db_handler.execute.return_value = [(1, test_hashed_password)]

    data = {'username': test_username, 'password': test_password}
    response, status = await UserService.login_user(data, mock_db_handler)
    
    assert response == {"error": "Password mismatched"}
    assert status == 401


# check that login is successful when valid credentials are provided
# @pytest.mark.asyncio
# async def test_login_user_success():
#     mock_db_handler = AsyncMock()
#     test_username = 'testuser'
#     test_password = 'validpassword123'
#     test_hashed_password = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#     test_user_id = 1
    
#     # Mock database return value
#     mock_db_handler.execute.return_value = [(test_user_id, test_hashed_password)]
    
#     # Mock token generation
#     with patch('app.models.user_model.User.generate_token', return_value='mock_token') as mock_generate_token:
#         mock_generate_token.side_effect = ['mock_access_token', 'mock_refresh_token']

#          # Mock token storage - Simulate successful storage
#         mock_db_handler.execute.side_effect = lambda query, *args: None 

#         data = {'username': test_username, 'password': test_password}
#         response, status = await UserService.login_user(data, mock_db_handler)

#         assert response == {
#             'access_token': 'mock_access_token',
#             'refresh_token': 'mock_refresh_token'
#         }
#         assert status == 200


# check that the login fails if storing the refresh token fails
@pytest.mark.asyncio
async def test_login_user_token_storage_failure():
    mock_db_handler = AsyncMock()
    test_username = 'testuser'
    test_password = 'validpassword123'
    test_hashed_password = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    test_user_id = 1
    
    mock_db_handler.execute.return_value = [(test_user_id, test_hashed_password)]
    
    # Mock token generation - define a sequence of return values by side_effect
    with patch('app.models.user_model.User.generate_token', side_effect=['mock_access_token', 'mock_refresh_token']):
        # Simulate token storage failure
        mock_db_handler.execute.side_effect = Exception("Database error")
        
        data = {'username': test_username, 'password': test_password}
        response, status = await UserService.login_user(data, mock_db_handler)
        
        assert response == {"error": "Internal Server Error"}
        assert status == 500

