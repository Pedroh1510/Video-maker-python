import logger from './infra/service/logger.js'
import CreateSentenceImage from './robots/createSentenceImage/index.js'
import Image from './robots/image/index.js'
import ImageFormatter from './robots/imageFormatter/index.js'
import TextWikipedia from './robots/text/index.js'
import UserInput from './robots/userInput/index.js'
import Video from './robots/video/index.js'
import Youtube from './robots/youtube/index.js'

async function main() {
  logger.info('Iniciando o programa')
  const inputId = await new UserInput().run()
  const start = performance.now()
  const textId = await new TextWikipedia().run({ inputId })
  await new Image().run({ textId })
  await new ImageFormatter().run()
  await new CreateSentenceImage().run({ textId })
  await new Video().run({ inputId })
  await new Youtube().run({ textId: 1 })
  const end = performance.now()
  logger.info(`Tempo de execução: ${(end - start) / 1000} segundos`)
  logger.info('Programa finalizado')
}

main()
