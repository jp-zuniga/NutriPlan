import { SESSION_ACCESS_COOKIE } from '$lib/cookies';
import { API_ME_ENDPOINT } from '$lib/endpoints';

export const GET = async ({ request, cookies }) => {
	const access = cookies.get(SESSION_ACCESS_COOKIE);

	if (!access) {
		return new Response(JSON.stringify({ error: 'No hay sesión activa' }), { status: 401 });
	}

	try {
		console.log(`Asked access with token: ${access}`);

		const response = fetch(API_ME_ENDPOINT, {
			method: 'POST',
			headers: {
				Authorization: `Bearer ${access}`
			}
		});
	} catch (err) {
		return new Response(JSON.stringify({ error: `Hubo un error: ${err}` }), { status: 401 });
	}
};
