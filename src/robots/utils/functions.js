import path from 'node:path'
import fs from 'node:fs/promises'
import Jimp from 'jimp'

export async function validateIfDirExistsOrCreate(dir = '') {
  const dirExists = await fs.stat(dir).catch(() => false)
  if (!dirExists) {
    await fs.mkdir(dir, { recursive: true })
  }
}

export async function cleanDir(dir = '') {
  const files = await fs.readdir(dir)
  for (const file of files) {
    const filePath = path.join(dir, file)
    const stats = await fs.stat(filePath)
    if (stats.isDirectory()) {
      await cleanDir(filePath)
    } else {
      await fs.unlink(filePath)
    }
  }
}

export async function getImagesPath(dir = '') {
  const files = await fs.readdir(dir)
  const images = new Set()
  for (const file of files) {
    const filePath = path.join(dir, file)
    const stats = await fs.stat(filePath)
    if (stats.isDirectory()) {
      const subImages = await getImagesPath(filePath)
      images.add(...subImages)
    } else {
      images.add(filePath)
    }
  }
  return [...images]
}

export async function getImages(dir = '') {
  const imagesPath = await getImagesPath(dir)
  const images = new Set()
  for (const imagePath of imagesPath) {
    const image = await Jimp.read(imagePath)
    images.add({ image, path: imagePath })
  }
  return [...images]
}