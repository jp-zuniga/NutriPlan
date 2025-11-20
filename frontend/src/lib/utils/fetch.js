import { PUBLIC_API_ENDPOINT } from '$env/static/public';
import { SESSION_ACCESS_COOKIE, SESSION_REFRESH_COOKIE } from '$lib/cookies';
import { getUser } from '$lib/stores/auth';

export const authenticatedFetch = async (url, request, { cookies }) => {
	if (url.includes(PUBLIC_API_ENDPOINT)) {
		const access = cookies.get(SESSION_ACCESS_COOKIE);
		const refresh = cookies.get(SESSION_REFRESH_COOKIE);

		const cookie_string = `${access ? SESSION_ACCESS_COOKIE + '=' + access : ''}${refresh ? ';' + SESSION_REFRESH_COOKIE + '=' + refresh : ''}`;

		const user = await getUser({ cookies });
		if (!user) return { error: 'El usuario no se pudo autenticar.' };

		request.headers['Cookie'] = cookie_string;
		const response = await fetch(url, request);

		console.log('Chefcito response: ', response);

		if (response.ok) {
			return { ok: true, data: await response.json() };
		} else {
			const data = await response.json();
			console.log('Chefcito response is not ok, data: ', data);
			return { error: data?.message ?? 'Error desconocido, HTTP status: ' + response.status };
		}
	} else {
		return { error: 'No se puede usar un authenticated fetch en un api externo' };
	}
};

export const JSONRequest = (body) => {
	return {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(body)
	};
};
