import { PUBLIC_API_ENDPOINT } from '$env/static/public';
import { NIGHTLY } from '$env/static/private';

export const API_LOGIN_ENDPOINT = PUBLIC_API_ENDPOINT + '/auth/login/';
export const API_REGISTER_ENDPOINT = PUBLIC_API_ENDPOINT + '/auth/register/';
export const API_USERS_ENDPOINT = PUBLIC_API_ENDPOINT + '/users/';
export const API_ME_ENDPOINT = PUBLIC_API_ENDPOINT + '/users/me/';

export const NIGHTLY_BUILD = NIGHTLY == 'True';
