import Jimp from 'jimp'
import path from 'node:path'
import { DEFAULT_IMAGE_FORMAT, DIR } from '../utils/constants.js'
import {
  cleanDir,
  getImages,
  getImagesPath,
  validateIfDirExistsOrCreate,
} from '../utils/functions.js'
import videoshow from 'videoshow'

export default class Video {
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

  async #compositeVideo(dirImages = '', nameVideo = '', dir = '') {
    const imagesPath = await getImagesPath(dirImages)
    return new Promise((resolve, reject) => {
      videoshow(imagesPath, {
        fps: 30,
        loop: 8,
        transition: true,
        transitionDuration: 1,
        videoBitrate: 1024,
        videoCodec: 'libx264',
        // size: '1280x720',
        format: 'mp4',
        // pixelFormat: 'argb',
        pixelFormat: 'yuva420p',
      })
        .save(path.join(dir, `${nameVideo}.mp4`))
        .on('start', function (command) {
          console.log('ffmpeg process started:', command)
        })
        .on('error', (err) => reject(err))
        .on('end', () => resolve())
    })
  }

  async run() {
    await validateIfDirExistsOrCreate(DIR.COMPOSITES)
    await validateIfDirExistsOrCreate(DIR.VIDEO)
    await cleanDir(DIR.COMPOSITES)
    await cleanDir(DIR.VIDEO)
    const imagesComposite = await this.#compositeVideoImages(
      DIR.IMAGES_FORMATED,
      DIR.SENTENCES
    )
    await this.#saveImages(imagesComposite, DIR.COMPOSITES)
    await this.#compositeVideo(DIR.COMPOSITES, 'video', DIR.VIDEO)
  }
}
