import pytest
import requests
import requests_mock

from utils.scraper import today_urls, scrape_article

@pytest.fixture(autouse=True)
def disable_network_calls_fixture(monkeypatch):
    """Fixture to disable all network calls."""
    def stunted_get():
        raise RuntimeError("Network access not allowed during testing!")
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: stunted_get())

@pytest.fixture
def mock_request_fixture():
    """Fixture to mock requests."""
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture
def mocked_today_urls_fixture(mock_request_fixture):
    """Fixture to mock the today_urls function."""
    base_url = "https://mock.example.com"
    mocked_list = ["https://mock.example1.com", "https://mock.example2.com"]
    status = 200
    return mocked_list, status

@pytest.fixture
def mocked_scrape_article_fixture(mock_request_fixture):
    """Fixture to mock the scrape_article function."""
    base_url = "https://mock.example.com"
    mocked_article = {
        "title": "Mock Title",
        "content": "Mock content",
        # Add more fields as necessary
    }
    status = 200
    return mocked_article, status