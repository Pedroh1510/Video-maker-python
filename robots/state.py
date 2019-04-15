import json
contentFilePath = 'content/content.json'
blackListFilePath = 'content/blackList/blackList.json'

def saveContent(content):
    with open(contentFilePath,'w') as save:
        json.dump(content,save)
def loadContent():
    with open(contentFilePath,'r') as contentJson:
        content = json.load(contentJson)
        return content
    
def saveBlackList(content):
    with open(blackListFilePath,'w') as save:
        json.dump(content,save)
def loadBlackList():
    with open(blackListFilePath,'r') as contentJson:
        content = json.load(contentJson)
        return content