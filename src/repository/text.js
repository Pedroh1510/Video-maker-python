import { PrismaClient } from '@prisma/client';

export default class TextRepository {
	#prisma = new PrismaClient();
	async save({ inputId, origin, content }) {
		const response = await this.#prisma.text.create({
			data: {
				content,
				origin,
				inputId
			}
		});
		return response;
	}
	async saveSentences({
		textId,
		sentences = [{ sentence: '', keywords: [''] }]
	}) {
		const formattedSentences = sentences.map(({ sentence, keywords }) => ({
			sentence,
			keywords: keywords.join(', ')
		}));
		for await (const item of formattedSentences) {
			await this.#prisma.sentence.create({
				data: {
					textId,
					...item
				}
			});
		}
	}
	async getSentencesByIdText(id) {
		return this.#prisma.sentence.findMany({
			where: {
				textId: id
			}
		});
	}
}
