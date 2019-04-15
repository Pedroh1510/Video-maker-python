from watson_developer_cloud import TextToSpeechV1
from credential.watsonC import ApiKeyTTS as watsonApiKey
from robots.state import saveContent,loadContent

def voice():
    text_to_speech = TextToSpeechV1(
            iam_apikey= watsonApiKey['iam_apikey'],
            url=watsonApiKey['url']
        )
    def sentencesToVoice(sentence,filename):
        output = './content/{}-audio.wav'.format(filename)
        try:
            with open(output, 'wb') as audio_file:
                audio_file.write(
                    text_to_speech.synthesize(
                sentence,
                voice='en-US_AllisonVoice',
                accept='audio/wav'        
            ).get_result().content)
            return True
        except:
            return False
        
    
    def fetchVoicesOfAllSentences(content):
        print('> Fetching voices of all sentences...')
        for i,item in enumerate(content['sentences']):
            content['sentences'][i]['audio'] = sentencesToVoice(content['sentences'][i]['text'],i)
        print('> Fetch voices of all sentences concluded')
        return content
    
    content = loadContent()
    fetchVoicesOfAllSentences(content)
    saveContent(content)