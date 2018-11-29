from textblob import TextBlob
from urllib.parse import unquote

def sentiment_analysis(input_text):
    input_text = unquote(input_text)
    text = TextBlob(input_text)
    return [(text.polarity + 1) * 50,(text.subjectivity + 1) * 50]

def sentiment_test(input_text):
    #input_text = unquote(input_text)
    text = TextBlob(input_text)
    return [(text.polarity + 1) * 50, (text.subjectivity + 1) * 50]

if __name__ == '__main__':
    print(sentiment_test("Great start up, with great management focused on improving and investing in it's employees."))