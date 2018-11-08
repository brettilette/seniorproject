from textblob import TextBlob

def sentiment_analysis(input_text):
    text = TextBlob(input_text)
    return [text.polarity,text.subjectivity]
