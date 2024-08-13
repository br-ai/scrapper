import requests
from bs4 import BeautifulSoup
import time
import socket
import json


class Analyzer:
    def __init__(self, url_base_api):
        self.url_base_api = url_base_api

    def add_domain(self):
        while True:
            try:
                domain = str(input("Enter the name of domain (without http(s)): ")).strip()
                if domain.startswith("http"):
                    print("Invalid domain name, please remove http(s) and try again.")
                    continue
                if not "." in domain:
                    print("Invalid domain name, please add an extension (.com, .fr etc...).")
                    continue

                data = {"domain": domain,
                        "ttfb": None,
                        "is_analyze": False,
                        "cms": None,
                        "techno_used": None,
                        "web_hoster": None,
                        "country_of_web_hoster": None
                        }
                headers = {'Content-type': 'application/json'}
                
                response = requests.post(self.url_base_api + "websites/", data=json.dumps(data), headers=headers)
                
                if response.status_code == 200:
                    print(f"Domain: {domain} was successfully added!")
                    time.sleep(5)
                    break
                else:
                    print(f"Failed to add domain: {domain}. Status code: {response.status_code}")
                    print(f"The error message is : {response.reason}, maybe the url already exists or connections issues")
                    time.sleep(5)
                    break

            except Exception as e:
                print(f"An error occurred: {e}")
                break
    
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
        try:
            response = requests.get(f"http://{domain}", timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check meta generator tag
            meta_generator = soup.find('meta', attrs={'name': 'generator'})
            if meta_generator:
                generator_content = meta_generator.get('content', '').lower()
                if 'wordpress' in generator_content:
                    return 'WordPress'
                if 'drupal' in generator_content:
                    return 'Drupal'
                if 'joomla' in generator_content:
                    return 'Joomla'
                if 'typo3' in generator_content:
                    return 'TYPO3'
                if 'ghost' in generator_content:
                    return 'Ghost'
                if 'hubspot' in generator_content:
                    return 'HubSpot'

            html_text = response.text.lower()
            
            if '/wp-content/' in html_text or '/wp-includes/' in html_text:
                return 'WordPress'
            if '/sites/all/' in html_text or '/modules/' in html_text or '/themes/' in html_text:
                return 'Drupal'
            if '/media/system/js/' in html_text or '/templates/' in html_text:
                return 'Joomla'
            if '/skin/frontend/' in html_text or '/js/mage/' in html_text or '/media/mage/' in html_text:
                return 'Magento'
            if '/modules/' in html_text and '/themes/' in html_text and '/ps_shoppingcart/' in html_text:
                return 'PrestaShop'
            if '/wixsite/' in html_text or 'wix.com' in html_text:
                return 'Wix'
            if '/cdn.shopify.com/s/' in html_text:
                return 'Shopify'
            if '/typo3/' in html_text:
                return 'TYPO3'
            if 'cdn.contentful.com' in html_text:
                return 'Contentful'
            if 'squarespace.com' in html_text:
                return 'Squarespace'
            if 'magnolia-cms.com' in html_text:
                return 'Magnolia'
            if 'sitecore' in html_text:
                return 'Sitecore'
            if '/ghost/' in html_text:
                return 'Ghost'
            if 'kentico' in html_text:
                return 'Kentico'
            if 'bigcommerce' in html_text:
                return 'BigCommerce'
            if 'adobe commerce' in html_text:
                return 'Adobe Commerce'
            
            return 'Unknown'
        except requests.RequestException as e:
            print(f"An error occurred while getting CMS info for {domain}: {e}")
            return None

    def get_technologies(self, domain):
        try:
            response = requests.get(f"http://{domain}", timeout=10)
            response.raise_for_status()
            html_text = response.text.lower()

            front_end = self.detect_front_end(html_text)
            back_end = self.detect_back_end(html_text)

            return {
                'front_end': front_end,
                'back_end': back_end,
            }
        except requests.RequestException as e:
            print(f"An error occurred while getting technologies info for {domain}: {e}")
            return {
                'front_end': 'Unknown',
                'back_end': 'Unknown',
            }

    def detect_front_end(self, html_text):

        if 'react' in html_text or 'react-dom' in html_text:
            return 'React'
        if 'vuejs' in html_text:
            return 'Vue.js'
        if 'angular' in html_text:
            return 'Angular'
        if 'svelte' in html_text:
            return 'Svelte'
        if 'next.js' in html_text:
            return 'Next.js'
        if 'nuxt' in html_text:
            return 'Nuxt.js'
        if 'nest' in html_text:
            return 'Nest.js'
        if 'alpine.js' in html_text:
            return 'Alpine.js'

        return 'Unknown'

    def detect_back_end(self, html_text):

        if 'django' in html_text:
            return 'Django'
        if 'flask' in html_text:
            return 'Flask'
        if 'spring' in html_text:
            return 'Spring'
        if 'rails' in html_text or 'ruby on rails' in html_text:
            return 'Ruby on Rails'
        if 'laravel' in html_text:
            return 'Laravel'
        if 'symfony' in html_text:
            return 'Symfony'
        if 'codeigniter' in html_text:
            return 'CodeIgniter'
        if 'express' in html_text:
            return 'Express.js'
        if 'node.js' in html_text or 'nodejs' in html_text:
            return 'Node.js'
        if 'next.js' in html_text:
            return 'Next.js'
        if 'asp.net' in html_text:
            return 'ASP.NET'
        if 'django' in html_text:
            return 'Django'
        if 'flask' in html_text:
            return 'Flask'

        return 'Unknown'

    def auto_scrapping(self):
        unscrapped_websites = self.get_unscrapped_website()
        print(f"Nombre de domaines a scrapper : {len(unscrapped_websites)}")
        for website in unscrapped_websites:
            domain = website['domain']
            print(f"En cours d'analyse de : {domain}")
            time.sleep(4)
            result = self.analyze_website(domain)
            print(result, flush=True)
            print("Pause de 4 secondes avant la prochaine analyse...")
            time.sleep(4)
            print("-----------------------------", flush=True)
    
        print("Analyse terminée")
