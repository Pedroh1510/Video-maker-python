import nltk
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from robots.state import saveContent, loadContent, loadApikey
from utils.functions import apiWikipedia, apiAlgorithmia
from unicodedata import normalize
# from credential.algorithmiaC import ApiKey as algorithmiaApiKey
# from credential.watsonC import ApiKeyNLU as watsonApiKey

watsonApiKey = loadApikey(
    path='./credential/watson-nlu.json')


def robotText():
    service = NaturalLanguageUnderstandingV1(
        version="2018-04-05",
        url=watsonApiKey['url'],
        iam_apikey=watsonApiKey['apikey']
    )

    def fetchContentFromWikipedia(content):
        print('> Wikipedia content downloading')
        wikipediaContent, wikipediaUrl = apiWikipedia(
            content['searchTerm'], content['language'])
        print('> Wikipedia content downloaded')
        return wikipediaContent, wikipediaUrl

    def sanitizeContent(sorceContentOriginal):
        def removeBlankLinesAndMarkdown(text):
            text = str(text)
            allLinesFirtState = list(
                filter(lambda x: x != '', text.split('\n')))
            allLines = list(filter(lambda x: not(
                x.startswith('==')), allLinesFirtState))
            allLines = ' '.join(allLines)
            allLines = allLines.replace(' ()', '')
            allLines = allLines.replace(' ( )', '')
            allLines = allLines.replace('[...]', '')

            return allLines

        withoutBlankLines = removeBlankLinesAndMarkdown(sorceContentOriginal)
        textNormalizede = normalize('NFKD', withoutBlankLines)
        return textNormalizede

    def breakContentSentences(text):
        conteudo = []
        sent_tokenizer = nltk.tokenize.PunktSentenceTokenizer()
        sentences = sent_tokenizer.tokenize(text)
        for i, _ in enumerate(sentences):
            a = {'text': sentences[i],
                 'keywords': [],
                 'images': []
                 }
            conteudo.append(a)
        print('> Break content sentences concluded')
        return conteudo

    def limitMaximumSentences(content):
        content['sentences'] = content['sentences'][0:content['maximumSentences']]
        print('> Limit maximum sentences {}'.format(
            content['maximumSentences']))
        return content

    def fetchWatsonAndReturnKeywords(sentence):
        response = service.analyze(
            text=sentence,
            features=Features(entities=EntitiesOptions(), keywords=KeywordsOptions())).get_result()
        # def filtro(value=[]):
        #     return value['text']
        # return list(map(filtro,response['keywords']))
        return [response['keywords'][i]['text'] for i in range(len(response['keywords']))]

    def fetchKeywordsOfAllSentences(content):
        print('> Fetching keywords of all sentences...')
        for i, _ in enumerate(content['sentences']):
            content['sentences'][i]['keywords'] = fetchWatsonAndReturnKeywords(
                content['sentences'][i]['text'])
        print('> Fetch keywords of all sentences concluded')
        return content

    content = loadContent()
    content['sourceContentOriginal'], content['wikipediaUrl'] = fetchContentFromWikipedia(
        content)
    content['sourceContentSanitize'] = sanitizeContent(
        content['sourceContentOriginal'])
    content['sentences'] = breakContentSentences(
        content['sourceContentSanitize'])
    content = limitMaximumSentences(content)
    content = fetchKeywordsOfAllSentences(content)
    saveContent(content)
