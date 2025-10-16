import { goto } from '$app/navigation';
import { API_ME_ENDPOINT } from '$lib/endpoints';
import { writable, get } from 'svelte/store';

// export const userPromise = new Promise((resolve, reject) => {
// 	console.log(`Getting session cookie...`);
// });

export const authUser = writable(undefined);

export const redirectIfNull = () => {
	if (!get(authUser)) goto('/login');
};

export const getUser = async () => {
	console.log(`Getting session cookie...`);

	try {
		const response = await fetch(API_ME_ENDPOINT, {
			method: 'GET',
			credentials: 'include'
		});

		if (response.ok) {
			const data = await response.json();
			console.log(`Response obtained: ${JSON.stringify(data)}`);
			return { user: data };
		} else {
			const data = await response.json();
			console.log(`Data obtained (failed): `, data);
			console.log(`Me auth returned error status ${response.status}, response body: `, response);
			return { user: null };
		}
	} catch (err) {
		console.log(`Error setting user info: ${err}`);
		return { user: null };
	}
};
