from robots.sendDb import createAndSend
from robots.userInput import user
from robots.text import robotText
# # from robots.voice import robotVoice
from robots.images import robotImages
from robots.userInputEnv import userEnv
from robots.video import robotVideo
from robots.youtube import robotYoutube
from robots.state import loadContent



def start():
    print('> Start!')
    response = userEnv()
    if(response == None):
        return None
    # user()
    robotText()
    robotImages()
    robotVideo()
    robotYoutube()
    # robotVoice()
    createAndSend()
    print('> Terminated')


if __name__ == "__main__":
    start()
