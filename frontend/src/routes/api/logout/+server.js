import { SESSION_ACCESS_COOKIE } from "$lib/cookies";
import { redirect } from "@sveltejs/kit";

export const GET = async({cookies}) => {
    cookies.delete(SESSION_ACCESS_COOKIE, { path: '/' });
    throw redirect(302, '/login');
}