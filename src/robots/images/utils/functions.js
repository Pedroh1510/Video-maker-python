import Jimp from 'jimp';

export async function compareImages(image1File, image2File) {
	const image1 = await Jimp.read(image1File);
	const image2 = await Jimp.read(image2File);
	// Perceived distance
	const distance = Jimp.distance(image1, image2);
	// Pixel difference
	const diff = Jimp.diff(image1, image2);

	console.log(
		`compareImages: distance: ${distance.toFixed(
			3
		)}, diff.percent: ${diff.percent.toFixed(3)}`
	);
	if (distance < 0.15 || diff.percent < 0.15) {
		console.log('compareImages: Images match!');
		return true;
	}
	console.log('compareImages: Images do NOT match!');
	return false;
}

import https from 'https';

export async function getBufferFromUrl(url) {
	return new Promise((resolve) => {
		https.get(url, (response) => {
			const body = [];
			response
				.on('data', (chunk) => {
					body.push(chunk);
				})
				.on('end', () => {
					resolve(Buffer.concat(body));
				})
				.on('error', (error) => {
					console.error(error);
				});
		});
	});
}
