from robots.state import loadContent, saveContent, saveScript
from wand.image import Image, COMPOSITE_OPERATORS ,GRAVITY_TYPES
from wand.color import Color
from wand.font import Font
import subprocess
from subprocess import Popen, PIPE
import sys

rootPath = sys.path[0]

def convertImage(sentenceIndex):
    inputFile = './content/{}-original.png'.format(sentenceIndex)
    outputFile = './content/{}-converted.png'.format(sentenceIndex)
    center = GRAVITY_TYPES[5]
    width = 1920
    height = 1080
    try:
        with Image(filename=inputFile) as original:
            original.format = 'png'
            with original.clone() as copy:
                copy.resize(width= width, height= height)
                copy.blur(sigma= 0x9, radius= 0x9)
                copy.composite(original, gravity= center)
                copy.save(filename=outputFile)
#             with original.clone() as gm:
#                 gm.format = 'png'
#                 gm.sample(width,height)
#                 gm.save(filename=outputFile)
        print('> Image converted: {}'.format(inputFile))
    except RuntimeError:
        print('error {}'.format(sentenceIndex))
    
def convertAllImages(content):
    print('> Converting all images...')
    for sentenceIndex in range(len((content['sentences']))):
        convertImage(sentenceIndex)
    print('> Converting all images completed')
        
def createSentenceImage(sentenceIndex, sentenceText, templateIndex):
    outputFile = '{}-sentence.png'.format(sentenceIndex)
    templateSettings = {
        0: {
          'size': '1920x400',
          'width': 1920,
          'height': 1080,
          'gravity': 'center',
          'g': 5
        },
        1: {
          'size': '1920x1080',
          'width': 1920,
          'height': 1080,
          'gravity': 'center',
          'g': 5
        },
        2: {
          'size': '800x1080',
          'width': 800,
          'height': 1080,
          'gravity': 'west',
          'g': 4
        },
        3: {
          'size': '1920x400',
          'width': 1920,
          'height': 400,
          'gravity': 'center',
          'g': 5
        },
        4: {
          'size': '1920x1080',
          'width': 1920,
          'height': 1080,
          'gravity': 'center',
          'g': 5
        },
        5: {
          'size': '800x1080',
          'width': 800,
          'height': 1080,
          'gravity': 'west',
          'g': 4
        },
        6: {
          'size': '1920x400',
          'width': 1920,
          'height': 400,
          'gravity': 'center',
          'g': 5
        }
      }
    w = templateSettings[templateIndex]['width']
    h = templateSettings[templateIndex]['height']
#     with Color('transparent') as bg:
#         with Image(width=w,height=h, background=bg) as img:
#             color = Color('#000')
#             a = Font('./robots/fonts/verdana/Verdana.fft',size= 40, color=color)
#             img.font_color
#             img.caption(text= sentenceText,font= a,gravity= GRAVITY_TYPES[templateSettings[templateIndex]['g']])
#             img.save(filename=outputFile)
    command = '''cd content
    magick -size {} -gravity {} -background transparent -fill white -kerning -1 -caption:"{}" {}
    '''.format(templateSettings[templateIndex]['size'],templateSettings[templateIndex]['gravity'],sentenceText,outputFile)
    process = Popen( 'cmd.exe', shell=False, universal_newlines=True,stdin=PIPE, stdout=PIPE, stderr=PIPE )                             
    out, err = process.communicate( command )
    print(command)
    print('> Sentence {} created: {}'.format(sentenceIndex,outputFile))
    
def createAllSentenceImages(content):
    print('> Creating all sentences images...')
    templateIndex = 0
    for sentenceIndex in range(len((content['sentences']))):
        templateIndex += 1
        if(templateIndex>6):
            templateIndex = 0
        createSentenceImage(sentenceIndex, content['sentences'][sentenceIndex]['text'], templateIndex)
    print('> Creating all sentences images completed')

def createYouTubeThumbnail(content):
    print('> Creating YouTube thumbnail')
    with Image(filename='./content/0-converted.png') as img:
        img.convert('jpg')
        img.save(filename= 'content/youtube-thumbnail.jpg')
    print('> Created YouTube thumbnail')
    
def createAfterEffectsScript(content):
    saveScript(content)
        
def renderVideoWithAfterEffects():
    aerender = 'C:\Program Files\Adobe\Adobe After Effects CC 2019\Support Files'
    templateFilePath = '{}/templates/1/template.aep'.format(rootPath)
    destinationFilePath = '{}/content/output.mov'.format(rootPath)
    cmd = '''c:
cd "{}" 

aerender.exe -comp main -project "{}" -output "{}"
'''.format(aerender, templateFilePath, destinationFilePath)
    print('> Starting After Effects')
    try:
        process = Popen( "cmd.exe", shell=False, universal_newlines=True,
                         stdin=PIPE, stdout=PIPE, stderr=PIPE )                             
        out, err = process.communicate( cmd )
        print(out)
    except subprocess.CalledProcessError as e:                            
        print ("error code: {}".format(e.returncode))
    print('> Terminated After Effects')
    
def video():
    content = loadContent()
#     convertAllImages(content)
    createAllSentenceImages(content)
#     createYouTubeThumbnail(content)
#     createAfterEffectsScript(content)
#     renderVideoWithAfterEffects()
    saveContent(content)