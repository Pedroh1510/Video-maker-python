export function removeBlankLines(text = '') {
	return text
		.split('\n')
		.filter((line) => line.trim() !== '')
		.join('\n');
}

export function normalizeText(text = '') {
	return text.normalize('NFC');
}
