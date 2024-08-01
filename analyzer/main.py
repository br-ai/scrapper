"""
This file execute main python progam
"""
from analyzer import Analyzer

def main():
    analyzer = Analyzer("http://api:8000/")
    print(f" Nombre de domaines a analyser : {len(analyzer.get_unscrapped_website())}")
    print("--------------------------")
    results = analyzer.analyze_all_websites()
    for result in results:
        print(result)
        
    print("Analyse terminée")
    
if __name__ == "__main__":
    main()
