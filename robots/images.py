from googleapiclient.discovery import build
from robots.state import saveContent, loadContent, loadBlackList, saveBlackList
from credential.googleSearch import googleSearchCredentials
import requests
from PIL import Image


def robotImages():
    def fetchGoogleAndReturnImagesLinks(query):
        service = build("customsearch", "v1", developerKey=googleSearchCredentials['apiKey'])
        response = service.cse().list(
            cx = googleSearchCredentials['searchEngineId'],
            q = query,
            searchType = 'image',
            num  = 30).execute()
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
        print('> Fetch images of all sentences concluded')
    
    
    def downloadAndSave(url, fileName):
        fileName = 'content/'+fileName
        f  = open(fileName,'wb')
        f.write(requests.get(url).content)
        f.close()
        return url
    
    def viewImage(imageUrl):
        try:
            im = Image.open(requests.get(imageUrl, stream=True).raw)
            im.show()
            decition = str(input('Use this image?(y/n) '))
            if(decition != 'y'):
                saveBlackList(imageUrl)
                return True
        except:
            return True
        return False
            
    
    def downloadAllImages(content):
        print('> Downloading all images...')
        content['downloadedImages'] = []
        for sentenceIndex in range(len((content['sentences']))):
            images = content['sentences'][sentenceIndex]['images']
            for imageIndex in range(len(images)):
                imageUrl = images[imageIndex]
                
                blackList = loadBlackList()
                
                if(imageUrl in (content['downloadedImages'] or blackList)):
                    print("> {} {} Erro imagem ja existe: {}".format(sentenceIndex,imageIndex,imageUrl))
                    continue
                elif(imageUrl in blackList):
                    print("> {} {} Erro imagem na Black List: {}".format(sentenceIndex,imageIndex,imageUrl))
                    continue
                elif(viewImage(imageUrl)):
                    print("> {} {} Erro imagem rejeitada: {}".format(sentenceIndex,imageIndex,imageUrl))
                    continue
                try:
                    content['downloadedImages'].append(downloadAndSave(imageUrl,'{}-original.png'.format(sentenceIndex)))
                    print("> {} {} Baixou imagem com sucesso: {}".format(sentenceIndex,imageIndex,imageUrl))
                    break
                except:
                    print("> {} {} Erro ao baixar: {}".format(sentenceIndex,imageIndex,imageUrl))
        print('> Downloaded all images...')
        
        
    content = loadContent()
    fetchImagesOfAllSentences(content)
    saveContent(content)
    content = loadContent()
    downloadAllImages(content)
    saveContent(content)