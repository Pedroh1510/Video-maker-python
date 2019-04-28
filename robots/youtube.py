from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from robots.state import loadContent
from http.server import HTTPServer, SimpleHTTPRequestHandler
from os.path import getsize


def robotYoutube():
    youtube = None
    def startWebServer():
        port = 5000
        server_address = ('', port) 
        handler_class = SimpleHTTPRequestHandler
        app = HTTPServer(server_address, handler_class)
        app.server_activate()
        return app
    
    def stopWebServer(webServer):
        webServer.server_close()
        
    def createOAuthClient():
        credentials  = './credential/youtubeC.json'
        SCOPES = ['https://www.googleapis.com/auth/youtube']
        OAuthClient = InstalledAppFlow.from_client_secrets_file(credentials, SCOPES)
        return OAuthClient
    
    def requestUserConsent(OAuthClient):
        credentials = OAuthClient.run_local_server(port= 5000,
                                                   success_message='''
                                                   Thank you!
                                                   Now close this tab.
                                                   ''',
                                                   access_type='offline',
                                                   include_granted_scopes='true'
                                                   )
        return credentials
    
    def setGlobalGoogleAuthentication(authorizationToken):
        youtube = build('youtube','v3',credentials=authorizationToken)
        return youtube
    
    def uploadVideo(content):
        def filtro(value=[]):
            return value['text']
        videoFilePath = './content/output.mov'
        videoFileSize = getsize(videoFilePath)
        videoTitle = '{} {}'.format(content['prefix'],content['searchTerm'])
        videoTags = [content['searchTerm']]
        videoTags.extend(content['sentences'][0]['keywords'])
        videoDescription = '\n\n'.join(list(map(filtro,content['sentences'])))
        
#         print('videoFilePath: '+videoFilePath)
#         print('videoFileSize: ',videoFileSize)
#         print('videoTitle: '+videoTitle)
#         print('videoTags: ',videoTags)
#         print('videoDescription: ',videoDescription)
        
        requestParameters = {
            'part': 'snippet, status',
            'requestBody': {
                'snippet': {
                    'title': videoTitle,
                    'description': videoDescription,
                    'tags': videoTags
                },
                'status': {
                    'privacyStatus': 'unlisted'
                }
            },
            'media': {
                'body': MediaFileUpload(videoFilePath, chunksize=-1, resumable=True)
            }
        }
        youtubeResponse = youtube.videos().insert(
            part= requestParameters['part'],
            body= requestParameters['requestBody'],
            media_body= requestParameters['media']['body']
            )
        print("Uploading file...")
        status, response = youtubeResponse.next_chunk()
        if 'id' in response:
            print('> Video available at: https://youtu.be/{}'.format(response['id']))
            return response['id']
        else:
            exit("The upload failed with an unexpected response: %s" % response)
            
    def uploadThumbnail(videoInformation):
        videoId = videoInformation['id']
        videoThumbnailFilePath = './content/youtube-thumbnail.jpg'
        
        requestParameters = {
            'videoId': videoId,
            'media': {
                'mimeType': 'image/jpeg',
                'body': MediaFileUpload(videoThumbnailFilePath, chunksize=-1, resumable=True)
                }
            }
        
        youtube.thumbnails().set(
            videoId= requestParameters['videoId'],
            media_body= requestParameters['media']['body']
            ).execute()
        
    OAuthClient = createOAuthClient()
    authorizationToken = requestUserConsent(OAuthClient)
    youtube = setGlobalGoogleAuthentication(authorizationToken)
#     content = loadContent()
#     videoInformation = uploadVideo(content)
    videoInformation = {
        'id': 'WsTqANx7E_E'
        }
    uploadThumbnail(videoInformation)