import path from 'node:path'

import Google from '../../infra/service/google.js'
import logger from '../../infra/service/logger.js'
import InputRepository from '../../repository/input.js'
import { DIR, VIDEO_NAME } from '../utils/constants.js'

export default class Youtube {
  #google = new Google()
  #inputRepository = new InputRepository()
  async #uploadVideo(dir = '', info = {}) {
    logger.info('Fazendo upload do vídeo')
    const videoPath = path.join(dir, VIDEO_NAME)
    return this.#google.uploadYoutubeVideo(videoPath, info)
  }

  #makeVideoInfo(input) {
    const { searchTerm, prefix, Text } = input
    if (!Array.isArray(Text)) throw new Error('Texto não é um array')
    const info = {
      description: '',
      tags: [searchTerm],
      title: `${prefix} ${searchTerm}`
        .split(' ')
        .map((w) => (w[0].toUpperCase() + w.substring(1).toLowerCase()).trim())
        .join(' '),
    }
    for (const text of Text) {
      if (!Array.isArray(text.Sentences))
        throw new Error('Sentenças não encontradas')
      const url = []
      for (const sentence of text.Sentences) {
        if (!sentence.sentence) throw new Error('Sentença não encontrada')
        if (info.description === '') info.description = sentence.sentence
        else info.description += `, ${sentence.sentence}`
        for (const image of sentence.image) {
          if (image.url) url.push(image.url)
        }
        info.tags.push(...sentence.keywords.split(', '))
      }
      info.description += `\n\ntext font:\n${
        text.origin
      }\n\nimages fonts: \n${url.join('\n')}`
    }
    return info
  }

  async run({ textId }) {
    logger.info('Iniciando processo de envio do vídeo')
    const start = performance.now()

    const fullInformation = await this.#inputRepository.getInfoToVideoById(
      textId
    )
    const videoInfo = this.#makeVideoInfo(fullInformation)
    const videoId = await this.#uploadVideo(DIR.VIDEO, videoInfo)
    const end = performance.now()
    logger.info(
      `Finalizado com sucesso. Tempo de execução: ${(end - start) / 1000}s`
    )
    return videoId
  }
}
