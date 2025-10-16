export function extractDirectImage(url) {
	const possible_params = ['imgurl', 'imgrefurl', 'url'];
	try {
		const u = new URL(url);

		let raw = null;

		for (let param of possible_params) {
			raw = u.searchParams.get(param);
			if (raw) break;
		}
		return raw ? decodeURIComponent(raw) : url;
	} catch {
		return url;
	}
}
