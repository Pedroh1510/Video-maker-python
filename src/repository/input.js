import { PrismaClient } from '@prisma/client';

export default class InputRepository {
	#prisma = new PrismaClient();
	async save(data) {
		const { lenguage, searchTerm, prefix, template, maxSentences } = data;
		const newData = {
			lenguage,
			searchTerm,
			prefix,
			template,
			maxSentences
		};
		const response = await this.#prisma.input.create({ data: newData });
		return response;
	}
	async getById(id) {
		return this.#prisma.input.findFirst({
			where: {
				id
			}
		});
	}
}
