<script>
	import RecipeCard from '$lib/components/RecipeCard.svelte';
	import SearchBox from '$lib/components/SearchBox.svelte';
	import { initialRecipes } from '$lib/stores/recipes';

	const user_name = 'Mauricio';
</script>

<div id="body">
	<div id="search-bar">
		<div id="bar-title"></div>
		<SearchBox />
		<div id="bar-left">
			<div><b>Hola,</b> {user_name}</div>
		</div>
	</div>
	<div id="sidebar">
		<ul>
			<li>My Account</li>
			<li>New Recipes</li>
			<li>Favorites</li>
			<li>Log out</li>
		</ul>
	</div>
	<div id="main-content">
		<div class="tab-text">Recomendado</div>
		<hr />

		<!-- Tarjeta por defecto para recetas -->
		<div class="recipe-grid">
			{#each $initialRecipes as receta}
				<RecipeCard {receta} />
			{/each}
		</div>
	</div>
</div>
