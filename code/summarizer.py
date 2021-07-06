from preprocessing_functions import remove_long_strings, remove_numbers, \
    remove_punctuation, remove_html_tags, remove_accented_chars,\
    remove_special_characters, remove_extra_whitespace_tabs, to_lowercase, lemmatize_text

from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")


class Summarizer:
    def __init__(self, n):
        self.n = n
        self.word_embeddings = {}

    def create_word_embeddings(self):
        # define dict to hold a word and its vector
        word_embeddings = {}

        # read the word embeddings file

        f = open('GloVe/glove.6B.100d.txt',
                 encoding='utf-8')
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            word_embeddings[word] = coefs
        f.close()
        self.word_embeddings = word_embeddings

    def preprocess(self, news_articles_):
        """
        This method preprocesses the Article text
        :param news_articles_: scraped data as input
        :return: pd.Series
        """
        if type(news_articles_)==pd.DataFrame:
            news_articles_ = news_articles_
        else:
            temp_dict = {"NewsText": news_articles_}
            news_articles_ = pd.DataFrame(temp_dict.values(),columns=temp_dict.keys())

        news_articles_.dropna(inplace=True)
        news_articles_ = news_articles_[news_articles_["NewsText"] != ""]
        news_articles_["NewsText"] = news_articles_["NewsText"].apply(remove_html_tags)
        news_articles_["NewsText"] = news_articles_["NewsText"].apply(remove_accented_chars)
        news_articles_["NewsText"] = news_articles_["NewsText"].apply(remove_special_characters)
        news_articles_["NewsText"] = news_articles_["NewsText"].apply(remove_numbers)
        news_articles_["NewsText"] = news_articles_["NewsText"].apply(remove_punctuation)
        news_articles_["NewsText"] = news_articles_["NewsText"].apply(lemmatize_text)
        # news_articles_["NewsText"] = news_articles_["NewsText"].apply(remove_stopwords)
        news_articles_["NewsText"] = news_articles_["NewsText"].apply(remove_extra_whitespace_tabs)
        news_articles_["NewsText"] = news_articles_["NewsText"].apply(to_lowercase)
        news_articles_["NewsText"] = news_articles_["NewsText"].apply(remove_long_strings)

        return news_articles_["NewsText"]

    def summarize(self, sentences):
        """
        main method : generates summary
        :param sentences: preprocessed input
        :return: str
        """
        sentences = sentences.split(".")
        sentences = [i for i in sentences if len(i) > 1]
        # create vector for each sentences
        # list to hold vector
        sentence_vectors = []
        # create vector for each clean normalized sentence
        for i in sentences:
            if len(i) != 0:
                v = sum([self.word_embeddings.get(w, np.zeros((100,))) for w in i.split()]) / (len(i.split()) + 0.001)
            else:
                v = np.zeros((100,))
            sentence_vectors.append(v)
        print('Total vectors created:', len(sentence_vectors))

        # Similarity between sentences

        # define matrix with all zero values
        sim_mat = np.zeros([len(sentences), len(sentences)])
        # will populate it with cosine_similarity values
        # for each sentences compared to other
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i != j:
                    sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1, 100), sentence_vectors[j]
                                                      .reshape(1, 100))[0, 0]
        # build graph and get pagerank
        nx_graph = nx.from_numpy_array(sim_mat)
        scores = nx.pagerank(nx_graph)
        top_sentences_index = list(dict(sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.n]).keys())
        summary_ = ".".join([sentences[i].strip().capitalize() for i in top_sentences_index])

        return summary_

        # def mail_summary(self,summary):
        #     # generated summary can be mailed and whole process can be automated
        #     pass


if __name__ == "__main__":
    news_articles = pd.read_csv("data/scraped_articles.csv")
    summ = Summarizer(n=5)
    clean_sentences = summ.preprocess(news_articles)
    summ.create_word_embeddings()
    summary = summ.summarize(clean_sentences[0])
    print(clean_sentences[0])
    print(summary)
    #for i in clean_sentences[:5]:
    #    print(summ.summarize(i))
