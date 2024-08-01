import requests
from bs4 import BeautifulSoup
import time
import socket

class Analyzer:
    def __init__(self, url_base_api):
        self.url_base_api = url_base_api
    
    def get_unscrapped_website(self):
        try:
            response = requests.get(self.url_base_api+"unscrapped_websites/")
        except Exception as e:
            print(f"An error occured : {e}")
        return response.json()
    
    def analyze_website(self, domain):
        ttfb = self.get_ttfb(domain)
        cms = self.get_cms(domain)
        technologies = self.get_technologies(domain)
        web_hoster, country_of_web_hoster = self.get_web_hoster_info(domain)
        
        return {
            'domain': domain,
            'ttfb': ttfb,
            'cms': cms,
            'technologies': technologies,
            'web_hoster': web_hoster,
            'country_of_web_hoster': country_of_web_hoster,
        }
    
    def get_ttfb(self, domain):
        start = time.time()
        try:
            response = requests.get(f"http://{domain}")
            ttfb = time.time() - start
        except requests.RequestException:
            ttfb = None
        return ttfb
    
    def get_web_hoster_info(self, domain):
        try:
            ip_address = socket.gethostbyname(domain)
            response = requests.get(f"http://ipinfo.io/{ip_address}")
            data = response.json()
            return data.get('org', 'Unknown'), data.get('country', 'Unknown')
        except (requests.RequestException, socket.gaierror) as e:
            print(f"An error occurred while getting hoster info for {domain}: {e}")
            return None, None

    def get_cms(self, domain):
        pass
    
    def get_technologies(self, domain):
        pass

    def analyze_all_websites(self):
        websites = self.get_unscrapped_website()
        analyses = []
        for website in websites:
            domain = website['domain']
            analysis = self.analyze_website(domain)
            analyses.append(analysis)
        return analyses