from pgmagick.api import Image
from robots.state import loadContent

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
    gm = Image((templateSettings[sentenceIndex]['width'],templateSettings[sentenceIndex]['height']), 'transparent')
#     gm.backgroundColor('transparent')
#     gm.orientation(templateSettings[sentenceIndex]['gravity'])
    gm.annotate(sentenceText,gravity=templateSettings[sentenceIndex]['gravity'])
#     gm.fillColor('white')
    gm.write(outputFile)
    
def createAllSentenceImages(content):
    for sentenceIndex in range(len((content['sentences']))):
        createSentenceImage(sentenceIndex,content['sentences'][sentenceIndex]['text'])
    
    
def video():
    content = loadContent()
#     convertAllImages(content)
    createAllSentenceImages(content)