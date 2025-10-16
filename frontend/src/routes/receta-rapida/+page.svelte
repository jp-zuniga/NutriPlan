<script>
	import Banner from '$lib/components/Banner.svelte';
	import { API_INGREDIENTS_ENDPOINT } from '$lib/endpoints';

	const pantry = ['Yuca', 'Repollo morado', 'Mango verde', 'Limón', 'Chiltoma', 'Frijoles cocidos'];

	const suggestions = [
		{
			recipe: 'Vigorón exprés',
			match: 88,
			time: '20 min',
			steps: 4,
			missing: ['Vinagre de caña'],
			health: '430 kcal por porción'
		},
		{
			recipe: 'Ensalada fresca de repollo',
			match: 74,
			time: '15 min',
			steps: 3,
			missing: ['Maní tostado'],
			health: '210 kcal por porción'
		},
		{
			recipe: 'Tacos de frijol y chiltoma',
			match: 69,
			time: '25 min',
			steps: 5,
			missing: ['Tortillas de maíz'],
			health: '380 kcal por porción'
		}
	];

	const smartTips = [
		'Sube una foto de tu despensa para sugerencias más precisas.',
		'Activa el modo temporada para priorizar ingredientes frescos locales.',
		'Guarda combinaciones frecuentes para que la IA aprenda tus gustos.'
	];

	let ingredients = $state(null);
	let loading = $state(true);

	let selected = $state([]);

	let search_query = $state('');
	let query = $state([]);

	const getIngredients = async () => {
		loading = true;

		const response = await fetch(API_INGREDIENTS_ENDPOINT, {
			method: 'GET'
		});

		if (response.ok) {
			const data = await response.json();
			ingredients = data;
		}

		loading = false;
	};

	const filterQuery = (ingredients) => {
		if (search_query == '') return ingredients;
		else
			return ingredients.filter((i) => {
				return i.name.toLowerCase().includes(search_query.toLowerCase());
			});
	};

	$effect(() => {
		query = filterQuery(ingredients);
	});

	getIngredients();
</script>

<main>
	<section>
		<div class="container">
			<p class="h3 txt-center">Receta Rápida</p>
		</div>
	</section>

	<section id="ingredients">
		{#if ingredients}
			<div class="flex-center direction-col">
				<input type="text" bind:value={search_query} />
				<div class="flex-center wrap gap-8 container">
					{#each query as ingredient}
						<button
							class="ingredient pad-10 bg-soft-gray clickable hoverable no-border"
							data-selected={selected.includes(ingredient)}
							onclick={() => {
								if (selected.includes(ingredient))
									selected = selected.filter((e) => e != ingredient);
								else selected.push(ingredient);
							}}
						>
							{ingredient.name}
						</button>
					{/each}
				</div>
			</div>
		{/if}
	</section>
</main>

<style>
	.ingredient {
		transition: 0.1s linear;
	}

	.ingredient[data-selected='true'] {
		background-color: var(--color-primary);
		color: white;
	}
</style>
