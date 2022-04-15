from urllib import request
from flask import Flask, request, render_template, redirect
from flask_restful import Api, Resource
from dotenv import load_dotenv
import requests
import os
import mysql.connector
from apiCalls import apApiSearch, bbcApiSearch, nytApiSearch, guarApiSearch

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
    mydb.commit()

    return(usrSearch)

def upVote(headline):
    sql = "UPDATE article_ratings SET rating = rating + 1 WHERE headline = %s"
    val = headline
    mycursor.execute(sql, (val,))
    mydb.commit()

def downVote(headline):
    sql = "UPDATE article_ratings SET rating = rating - 1 WHERE headline = %s"
    val = headline
    mycursor.execute(sql, (val,))
    mydb.commit()


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
     
        apSearch = apApiSearch(search_data)
        bbcSearch = bbcApiSearch(search_data)       
        nytSearch = nytApiSearch(search_data)
        guarSearch = guarApiSearch(search_data)
        usrSearch = nytSearch + guarSearch + bbcSearch + apSearch

        databaseUpdate(usrSearch)
        usrSearch = getRatings(usrSearch)

        return render_template('results.html', usrSearch = usrSearch)

@app.route('/vote', methods=['POST'])
def vote():
        if request.method == 'POST':
            headLine = list(request.form.keys())
            vote = list(request.form.values())
            vote = vote[0]
            headLine = headLine[0]
            if(vote == "upvote"):
                print(headLine)
                upVote(headLine)
            elif(vote == "downvote"):
                downVote(headLine)

            return redirect('/search')


if __name__ == "__main__":
    app.run(debug=True)
