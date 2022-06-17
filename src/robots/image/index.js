import Jimp from 'jimp'
import fs from 'node:fs/promises'
import path from 'node:path'

import Google from '../../infra/service/google.js'
import logger from '../../infra/service/logger.js'
import BlacklistRepository from '../../repository/blacklist.js'
import ImageRepository from '../../repository/image.js'
import TextRepository from '../../repository/text.js'
import { DIR } from '../utils/constants.js'
import { cleanDir, validateIfDirExistsOrCreate } from '../utils/functions.js'
import { TOTAL_IMAGES } from './utils/constants.js'
import { compareImages } from './utils/functions.js'

export default class Images {
  #textRepository = new TextRepository()
  #imageRepository = new ImageRepository()
  #blacklistRepository = new BlacklistRepository()
  #google = new Google()
  constructor(imageRepository = new ImageRepository()) {
    this.#imageRepository = imageRepository
  }

  #getimagesLinkByQuery(query) {
    return this.#google.fetchImage(query)
  }

  async #getImagesPerSentence(sentence, keywords) {
    const listKeywords = keywords.split(', ')
    const linkImages = new Set()
    let totalImages = 0
    let attempts = 0
    let totalError = 0
    do {
      const query = `${sentence} ${listKeywords[attempts]}`
      try {
        const images = await this.#getimagesLinkByQuery(query)
        images.forEach((image) => {
          if (!linkImages.has(image)) {
            linkImages.add(image)
            totalImages++
          }
        })
      } catch (err) {
        logger.error(err)
        totalError++
        if (totalError > TOTAL_IMAGES.ATTEMPTS) {
          // throw new Error('Não foi possível obter imagens');
        }
      }
      attempts++
    } while (
      totalImages < TOTAL_IMAGES.AMOUNT &&
      attempts < TOTAL_IMAGES.ATTEMPTS
    )
    return [...linkImages]
  }

  async #getImagesAllSentences(sentences = []) {
    const imagesPerSentence = []
    for (const item of sentences) {
      const { sentence, keywords, id } = item
      const linkImages = await this.#getImagesPerSentence(sentence, keywords)
      if (linkImages.length > 0) {
        imagesPerSentence.push({ linkImages, sentenceId: id })
      }
    }
    return imagesPerSentence
  }

  async #downloadImage(url) {
    const file = await Jimp.read(url)
    return file.getBufferAsync(Jimp.MIME_JPEG)
  }

  async #downloadAllImages(images = [{ id: '', url: '' }]) {
    const imagesDownloaded = []
    for (const item of images) {
      const { id, url } = item
      try {
        const file = await this.#downloadImage(url)
        imagesDownloaded.push({ file, id, url })
      } catch (error) {}
    }
    return imagesDownloaded
  }

  async #getFilesByDir(dir) {
    const filesNames = await fs.readdir(dir)
    const files = []
    for await (const file of filesNames) {
      const filePath = path.join(dir, file)
      const fileStat = await fs.stat(filePath)
      if (fileStat.isFile()) {
        files.push(await fs.readFile(filePath))
      }
    }
    return files
  }

  async #checkImage(image, imageDownloaded) {
    if (await compareImages(image, imageDownloaded)) {
      return true
    }
  }

  async #checkImages(image, dir = '') {
    const files = await this.#getFilesByDir(dir)
    for await (const file of files) {
      if (await this.#checkImage(image, file)) {
        return true
      }
    }
    return false
  }

  async #checkImageInBlacklist(image, urlImage = '') {
    const blacklist = await this.#blacklistRepository.getAll()
    for await (const item of blacklist) {
      const { url } = item
      if (url === urlImage) {
        return true
      }
      const imageBlacklist = await this.#downloadImage(url)
      if (await this.#checkImage(image, imageBlacklist)) {
        return true
      }
    }
    return false
  }

  async #saveImageOnDir(image = Buffer.from(), sentenceId = '', dir = '') {
    return fs.writeFile(`${dir}/${sentenceId}.jpg`, image)
  }

  async #downloadImagesBySentenceId(sentenceId, dir = '') {
    const images = await this.#imageRepository.getImagesBySentenceId(sentenceId)
    const imagesDownloaded = await this.#downloadAllImages(images)
    for await (const image of imagesDownloaded) {
      const { file, id, url } = image
      if (!(await this.#checkImages(file, dir))) {
        await this.#saveImageOnDir(file, sentenceId, dir)
        return id
      } else if (await this.#checkImageInBlacklist(file, url)) {
        return id
      }
    }
    return false
  }

  async #downloadImagesBySentences(sentences = []) {
    logger.info('Baixando imagens')
    await validateIfDirExistsOrCreate(DIR.IMAGES_DOWNLOADED)
    await cleanDir(DIR.IMAGES_DOWNLOADED)
    const imagesDownloaded = []
    for (const sentence of sentences) {
      const { id } = sentence
      const imageId = await this.#downloadImagesBySentenceId(
        id,
        DIR.IMAGES_DOWNLOADED
      )
      if (imageId) {
        imagesDownloaded.push({
          id: imageId,
          sentenceId: id,
          downloaded: true,
        })
      }
    }
    return imagesDownloaded
  }

  async run({ textId }) {
    logger.info('Iniciando processamento de imagens')
    const start = new Date().getTime()
    const sentences = await this.#textRepository.getSentencesByIdText(textId)
    const images = await this.#getImagesAllSentences(sentences)
    await this.#imageRepository.save({ images })
    const imagesDownloaded = await this.#downloadImagesBySentences(sentences)
    await this.#imageRepository.update({ images: imagesDownloaded })
    const end = new Date().getTime()
    logger.info(
      `Finalizado processamento de imagens. Tempo de execução: ${
        (end - start) / 1000
      }s`
    )
  }
}
