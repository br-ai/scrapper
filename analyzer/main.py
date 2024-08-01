"""
This file execute main python progam
"""
from analyzer import Analyzer

def main():
    analyzer = Analyzer("http://api:8000/")
    print(analyzer.get_unscrapped_website())

if __name__ == "__main__":
    main()
