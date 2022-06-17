import { authenticate } from '@google-cloud/local-auth'
import { google } from 'googleapis'
import fs from 'node:fs'

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

  async login() {
    logger.info('Iniciando login')
    return authenticate({
      scopes: [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube',
      ],
      keyfilePath: CONFIG.GOOGLE_CLIENT_SECRET_PATH,
    })
  }

  async uploadYoutubeVideo(videoPath, { title, description, tags }) {
    console.log(title)
    const auth = await this.login()
    google.options({ auth })
    logger.info('Iniciando upload do vídeo')
    const youtube = google.youtube({
      version: 'v3',
      key: CONFIG.GOOGLE_YOUTUBE_API_KEY,
    })
    const response = await youtube.videos.insert({
      part: 'id,snippet,status',
      notifySubscribers: false,
      requestBody: {
        snippet: {
          title,
          description,
          tags,
          publishedAt: new Date().toISOString(),
        },
        status: {
          privacyStatus: 'private',
        },
      },
      media: {
        body: fs.createReadStream(videoPath),
      },
    })
    if (response?.data?.id) {
      return response.data.id
    }
    logger.error('Falha ao fazer upload do vídeo')
  }
}
