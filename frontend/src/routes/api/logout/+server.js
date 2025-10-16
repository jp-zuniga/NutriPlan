import { API_LOGOUT_ENDPOINT } from '$lib/endpoints.js';
import { error, redirect } from '@sveltejs/kit';

export const GET = async () => {
	const response = fetch(API_LOGOUT_ENDPOINT, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include',
		body: {}
	});

	console.log('Logout response: ', response);

	if (response.ok) throw redirect(302, '/login');
	else error(500, 'Could not log you out');
};
