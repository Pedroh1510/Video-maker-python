import Jimp from 'jimp'
import fs from 'node:fs/promises'
import path from 'node:path'
import videoshow from 'videoshow'

import InputRepository from '../../repository/input.js'
import { DEFAULT_IMAGE_FORMAT, DIR, VIDEO_NAME } from '../utils/constants.js'
import {
  cleanDir,
  getImages,
  getImagesPath,
  validateIfDirExistsOrCreate,
} from '../utils/functions.js'
import { VIDEO_OPTIONS } from './utils/constants.js'

export default class Video {
  #inputRepository = new InputRepository()
  async #compositeVideoImage(
    imageBackground = Jimp.prototype,
    imageForeground = Jimp.prototype
  ) {
    const background = await Jimp.read(imageBackground)
    const image = background.composite(imageForeground, 0, 0, {
      mode: Jimp.BLEND_SOURCE_OVER,
      opacitySource: 0.7,
      opacityDest: 0.5,
    })
    return image
  }

  #getFileNameWithoutExtension(filePath = '') {
    return path.basename(filePath).split('.')[0]
  }

  async #compositeVideoImages(dirImage = '', dirSentence = '') {
    const images = await getImages(dirImage)
    const imagesSentence = await getImages(dirSentence)
    if (!images.length) throw new Error('No images found')
    if (!imagesSentence.length) throw new Error('No images sentence found')
    const imagesComposite = []
    let previusImage = null
    for await (const imageSentence of imagesSentence) {
      const hasImage = images.find(
        (image) =>
          this.#getFileNameWithoutExtension(image.path) ===
          this.#getFileNameWithoutExtension(imageSentence.path)
      )
      if (hasImage) {
        previusImage = hasImage
        const imageComposite = await this.#compositeVideoImage(
          hasImage.image,
          imageSentence.image
        )
        imagesComposite.push({
          image: imageComposite,
          name: this.#getFileNameWithoutExtension(imageSentence.path),
        })
      } else {
        const image = previusImage || images[0]
        const imageComposite = await this.#compositeVideoImage(
          image.image,
          imageSentence.image
        )
        imagesComposite.push({
          image: imageComposite,
          name: this.#getFileNameWithoutExtension(imageSentence.path),
        })
      }
    }
    return imagesComposite
  }

  async #saveImages(images = [{ image: Jimp.prototype, name: '' }], dir = '') {
    for (const image of images) {
      const imagePath = path.join(dir, `${image.name}${DEFAULT_IMAGE_FORMAT}`)
      await image.image.writeAsync(imagePath)
    }
  }

  async #getAudioPath(inputId = 1) {
    const { template } = await this.#inputRepository.getById(inputId)
    if (!template) throw new Error('No template found')
    const templatePath = path.join(DIR.AUDIO, template)
    const dir = await fs.stat(templatePath)
    if (!dir.isDirectory()) throw new Error('No template found')
    const files = await fs.readdir(templatePath)
    for await (const file of files) {
      if (file.includes('.mp3')) return path.join(templatePath, file)
    }
    throw new Error('No audio found')
  }

  async #compositeVideo(dirImages = '', dir = '', audio = '') {
    const imagesPath = await getImagesPath(dirImages)
    return new Promise((resolve, reject) => {
      videoshow(imagesPath, {
        fps: VIDEO_OPTIONS.fps,
        loop: VIDEO_OPTIONS.imageDwellTime,
        transition: true,
        transitionDuration: VIDEO_OPTIONS.transitionDuration,
        videoBitrate: VIDEO_OPTIONS.videoBitrate,
        videoCodec: 'libx264',
        format: VIDEO_OPTIONS.format,
        pixelFormat: 'yuva420p',
        audioBitrate: VIDEO_OPTIONS.audioBitrate,
        audioChannels: VIDEO_OPTIONS.audioChannels,
      })
        .audio(audio)
        .save(path.join(dir, VIDEO_NAME))
        .on('start', function (command) {
          console.log('ffmpeg process started:', command)
        })
        .on('error', (err) => reject(err))
        .on('end', () => resolve())
    })
  }

  async run({ inputId }) {
    await validateIfDirExistsOrCreate(DIR.COMPOSITES)
    await validateIfDirExistsOrCreate(DIR.VIDEO)
    await cleanDir(DIR.COMPOSITES)
    await cleanDir(DIR.VIDEO)
    const imagesComposite = await this.#compositeVideoImages(
      DIR.IMAGES_FORMATED,
      DIR.SENTENCES
    )
    await this.#saveImages(imagesComposite, DIR.COMPOSITES)
    const audioPath = await this.#getAudioPath(inputId)
    await this.#compositeVideo(DIR.COMPOSITES, DIR.VIDEO, audioPath)
  }
}
