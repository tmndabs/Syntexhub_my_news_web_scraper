import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin, urlparse

# Dictionary of authorized news sources
AUTHORIZED_SOURCES = {
    'bbc': {
        'url': 'https://www.bbc.com/news',
        'base_url': 'https://www.bbc.com'
    },
    'reuters': {
        'url': 'https://www.reuters.com/world/',
        'base_url': 'https://www.reuters.com'
    },
    'ap': {
        'url': 'https://apnews.com/',
        'base_url': 'https://apnews.com'
    }
}

def get_source_choice( ):
    print("Please choose a news source from the following options:")
    for key in AUTHORIZED_SOURCES:
        print(f"- {key}")

    while True:
        choice = input("Enter your choice: ").lower()
        if choice in AUTHORIZED_SOURCES:
            return AUTHORIZED_SOURCES[choice]
        else:
            print("Invalid choice. Please choose from the authorized list.")

def scrape_news(source):
    url = source['url']
    base_url = source['base_url']

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = []
        for item in soup.find_all(['h1', 'h2', 'h3']):
            title = item.get_text(strip=True)
            link_el = item.find_parent('a') or item.find('a')

            if title and link_el and 'href' in link_el.attrs:
                link = urljoin(base_url, link_el['href'])


                if link.startswith(base_url):
                    articles.append({
                        'Title': title,
                        'URL': link,
                        'Time': 'N/A' 
                    })

        if articles:
            # Save articles to a CSV file
            filename = 'headlines.csv'
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['Title', 'URL', 'Time'])
                writer.writeheader()
                writer.writerows(articles)
            print(f"Saved {len(articles)} headlines to {filename}")
        else:
            print("No headlines found.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print('----------------------------------')
    print('     Welcome to Scrapped News     ')
    print('----------------------------------')
    chosen_source = get_source_choice()
    scrape_news(chosen_source)
