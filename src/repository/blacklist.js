import { PrismaClient } from '@prisma/client';

export default class BlacklistRepository {
	#prisma = new PrismaClient();
	async getAll() {
		return this.#prisma.blacklist.findMany({ select: { url: true } });
	}
}
