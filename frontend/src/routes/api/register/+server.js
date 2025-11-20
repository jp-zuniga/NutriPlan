import { API_REGISTER_ENDPOINT } from '$lib/endpoints';
import { setCookies } from '$lib/stores/auth.js';

export const POST = async ({ request, cookies }) => {
	let payload;
	try {
		payload = await request.json();
		// console.log("Payload: ", payload)
	} catch {
		return new Response(JSON.stringify({ error: 'Body inválido' }), { status: 400 });
	}

	try {
		console.log('Request to ' + API_REGISTER_ENDPOINT + ' with body:', payload);

		const upstream = await fetch(API_REGISTER_ENDPOINT, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			credentials: 'include',
			body: JSON.stringify(payload)
		}).catch((err) => {
			console.log(`Communication error:`, err);
			return new Response(JSON.stringify({ error: err }), { status: 500 });
		});

		console.log('Upstream: ', upstream);
		const data = await upstream.json();

		if (!upstream.ok) {
			const message = data?.message ?? `Error desconocido (HTTP ${upstream.status})`;
			return new Response(JSON.stringify({ error: message }), { status: upstream.status });
		}

		const access = data.access;
		const refresh = data.refresh;

		if (!access) {
			return new Response(
				JSON.stringify({ error: 'Respuesta invalida del servidor de autentificación' }),
				{ status: 500 }
			);
		}

		setCookies(access, refresh, { cookies });

		return new Response(JSON.stringify({ ok: true, user: data.user }), { status: 200 });
	} catch (err) {
		return new Response(JSON.stringify({ error: err }), { status: 500 });
	}
};
