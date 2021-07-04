import pandas as pd
import preprocessing_functions
class summarizer():
    def __init__(self):
        pass
    def preprocess(self):
        pass
    def summarize(self):
        pass

if __name__ == "__main__":
    news_articles = pd.read_csv("../data/scraped_articles.csv")
    summ = summarizer()
    summ.preprocess()
    summ.summarize()