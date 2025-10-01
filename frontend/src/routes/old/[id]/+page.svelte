<script>
	// Load slug
	import { page } from '$app/stores';
	import { obtenerRecetaPorID } from '$lib/classes/receta';
	import RecipeCard from '$lib/components/RecipeCard.svelte';
	import { initialRecipes } from '$lib/stores/recipes';

	let receta = obtenerRecetaPorID($initialRecipes, $page.params.id);
	console.log(receta);
</script>

<h1>Receta con ID: {$page.params.id}</h1>
{#if receta}
	<RecipeCard {receta} />
{:else}
	<p>La receta no fue encontrada</p>
{/if}
