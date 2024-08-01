import requests

class Analyzer:
    def __init__(self, url_base_api):
        self.url_base_api = url_base_api
    
    def get_unscrapped_website(self):
        try:
            response = requests.get(self.url_base_api+"unscrapped_websites/")
        except Exception as e:
            print(f"An error occured : {e}")
        return response.json()
    