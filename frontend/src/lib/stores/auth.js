import { goto } from '$app/navigation';
import { writable, get } from 'svelte/store';

export const authUser = writable(null);

export const redirectIfNull = () => {
	if (!get(authUser)) goto('/login');
};
