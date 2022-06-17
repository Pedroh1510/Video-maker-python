import Jimp from 'jimp'
import fs from 'node:fs/promises'
import path from 'node:path'

import TextRepository from '../../repository/text.js'
import { FORMAT_IMAGE } from '../ImageFormatter/utils/constants.js'
import { DIR } from '../utils/constants.js'
import { cleanDir, validateIfDirExistsOrCreate } from '../utils/functions.js'

export default class CreateSentenceImage {
  #textRepository = new TextRepository()

  async #createImage(text = '', { width, height, quality }) {
    const image = new Jimp(width, height)
    const font = await Jimp.loadFont(Jimp.FONT_SANS_64_WHITE)
    image.print(
      font,
      0,
      0,
      {
        text,
        alignmentX: Jimp.HORIZONTAL_ALIGN_CENTER,
        alignmentY: Jimp.VERTICAL_ALIGN_MIDDLE,
      },
      width,
      height
    )
    if (quality) {
      image.quality(quality)
    }
    return image
  }

  async #createImages(
    texts = [{ id: 1, sentence: '' }],
    { width, height, quality }
  ) {
    const images = []
    for (const text of texts) {
      const image = await this.#createImage(text.sentence, {
        width,
        height,
        quality,
      })
      images.push({ image, name: text.id })
    }
    return images
  }

  async #saveImages(images = [{ image: Jimp.prototype, name: '' }], dir = '') {
    for (const image of images) {
      const imageName = `${image.name}.jpeg`
      const imagePath = path.join(dir, imageName)
      const a = await image.image.getBufferAsync(Jimp.MIME_JPEG)
      await fs.writeFile(imagePath, a)
      // await image.image.write(imagePath)
    }
  }

  async run({ textId }) {
    await validateIfDirExistsOrCreate(DIR.SENTENCES)
    await cleanDir(DIR.SENTENCES)
    const sentences = await this.#textRepository.getSentencesByIdText(textId)
    const images = await this.#createImages(sentences, FORMAT_IMAGE)
    await this.#saveImages(images, DIR.SENTENCES)
  }
}
