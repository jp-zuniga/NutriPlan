<script>
	import ArticleCard from '$lib/components/ArticleCard.svelte';
	import { authUser } from '$lib/stores/auth';
	import { API_ARTICLES_ENDPOINT } from '$lib/endpoints';
	import RotatingNutriplan from '$lib/components/RotatingNutriplan.svelte';
	import { canCreateArticles } from '$lib/utils/permissions';

	let loading = $state(true);
	let articleResults = $state(null);
	let filterResults = $state(null);
	let searchTerm = $state('');
	let page = $state(1);

	const resolveResults = async (page) => {
		loading = true;

		try {
			const response = await fetch(API_ARTICLES_ENDPOINT, {
				method: 'GET'
			});

			if (response.ok) {
				const data = await response.json();
				console.log('Articles data:', data);
				articleResults = data;
				loading = false;
				return;
			}

			articleResults = null;
		} catch (error) {
			console.error('Error fetching articles:', error);
			articleResults = null;
		}

		loading = false;
	};

	resolveResults();

	let orderby = $state('Más recientes');
	const orderby_options = ['Más recientes', 'Más antiguos', 'A-Z', 'Z-A'];

	// Filtrar artículos basado en búsqueda
	$effect(() => {
		if (searchTerm && articleResults && Array.isArray(articleResults)) {
			const term = searchTerm.toLowerCase();
			filterResults = articleResults.filter(
				(article) =>
					article.title.toLowerCase().includes(term) ||
					article.content.toLowerCase().includes(term) ||
					(article.author && article.author.toLowerCase().includes(term))
			);
		} else if (articleResults && Array.isArray(articleResults)) filterResults = articleResults;
	});
</script>

<svelte:head>
	<title>Artículos - NutriPlan</title>
</svelte:head>

<div class="main flex-center direction-col">
	<section class="flex-center full-width" style="background-color: #84994F">
		<div class="container flex-center direction-col pad-20 full-width">
			<p class="h2 bold text-col-white animate-fade-in-down">Artículos de Nutrición</p>
			<p class="lg-p text-col-white mb animate-fade-in-up animate-delay-1">
				Aprende sobre nutrición, salud y bienestar con nuestros artículos
			</p>
			<div
				id="search-box"
				class="container full-width mt flex justify-center items-center pad-20 bg-white b-shadow round-10 animate-scale-in animate-delay-2"
				style="max-width: 600px;"
			>
				<input
					type="text"
					class="full-width"
					bind:value={searchTerm}
					placeholder="Buscar artículos..."
				/>
			</div>
		</div>
	</section>

	<section id="results" class="flex-center direction-col full-width pad-50">
		<div class="container" style="min-height: 600px;">
			<div class="results flex direction-col">
				<div class="top-line flex justify-between items-center mb-l">
					<div class="titles">
						<p class="h2 bold">Artículos</p>
						{#if !loading}
							<p class="md-p p-ghost">{articleResults ? articleResults.length : 0} artículo(s)</p>
						{:else}
							<p class="md-p p-ghost">Cargando...</p>
						{/if}
					</div>
					<div class="actions flex items-center gap-16">
						{#if canCreateArticles()}
							<a href="/articulos/nuevo" class="btn primary">
								<i class="las la-plus"></i>
								Crear Artículo
							</a>
						{/if}
						<div class="order-by flex-center gap-8">
							<p class="md-p p-ghost">Ordenar por</p>
							<select name="orderby" bind:value={orderby} class="round-5">
								{#each orderby_options as option}
									<option value={option}>{option}</option>
								{/each}
							</select>
						</div>
					</div>
				</div>

				<div id="article-grid" class="flex wrap gap-16 pad-20 bg-white full-width round-10">
					{#if !loading}
						{#if articleResults && Array.isArray(articleResults) && articleResults.length > 0}
							{#each filterResults as article, i}
								<div class="article" style="animation-delay: calc(0.1s * {i});">
									<ArticleCard {article} />
								</div>
							{/each}
						{:else if articleResults === null}
							<div class="full-size flex-center pad-50">
								<p class="lg-p p-ghost txt-center">Hubo un error obteniendo los artículos</p>
							</div>
						{:else}
							<div class="full-size flex-center pad-50">
								<p class="lg-p p-ghost txt-center">No se encontraron artículos</p>
							</div>
						{/if}
					{:else}
						<div class="full-size flex-center pad-50">
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

	#article-grid .article {
		animation: FadeIn 1s ease;
		animation-fill-mode: both;
	}
</style>
