import Algorithmia as algorithmia
import nltk
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

from robots.state import saveContent,loadContent
from credential.algorithmiaC import ApiKey as algorithmiaApiKey
from credential.watsonC import ApiKey as watsonApiKey


def text():
    content = loadContent()
    service = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    url='https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2018-11-16',
    iam_apikey=watsonApiKey)
    
    
    def fetchContentFromWikipedia(searchTerm):
        algorithmiaAutheticated = algorithmia.client(algorithmiaApiKey)
        wikipediaAlgorithm = algorithmiaAutheticated.algo('web/WikipediaParser/0.1.2')
        wikipediaResponde = wikipediaAlgorithm.pipe(searchTerm).result
        wikipediaContent = wikipediaResponde
        return wikipediaContent["content"]


    def sanitizeContent(sorceContentOriginal):
        def removeBlankLinesAndMarkdown(text):
            allLinesFirtState = list(filter(lambda x: x!='', text.split('\n')))
            allLines = list(filter(lambda x: not(x.startswith('=')), allLinesFirtState))
            allLines = ' '.join(allLines)
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
                 'imagens': []}
            conteudo.append(a)
        return conteudo
    
    def limitMaximumSentences(content):
        content['sentences'] = content['sentences'][0:content['maximumSentences']]
        return content
    
    def fetchWatsonAndReturnKeywords(sentence):
        response = service.analyze(
    text=sentence,
    features=Features(entities=EntitiesOptions(),
    keywords=KeywordsOptions())).get_result()
        def filtro(value=[]):
            return value['text']
        return list(map(filtro,response['keywords']))
    
    def fetchKeywordsOfAllSentences(content):
        for i,item in enumerate(content['sentences']):
            content['sentences'][i]['keywords'] = fetchWatsonAndReturnKeywords(content['sentences'][i]['text'])
        return content
        
    content['sorceContentOriginal'] = fetchContentFromWikipedia(content['searchTerm'])
    content['sourceContentSanitize'] = sanitizeContent(content['sorceContentOriginal'])
    content['sentences'] = breakContentSentences(content['sourceContentSanitize'])
    content = limitMaximumSentences(content)
    content = fetchKeywordsOfAllSentences(content)
    print(json.dumps(content,indent=2))
    saveContent(content) 
