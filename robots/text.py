import Algorithmia as algorithmia
import nltk
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from robots.state import saveContent,loadContent
from credential.algorithmiaC import ApiKey as algorithmiaApiKey
from credential.watsonC import ApiKeyNLU as watsonApiKey
from unicodedata import normalize

def robotText():
    service = NaturalLanguageUnderstandingV1(
        version= watsonApiKey['version'],
        url= watsonApiKey['url'],
        iam_apikey= watsonApiKey['iam_apikey']
    )
    
    def fetchContentFromWikipedia(content):
        print('> Wikipedia content downloading')
        algorithmiaAutheticated = algorithmia.client(algorithmiaApiKey)
        wikipediaAlgorithm = algorithmiaAutheticated.algo('web/WikipediaParser/0.1.2')
#         wikipediaResponde = wikipediaAlgorithm.pipe(content['searchTerm']).result
        
        wikipediaResponde = wikipediaAlgorithm.pipe({
            'articleName': content['searchTerm'],
            'lang': content['language']
            }).result
#         wikipediaContent = wikipediaResponde["content"].encode('utf-8').decode('utf-8')
#         wikipediaContent = normalize('NFKD', wikipediaResponde["content"]).encode('ASCII', 'ignore').decode('ASCII')
        wikipediaContent = wikipediaResponde["content"]
#         wikipediaContent = wikipediaResponde["content"].encode('utf-8').decode('utf-8')
        
        wikipediaUrl = wikipediaResponde['url']
        print('> Wikipedia content downloaded')
        return wikipediaContent, wikipediaUrl


    def sanitizeContent(sorceContentOriginal):
        def removeBlankLinesAndMarkdown(text):
            text = str(text)
            allLinesFirtState = list(filter(lambda x: x!='', text.split('\n')))
            allLines = list(filter(lambda x: not(x.startswith('==')), allLinesFirtState))
            allLines = ' '.join(allLines)
#             allLines = normalize('NFKD', allLines).encode('ASCII', 'ignore').decode('ASCII')
            allLines = allLines.replace(' ()', '')
            allLines = allLines.replace(' ( )', '')
            allLines = allLines.replace('[...]', '')
            # allLines = allLines.replace('%u', '\u')

            return allLines
            
        withoutBlankLines = removeBlankLinesAndMarkdown(sorceContentOriginal)
        return withoutBlankLines
    
    def breakContentSentences(text):
        conteudo=[]
        sent_tokenizer = nltk.tokenize.PunktSentenceTokenizer()
        sentences = sent_tokenizer.tokenize(text)
        for i, item in enumerate(sentences):
            a = {'text': sentences[i],
                 'keywords': [],
                 'images': []
                 }
            conteudo.append(a)
        print('> Break content sentences concluded')
        return conteudo
    
    def limitMaximumSentences(content):
        content['sentences'] = content['sentences'][0:content['maximumSentences']]
        print('> Limit maximum sentences {}'.format(content['maximumSentences']))
        return content
    
    def fetchWatsonAndReturnKeywords(sentence):
        response = service.analyze(
            text=sentence,
            features=Features(entities=EntitiesOptions(),keywords=KeywordsOptions())).get_result()
        def filtro(value=[]):
            return value['text']
        return list(map(filtro,response['keywords']))
    
    def fetchKeywordsOfAllSentences(content):
        print('> Fetching keywords of all sentences...')
        for i,item in enumerate(content['sentences']):
            content['sentences'][i]['keywords'] = fetchWatsonAndReturnKeywords(content['sentences'][i]['text'])
        print('> Fetch keywords of all sentences concluded')
        return content
    
    content = loadContent()
    content['sorceContentOriginal'] ,content['wikipediaUrl'] = fetchContentFromWikipedia(content)
    content['sourceContentSanitize'] = sanitizeContent(content['sorceContentOriginal'])
    content['sentences'] = breakContentSentences(content['sourceContentSanitize'])
    content = limitMaximumSentences(content)
    content = fetchKeywordsOfAllSentences(content)
    saveContent(content)