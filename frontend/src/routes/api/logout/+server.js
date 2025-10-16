import { clearCookies } from '$lib/stores/auth.js';
import { redirect } from '@sveltejs/kit';

export const GET = async ({ cookies }) => {
	clearCookies({ cookies });
	throw redirect(302, '/login');
};
