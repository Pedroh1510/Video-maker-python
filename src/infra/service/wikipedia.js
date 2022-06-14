import wiki from 'wikijs';
const instanceWiki = wiki.default;

export default class Wikipedia {
	#instance = instanceWiki;
	constructor(lenguage = 'en') {
		this.lenguage = lenguage;
		this.#instance = instanceWiki({
			apiUrl: `https://${lenguage}.wikipedia.org/w/api.php`
		});
	}

	async searchTerm({ searchTerm }) {
		return this.#instance.search(searchTerm, 1).then((data) => data.results);
	}

	async getContent({ searchTerm }) {
		return this.#instance.page(searchTerm).then(async (page) => {
			const content = await page.content();
			return {
				url: page.url(),
				summary: await page.summary(),
				content: content.map((line) => line.content).join('\n')
			};
		});
	}
}
