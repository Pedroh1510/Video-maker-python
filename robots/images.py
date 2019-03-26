# from googleapiclient.discovery import build
from robots.state import saveContent,loadContent
from credential.googleSearch import googleSearchCredentials
import json

from apiclient.discovery import build

my_api_key = "AIzaSyC-uVWhk_GWhVknT9aM-aFn1MMsS8t9zsw"
my_cse_id = "007123468179688762635:bcdnztst0_o"


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

def images():
    content = loadContent()
    fetchImagesOfAllSentences(content)
    print(json.dumps(content,indent=2))
    saveContent(content)