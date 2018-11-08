from textblob import TextBlob

def sentiment_analysis(input_text):
    text = TextBlob(input_text)
    print(text.sentiment)
    return [text.polarity,text.subjectivity]
