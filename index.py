import os
from robots.userInput import user
from robots.text import robotText
# # from robots.voice import robotVoice
from robots.images import robotImages
from robots.userInputEnv import userEnv
from robots.video import robotVideo
from robots.youtube import robotYoutube
from robots.state import loadContent
import json


def start():
    try:
        userEnv()
    except:
        user()
    robotText()
    robotImages()
    robotVideo()
    robotYoutube()
    # robotVoice()


if __name__ == "__main__":
    print('> Start!')
    start()
    # print(json.dumps(loadContent()['sentences'], indent=2))
    # print(json.dumps(loadContent()['sentences']))
    print('> Terminated')
