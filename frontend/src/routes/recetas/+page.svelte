<script>
	import Banner from '$lib/components/Banner.svelte';

	import ImagenVigoron from '$lib/assets/vigoron.jpg';
	import GalloPinto from '$lib/assets/gallo-pinto.jpg';
	import PlatosTipicos from '$lib/assets/platos-tipicos.jpeg';
	import SearchBox from '$lib/components/SearchBox.svelte';
	import SVG_MAGNIFYING_GLASS from '$lib/assets/magnifying-glass.svg';
	import RecipeCard from '$lib/components/RecipeCard.svelte';
	import Checkbox from '$lib/components/Checkbox.svelte';
	import { resolve } from '$app/paths';
	import { API_RECIPES_ENDPOINT } from '$lib/endpoints';
	import RotatingNutriplan from '$lib/components/RotatingNutriplan.svelte';

	const categories = ['Tradicional', 'Saludable', 'Vegetariano', 'Sin gluten', 'Postres'];

	const quickFilters = [
		{ label: '≤ 30 min', value: 'fast' },
		{ label: 'Alto en proteína', value: 'protein' },
		{ label: 'Bajo en sodio', value: 'low-salt' },
		{ label: 'Familiar', value: 'family' },
		{ label: 'IA recomendadas', value: 'ai' }
	];

	let loading = $state(true);

	const max_page_count = 20;

	const spotlight = [
		{
			title: 'Colección Nica Fit',
			description: '15 recetas ligeras inspiradas en clásicos nicaragüenses con ajustes saludables.'
		},
		{
			title: 'Menú semanal económico',
			description: 'Planifica con ingredientes locales accesibles sin perder sabor.'
		},
		{
			title: 'Especial lluvias',
			description: 'Sopas y caldos reconfortantes listos en menos de 40 minutos.'
		}
	];

	let url_params = $state('');
	let recipeResults = $state([]);

	$effect(() => {
		resolveResults(page);
	});

	const resolveResults = async (page) => {
		loading = true;

		recipeResults = [];

		const response = await fetch(API_RECIPES_ENDPOINT, {
			method: 'GET'
		});

		if (response.ok) {
			const data = await response.json();
			console.log(data);
			recipeResults = data;
			loading = false;
			return;
		}

		recipeResults = null;

		loading = false;
	};

	const filter_groups = $state([
		{
			name: 'Tiempo de Preparación',
			type: 'select',
			options: ['Hasta 45 minutos', 'Hasta 2 horas', 'Hasta 4 horas'],
			value: ''
		},
		{
			name: 'Preferencias',
			type: 'checkbox',
			options: [
				{ name: 'Sin gluten', id: 'sin-gluten', checked: false },
				{ name: 'Sin lactosa', id: 'sin-lactosa', checked: false },
				{ name: 'Bajo en calorías', id: 'bajo-calorias', checked: false },
				{ name: 'Bajo en sodio', id: 'bajo-sodio', checked: false }
			]
		},
		{
			name: 'Tipo de Comida',
			type: 'select',
			options: ['Desayuno', 'Almuerzo', 'Cena', 'Merienda', 'Postres', 'Bebidas'],
			value: ''
		},
		{
			name: 'Objetivo',
			type: 'select',
			options: [
				'Perder peso',
				'Ganar masa',
				'Mantener',
				'Control glucosa',
				'Colesterol',
				'Embarazo',
				'Para niños'
			],
			value: ''
		},
		{
			name: 'Dificultad',
			type: 'select',
			options: ['Fácil', 'Media', 'Avanzada'],
			value: ''
		},
		{
			name: 'Porciones',
			type: 'select',
			options: ['1', '2–3', '4–6', '7+'],
			value: ''
		},
		{
			name: 'Alergias',
			type: 'checkbox',
			options: [
				{ name: 'Maní', id: 'alergia-mani', checked: false },
				{ name: 'Mariscos', id: 'alergia-mariscos', checked: false },
				{ name: 'Huevo', id: 'alergia-huevo', checked: false },
				{ name: 'Soya', id: 'alergia-soya', checked: false }
			]
		}
	]);

	let orderby = $state('Relevancia');
	const orderby_options = [
		{ name: 'Relevancia', url_param: '' },
		{ name: 'Mayor Valoración', url_param: '' },
		{ name: 'Menor Tiempo', url_param: '' },
		{ name: 'Menos Calorías', url_params: '' }
	];

	let selected_categories = $state([]);

	let searchTerm = $state('');
	let page = $state(1);
</script>

<div class="main flex-center direction-col">
	<section class="flex-center full-width" style="background-color: #84994F">
		<div class="container flex-center direction-col pad-20 full-width">
			<p class="h2 bold text-col-white">¿Que quieres cocinar hoy?</p>
			<div
				id="search-box"
				class="container full-width mt flex justify-between items-center direction-col gap-16 pad-20 bg-white b-shadow"
				style="max-width: 800px;"
			>
				<input type="text" class="full-width" bind:value={searchTerm} />
				<div class="categories flex-center gap-16 wrap">
					{#each categories as category}
						<button
							class="sm-p pad-10 hoverable p-ghost bg-soft-gray clickable no-border"
							data-selected={selected_categories.includes(category)}
							onclick={() => {
								if (selected_categories.includes(category))
									selected_categories = selected_categories.filter((c) => c != category);
								else selected_categories.push(category);
							}}
						>
							{category}
						</button>
					{/each}
				</div>
			</div>
		</div>
	</section>

	<section id="results" class="flex-center direcion-col full-width pad-50">
		<div class="container grid regrid-cols-2" style="min-height: 900px; max-height: 900px;">
			<div class="filters bg-white b-shadow pad-20 flex direction-col justify-between gap-16">
				<div id="filter-groups" class="flex direction-col gap-16">
					{#each filter_groups as filter}
						<fieldset>
							<legend class="sm-p">{filter.name}</legend>
							{#if filter.type == 'select'}
								<select name={filter.name} bind:value={filter.value} class="full-width">
									<option value="">Cualquiera</option>
									{#each filter.options as option}
										<option value={option}>{option}</option>
									{/each}
								</select>
							{:else if filter.type == 'checkbox'}
								{#each filter.options as option}
									<Checkbox label={option.name} bind:value={option.checked} />
								{/each}
							{/if}
						</fieldset>
					{/each}
				</div>
				<button class="btn primary" onclick={resolveResults}>Actualizar</button>
			</div>
			<div class="results flex direction-col justify-between" style="max-height: 900px;">
				<div class="top-line flex justify-between items-center">
					<div class="titles">
						<p class="h2 bold">Resultados</p>
						{#if !loading}
							<p class="md-p p-ghost">{recipeResults.length} resultado(s)</p>
						{:else}
							<p class="md-p p-ghost">Cargando...</p>
						{/if}
					</div>
					<div class="order-by flex-center gap-8">
						<p class="md-p p-ghost">Ordenar por</p>
						<select name="orderby" bind:value={orderby}>
							{#each orderby_options as option}
								<option value={option}>{option}</option>
							{/each}
						</select>
					</div>
				</div>
				<div
					id="recipe-grid"
					class="flex-center justify-between gap-16 wrap ov-scroll-y pad-20 bg-white full-size"
				>
					{#if !loading}
						{#each recipeResults as recipe, i}
							<div class="recipe" style="animation-delay: calc(0.1s * {i});">
								<RecipeCard {recipe} />
							</div>
						{/each}
						{#if recipeResults === null}
							<div class="full-size flex-center">
								<p class="lg-p p-ghost txt-center">Hubo un error obteniendo las recetas</p>
							</div>
						{/if}
					{:else}
						<div class="full-size flex-center">
							<!-- <p class="h3 p-ghost">Cargando recetas...</p> -->
							<RotatingNutriplan />
						</div>
					{/if}
				</div>
				<div class="flex justify-end items-center gap-24 mt">
					<button
						class="btn ghost"
						style="width: 15px; height: 15px;"
						onclick={() => {
							if (page > 1 && !loading) page--;
						}}
						disabled={page <= 1}
						aria-label="previous"
					>
						<i class="las la-angle-left"></i>
					</button>
					<p class="md-p p-ghost">{page}</p>
					<button
						class="btn ghost"
						style="width: 15px; height: 15px;"
						onclick={() => {
							if (!loading) page++;
						}}
						aria-label="next"
					>
						<i class="las la-angle-right"></i>
					</button>
				</div>
			</div>
		</div>
	</section>
</div>

<style>
	#search-box input {
		background-image: url('$lib/assets/magnifying-glass.svg');
		background-repeat: no-repeat;
		background-size: 16px;
		background-position: 12px 12px;

		padding-left: 40px;
	}

	.categories button[data-selected='true'] {
		background-color: var(--color-primary-dark);
		color: white;
	}

	#results .grid {
		grid-template-columns: 1fr 3fr;
	}

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

	#recipe-grid .recipe {
		animation: FadeIn 1s ease;
		animation-fill-mode: both;
	}
</style>
