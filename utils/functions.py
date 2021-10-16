from mediawiki import MediaWiki
import Algorithmia as algorithmia
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
    wikipedia = MediaWiki(lang=language)
    if(len(wikipedia.search(search)) < 1):
        raise Exception('apiWikipedia: Content not found')
    page = wikipedia.page(search)
    return page.summary, page.url
