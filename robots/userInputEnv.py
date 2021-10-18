from robots.state import saveContent
import os


def userEnv():
    def language():
        language = ['en', 'pt', 'pt-br']
        choose = getEnv('language')
        choose = language.index(choose)
        if(choose == -1):
            raise Exception("Language not accept")
        return language[choose]

    def getEnv(name=''):
        choose = os.environ[name]
        if(len(choose) == 0):
            raise Exception(f"{name} is empty")
        return choose

    content = {
        'language': language(),
        'searchTerm': getEnv('searchTerm'),
        'prefix': getEnv('prefix'),
        'maximumSentences': 7,
        'template': getEnv('template')
    }
    saveContent(content)
