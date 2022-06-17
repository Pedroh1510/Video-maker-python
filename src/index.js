// import Image from './robots/image/index.js'
// import CreateSentenceImage from './robots/CreateSentenceImage/index.js'
// import ImageFormatter from './robots/ImageFormatter/index.js'
import Video from './robots/video/index.js'
// import TextWikipedia from './robots/text/index.js'
// import UserInput from './robots/userInput/index.js'

async function main() {
  // const idInput = await new UserInput().run();
  // const idText = await new TextWikipedia().run({ inputId: idInput });
  // await new Image().run({ textId: 1 })
  // await new ImageFormatter().run()
  // await new CreateSentenceImage().run(1)
  await new Video().run({ inputId: 1 })
}

main()
