import pytest
from .analyzer import *
from unittest.mock import patch, MagicMock
import requests
import json

@pytest.fixture
def analyzer():
    return Analyzer("http://api:8000/")

def test_get_unscrapped_website(analyzer):
    fake_response = [
        {'domain': 'sitedjeya.pages.dev', 'ttfb': None, 'is_analyze': False, 'cms': None, 'techno_used': None, 'web_hoster': None, 'country_of_web_hoster': None, 'id': 14}
    ]
    with patch('analyzer.requests.get') as mock_get:
        mock_get.return_value.json.return_value = fake_response
        mock_get.return_value.status_code = 200
        
        websites = analyzer.get_unscrapped_website()
        
        mock_get.assert_called_once_with("http://api:8000/unscrapped_websites/")
        assert websites == fake_response

def test_get_cms_wordpress(analyzer):
    domain = "https://example.com"
    html_content = '<meta name="generator" content="WordPress 5.7"/>'
    
    with patch('analyzer.requests.get') as mock_get:
        mock_get.return_value.text = html_content
        mock_get.return_value.status_code = 200
        
        cms = analyzer.get_cms(domain)
        
        assert cms == "WordPress"

def test_get_cms_unknown(analyzer):
    domain = "https://example.com"
    html_content = '<meta name="generator" content="UnknownCMS 1.0"/>'
    
    with patch('analyzer.requests.get') as mock_get:
        mock_get.return_value.text = html_content
        mock_get.return_value.status_code = 200
        
        cms = analyzer.get_cms(domain)
        
        assert cms == "Unknown"

def test_get_tech_stack(analyzer):
    domain = "https://example.com"
    html_content = '''
    <script src="https://cdn.example.com/react.js"></script>
    <div id="app">This is powered by React</div>
    '''
    
    with patch('analyzer.requests.get') as mock_get:
        mock_get.return_value.text = html_content
        mock_get.return_value.status_code = 200
        
        tech_stack = analyzer.get_tech_stack(domain)
        
        assert tech_stack['frontend'] == "React"
        assert tech_stack['backend'] == "Unknown"

def test_get_web_hoster_info(analyzer):
    domain = "https://example.com"
    
    with patch('analyzer.socket.gethostbyname') as mock_gethostbyname, \
         patch('analyzer.requests.get') as mock_get:
        
        mock_gethostbyname.return_value = '93.184.216.34'
        mock_get.return_value.json.return_value = {
            'ip': '93.184.216.34',
            'organization': 'Example Inc.',
            'country': 'US'
        }
        
        web_hoster_info = analyzer.get_web_hoster_info(domain)
        
        assert web_hoster_info['hoster'] == "Example Inc."
        assert web_hoster_info['country'] == "US"

def test_add_domain(analyzer):
    domain = "https://newdomain.com"
    
    with patch('analyzer.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        
        analyzer.add_domain(domain)
        
        mock_post.assert_called_once_with(
            "http://api:8000/create_website/",
            data='{"domain": "https://newdomain.com"}',
            headers={'Content-Type': 'application/json'}
        )

def test_update_to_db(analyzer):
    result = {
        "domain": "https://example.com",
        "ttfb": 100,
        "cms": "WordPress"
    }
    
    with patch('analyzer.requests.patch') as mock_patch:
        mock_patch.return_value.status_code = 200
        
        analyzer.update_to_db(result)
        
        mock_patch.assert_called_once_with(
            "http://api:8000/websites/",
            data=json.dumps(result)
        )

def test_update_to_db_no_ttfb(analyzer):
    result = {
        "domain": "https://example.com",
        "ttfb": None
    }
    
    with patch('analyzer.requests.patch') as mock_patch:
        analyzer.update_to_db(result)
        
        mock_patch.assert_not_called()

def test_get_all_links(analyzer):
    domain = "https://example.com"
    html_content = '''
    <html>
        <body>
            <a href="https://external.com/page1">Link 1</a>
            <a href="https://another-domain.com/page2">Link 2</a>
            <a href="/relative-page">Relative Link</a>
            <a href="https://example.com/internal-page">Internal Link</a>
        </body>
    </html>
    '''
    
    with patch('analyzer.requests.get') as mock_get, \
         patch('analyzer.requests.head') as mock_head, \
         patch.object(analyzer, 'add_domain') as mock_add_domain:
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = html_content

        mock_head.return_value.status_code = 200

        analyzer.get_all_links(domain)

        mock_add_domain.assert_any_call("https://external.com")
        mock_add_domain.assert_any_call("https://another-domain.com")
        assert mock_add_domain.call_count == 2
