import Google from '../../infra/service/google.js';
import ImageRepository from '../../repository/image.js';
import TextRepository from '../../repository/text.js';
import { TOTAL_IMAGES } from './utils/constants.js';
import fs from 'node:fs/promises';
import fsSync from 'node:fs';
import { compareImages, getBufferFromUrl } from './utils/functions.js';
import path from 'node:path';
import Jimp from 'jimp';

export default class Images {
	#textRepository = new TextRepository();
	#imageRepository = new ImageRepository();
	constructor(imageRepository = new ImageRepository()) {
		this.#imageRepository = imageRepository;
	}
	#getimagesLinkByQuery(query) {
		const google = new Google();
		return google.fetchImage(query);
	}

	async #getImagesPerSentence(sentence, keywords) {
		const listKeywords = keywords.split(', ');
		const linkImages = new Set();
		let totalImages = 0;
		let attempts = 0;
		let totalError = 0;
		do {
			const query = `${sentence} ${listKeywords[attempts]}`;
			try {
				const images = await this.#getimagesLinkByQuery(query);
				console.log({ images });
				images.forEach((image) => {
					if (!linkImages.has(image)) {
						linkImages.add(image);
						totalImages++;
					}
				});
			} catch (err) {
				console.log(err);
				totalError++;
				if (totalError > TOTAL_IMAGES.ATTEMPTS) {
					// throw new Error('Não foi possível obter imagens');
				}
			}
			attempts++;
		} while (
			totalImages < TOTAL_IMAGES.AMOUNT &&
			attempts < TOTAL_IMAGES.ATTEMPTS
		);
		return [...linkImages];
	}

	async #getImagesAllSentences(sentences = []) {
		const imagesPerSentence = [];
		for (const item of sentences) {
			const { sentence, keywords, id } = item;
			const linkImages = await this.#getImagesPerSentence(sentence, keywords);
			if (linkImages.length > 0) {
				imagesPerSentence.push({ linkImages, sentenceId: id });
			}
		}
		// if (sentences.length !== imagesPerSentence.length)
		// 	throw new Error('Não foi possível obter todas as imagens');
		return imagesPerSentence;
	}

	async #downloadImage(url) {
		const file = await Jimp.read(url);
		return file.getBufferAsync(Jimp.MIME_JPEG);
	}

	async #downloadAllImages(images = [{ id: '', url: '' }]) {
		const imagesDownloaded = [];
		for (const item of images) {
			const { id, url } = item;
			try {
				const file = await this.#downloadImage(url);
				imagesDownloaded.push({ file, id });
			} catch (error) {}
		}
		return imagesDownloaded;
	}

	async #getFilesByDir(dir) {
		const filesNames = await fs.readdir(dir);
		const files = [];
		for await (const file of filesNames) {
			const filePath = `${dir}/${file}`;
			const fileStat = await fs.stat(filePath);
			if (fileStat.isFile()) {
				files.push(await fs.readFile(filePath));
			}
		}
		return files;
	}

	async #checkImage(image = new File(), imageDownloaded = new File()) {
		if (await compareImages(image, imageDownloaded)) {
			return true;
		}
	}

	async #checkImages(image = new File(), dir = '') {
		const files = await this.#getFilesByDir(dir);
		for await (const file of files) {
			if (await this.#checkImage(image, file)) {
				return true;
			}
		}
		return false;
	}

	async #saveImageOnDir(image = Buffer.from(), sentenceId = '', dir = '') {
		return fs.writeFile(`${dir}/${sentenceId}.jpg`, image);
	}

	async #downloadImagesBySentenceId(sentenceId, dir = '') {
		const images = await this.#imageRepository.getImagesBySentenceId(
			sentenceId
		);
		const imagesDownloaded = await this.#downloadAllImages(images);
		for await (const image of imagesDownloaded) {
			const { file, id } = image;
			if (!(await this.#checkImages(file, dir))) {
				await this.#saveImageOnDir(file, sentenceId, dir);
				return id;
			}
		}
		return false;
	}

	#cleanDir(dir) {
		return fs.rm(dir + '/*', { force: true, recursive: true });
	}

	async #downloadImagesBySentences(sentences = []) {
		const dir = path.resolve('src', '..', 'images', 'downloads');
		await this.#cleanDir(dir);
		const imagesDownloaded = [];
		for (const sentence of sentences) {
			const { id } = sentence;
			const imageId = await this.#downloadImagesBySentenceId(id, dir);
			if (imageId) {
				imagesDownloaded.push({
					id: imageId,
					sentenceId: id,
					downloaded: true
				});
			}
		}
		return imagesDownloaded;
	}

	async run({ textId }) {
		console.log('Iniciando processamento de imagens...');
		const sentences = await this.#textRepository.getSentencesByIdText(textId);
		// const images = await this.#getImagesAllSentences(sentences);
		// await this.#imageRepository.save({ images });
		const images = await this.#downloadImagesBySentences(sentences);
		await this.#imageRepository.update({ images });

		console.log('Processamento de imagens finalizado.');
	}
}
