import jimp from 'jimp'
import fs from 'node:fs/promises'
import path from 'node:path'

import logger from '../../infra/service/logger.js'
import { DIR } from '../utils/constants.js'
import { cleanDir, validateIfDirExistsOrCreate } from '../utils/functions.js'
import { FORMAT_IMAGE } from './utils/constants.js'

export default class ImageFormatter {
  async #getImagesPath(dir = '') {
    const files = await fs.readdir(dir)
    const images = new Set()
    for (const file of files) {
      const filePath = path.join(dir, file)
      const stats = await fs.stat(filePath)
      if (stats.isDirectory()) {
        const subImages = await this.#getImagesPath(filePath)
        images.add(...subImages)
      } else {
        images.add(filePath)
      }
    }
    return [...images]
  }

  async #getImages(dir = '') {
    logger.info(`Obtendo imagens do diretorio ${dir}`)
    const imagesPath = await this.#getImagesPath(dir)
    const images = new Set()
    for (const imagePath of imagesPath) {
      const image = await jimp.read(imagePath)
      images.add({ image, path: imagePath })
    }
    return [...images]
  }

  async #ajustImage(image, { width, height, quality }) {
    image.resize(width, height)
    if (quality) {
      image.quality(quality)
    }
    return image
  }

  async #ajustAllImages(
    images = [{ image: jimp.prototype }],
    { width, height, quality }
  ) {
    logger.info(`Ajustando imagens`)
    for await (const image of images) {
      await this.#ajustImage(image.image, { width, height, quality })
    }
    return images
  }

  async #saveImages(images = [{ image: jimp.prototype, path: '' }], dir = '') {
    logger.info(`Salvando imagens`)
    for (const image of images) {
      const imageName = path.basename(image.path)
      const imagePath = path.join(dir, imageName)
      await image.image.writeAsync(imagePath)
    }
  }

  async run() {
    logger.info('Iniciando formatação de imagens')
    const start = new Date().getTime()
    await validateIfDirExistsOrCreate(DIR.IMAGES_FORMATED)
    await cleanDir(DIR.IMAGES_FORMATED)
    const images = await this.#getImages(DIR.IMAGES_DOWNLOADED)
    const ajustedImages = await this.#ajustAllImages(images, FORMAT_IMAGE)
    await this.#saveImages(ajustedImages, DIR.IMAGES_FORMATED)
    const end = new Date().getTime()
    logger.info(
      `Formatação de imagens finalizada, tempo de execução: ${
        (end - start) / 1000
      }s`
    )
  }
}
