from robots.state import saveContent

def user():
    def askAndReturnSearchTerm():
        return str(input('Type a Wikipedia search term: '))
    def askAndReturnPrefix():
        def redLine(lista, text):
            for i in range(len(lista)):
                print('[',i,']',lista[i])
            return int(input(text))
        prefixes = ['Who is','What is','The history of']
        prefix = redLine(prefixes,'Choose a option: ')
        return prefixes[prefix]
    
    content={
      'searchTerm': askAndReturnSearchTerm(),
      'prefix': askAndReturnPrefix(),
      'maximumSentences': 7
      }
    saveContent(content)