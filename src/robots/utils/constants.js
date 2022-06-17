import path from 'node:path'

export const DIR = {
  IMAGES_DOWNLOADED: path.resolve('src', '..', 'images', 'downloads'),
  IMAGES_FORMATED: path.resolve('src', '..', 'images', 'formated'),
  SENTENCES: path.resolve('src', '..', 'images', 'sentences'),
  COMPOSITES: path.resolve('src', '..', 'images', 'composites'),
  VIDEO: path.resolve('src', '..', 'images', 'video'),
}

export const DEFAULT_IMAGE_FORMAT = '.png'
