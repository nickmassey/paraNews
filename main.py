from urllib import request
from flask import Flask, request, render_template
from flask_restful import Api, Resource
from dotenv import load_dotenv
import requests
import os
import mysql.connector
from apiCalls import nytApiSearch, guarApiSearch

app = Flask(__name__)
api = Api(app)
load_dotenv()

api_key = os.getenv('NYT_API_KEY')

mydb = mysql.connector.connect(
    host = os.getenv('ONLINE_DB_HOST'),
    user = os.getenv('ONLINE_DB_USER'),
    password = os.getenv('ONLINE_DB_PASS'),
    database = os.getenv('ONLINE_DB')
)

mycursor = mydb.cursor(buffered=True)

def databaseUpdate(usrSearch):
    sql = "INSERT IGNORE INTO article_ratings(headLine, source) VALUES (%s, %s)"
    for key in usrSearch:
            headline = (key[0])
            source = (key[2])
            data = headline, source
            mycursor.execute(sql, data)
    mydb.commit()

def getRatings(usrSearch):    
    for item in usrSearch:
        sql = "SELECT rating FROM article_ratings WHERE headline = %s"
        val = (item[0])
        mycursor.execute(sql,(val,))
        rating = mycursor.fetchall()
        item.append(rating[0][0])
    mycursor.reset()

    return(usrSearch)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/results', methods = ['POST', 'GET'])
def results():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/search' to submit form"
    if request.method == 'POST':
        search_data = request.form
     
        nytSearch = nytApiSearch(search_data)
        guarSearch = guarApiSearch(search_data)
        usrSearch = nytSearch + guarSearch

        databaseUpdate(usrSearch)
        usrSearch = getRatings(usrSearch)

        return render_template('results.html', usrSearch = usrSearch)

if __name__ == "__main__":
    app.run(debug=True)
