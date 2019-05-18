from robots.userInput import user
from robots.text import robotText
from robots.voice import robotVoice
from robots.images import robotImages
from robots.video import robotVideo
from robots.youtube import robotYoutube
from robots.state import loadContent
import json
import sys

def start():
    user()
    robotText()
#     robotVoice()
    robotImages()
    robotVideo()
    robotYoutube()

print('> Start!')
start()
# print(json.dumps(loadContent()['sentences'], indent= 2))
print('> Terminated')
