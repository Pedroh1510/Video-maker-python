import mysql.connector
from robots.state import loadApikey
dbCredential = loadApikey('./credential/db.json')

def connect():
    return mysql.connector.connect(
        host=dbCredential['host'],
        user=dbCredential['user'],
        password=dbCredential['password'],
        database=dbCredential['database'],
        port=dbCredential['port']
    )

def tupleToDict(tuple):
    if(len(tuple) == 0):
        return None
    return {
        'id': tuple[0][0],
        'sugestao': tuple[0][1]
    }

def getVideoPending(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, sugestao FROM chat WHERE status = 'Pendente' LIMIT 1")
    videos = cursor.fetchall()
    return tupleToDict(videos)

def updateChatVideoStatus(conn, chat, status,autoCommint=True):
    if(conn==None):
        conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE chat SET status = %s, videoId = %s WHERE id = %s", (status, chat['videoId'],chat['id']))
    if(autoCommint):
        conn.commit()

def createVideo(conn, video,autoCommint=True):
    if(conn==None):
        conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO video (url,idChat,titulo) VALUES (%s,%s,%s)", (video['urlVideo'], video['idChat'], video['titleVideo']))
    if(autoCommint):
        conn.commit()
    return cursor.lastrowid

def createVideoAndUpdateChat(conn, video,chat):
    if(conn==None):
        conn = connect()
    videoId = createVideo(conn, video)
    chat['videoId'] = videoId
    updateChatVideoStatus(conn, chat, chat['status'])
    conn.commit()
    return videoId

def getVideo():
    videos = getVideoPending(connect())
    if(videos == None):
        return None
    return videos


