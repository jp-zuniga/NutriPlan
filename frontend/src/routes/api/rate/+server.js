import { SESSION_ACCESS_COOKIE } from '$lib/cookies';
import { API_RECIPES_ENDPOINT } from '$lib/endpoints';
import { getUser } from '$lib/stores/auth';

export const POST = async ({ request, cookies }) => {
	let payload;
	try {
		payload = await request.json();
	} catch (err) {
		return new Response(JSON.stringify({ error: 'Invalid Body: ' + err }), { status: 400 });
	}

	const user = getUser({ cookies });

	if (!user)
		return new Response(JSON.stringify({ error: 'User is not logged in' }), { status: 400 });

	const sessionCookie = cookies.get(SESSION_ACCESS_COOKIE);

	try {
		const response = await fetch(API_RECIPES_ENDPOINT + '/' + payload.slug + '/rate', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${sessionCookie}`
			},
			body: JSON.stringify({
				rating: payload.rating,
				comment: payload.comment
			})
		}).catch((err) => {
			return new Response(JSON.stringify({ error: err }), { status: 400 });
		});

		if (!response.ok) {
			const data = await response.json();
			return new Response(
				JSON.stringify({ error: data?.message ?? `HTTP error: status ${response.status}` }),
				{
					status: 400
				}
			);
		}

		const data = await response.json();

		if (data.error) return new Response(JSON.stringify({ error: data.error }), { status: 400 });

		if (data.created_at) return new Response(JSON.stringify({ ok: true }), { status: 200 });
		else return new Response(JSON.stringify({ error: 'Error desconocido' }), { status: 400 });
	} catch (err) {
		return new Response(JSON.stringify({ error: err }), { status: 400 });
	}
};
