import os
from mediawiki import MediaWiki
import Algorithmia as algorithmia
import requests
from robots.state import loadApikey

algorithmiaApiKey = loadApikey(
    path='./credential/algorithmia.json')['apiKey']


def apiAlgorithmia():
    algorithmiaAutheticated = algorithmia.client(algorithmiaApiKey)
    wikipediaAlgorithm = algorithmiaAutheticated.algo(
        'web/WikipediaParser/0.1.2?timeout=30')
    wikipediaResponde = wikipediaAlgorithm.pipe({
        'articleName': content['searchTerm'],
        'lang': content['language']
    }).result
    wikipediaContent = wikipediaResponde["content"]
    wikipediaUrl = wikipediaResponde['url']
    return wikipediaContent, wikipediaUrl


def apiWikipedia(search, language):
    print(language, search)
    if(language == 'pt'):
        language = 'pt-br'
    wikipedia = MediaWiki()
    if(len(wikipedia.search(search)) < 1):
        raise Exception('apiWikipedia: Content not found')
    page = wikipedia.page(search)
    return page.summary, page.url

def getEnv(name=''):
    choose = os.environ[name]
    if(len(choose) == 0):
        raise Exception(f"{name} is empty")
    return choose

def sendRequestConcluded(videoId):
    try:
        print(f"sendRequestConcl: {videoId}")
        requests.post('https://bot-telegram-video-maker.herokuapp.com/readyVideo', data={'videoId': videoId})
        print(f"sendRequestConcluded: {videoId}")
    except Exception as e:
        print(e)
        pass