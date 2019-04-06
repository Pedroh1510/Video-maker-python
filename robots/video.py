from robots.state import loadContent, saveContent
from wand.image import Image
from wand.color import Color
from wand.font import Font
import sys

rootPath = sys.path[0]

def convertImage(sentenceIndex):
    inputFile = 'content/{}-original.png'.format(sentenceIndex)
    outputFile = 'content/{}-converted.png'.format(sentenceIndex)
    width = '1920'
    height = '1080'
    gm = Image(inputFile)
#     gm.blur(0x9)
    gm.backgroundColor('white')
    gm.resize((width+'x'+height))
#     gm.extent((str(width)+'x'+str(height)))
    try:
        gm.write(outputFile)
        print('> Image converted: {}'.format(inputFile))
    except RuntimeError:
        print('error {}'.format(sentenceIndex))
    
def convertAllImages(content):
    for sentenceIndex in range(len((content['sentences']))):
        print(sentenceIndex)
        convertImage(sentenceIndex)
        
def createSentenceImage(sentenceIndex, sentenceText):
    outputFile = './content/{}-sentence.png'.format(sentenceIndex)
    templateSettings = {
        0: {
          'size': '1920x400',
          'width': 1920,
          'height': 1080,
          'gravity': 'center'
        },
        1: {
          'size': '1920x1080',
          'width': 1920,
          'height': 1080,
          'gravity': 'center'
        },
        2: {
          'size': '800x1080',
          'width': 800,
          'height': 1080,
          'gravity': 'west'
        },
        3: {
          'size': '1920x400',
          'width': 1920,
          'height': 400,
          'gravity': 'center'
        },
        4: {
          'size': '1920x1080',
          'width': 1920,
          'height': 1080,
          'gravity': 'center'
        },
        5: {
          'size': '800x1080',
          'width': 800,
          'height': 1080,
          'gravity': 'west'
        },
        6: {
          'size': '1920x400',
          'width': 1920,
          'height': 400,
          'gravity': 'center'
        }
      }
    w = templateSettings[sentenceIndex]['width']
    h = templateSettings[sentenceIndex]['height']
    with Color('transparent') as bg:
        with Image(width=w,height=h, background=bg) as img:
            a = Font('./robots/fonts/verdana/Verdana.fft')
            img.caption(text= sentenceText,left= 15,top= 15,font= a)
            img.save(filename=outputFile)
            print('> Sentence created: {}'.format(outputFile))
    
def createAllSentenceImages(content):
    for sentenceIndex in range(len((content['sentences']))):
        createSentenceImage(sentenceIndex,content['sentences'][sentenceIndex]['text'])

def createYouTubeThumbnail(content):
    with Image(filename='./content/0-converted.png') as img:
        print('> Creating YouTube thumbnail')
        img.save(filename= 'content/youtube-thumbnail.jpg')
        
def renderVideoWithAfterEffects():
    aerender = 'C:\Program Files\Adobe\Adobe After Effects CS6'
    templateFilePath = '{}/templates/1/template.aep'.format(rootPath)
    destinationFilePath = '{}/content/output.mov'.format(rootPath)
    
def video():
    content = loadContent()
    convertAllImages(content)
    createAllSentenceImages(content)
    createYouTubeThumbnail(content)
    renderVideoWithAfterEffects()
    saveContent(content)