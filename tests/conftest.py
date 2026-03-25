import os
import pytest
from unittest.mock import patch

os.environ["VECTOR_DB_PROVIDER"] = "in_memory"
os.environ["OLLAMA_EMBEDDING_URL"] = ""  # Force HashTokenEmbedder

@pytest.fixture(autouse=True)
def mock_external_calls():
    class MockResponse:
        def __init__(self, json_data, status_code=200):
            self.json_data = json_data
            self.status_code = status_code
        def json(self):
            return self.json_data
        def raise_for_status(self):
            pass

    def mock_post(url, *args, **kwargs):
        if "api/chat" in url:
            return MockResponse({"message": {"content": "Mocked LLM response 18,200"}})
        return MockResponse({})

    with patch("httpx.post", side_effect=mock_post):
        yield
