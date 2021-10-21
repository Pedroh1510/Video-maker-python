import json
contentFilePath = './content/content.json'
scriptFilePath = './content/after-effects-script.js'
blackListFilePath = './content/blackList/blackList.json'


def saveContent(content):
    with open(contentFilePath, 'w+', encoding='utf-8') as save:
        json.dump(content, save, ensure_ascii=False)


def loadContent():
    with open(contentFilePath, 'r', encoding='utf-8') as contentJson:
        return json.load(contentJson)


def saveScript(content):
    with open(scriptFilePath, 'w+', encoding='utf-8') as save:
        scriptString = 'var content = {}'.format(content)
        save.write(scriptString)


def loadBlackList():
    with open(blackListFilePath, 'r+') as contentJson:
        content = json.load(contentJson)
        return content


def saveBlackList(url):
    content = loadBlackList()
    content['blackList'].append(url)
    with open(blackListFilePath, 'w+') as save:
        json.dump(content, save)


def loadApikey(path):
    with open(path, 'r', encoding='utf-8') as contentJson:
        content = json.load(contentJson)
        return content


if __name__ == "__main__":
    saveContent('aaaaa')
