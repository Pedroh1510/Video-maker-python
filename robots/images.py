from googleapiclient.discovery import build
from robots.state import saveContent, loadContent, loadBlackList, saveBlackList
from credential.googleSearch import googleSearchCredentials
from PIL import Image
import requests
import cv2
import numpy as np
import json


def robotImages():

    def fetchGoogleAndReturnImagesLinks(query):
        service = build("customsearch", "v1", developerKey=googleSearchCredentials['apiKey'])
        response = service.cse().list(
            cx = googleSearchCredentials['searchEngineId'],
            q = query,
            searchType = 'image',
            num = 10).execute()
        def filtro(value=[]):
                return value['link']
        if not 'items' in response:
            return None
        else:
            return list(map(filtro,response['items']))
        
    def ajustFetchImages(content, sentence):
        if(content['searchTerm'].lower() in sentence.lower()):
            return content['searchTerm']
        else:
            query = '{} {}'.format(content['searchTerm'], sentence)
            return query
    
    def fetchImagesOfAllSentences(content):
        print('> Fetching images of all sentences...')
        for sentence in content['sentences']:
            query = ajustFetchImages(content, sentence['keywords'][0])
            sentence['images'] = fetchGoogleAndReturnImagesLinks(query)
#             query = ajustFetchImages(content, sentence['keywords'][1])
#             sentence['images'] = sentence['images'].extend(fetchGoogleAndReturnImagesLinks(query))
            sentence['googleSeachQuery'] = query
        print('> Fetch images of all sentences concluded')
    
    def downloadAndSave(url, fileName):
        fileName = 'content/'+fileName
        f  = open(fileName,'wb')
        f.write(requests.get(url).content)
        f.close()
        return url
    
    def checkSupportImage(imageUrl):
        try:
            Image.open(requests.get(imageUrl, stream=True).raw)
            return True
        except:
            return False

    def viewImage(imageUrl):
        try:
            im = Image.open(requests.get(imageUrl, stream=True).raw)
            im.show()
            print()
            decition = str(input('Use this image?(y/n) '))
            if(decition != 'y'):
                saveBlackList(imageUrl)
                return True
        except:
            return True
        return False

    def checkDuplicatedImage(sentenceIndex, imageIndex, imageUrl):
        def url_to_image(url):
            resp = requests.get(url)
            image = np.asarray(bytearray(resp.content), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            return image

        image_to_compare = url_to_image(imageUrl)
        for i in range(0, sentenceIndex):
            filename = 'content/{}-original.png'.format(i)
            original = cv2.imread(filename)
            if original.shape == image_to_compare.shape:
                difference = cv2.subtract(original, image_to_compare)
                b, g, r = cv2.split(difference)
                if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    return True
            sift = cv2.xfeatures2d.SIFT_create()
            kp_1, desc_1 = sift.detectAndCompute(original, None)
            kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)
            index_params = dict(algorithm=0, trees=5)
            search_params = dict()
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(desc_1, desc_2, k=2)
            good_points = []
            ratio = 0.6
            for m, n in matches:
                if m.distance < ratio * n.distance:
                    good_points.append(m)
            if (len(good_points) > 50):
                return True
        return False

    def downloadAllImages(content):
        print('> Downloading all images...')
        content['downloadedImages'] = []
        for sentenceIndex in range(len((content['sentences']))):
            images = content['sentences'][sentenceIndex]['images']
            for imageIndex in range(len(images)):
                imageUrl = images[imageIndex]
                blackList = loadBlackList()['blackList']
                
                if(imageUrl in (content['downloadedImages'] or blackList)):
                    print("> {} {} Erro imagem ja existe: {}".format(sentenceIndex,imageIndex,imageUrl))
                    continue
                elif(imageUrl in blackList):
                    print("> {} {} Erro imagem na Black List: {}".format(sentenceIndex,imageIndex,imageUrl))
                    continue
                elif(not(checkSupportImage(imageUrl))):
                    print("> {} {} Erro nao foi possivel abrir a imagem: {}".format(sentenceIndex,imageIndex,imageUrl))
                    continue
                elif(sentenceIndex>0):
                    if(checkDuplicatedImage(sentenceIndex, imageIndex, imageUrl)):
                        print("> {} {} Erro imagem duplicada: {}".format(sentenceIndex,imageIndex,imageUrl))
                        continue
#                 elif(viewImage(imageUrl)):
#                     print("> {} {} Erro imagem rejeitada: {}".format(sentenceIndex,imageIndex,imageUrl))
#                     continue
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