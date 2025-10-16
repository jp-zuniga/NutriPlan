import { API_RECIPES_ENDPOINT } from '$lib/endpoints';

export const getRecipe = async (recipe_slug) => {
	const recipeFetchResponse = await fetch(API_RECIPES_ENDPOINT + '/' + recipe_slug, {
		method: 'GET'
	});

	const reviewFetchResponse = await fetch(API_RECIPES_ENDPOINT + '/' + recipe_slug + '/reviews', {
		method: 'GET'
	});

	if (recipeFetchResponse.ok) {
		const recipe = await recipeFetchResponse.json();
		const reviews = await reviewFetchResponse.json();

		return { recipe: recipe, reviews: reviews };
	} else return null;
};
