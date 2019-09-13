from os.path import getsize
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from robots.state import loadContent


def robotYoutube():
    youtube = None
        
    def createOAuthClient():
        credentials  = './credential/youtubeC.json'
        SCOPES = ['https://www.googleapis.com/auth/youtube',
                  'https://www.googleapis.com/auth/yt-analytics.readonly']
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
        youtubeAnalytics = build('youtubeAnalytics','v2',credentials=authorizationToken)
        return youtube, youtubeAnalytics
    
    def uploadVideo(content):
        # def filtro(value=[]):
        #     return value['text']
        videoFilePath = './content/output.mp4'
        videoFileSize = getsize(videoFilePath)
        videoTitle = '{} {}'.format(content['prefix'],content['searchTerm'])
        videoTags = [content['searchTerm']]
        videoTags.extend(content['sentences'][0]['keywords'])
        # videoDescription = '\n\n'.join(list(map(filtro,content['sentences'])))
        videoDescription = '\n\n'.join([content['sentences'][i]['text'] for i in range(len(content['sentences']))])
        idealizer = 'https://www.youtube.com/channel/UCU5JicSrEM5A63jkJ2QvGYw'
        credits = '''\n\nCredits:
-Wikipedia: {}
-Images:
-{}
-{}
-{}
-{}
-{}
-{}
-{}
-Idealizer of the project: Filipe Deschamps
-{}
'''.format(content['wikipediaUrl'],
           content['downloadedImages'][0],
           content['downloadedImages'][1],
           content['downloadedImages'][2],
           content['downloadedImages'][3],
           content['downloadedImages'][4],
           content['downloadedImages'][5],
           content['downloadedImages'][6],
           idealizer)
        videoDescription += credits
        if content['template'] > 1:
            videoDescription += '\n-Music: https://www.bensound.com/royalty-free-music'
        
        requestParameters = {
            'part': 'snippet, status',
            'requestBody': {
                'snippet': {
                    'title': videoTitle,
                    'description': videoDescription,
                    'tags': videoTags
                },
                'status': {
                    'privacyStatus': 'public'
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
        print("> Uploading video file...")
        status, response = youtubeResponse.next_chunk()
        if 'id' in response:
            print('> Video available at: https://youtu.be/{}'.format(response['id']))
            return response['id']
        else:
            exit("The upload failed with an unexpected response: %s" % response)
            
    def uploadThumbnail(videoInformation):
        videoId = videoInformation
        videoThumbnailFilePath = './content/youtube-thumbnail.jpg'
        
        requestParameters = {
            'videoId': videoId,
            'media': {
                'mimeType': 'image/jpeg',
                'body': MediaFileUpload(videoThumbnailFilePath, chunksize=-1, resumable=True)
                }
            }
        print("> Uploading thumbnails file...")
        youtube.thumbnails().set(
            videoId= requestParameters['videoId'],
            media_body= requestParameters['media']['body']
            ).execute()
        print("> Uploaded thumbnails")
        
    def analitics(youtube):
        def execute_api_request(client_library_function, **kwargs):
            response = client_library_function(
              **kwargs
            ).execute()
            return response
#             print(response)
        return execute_api_request(
            youtubeAnalytics.reports().query,
            ids='channel==MINE',
            startDate='2019-04-28',
            endDate='2019-05-12',
            metrics='estimatedMinutesWatched,views,likes,subscribersGained',
            dimensions='day',
            sort='day'
            )
        
    def insertPlaylist(videoInformation):
        print("> Inserting into the playlist")
        videoID = videoInformation
        playlistID= 'PL771Qy0TVPUh9Vdnk7ezLpED0F3aAiz7Z'
        youtube.playlistItems().insert(
            part="snippet",
            body={
                'snippet': {
                    'playlistId': playlistID,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': videoID
                        }
                    }
                }).execute()
        print("> Inserted into the playlist")

    OAuthClient = createOAuthClient()
    authorizationToken = requestUserConsent(OAuthClient)
    youtube, youtubeAnalytics = setGlobalGoogleAuthentication(authorizationToken)
    content = loadContent()
#     content['analitics'] = analitics(youtube)
#     saveContent(content)
    videoInformation = uploadVideo(content)
    uploadThumbnail(videoInformation)
    insertPlaylist(videoInformation)