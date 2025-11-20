<script>
	import Banner from '$lib/components/Banner.svelte';
	import { API_INGREDIENTS_ENDPOINT } from '$lib/endpoints';
	import RotatingNutriplan from '$lib/components/RotatingNutriplan.svelte';

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
	let showResults = $state(false);
	let searching = $state(false);

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

	const searchRecipes = async () => {
		if (selected.length === 0) return;

		searching = true;
		showResults = false;

		// Simular búsqueda
		setTimeout(() => {
			searching = false;
			showResults = true;
		}, 1500);
	};

	$effect(() => {
		query = filterQuery(ingredients);
	});

	getIngredients();
</script>

<div class="main flex-center direction-col">
	<!-- Hero Section -->
	<section class="flex-center full-width" style="background-color: #84994F">
		<div class="container flex-center direction-col pad-20 full-width">
			<p class="h2 bold text-col-white">¿Qué tienes en tu despensa?</p>
			<p class="md-p text-col-white txt-center mt">
				Selecciona los ingredientes que tienes disponibles y descubre recetas perfectas para ti
			</p>
		</div>
	</section>

	<!-- Paso 2: Resultados sugeridos -->
	{#if showResults}
		<section id="results" class="flex-center direction-col full-width pad-50 bg-soft-gray">
			<div class="container flex-center direction-col gap-24">
				<div class="flex-center direction-col">
					<p class="h2 bold">Recetas sugeridas</p>
					<p class="md-p p-ghost">Basadas en tus ingredientes seleccionados</p>
				</div>

				<div class="results-grid regrid-cols-3 gap-16" style="max-width: 1000px;">
					{#each suggestions as recipe, i}
						<div
							class="recipe-card bg-white b-shadow pad-20 round-10 hoverable"
							style="animation-delay: calc(0.1s * {i});"
						>
							<div class="flex justify-between items-center mb">
								<h3 class="h3 bold">{recipe.recipe}</h3>
								<div class="match-badge">
									<span class="tag">{recipe.match}% match</span>
								</div>
							</div>

							<div class="recipe-info flex gap-16 mb">
								<div class="info-item flex items-center gap-8">
									<i class="las la-clock p-emphasis"></i>
									<span class="sm-p">{recipe.time}</span>
								</div>
								<div class="info-item flex items-center gap-8">
									<i class="las la-list p-emphasis"></i>
									<span class="sm-p">{recipe.steps} pasos</span>
								</div>
							</div>

							<div class="missing-ingredients mb">
								<p class="sm-p bold mb-s">Ingredientes faltantes:</p>
								<div class="flex wrap gap-8">
									{#each recipe.missing as missing}
										<span
											class="chip"
											style="background-color: rgba(200, 111, 86, 0.1); color: var(--color-emphasis);"
										>
											{missing}
										</span>
									{/each}
								</div>
							</div>

							<div class="nutrition-info">
								<p class="sm-p p-ghost">{recipe.health}</p>
							</div>
						</div>
					{/each}
				</div>
			</div>
		</section>
	{/if}

	<!-- Paso 1: Selección de ingredientes -->
	<section id="ingredients" class="flex-center direction-col full-width pad-50">
		<div class="container flex-center direction-col gap-24">
			<!-- Barra de búsqueda -->
			<div
				class="search-container bg-white b-shadow pad-20 round-10"
				style="max-width: 600px; width: 100%;"
			>
				<input
					type="text"
					bind:value={search_query}
					placeholder="Buscar ingredientes..."
					class="full-width"
				/>
			</div>

			<!-- Contador de ingredientes seleccionados -->
			{#if selected.length > 0}
				<div class="flex-center gap-16">
					<p class="md-p bold">Ingredientes seleccionados: {selected.length}</p>
					<button class="btn primary" onclick={searchRecipes} disabled={searching}>
						{#if searching}
							Buscando recetas...
						{:else}
							Buscar recetas
						{/if}
					</button>
				</div>
			{/if}

			<!-- Grid de ingredientes -->
			{#if loading}
				<div class="flex-center full-width" style="min-height: 200px;">
					<RotatingNutriplan />
				</div>
			{:else if ingredients}
				<div class="ingredients-grid flex-center wrap gap-8" style="max-width: 800px;">
					{#each query as ingredient}
						<button
							class="ingredient pad-10 bg-soft-gray clickable hoverable no-border round-5"
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
			{/if}
		</div>
	</section>
</div>

<style>
	/* Hero section con ícono de búsqueda */
	.search-container input {
		background-image: url('$lib/assets/magnifying-glass.svg');
		background-repeat: no-repeat;
		background-size: 16px;
		background-position: 12px 12px;
		padding-left: 40px;
	}

	/* Ingredientes seleccionables */
	.ingredient {
		transition: 0.2s ease;
		font-weight: 500;
	}

	.ingredient[data-selected='true'] {
		background-color: var(--color-primary-dark);
		color: white;
		transform: translateY(-2px);
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
	}

	.ingredient:hover:not([data-selected='true']) {
		background-color: var(--color-soft-gray-darker);
		transform: translateY(-1px);
	}

	/* Grid de ingredientes */
	.ingredients-grid {
		justify-content: center;
	}

	/* Tarjetas de recetas */
	.recipe-card {
		transition:
			transform 0.2s ease,
			box-shadow 0.2s ease;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.recipe-card:hover {
		transform: translateY(-4px);
		box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
	}

	/* Badge de match */
	.match-badge .tag {
		background-color: var(--color-leaf);
		color: white;
		font-weight: 600;
	}

	/* Información de receta */
	.recipe-info {
		border-bottom: 1px solid var(--color-soft-gray);
		padding-bottom: 0.75rem;
	}

	.info-item {
		color: var(--color-soft);
	}

	/* Ingredientes faltantes */
	.missing-ingredients {
		flex-grow: 1;
	}

	/* Animaciones */
	@keyframes FadeIn {
		0% {
			opacity: 0;
			transform: translateY(-15px);
		}
		100% {
			opacity: 1;
			transform: translateY(0px);
		}
	}

	.recipe-card {
		animation: FadeIn 0.6s ease;
		animation-fill-mode: both;
	}

	/* Responsive */
	@media (max-width: 768px) {
		.results-grid {
			grid-template-columns: 1fr;
		}

		.ingredients-grid {
			justify-content: flex-start;
		}
	}

	@media (max-width: 480px) {
		.search-container {
			margin: 0 1rem;
		}

		.recipe-card {
			margin: 0 1rem;
		}
	}
</style>
