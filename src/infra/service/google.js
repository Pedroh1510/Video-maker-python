import { google } from 'googleapis'

import CONFIG from '../config/env.js'
import logger from './logger.js'
export default class Google {
  async fetchImage(query) {
    logger.debug('Buscando imagem')
    const response = await google.customsearch('v1').cse.list({
      cx: CONFIG.GOOGLE_SEARCH_ENGINE_ID,
      q: query,
      auth: CONFIG.GOOGLE_SEARCH_API_KEY,
      searchType: 'image',
      num: 10,
      filter: '1',
    })
    if (response?.data?.items && response?.data?.items.length > 0) {
      return response.data.items.map((item) => item.link)
    }
    logger.error('Nenhuma imagem encontrada')
    throw new Error('Nenhuma imagem encontrada')
  }
}
