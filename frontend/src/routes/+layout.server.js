// import { SESSION_ACCESS_COOKIE, SESSION_REFRESH_COOKIE } from '$lib/cookies.js';
// import { API_ME_ENDPOINT } from '$lib/endpoints.js';
import { getUser } from '$lib/stores/auth.js';

export const load = async ({ cookies }) => {
	return await getUser({ cookies });
	// const access = cookies.get(SESSION_ACCESS_COOKIE);
	// const refresh = cookies.get(SESSION_REFRESH_COOKIE);

	// console.log(SESSION_ACCESS_COOKIE + ': ' + access);
	// console.log(SESSION_REFRESH_COOKIE + ': ' + refresh);

	// try {
	// 	const cookie_string = `${access ? SESSION_ACCESS_COOKIE + '=' + access : ''}${refresh ? ';' + SESSION_REFRESH_COOKIE + '=' + refresh : ''}`;

	// 	console.log('Cookie string: \n' + cookie_string);
	// 	const response = await fetch(API_ME_ENDPOINT, {
	// 		method: 'GET',
	// 		headers: {
	// 			Authorization: `Bearer ${access}`,
	// 			Cookie: cookie_string
	// 		},
	// 		credentials: 'include'
	// 	});

	// 	if (response.ok) {
	// 		const data = await response.json();
	// 		console.log(`Response obtained: ${JSON.stringify(data)}`);
	// 		return { user: data };
	// 	} else {
	// 		const data = await response.json();
	// 		console.log(`Data obtained (failed): `, data);
	// 		console.log(`Me auth returned error status ${response.status}, response body: `, response);
	// 		return { user: null };
	// 	}
	// } catch (err) {
	// 	console.log(`Error setting user info: ${err}`);
	// 	return { user: null };
	// }
};
