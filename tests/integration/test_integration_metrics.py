import pytest
import re
import time
import os
from unittest.mock import Mock, patch
from app.app import app

# Configura ambiente de teste para usar Redis local
os.environ['APP_ENV'] = 'testing'
os.environ['REDIS_HOST'] = 'localhost'

@pytest.fixture(autouse=True)
def mock_redis():
    """Mock básico do Redis para testes que não dependem dele diretamente"""
    with patch('app.redis_connection.redis_client') as mock_redis:
        mock_redis.get = Mock(return_value=None)
        mock_redis.set = Mock(return_value=True)
        yield mock_redis

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

# ... (o restante do código de teste permanece igual) ...