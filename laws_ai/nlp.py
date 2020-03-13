import nltk
from string import punctuation
import re
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')
stop_words = set(stopwords + list(punctuation))


def text_lower(text):
    text = " ".join(text.split())
    text = re.sub('<[^>]+>', '', text)
    text = text.split("(function")[0]
    text = text.lower()
    text = [palavra for palavra in text.split() if palavra not in stop_words]
    text = " ".join(text)
    return text


def text_paragraphs(text):
    text = " ".join(text.split())
    text = re.sub('<[^>]+>', '', text)
    text = text.split("(function")[0]
    text = text.lower()
    text = [palavra for palavra in text.split() if palavra not in stop_words]
    text = " ".join(text)
    return text
 
