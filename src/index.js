import Image from './robots/images/index.js';
import TextWikipedia from './robots/text/index.js';
import UserInput from './robots/userInput/index.js';

async function main() {
	// const idInput = await new UserInput().run();
	// const idText = await new TextWikipedia().run({ inputId: idInput });
	await new Image().run({ textId: 1 });
}

main();
