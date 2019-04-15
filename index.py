from robots.userInput import user
from robots.text import text
from robots.voice import voice
from robots.images import images
from robots.video import video

def start():
    user()
    text()
    voice()
    images()
    video()
    
print('Start!')
start()
print('Terminated')