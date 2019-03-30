import json
contentFilePath = 'content/content.json'

def saveContent(content):
    with open(contentFilePath,'w') as save:
        json.dump(content,save)
def loadContent():
    with open(contentFilePath,'r') as contentJson:
        content = json.load(contentJson)
        return content