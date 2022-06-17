import CreateSentenceImage from './robots/createSentenceImage/index.js'
import Image from './robots/image/index.js'
import ImageFormatter from './robots/imageFormatter/index.js'
import TextWikipedia from './robots/text/index.js'
import UserInput from './robots/userInput/index.js'
import Video from './robots/video/index.js'

async function main() {
  const inputId = await new UserInput().run()
  const textId = await new TextWikipedia().run({ inputId })
  await new Image().run({ textId })
  await new ImageFormatter().run()
  await new CreateSentenceImage().run({ textId })
  await new Video().run({ inputId })
}

main().finally(() => process.exit())
