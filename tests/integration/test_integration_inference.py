import os
import sys

# Adiciona o caminho absoluto para a pasta api-service (subindo dois níveis)
folderpath = os.path.join(os.path.dirname(__file__), "../../api-service")
sys.path.insert(0, os.path.abspath(folderpath))

import pytest
from unittest.mock import patch

# Import corrigido:
from app.inference_service import app as inference_app

@pytest.fixture
def client():
    with inference_app.test_client() as client:
        yield client

def test_generate_success(client):
    with patch("app.inference_service.generator.generate_story", return_value="Era uma vez...") as mock_generate:
        payload = {
            "text": "Once upon a time",
            "size": 50,
            "temperature": 0.8
        }

        response = client.post("/generate", json=payload)
        assert response.status_code == 200

        json_data = response.get_json()
        assert "story" in json_data
        assert json_data["story"] == "Era uma vez..."
        mock_generate.assert_called_once_with("Once upon a time", 50, 0.8)
