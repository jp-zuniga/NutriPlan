import { getUser } from '$lib/stores/auth.js';

export const load = async ({ cookies }) => {
	const access = cookies.get('np-access');
	const refresh = cookies.get('np-refresh');

	console.log(`Access cookie: `, access, ', Refresh cookie: ', refresh);

	return getUser();
};
