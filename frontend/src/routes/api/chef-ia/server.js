import { API_CHEFCITO_CHAT_ENDPOINT } from '$lib/endpoints';
import { authenticatedFetch, JSONRequest } from '$lib/utils/fetch.js';

export const POST = async ({ request, cookies }) => {
	let payload;

	try {
		payload = await request.json();
	} catch (err) {
		return new Response(JSON.stringify({ error: 'Invalid Body: ' + err }), { status: 400 });
	}

	console.log('Preguntandole a chefcito...');

	try {
		const response = await authenticatedFetch(
			API_CHEFCITO_CHAT_ENDPOINT,
			JSONRequest({
				message: payload.message
			}),
			{ cookies }
		);

		console.log('Chefcito response data: ', response.data);

		if (response.data) {
			return new Response(JSON.stringify({ ok: true, data: response.data }), { status: 200 });
		} else {
			return new Response(JSON.stringify({ error: response.error ?? 'Error desconocido' }), {
				status: 400
			});
		}
	} catch (err) {
		return new Response(JSON.stringify({ error: err }), { status: 400 });
	}
	// let payload;
	// try {
	// 	payload = await request.json();
	// } catch (err) {
	// 	return new Response(JSON.stringify({ error: 'Invalid Body: ' + err }), { status: 400 });
	// }

	// const user = getUser();

	// if (!user)
	// 	return new Response(JSON.stringify({ error: 'User is not logged in' }), { status: 400 });

	// try {
	// 	const response = await fetch(API_RECIPES_ENDPOINT + '/' + payload.slug + '/rate', {
	// 		method: 'POST',
	// 		headers: {
	// 			'Content-Type': 'application/json'
	// 		},
	// 		credentials: 'include',
	// 		body: JSON.stringify({
	// 			rating: payload.rating,
	// 			comment: payload.comment
	// 		})
	// 	}).catch((err) => {
	// 		return new Response(JSON.stringify({ error: err }), { status: 400 });
	// 	});

	// 	if (!response.ok) {
	// 		const data = await response.json();
	// 		return new Response(
	// 			JSON.stringify({ error: data?.message ?? `HTTP error: status ${response.status}` }),
	// 			{
	// 				status: 400
	// 			}
	// 		);
	// 	}

	// 	const data = await response.json();

	// 	if (data.error) return new Response(JSON.stringify({ error: data.error }), { status: 400 });

	// 	if (data.created_at) return new Response(JSON.stringify({ ok: true }), { status: 200 });
	// 	else return new Response(JSON.stringify({ error: 'Error desconocido' }), { status: 400 });
	// } catch (err) {
	// 	return new Response(JSON.stringify({ error: err }), { status: 400 });
	// }
};
