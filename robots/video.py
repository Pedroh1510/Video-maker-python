import sys
from subprocess import Popen, PIPE, CalledProcessError
from robots.state import loadContent, saveContent, saveScript
from PIL import Image, ImageFilter, ImageDraw
import cv2
import numpy as np
import textwrap
import glob
import moviepy.editor as mp

rootPath = sys.path[0]

def robotVideo():
    
    def convertImage(sentenceIndex):
        def adjustImage(imageOriginal,widthDefault,heightDefault,proportionDefault):
            width = imageOriginal.size[0]
            height = imageOriginal.size[1]
            proportion = width / height
            adjustWidth = widthDefault/proportionDefault 
            adjustHeight = heightDefault/proportionDefault
            differenceWidth = width - widthDefault
            differenceHeight = height - heightDefault
            if round(proportion, 2) == round(proportionDefault, 2):
                imageOriginal.resize((int(widthDefault/proportionDefault), int(heightDefault/proportionDefault)))
            elif differenceWidth > differenceHeight:
                imageOriginal.resize((int(adjustWidth),int(height/proportion)))
            elif differenceWidth < differenceHeight:
                imageOriginal.resize((int(width/proportion),int(adjustHeight)))
            return imageOriginal

        inputFile = './content/{}-original.png'.format(sentenceIndex)
        outputFile = './content/{}-converted.png'.format(sentenceIndex)
        width = 1920
        height = 1080
        proportionDefault = width / height
        try:
            with Image.open(inputFile) as original:
                original = adjustImage(original,width,height,proportionDefault)
                size=[original.size[0]//2, original.size[1]//2]
                with original.copy() as copy:
                    copy = copy.resize((width,height))
                    copy = copy.filter(ImageFilter.GaussianBlur(5))
                    copy.paste(original,((width//2)-size[0],(height//2)-size[1]))
                    copy.save(outputFile)
                
            print('> Image converted: {}'.format(outputFile))
        except RuntimeError:
            print('error {}'.format(sentenceIndex))
        
    def convertAllImages(content):
        print('> Converting all images...')
        for sentenceIndex in range(len((content['sentences']))):
            convertImage(sentenceIndex)
        print('> Converting all images completed')
        
    def adjustFontSentence(text):
        sizeSentence = len(text)
        if sizeSentence>=150 and sizeSentence<=250:
            return 1.8
        if sizeSentence >= 250:
            return 1.3
        else:
            return 2

    def adjustTextWratSentence(sentenceText,w,h):
        sizeSentence = len(sentenceText)

        if w>=1080 and h == 1080:
            return 40
        if w<=900 and h==1080:
            return 20
        if w==1920 and h<=540:
            return 60
        else:
            return 20

    def writeText(filename, text,w,h):
        img = np.zeros((h, w, 4),dtype=np.uint8)
        height, width, channel = img.shape
        text_img = np.zeros((height, width,4))
        font = cv2.FONT_HERSHEY_TRIPLEX
        wrapped_text = textwrap.wrap(text, width=adjustTextWratSentence(text,width,height))
        x, y = 10, 40
        font_size = adjustFontSentence(text)
        font_thickness = 2
        
        i=0
        for line in wrapped_text:
            textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]
            
            gap = textsize[1] + 25
            y = int((img.shape[0] + textsize[1]) / 10) + i * gap
            x = int((img.shape[1] - textsize[0]) / 5)
            cv2.putText(img, line, (x, y), font,
                font_size, 
                (255,255,255,250),
                font_thickness, 
                lineType = cv2.LINE_AA)
            i+=1
        cv2.imwrite(filename,img)
            
    def createSentenceImage(sentenceIndex, sentenceText, templateIndex):
        outputFile = './content/{}-sentence.png'.format(sentenceIndex)
        templateSettings = {
            0: {
              'size': '1920x400',
              'width': 1920,
              'height': 400,
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
        writeText(outputFile,sentenceText,w,h)

    def createAllSentenceImages(content):
        print('> Creating all sentences images...')
        templateIndex = 0
        for sentenceIndex in range(len((content['sentences']))):
            if templateIndex > 6:
                templateIndex = 0
            createSentenceImage(sentenceIndex, content['sentences'][sentenceIndex]['text'], templateIndex)
            templateIndex += 1
        print('> Creating all sentences images completed')
    
    def createYouTubeThumbnail():
        print('> Creating YouTube thumbnail')
        with Image.open('./content/0-converted.png') as img:
            img.save('content/youtube-thumbnail.png',"PNG")
        print('> Created YouTube thumbnail')

    def createImageVideo(imageIndex,imageIndexOutput):
        inputImage = f'./content/{imageIndex}-converted.png'
        inputImageSentence = f'./content/{imageIndex}-sentence.png'
        outputFile = f'./content/final/image{imageIndexOutput}.png'
        originalImage = Image.open(inputImage,'r')
        originalImageSentence = Image.open(inputImageSentence,'r')
        text_img = Image.new('RGBA', (1920,1080), (0, 0, 0, 0))
        text_img.paste(originalImage, (0,0))
        img = Image.new('RGBA', (1920,1080), (0, 0, 0, 10))
        img.paste(originalImageSentence, (0,0), mask=originalImageSentence)
        text_img = Image.blend(img,text_img,.2)
        text_img.save(outputFile,'PNG')

    def createTransitionImage(imageIndex1, imageIndex2,imageIndexOutput,alph):
        alph /=60
        inputImage1 = f'./content/final/image{imageIndex1}.png'
        inputImage2 = f'./content/final/image{imageIndex2}.png'
        outputFile = f'./content/final/image{imageIndexOutput}.png'
        with Image.open(inputImage1) as firstImage:
            with Image.open(inputImage2) as secundImage:
                text_img = Image.blend(firstImage,secundImage,alpha=alph)
                text_img.save(outputFile,'PNG')

    def createAllImagesVideo():
        print('> Creating all images of video...')
        amountImages = len(glob.glob('./content/*-converted.png'))
        count = 15
        transitionPercert = count*0.25
        for imageIndex in range(amountImages):
            for i in range(count):
                if i<(count-transitionPercert):
                    a='{: 03d}-{: 04d}'.format(imageIndex,i)
                    createImageVideo(imageIndex,a)
        for imageIndex in range(amountImages):
            index=0
            for i in range(count):
                if i>=(count-transitionPercert):
                    image1='{: 03d}-{: 04d}'.format(imageIndex,0)
                    if imageIndex+1 in range(amountImages):
                        image2='{: 03d}-{: 04d}'.format(imageIndex+1,0)
                        outputName = '{: 03d}-{: 04d}'.format(imageIndex,i)
                        createTransitionImage(image1,image2,outputName,index)
                        index+=1
        print('> Creating all images of video completed')
    
    def createVideo():
        imgArray=[]
        files = glob.glob('./content/final/*.png')
        files.sort()
        with open('novoArquivo','w') as a:
            for i in files:
                a.write(f'{i}\n')
        for filename in files:
            img = cv2.imread(filename)
            imgArray.append(img)
        height, width, _ = imgArray[0].shape
        size = (width,height)
        out = cv2.VideoWriter('./content/final/project.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 24, size)
        for i in range(len(imgArray)):
            out.write(imgArray[i])
        out.release()

    def addAudioInVideo():
        file = "./templates/3/bensound-epic.mp3"
        video = mp.VideoFileClip("./content/final/project.mp4")
        audio = mp.AudioFileClip("./templates/3/bensound-epic.mp3")
        video = video.set_audio(audio.set_duration(video.duration))
        video.write_videofile("./content/final/project_audio.mp4")

    content = loadContent()
    convertAllImages(content)
    createAllSentenceImages(content)
    createYouTubeThumbnail()
    saveContent(content)
    createAllImagesVideo()
    createVideo()
    addAudioInVideo()
