import { getUser } from '$lib/stores/auth.js';

export const load = async ({ cookies }) => {
	return getUser({ cookies });
};
