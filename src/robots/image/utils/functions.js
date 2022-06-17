import https from 'https'
import Jimp from 'jimp'

export async function compareImages(image1File, image2File) {
  const image1 = await Jimp.read(image1File)
  const image2 = await Jimp.read(image2File)
  // Perceived distance
  const distance = Jimp.distance(image1, image2)
  // Pixel difference
  const diff = Jimp.diff(image1, image2)
  if (distance < 0.15 || diff.percent < 0.15) {
    return true
  }
  return false
}

export async function getBufferFromUrl(url) {
  return new Promise((resolve) => {
    https.get(url, (response) => {
      const body = []
      response
        .on('data', (chunk) => {
          body.push(chunk)
        })
        .on('end', () => {
          resolve(Buffer.concat(body))
        })
        .on('error', (error) => {
          console.error(error)
        })
    })
  })
}
