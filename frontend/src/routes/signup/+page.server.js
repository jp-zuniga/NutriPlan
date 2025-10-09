import { SESSION_ACCESS_COOKIE } from '$lib/cookies';
import { NODE_ENV } from '$env/static/private';
import { API_REGISTER_ENDPOINT } from '$lib/endpoints';
import { fail, redirect } from '@sveltejs/kit';

export const actions = {
	default: async ({ cookies, request }) => {
		const data = await request.formData();

		const fields = ['full_name', 'email', 'phone', 'password', 'password_confirm'];

		let requestBody = {};
		for (let field of fields) {
			requestBody[field] = data.get(field);
		}

		console.log(
			'Request body: ' + JSON.stringify(requestBody) + ' to endpoint: ' + API_REGISTER_ENDPOINT
		);

		const res = await fetch(API_REGISTER_ENDPOINT, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(requestBody)
		}).catch((err) => {
			return fail(400, `Hubo un problema comunicandose con el servidor.`);
		});

		console.log(res);

		const body = await res?.json();
		if (!res.ok) {
			return fail(
				400,
				data?.message ?? `Error desconocido creando tu cuenta, status: ${res.status}`
			);
		}

		console.log(body);
		console.log(`Access: ${body.access}`);

		cookies.set(SESSION_ACCESS_COOKIE, body.access, {
			path: '/',
			httpOnly: true,
			sameSite: 'lax',
			secure: NODE_ENV == 'production',
			maxAge: 60 * 60
		});

		return { success: true, data: body };
	}
};
