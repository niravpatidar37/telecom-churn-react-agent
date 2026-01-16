# tests/test_api.py
from fastapi.testclient import TestClient
from src.api import app
from src.config import settings

client = TestClient(app)

def test_ask_endpoint():
    """
    Test the /ask endpoint. 
    Note: This attempts to call the real agent. 
    If you want to mock the agent, you'd patch 'src.api.react_telecom_agent'.
    For now, we'll assume a real integration test or we can mock it here.
    """
    # We'll mock the agent to avoid spending tokens and network calls during basic tests
    from unittest.mock import patch
    
    with patch("src.api.react_telecom_agent") as mock_agent:
        mock_agent.return_value = "Mocked answer"
        
        response = client.post("/ask", json={"question": "Test question"})
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert data["answer"] == "Mocked answer"
        
        mock_agent.assert_called_once_with("Test question")
