<script>
	import Banner from '$lib/components/Banner.svelte';

	import ImagenVigoron from '$lib/assets/vigoron.jpg';
	import GalloPinto from '$lib/assets/gallo-pinto.jpg';
	import PlatosTipicos from '$lib/assets/platos-tipicos.jpeg';

	const categories = ['Todos', 'Tradicional', 'Saludable', 'Vegetariano', 'Sin gluten', 'Postres'];

	const quickFilters = [
		{ label: '≤ 30 min', value: 'fast' },
		{ label: 'Alto en proteína', value: 'protein' },
		{ label: 'Bajo en sodio', value: 'low-salt' },
		{ label: 'Familiar', value: 'family' },
		{ label: 'IA recomendadas', value: 'ai' }
	];

	const recipeResults = [
		{
			id: 'vigoron-saludable',
			title: 'Vigorón saludable',
			calories: '430 kcal',
			time: '35 min',
			portions: '2 porciones',
			tags: ['Top nica', 'Alto en fibra'],
			score: 4.8,
			image: ImagenVigoron
		},
		{
			id: 'gallo-pinto-energizante',
			title: 'Gallo pinto energizante',
			calories: '380 kcal',
			time: '25 min',
			portions: '4 porciones',
			tags: ['Desayuno', 'Vegetariano'],
			score: 4.9,
			image: GalloPinto
		},
		{
			id: 'sopa-queso-liviana',
			title: 'Sopa de queso liviana',
			calories: '320 kcal',
			time: '40 min',
			portions: '4 porciones',
			tags: ['Reconfortante', 'Sin gluten'],
			score: 4.7,
			image: PlatosTipicos
		},
		{
			id: 'ensalada-chayote-verde',
			title: 'Ensalada de chayote verde',
			calories: '280 kcal',
			time: '20 min',
			portions: '3 porciones',
			tags: ['Refrescante', 'Baja en carbohidratos'],
			score: 4.6,
			image: PlatosTipicos
		}
	];

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
</script>

<Banner />

<main class="recipes">
	<section class="hero">
		<div class="container">
			<div class="hero-copy">
				<h1>Explora recetas nicaragüenses curadas para tu bienestar</h1>
				<p>
					Combina tradición y nutrición con filtros avanzados, recomendaciones de IA y colecciones
					temáticas listas para inspirarte.
				</p>
			</div>
			<div class="search-panel">
				<label for="recipe-search">¿Qué te apetece cocinar?</label>
				<div class="search-input">
					<input
						id="recipe-search"
						type="text"
						placeholder="Buscar por ingrediente, receta o estilo"
					/>
					<button type="button">Buscar</button>
				</div>
				<div class="filter-row">
					<div class="categories">
						{#each categories as category, index}
							<button type="button" class:active={!index}>{category}</button>
						{/each}
					</div>
					<div class="quick-filters">
						{#each quickFilters as filter}
							<span class="chip">{filter.label}</span>
						{/each}
					</div>
				</div>
			</div>
		</div>
	</section>

	<section class="results">
		<div class="container results-grid">
			<aside class="filters">
				<h2>Filtrar por</h2>
				<div class="filter-group">
					<h3>Categorías</h3>
					<label><input type="checkbox" checked /> Tradicional</label>
					<label><input type="checkbox" /> Saludable</label>
					<label><input type="checkbox" /> Vegano</label>
					<label><input type="checkbox" /> Alta proteína</label>
				</div>
				<div class="filter-group">
					<h3>Tiempo de preparación</h3>
					<input type="range" min="10" max="120" value="45" />
					<span class="range-label">Hasta 45 minutos</span>
				</div>
				<div class="filter-group">
					<h3>Preferencias</h3>
					<label><input type="checkbox" /> Sin gluten</label>
					<label><input type="checkbox" /> Bajo en sodio</label>
					<label><input type="checkbox" checked /> Recomendadas por IA</label>
				</div>
			</aside>
			<section class="cards">
				<header>
					<div>
						<h2>Resultados populares</h2>
						<p>Basados en tus preferencias y los ingredientes que marcaste como favoritos.</p>
					</div>
					<select>
						<option>Ordenar por relevancia</option>
						<option>Mayor valoración</option>
						<option>Menor tiempo</option>
						<option>Menor calorías</option>
					</select>
				</header>
				<div class="card-grid">
					{#each recipeResults as recipe}
						<article class="recipe-card">
							<div class="image">
								<img src={recipe.image} alt={recipe.title} loading="lazy" />
								<span class="score">★ {recipe.score}</span>
							</div>
							<div class="body">
								<h3>{recipe.title}</h3>
								<p>{recipe.calories} • {recipe.time} • {recipe.portions}</p>
								<div class="tags">
									{#each recipe.tags as tag}
										<span>{tag}</span>
									{/each}
								</div>
								<a class="details" href={`/recetas/${recipe.id}`}>Ver receta completa →</a>
							</div>
						</article>
					{/each}
				</div>
			</section>
		</div>
	</section>

	<section class="spotlight">
		<div class="container">
			<header class="section-head">
				<h2>Colecciones destacadas</h2>
				<p>
					Dale variedad a tus planes con selecciones temáticas listas para agregar a tu menú
					semanal.
				</p>
			</header>
			<div class="spotlight-grid">
				{#each spotlight as item}
					<article>
						<h3>{item.title}</h3>
						<p>{item.description}</p>
						<a href="#">Explorar colección</a>
					</article>
				{/each}
			</div>
		</div>
	</section>
</main>

<style>
	.recipes {
		display: flex;
		flex-direction: column;
		gap: 5rem;
		padding-bottom: 5rem;
	}

	.container {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 1.5rem;
	}

	.hero {
		padding: 2rem 0 1rem;
	}

	.hero-copy {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.hero-copy h1 {
		margin: 0;
		font-size: clamp(2rem, 3vw, 3.1rem);
	}

	.hero-copy p {
		margin: 0;
		color: var(--color-soft);
	}

	.search-panel {
		margin-top: 2.5rem;
		background: rgba(255, 255, 255, 0.86);
		backdrop-filter: blur(14px);
		border-radius: var(--radius-lg);
		padding: 2.5rem;
		box-shadow: var(--shadow-soft);
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.search-panel label {
		font-size: 0.95rem;
	}

	.search-input {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 1rem;
	}

	.search-input input {
		width: 100%;
	}

	.search-input button {
		background: var(--gradient-leaf);
		color: white;
		border: none;
		border-radius: 999px;
		padding: 0 1.8rem;
		font-weight: 600;
		cursor: pointer;
		box-shadow: 0 14px 24px rgba(15, 184, 114, 0.28);
	}

	.filter-row {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.categories {
		display: flex;
		flex-wrap: wrap;
		gap: 0.75rem;
	}

	.categories button {
		padding: 0.6rem 1.3rem;
		border-radius: 999px;
		border: 1px solid rgba(5, 70, 58, 0.12);
		background: rgba(255, 255, 255, 0.75);
		font-weight: 600;
		color: var(--color-soft);
		cursor: pointer;
		transition:
			background 0.2s ease,
			color 0.2s ease,
			border-color 0.2s ease;
	}

	.categories button.active,
	.categories button:hover {
		background: rgba(15, 184, 114, 0.12);
		color: var(--color-forest);
		border-color: rgba(15, 184, 114, 0.35);
	}

	.quick-filters {
		display: flex;
		flex-wrap: wrap;
		gap: 0.75rem;
	}

	.results .container {
		display: grid;
		grid-template-columns: 300px 1fr;
		gap: 2rem;
	}

	.filters {
		background: rgba(255, 255, 255, 0.88);
		backdrop-filter: blur(12px);
		border-radius: var(--radius-lg);
		padding: 2rem;
		box-shadow: var(--shadow-soft);
		display: flex;
		flex-direction: column;
		gap: 2rem;
	}

	.filters h2 {
		margin: 0;
	}

	.filter-group {
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
	}

	.filter-group h3 {
		margin: 0;
		font-size: 1rem;
	}

	.filter-group label {
		display: flex;
		align-items: center;
		gap: 0.6rem;
		font-weight: 500;
		color: var(--color-soft);
	}

	.filter-group input[type='range'] {
		width: 100%;
	}

	.range-label {
		font-size: 0.9rem;
		color: var(--color-soft);
	}

	.cards {
		display: flex;
		flex-direction: column;
		gap: 2rem;
	}

	.cards header {
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		align-items: center;
		gap: 1rem;
	}

	.cards header h2 {
		margin: 0;
	}

	.cards header p {
		margin: 0;
		color: var(--color-soft);
	}

	.cards header select {
		border-radius: 999px;
		padding: 0.6rem 1.1rem;
	}

	.card-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
		gap: 1.5rem;
	}

	.recipe-card {
		background: var(--color-card);
		border-radius: var(--radius-md);
		overflow: hidden;
		box-shadow: 0 18px 32px rgba(8, 44, 36, 0.1);
		display: flex;
		flex-direction: column;
		transition:
			transform 0.25s ease,
			box-shadow 0.25s ease;
	}

	.recipe-card:hover {
		transform: translateY(-4px);
		box-shadow: 0 24px 38px rgba(8, 44, 36, 0.14);
	}

	.recipe-card .image {
		position: relative;
		height: 180px;
	}

	.recipe-card img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.score {
		position: absolute;
		top: 0.75rem;
		right: 0.75rem;
		background: rgba(0, 0, 0, 0.6);
		color: white;
		padding: 0.3rem 0.75rem;
		border-radius: 999px;
		font-size: 0.85rem;
	}

	.recipe-card .body {
		padding: 1.5rem;
		display: flex;
		flex-direction: column;
		gap: 0.8rem;
	}

	.recipe-card h3 {
		margin: 0;
		font-size: 1.2rem;
	}

	.recipe-card p {
		margin: 0;
		color: var(--color-soft);
		font-size: 0.95rem;
	}

	.recipe-card .tags {
		display: flex;
		flex-wrap: wrap;
		gap: 0.4rem;
	}

	.recipe-card .tags span {
		background: rgba(15, 184, 114, 0.12);
		color: var(--color-forest);
		padding: 0.25rem 0.7rem;
		border-radius: 999px;
		font-weight: 600;
		font-size: 0.8rem;
	}

	.details {
		margin-top: auto;
		font-weight: 600;
		color: var(--color-forest);
		text-decoration: none;
	}

	.spotlight-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
		gap: 1.5rem;
		margin-top: 2rem;
	}

	.spotlight-grid article {
		background: rgba(255, 255, 255, 0.92);
		border-radius: var(--radius-md);
		padding: 1.8rem;
		box-shadow: var(--shadow-soft);
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.spotlight-grid h3 {
		margin: 0;
	}

	.spotlight-grid p {
		margin: 0;
		color: var(--color-soft);
	}

	.spotlight-grid a {
		font-weight: 600;
		color: var(--color-forest);
		text-decoration: none;
	}

	select option:hover,
	select option:checked {
		box-shadow: 0 0 10px 100px #1882a8 inset;
	}

	@media (max-width: 960px) {
		.results .container {
			grid-template-columns: 1fr;
		}

		.filters {
			flex-direction: row;
			flex-wrap: wrap;
			gap: 1.5rem;
		}

		.filter-group {
			flex: 1 1 200px;
		}
	}

	@media (max-width: 640px) {
		.search-input {
			grid-template-columns: 1fr;
		}

		.search-input button {
			padding: 0.8rem 1.2rem;
		}

		.filters {
			padding: 1.5rem;
		}
	}
</style>
