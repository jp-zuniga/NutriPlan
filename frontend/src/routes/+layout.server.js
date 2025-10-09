import { SESSION_ACCESS_COOKIE } from '$lib/cookies';
import { API_ME_ENDPOINT } from '$lib/endpoints.js';

export const load = async ({ cookies, fetch }) => {
	console.log(`Getting session cookie...`);

	const sessionCookie = cookies.get(SESSION_ACCESS_COOKIE);
	if (!sessionCookie) {
		console.log(`No session cookie`);
		return { user: null };
	}

	try {
		console.log(`Token obtained: ${sessionCookie}`);
		const response = await fetch(API_ME_ENDPOINT, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${sessionCookie}`
			}
		});

		if (response.ok) {
			const data = await response.json();
			console.log(`Response obtained: ${JSON.stringify(data)}`);
			return { user: data };
		} else return { user: null };
	} catch (err) {
		console.log(`Error setting user info: ${err}`);
		return { user: null };
	}
};
