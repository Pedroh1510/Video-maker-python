from googleapiclient.discovery import build
from robots.state import saveContent, loadContent, loadBlackList
from credential.googleSearch import googleSearchCredentials
import requests


def fetchGoogleAndReturnImagesLinks(query):
    service = build("customsearch", "v1", developerKey=googleSearchCredentials['apiKey'])
    response = service.cse().list(
        cx = googleSearchCredentials['searchEngineId'],
        q = query,
        searchType = 'image',
        num  = 5).execute()
    def filtro(value=[]):
            return value['link']
    if not 'items' in response:
        return None
    else:
        return list(map(filtro,response['items']))

def fetchImagesOfAllSentences(content):
    print('> Fetching images of all sentences...')
    for sentence in content['sentences']:
        query = '{} {}'.format(content['searchTerm'], sentence['keywords'][0])
        sentence['images'] = fetchGoogleAndReturnImagesLinks(query)
        sentence['googleSeachQuery'] = query
    print('> Fetch voices of all sentences concluded')


def downloadAndSave(url, fileName):
    fileName = 'content/'+fileName
    f  = open(fileName,'wb')
    f.write(requests.get(url).content)
    f.close()
    return url


def downloadAllImages(content,blackList):
    print('> Downloading all images...')
    content['downloadedImages'] = []
    for sentenceIndex in range(len((content['sentences']))):
        images = content['sentences'][sentenceIndex]['images']
        for imageIndex in range(len(images)):
            imageUrl = images[imageIndex]
            if(imageUrl in content['downloadedImages']):
                print("> {} {} Erro imagem ja existe: {}".format(sentenceIndex,imageIndex,imageUrl))
                continue
            elif(imageUrl in blackList):
                print("> {} {} Erro imagem na Black List: {}".format(sentenceIndex,imageIndex,imageUrl))
                continue
            try:
                content['downloadedImages'].append(downloadAndSave(imageUrl,'{}-original.png'.format(sentenceIndex)))
                print("> {} {} Baixou imagem com sucesso: {}".format(sentenceIndex,imageIndex,imageUrl))
                break
            except:
                print("> {} {} Erro ao baixar: {}".format(sentenceIndex,imageIndex,imageUrl))
    print('> Downloaded all images...')

def images():
    content = loadContent()
    blackList = loadBlackList()
    fetchImagesOfAllSentences(content)
    downloadAllImages(content, blackList['blackList'])
    saveContent(content)
    