import { authUser } from '$lib/stores/auth';
import { get } from 'svelte/store';

/**
 * Verifica si el usuario actual puede crear artículos
 * @returns {boolean} true si el usuario tiene rol staff o admin
 */
export function canCreateArticles() {
	return get(authUser) && (get(authUser).role === 'staff' || get(authUser).role === 'admin');
}

/**
 * Verifica si el usuario actual puede editar artículos
 * @returns {boolean} true si el usuario tiene rol staff o admin
 */
export function canEditArticles() {
	return get(authUser) && (get(authUser).role === 'staff' || get(authUser).role === 'admin');
}

/**
 * Verifica si el usuario actual puede eliminar artículos
 * @returns {boolean} true si el usuario tiene rol admin
 */
export function canDeleteArticles() {
	return get(authUser) && get(authUser).role === 'admin';
}

/**
 * Verifica si el usuario actual es admin
 * @returns {boolean} true si el usuario tiene rol admin
 */
export function isAdmin() {
	return get(authUser) && get(authUser).role === 'admin';
}

/**
 * Verifica si el usuario actual es staff o admin
 * @returns {boolean} true si el usuario tiene rol staff o admin
 */
export function isStaffOrAdmin() {
	return get(authUser) && (get(authUser).role === 'staff' || get(authUser).role === 'admin');
}
