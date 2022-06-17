import path from 'node:path'
import { VIDEO_OPTIONS } from '../video/utils/constants.js'

export const DIR = {
  IMAGES_DOWNLOADED: path.resolve('src', '..', 'images', 'downloads'),
  IMAGES_FORMATED: path.resolve('src', '..', 'images', 'formated'),
  SENTENCES: path.resolve('src', '..', 'images', 'sentences'),
  COMPOSITES: path.resolve('src', '..', 'images', 'composites'),
  VIDEO: path.resolve('src', '..', 'images', 'video'),
  AUDIO: path.resolve('src', '..', 'templates'),
}

export const DEFAULT_IMAGE_FORMAT = '.png'

export const VIDEO_NAME = `video.${VIDEO_OPTIONS.format}`
