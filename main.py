from urllib import request
from flask import Flask, request, render_template
from flask_restful import Api, Resource
from dotenv import load_dotenv
import requests
import os
import mysql.connector


app = Flask(__name__)
api = Api(app)
load_dotenv()

api_key = os.getenv('NYT_API_KEY')

mydb = mysql.connector.connect(
    #host = "localhost",
    #user = "nico",
    #password = os.getenv('DB_PASS'),
    #database = "paraNews"
    host = os.getenv('ONLINE_DB_HOST'),
    user = os.getenv('ONLINE_DB_USER'),
    password = os.getenv('ONLINE_DB_PASS'),
    database = os.getenv('ONLINE_DB')
)

mycursor = mydb.cursor()

def apiSearch(formDict):
    query = formDict['Query']
    news_desk = formDict['Topic']
    begin_date = formDict['Start Date']
    page = "0"
    sort = "relevance"
    query_url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?" \
            f"q={query}" \
            f"&api-key={api_key}" \
            f"&begin_date={begin_date}" \
            f"&fq={news_desk}" \
            f"&page={page}" \
            f"&sort={sort}"

    r = requests.get(query_url)

    output = r.json()

    output = output['response']['docs']

    usrResult = []    

    for key in output:
        usrResult.append([key['headline']['main'], key['snippet'], key['web_url']])
        dbInsert = str(key['headline']['main'])
        sql = "INSERT INTO article_ratings(articleHeadline) VALUES (%s)"
        val = dbInsert
        mycursor.execute(sql,(val,))
    
    mydb.commit()

    return(usrResult)

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
     
        usrSearch = apiSearch(search_data)
        
        return render_template('results.html', usrSearch = usrSearch)

if __name__ == "__main__":
    app.run(debug=True)
