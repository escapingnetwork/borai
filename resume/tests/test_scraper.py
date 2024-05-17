"""Tests for resume.utils.scraper"""

import pytest

from resume.utils.scraper import today_urls, scrape_article


def test_today_uurls_type(mock_today_urls):
    
    urls, _ = mock_today_urls
    assert type(urls) == list

def test_today_urls_status(mock_today_urls):

    _, status = mock_today_urls
    assert status == 200

def test_scrape_article_status():
    pass

