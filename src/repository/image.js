import { PrismaClient } from '@prisma/client';

export default class ImageRepository {
	#prisma = new PrismaClient();
	async save({ images = [{ sentenceId: '', linkImages: [''] }] }) {
		for await (const item of images) {
			const { sentenceId, linkImages } = item;
			for await (const linkImage of linkImages) {
				await this.#prisma.image.create({
					data: {
						sentenceId: sentenceId,
						url: linkImage
					}
				});
			}
		}
	}

	async getImagesBySentenceId(sentenceId) {
		return this.#prisma.image.findMany({
			where: {
				sentenceId: sentenceId
			}
		});
	}

	async update({ images = [{ id: '', downloaded: false }] }) {
		for await (const item of images) {
			const { id, downloaded } = item;
			await this.#prisma.image.update({
				where: {
					id: id
				},
				data: {
					downloaded: downloaded
				}
			});
		}
	}
}
