# import required libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")

# create a dict of various rss feed link and their categories. Will iterate them one by one.
timesofindia = {'latest':'http://timesofindia.indiatimes.com/rssfeeds/1221656.cms',
               'India':'https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms',
               'World':'https://timesofindia.indiatimes.com/rssfeeds/296589292.cms',
                'Cricket':'https://timesofindia.indiatimes.com/rssfeeds/54829575.cms',
                'Sports':'https://timesofindia.indiatimes.com/rssfeeds/4719148.cms',
                'Bussiness':'https://timesofindia.indiatimes.com/rssfeeds/1898055.cms',
                'Tech':'https://timesofindia.indiatimes.com/rssfeeds/66949542.cms'
               }

# store details for each category
all_items = {}
for category, rsslink in timesofindia.items():
    print('Processing for category: {0}. \nRSS link: {1}'.format(category,rsslink))
    # get the webpage URL and read the html
    rssdata = requests.get(rsslink)
    #print(rssdata.content)
    soup = BeautifulSoup(rssdata.content)
    all_items[category] = soup.find_all('item')
    #print(soup.prettify())

# Function to fetch each news link to get news essay
def fetch_news_text(link):
    # read the html webpage and parse it
    soup = BeautifulSoup(requests.get(link).content, 'html.parser')
    # fetch the news article text box
    # these are with element <div class="_3WlLe clearfix">
    text_box = soup.find_all('div', attrs={'class':'clearfix rel'})
    # extract text and combine
    news_text = str(". ".join(t.text.strip() for t in text_box))
    return news_text

# using the above function, process text
news_articles = [{'Feed':'timesofindia',
                  'Category': category,
                  'Headline': all_items[category][item].title.text,
                  'Link': all_items[category][item].guid.text,
                  'Pubdate': all_items[category][item].pubdate.text,
                  'NewsText': fetch_news_text(all_items[category][item].guid.text)}
                     for category in all_items.keys() for item in range(len(all_items[category]))]
news_articles = pd.DataFrame(news_articles)

#export
news_articles.to_csv("../data/scraped_articles.csv")