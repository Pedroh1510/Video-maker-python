from robots.state import saveContent

def user():
    def askAndReturnSearchTerm():
        return str(input('Type a Wikipedia search term: ')).title()
    
    def redLine(lista, text):
        for i in range(len(lista)):
            print('[',i,']',lista[i])
        return int(input(text))
    
    def askAndReturnPrefix(language):
        if(language=='en'):
            prefixes = ['Who is','What is','The history of']
        else:
            prefixes = ['Quem é', 'Oque é', 'A história de']
        prefix = redLine(prefixes,'Choose a option: ')
        return prefixes[prefix]
    def askAndReturnTemplate():
        prefixes = ['Know the world ','Senta que la vem historia - newsroom',
                    'Senta que la vem historia - music epic',
                    'Senta que la vem historia - music evolution',
                    'Senta que la vem historia - music Missing My Girl']
        prefix = redLine(prefixes,'Choose a Template option: ')
        return prefix+1
    def askAndReturnLanguage():
        prefixes = ['English','Portuguese']
        language = ['en','pt']
        prefix = redLine(prefixes,'Choose a Language option: ')
        return language[prefix]
    
    language = askAndReturnLanguage()
    
    content={
        'language': language,
        'searchTerm': askAndReturnSearchTerm(),
        'prefix': askAndReturnPrefix(language),
        'maximumSentences': 7,
        'template': askAndReturnTemplate()
        }
    saveContent(content)
