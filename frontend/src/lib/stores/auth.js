import { goto } from '$app/navigation';
import { SESSION_ACCESS_COOKIE, SESSION_REFRESH_COOKIE } from '$lib/cookies';
import { API_ME_ENDPOINT } from '$lib/endpoints';
import { writable, get } from 'svelte/store';

// export const userPromise = new Promise((resolve, reject) => {
// 	console.log(`Getting session cookie...`);
// });

export const authUser = writable(undefined);

export const redirectIfNull = () => {
	if (!get(authUser)) goto('/login');
};

export const setCookies = (access, refresh, { cookies }) => {
	if (access) {
		cookies.set(SESSION_ACCESS_COOKIE, access, {
			path: '/',
			httpOnly: true,
			sameSite: 'lax',
			secure: true,
			maxAge: 60 * 60 // 1h
		});
	}

	if (refresh) {
		cookies.set(SESSION_REFRESH_COOKIE, refresh, {
			path: '/',
			httpOnly: true,
			sameSite: 'lax',
			secure: true,
			maxAge: 60 * 60 * 24 * 7 // 7d
		});
	}
};

export const clearCookies = async ({ cookies }) => {
	cookies.delete(SESSION_ACCESS_COOKIE, { path: '/' });
	cookies.delete(SESSION_REFRESH_COOKIE, { path: '/' });
};

export const getUser = async ({ cookies }) => {
	const access = cookies.get(SESSION_ACCESS_COOKIE);
	const refresh = cookies.get(SESSION_REFRESH_COOKIE);

	try {
		const cookie_string = `${access ? SESSION_ACCESS_COOKIE + '=' + access : ''}${refresh ? ';' + SESSION_REFRESH_COOKIE + '=' + refresh : ''}`;

		console.log('Cookie string: \n' + cookie_string);
		const response = await fetch(API_ME_ENDPOINT, {
			method: 'GET',
			headers: {
				Cookie: cookie_string
			},
			credentials: 'include'
		}).catch((err) => {
			return { user: null, error: err };
		});

		if (response.ok) {
			const data = await response.json();
			setCookies(data.access, data.refresh, { cookies });
			return { user: data.user };
		} else {
			const data = await response.json();
			console.log(`Data obtained (failed): `, data);
			console.log(`Me auth returned error status ${response.status}, response body: `, response);
			return {
				user: null,
				error: data?.message ?? `Error desconocido, HTTP status: ${response.status}`
			};
		}
	} catch (err) {
		console.log(`Error setting user info: ${err}`);
		return { user: null, error: err };
	}
};
