"""
This file execute main python progam
"""
import time
from analyzer import Analyzer

def main():
    analyzer = Analyzer("http://api:8000/")
    unscrapped_websites = analyzer.get_unscrapped_website()
    print(f"Nombre de domaines à analyser : {len(unscrapped_websites)}")
    
    for website in unscrapped_websites:
        domain = website['domain']
        print(f"En cours d'analyse de : {domain}")
        time.sleep(4)
        result = analyzer.analyze_website(domain)
        print(result, flush=True)
        # Attente de 7 secondes entre chaque analyse
        print("Pause de 7 secondes avant la prochaine analyse...")
        time.sleep(7)
        print("-----------------------------", flush=True)
    
    print("Analyse terminée")

if __name__ == "__main__":
    main()