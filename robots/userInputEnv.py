from robots.state import saveContent
import os

from utils.db import getVideo
from utils.functions import getEnv

def userEnv():
    def language():
        language = ['en', 'pt', 'pt-br']
        choose = getEnv('language')
        choose = language.index(choose)
        if(choose == -1):
            raise Exception("Language not accept")
        return language[choose]

    if(getEnv('db')==None):
        content = {
            'language': language(),
            'searchTerm': getEnv('searchTerm'),
            'prefix': getEnv('prefix'),
            'maximumSentences': 7,
            'template': getEnv('template')
        }
    else:
        video = getVideo()
        if(video == None):
            return None
        content = {
            'language': 'pt',
            'searchTerm': video['sugestao'],
            'idSearchTerm': video['id'],
            'prefix': "",
            'maximumSentences': 7,
            'template': 1
        }
    saveContent(content)
    return content
