import requests
import os
import json
from newsapi import NewsApiClient

nyt_api_key = os.getenv('NYT_API_KEY')
guar_api_key = os.getenv('GUAR_API_KEY')


def nytApiSearch(formDict):
    query = formDict['Query']
    news_desk = formDict['Topic']
    begin_date = formDict['Start Date']
    page = "0"
    sort = "relevance"
    query_url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?" \
            f"q={query}" \
            f"&api-key={nyt_api_key}" \
            f"&begin_date={begin_date}" \
            f"&fq={news_desk}" \
            f"&page={page}" \
            f"&sort={sort}"

    r = requests.get(query_url)
    output = r.json()
    output = output['response']['docs']
    usrResult = []    

    for key in output:
        usrResult.append([key['headline']['main'], key['web_url'], 'NYT'])

    return(usrResult)

def guarApiSearch(formDict):
    query = formDict['Query']
    page = "1"
    query_url = f"https://content.guardianapis.com/search?" \
            f"api-key={guar_api_key}" \
            f"&q={query}" \
            f"&page={page}"
            
    r = requests.get(query_url)
    response = json.loads(r.text)['response']
    output = response['results']
    usrResult = []

    for key in output:
        usrResult.append([key['webTitle'], key['webUrl'], 'Guardian'])
      
    return(usrResult)

def bbcApiSearch(formDict):
    newsapi = NewsApiClient(api_key='de6bdb27a1624954a42b444accfb50ef')

    all_articles = newsapi.get_everything(
        q=formDict['Query'],
        sources = 'bbc-news',
        domains = 'bbc.co.uk',
        language = 'en',
        sort_by = 'relevancy',
        page=1
    )
    
    output = all_articles['articles']
    usrResult = []

    for key in output:
        usrResult.append([key['title'], key['url'], 'BBC'])

    return(usrResult)

def apApiSearch(formDict):
    newsapi = NewsApiClient(api_key='de6bdb27a1624954a42b444accfb50ef')

    all_articles = newsapi.get_everything(
        q=formDict['Query'],
        sources = 'associated-press',
        domains = 'apnews.com',
        language = 'en',
        sort_by = 'relevancy',
        page=1
    )

    output = all_articles['articles']
    usrResult = []

    for key in output:
        usrResult.append([key['title'], key['url'], 'AP'])

    return(usrResult)    
   