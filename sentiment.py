from textblob import TextBlob
from urllib.parse import unquote

def sentiment_analysis(input_text):
    input_text = unquote(input_text)
    text = TextBlob(input_text)
    return [(text.polarity + 1) * 50,(text.subjectivity + 1) * 50]
