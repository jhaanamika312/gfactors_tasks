from flask import Flask, request, render_template,Response
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from string import punctuation
import re
from nltk.corpus import stopwords

import pika
import sys
import uuid


nltk.download('stopwords')

set(stopwords.words('english'))

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('form.html')

@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method=="POST":
         message = sentimentAnalysis.call(request.form['Message'])
    #response = sentimentAnalysis.call(message)
    return Response( message)

@app.route('/', methods=['POST'])
def my_form_post():
    stop_words = stopwords.words('english')
    
    #convert to lowercase
    text1 = request.form['text1'].lower()
    
    text_final = ''.join(c for c in text1 if not c.isdigit())
    
    #remove punctuations
    #text3 = ''.join(c for c in text2 if c not in punctuation)
        
    #remove stopwords    
    processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

    sa = SentimentIntensityAnalyzer()
    dd = sa.polarity_scores(text=processed_doc1)
    compound = round((1 + dd['compound'])/2, 2)

    return render_template('form.html', final=compound, text1=text_final,text2=dd['pos'],text5=dd['neg'],text4=compound,text3=dd['neu'])

class RabbitMq(object):
     def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

     def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

     def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return (self.response)
       

sentimentAnalysis=RabbitMq()

   
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')