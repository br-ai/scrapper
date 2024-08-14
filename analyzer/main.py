"""
This file execute main python progam
"""
import time
from analyzer import Analyzer

def main():
    analyzer = Analyzer("http://api:8000/")
    while True:
        print("0: ➕ Add a new domain \n1: 🛠️  Start auto-scraping \n2: 🌐 scrap a website now\n")
        print("---------------------------------------\n")
        choice = input("Enter the number of your choice (or 'q' to quit):  ").strip()

        if choice == '0':
            analyzer.add_domain()

        elif choice == '1':
            analyzer.auto_scrapping()

        elif choice == '2':
            analyzer.scrap()

        elif choice.lower() == 'q':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid number or 'q' to quit.")

if __name__ == '__main__':
    main()

