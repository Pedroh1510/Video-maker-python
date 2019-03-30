from googleapiclient.discovery import build
from robots.state import saveContent,loadContent
from credential.googleSearch import googleSearchCredentials
import json

import requests


def fetchGoogleAndReturnImagesLinks(query):
    service = build("customsearch", "v1", developerKey=googleSearchCredentials['apiKey'])
    response = service.cse().list(
        cx = googleSearchCredentials['searchEngineId'],
        q = query,
        searchType = 'image',
        num  = 3).execute()
    def filtro(value=[]):
            return value['link']
    if not 'items' in response:
        return None
    else:
        return list(map(filtro,response['items']))

def fetchImagesOfAllSentences(content):
    for sentence in content['sentences']:
        query = '{} {}'.format(content['searchTerm'], sentence['keywords'][0])
        sentence['images'] = fetchGoogleAndReturnImagesLinks(query)
        sentence['googleSeachQuery'] = query


def downloadAndSave(url, fileName):
    fileName = 'content/'+fileName
    f  = open(fileName,'wb')
    f.write(requests.get(url).content)
    f.close()
    return url


def downloadAllImages(content):
    content['downloadedImages'] = []
    print(json.dumps(content,indent=2))
    for sentenceIndex in range(len((content['sentences']))):
        images = content['sentences'][sentenceIndex]['images']
        for imageIndex in range(len(images)):
            imageUrl = images[imageIndex]
            if(imageUrl in content['downloadedImages']):
                continue
            try:
                content['downloadedImages'].append(downloadAndSave(imageUrl,'{}-original.png'.format(sentenceIndex)))
                print("{} {} Baixou imagem com sucesso: {}".format(sentenceIndex,imageIndex,imageUrl))
            except:
                print("{} {} Erro ao baixar: {}".format(sentenceIndex,imageIndex,imageUrl))


def images():
    content = loadContent()
    fetchImagesOfAllSentences(content)
    downloadAllImages(content)
    
    print(json.dumps(content,indent=2))
    saveContent(content)