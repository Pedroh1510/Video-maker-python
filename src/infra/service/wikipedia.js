import wiki from 'wikijs'

import logger from './logger.js'
const instanceWiki = wiki.default

export default class Wikipedia {
  #instance = instanceWiki
  constructor(lenguage = 'en') {
    this.lenguage = lenguage
    this.#instance = instanceWiki({
      apiUrl: `https://${lenguage}.wikipedia.org/w/api.php`,
    })
  }

  async searchTerm({ searchTerm }) {
    logger.debug('Buscando termo')
    return this.#instance.search(searchTerm, 1).then((data) => data.results)
  }

  async getContent({ searchTerm }) {
    logger.debug('Buscando conteúdo')
    return this.#instance.page(searchTerm).then(async (page) => {
      const content = await page.content()
      return {
        url: page.url(),
        summary: await page.summary(),
        content: content.map((line) => line.content).join('\n'),
      }
    })
  }
}
