from urllib import request
from flask import Flask, request, render_template
from flask_restful import Api, Resource
import requests


app = Flask(__name__)
api = Api(app)

api_key = "fGSQhMjcLuFWe8sHJncYhEAfWDsFzIdy"

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

    print(output)

    output = output['response']['docs']

    usrResult = []

    for key in output:
        usrResult.append([key['headline']['main'], key['snippet'], key['web_url']])

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



