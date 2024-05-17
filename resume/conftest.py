
import pytest
import requests
import requests_mock

from utils.scraper import today_urls, scrape_article

@pytest.fixture(autouse=True)
def disable_network_calls(monkeypatch):
    def stunted_get():
        raise RuntimeError("Network access not allowed during testing!")
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: stunted_get())

@pytest.fixture
def mock_request():
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture
def mock_today_urls(mock_request):
    base_url = "https://mock.example.com"
    mocked_list = ["https://mock.example1.com", "https://mock.example2.com"]
    status = 200
    return mocked_list, status

@pytest.fixture
def mock_scrape_article(mock_request):
    base_url = "https://mock.example.com"
    mocked_article = {

    }
    status = 200
    return mocked_article, status