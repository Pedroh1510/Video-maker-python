
from robots.state import loadContent
from utils.db import createVideoAndUpdateChat
from utils.functions import getEnv, sendRequestConcluded


def createAndSend():
    if(getEnv('db')!=None):
        content = loadContent()
        video = {
            'idChat': content['idSearchTerm'],
            'urlVideo': content['urlVideo'],
            'titleVideo': content['titleVideo']
        }
        chat = {
            'id': content['idSearchTerm'],
            'status': 'Concluido'
        }
        videoId =  createVideoAndUpdateChat(None, video, chat)
        sendRequestConcluded(videoId)