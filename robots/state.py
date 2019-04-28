import json
contentFilePath = './content/content.json'
scriptFilePath = './content/after-effects-script.js'
blackListFilePath = './content/blackList/blackList.json'

def saveContent(content):
    with open(contentFilePath,'w') as save:
        json.dump(content,save)
def loadContent():
    with open(contentFilePath,'r') as contentJson:
        content = json.load(contentJson)
        return content

def saveScript(content):
    with open(scriptFilePath,'w') as save:
        scriptString = 'var content = {}'.format(content)
        save.write(scriptString)
    
def saveBlackList(content):
    with open(blackListFilePath,'w') as save:
        json.dump(content,save)
def loadBlackList():
    with open(blackListFilePath,'r') as contentJson:
        content = json.load(contentJson)
        return content