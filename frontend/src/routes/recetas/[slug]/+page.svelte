<script>
	import { onMount } from 'svelte';
	import Banner from '$lib/components/Banner.svelte';

	import ImagenVigoron from '$lib/assets/vigoron.jpg';
	import GalloPinto from '$lib/assets/gallo-pinto.jpg';
	import PlatosTipicos from '$lib/assets/platos-tipicos.jpeg';

	const coverMap = {
		vigoron: ImagenVigoron,
		'gallo-pinto': GalloPinto,
		'sopa-queso': PlatosTipicos,
		chayote: PlatosTipicos
	};

	export let data;

	let { recipe, recommended, notFound } = data;

	$: heroImage = coverMap[recipe.cover] ?? PlatosTipicos;
	$: recommendedWithImages = recommended.map((item) => ({
		...item,
		image: coverMap[item.cover] ?? PlatosTipicos
	}));

	onMount(() => {
		window.scrollTo({ top: 0, behavior: 'smooth' });
	});
</script>

<svelte:head>
	<title>{recipe.title}</title>
</svelte:head>

<Banner />

<main class="recipe-detail">
	<section class="hero">
		<div class="container hero-grid">
			<div class="copy">
				{#if notFound}
					<span class="badge warning">Receta sugerida</span>
				{/if}
				<h1>{recipe.title}</h1>
				<p>{recipe.tagline}</p>
				<div class="meta">
					<span class="tag">{recipe.origin}</span>
					<span>{recipe.time}</span>
					<span>{recipe.difficulty}</span>
					<span>{recipe.calories} kcal</span>
				</div>
				<div class="tag-row">
					{#each recipe.tags as tag}
						<span class="chip">{tag}</span>
					{/each}
				</div>
				<div class="cta">
					<a class="btn primary" href="/planes">Añadir a mi plan</a>
					<a class="btn ghost" href="/recetas">Volver al catálogo</a>
				</div>
			</div>
			<div class="media">
				<img src={heroImage} alt={recipe.title} />
				<div class="overlay-card">
					<h3>Información nutricional</h3>
					<ul>
						<li><strong>Proteína:</strong> {recipe.macros.protein}</li>
						<li><strong>Carbohidratos:</strong> {recipe.macros.carbs}</li>
						<li><strong>Grasas:</strong> {recipe.macros.fats}</li>
					</ul>
				</div>
			</div>
		</div>
	</section>

	<section class="content">
		<div class="container content-grid">
			<article class="card ingredients">
				<h2>Ingredientes</h2>
				<ul>
					{#each recipe.ingredients as ingredient}
						<li>{ingredient}</li>
					{/each}
				</ul>
			</article>
			<article class="card steps">
				<h2>Preparación</h2>
				<ol>
					{#each recipe.steps as step, index}
						<li>
							<span class="step-index">{index + 1}</span>
							<p>{step}</p>
						</li>
					{/each}
				</ol>
			</article>
		</div>
	</section>

	<section class="extras">
		<div class="container extras-grid">
			<article class="card tips">
				<h2>Trucos de la comunidad</h2>
				<ul>
					{#each recipe.tips as tip}
						<li>{tip}</li>
					{/each}
				</ul>
			</article>
			<article class="card comments">
				<h2>Comentarios destacados</h2>
				{#each recipe.comments as comment}
					<div class="comment">
						<strong>{comment.user}</strong>
						<span>{comment.city}</span>
						<p>{comment.comment}</p>
					</div>
				{/each}
			</article>
		</div>
	</section>

	<section class="recommended">
		<div class="container">
			<header class="section-head">
				<h2>También te puede gustar</h2>
				<p>Recetas con perfiles nutricionales similares para mantener tu plan variado.</p>
			</header>
			<div class="carousel">
				{#each recommendedWithImages as item}
					<a class="card" href={`/recetas/${item.slug}`}>
						<img src={item.image} alt={item.title} />
						<div class="card-body">
							<h3>{item.title}</h3>
							<p>{item.time} • {item.calories} kcal</p>
							<div class="tags">
								{#each item.tags as tag}
									<span>{tag}</span>
								{/each}
							</div>
						</div>
					</a>
				{/each}
			</div>
		</div>
	</section>
</main>

<style>
	.recipe-detail {
		display: flex;
		flex-direction: column;
		gap: 4.5rem;
		padding-bottom: 5rem;
	}

	.container {
		max-width: 1100px;
		margin: 0 auto;
		padding: 0 1.5rem;
	}

	.hero {
		padding-top: 2.5rem;
	}

	.hero-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 3rem;
		align-items: center;
	}

	.copy h1 {
		margin: 0 0 0.75rem;
		font-size: clamp(2.2rem, 3vw, 3.1rem);
	}

	.copy p {
		margin: 0;
		color: var(--color-soft);
		font-size: 1.05rem;
	}

	.meta {
		margin-top: 1.5rem;
		display: flex;
		flex-wrap: wrap;
		gap: 0.8rem;
		color: var(--color-soft);
		font-weight: 600;
	}

	.tag-row {
		margin-top: 1.2rem;
		display: flex;
		gap: 0.6rem;
		flex-wrap: wrap;
	}

	.cta {
		margin-top: 2rem;
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
	}

	.media {
		position: relative;
	}

	.media img {
		width: 100%;
		border-radius: var(--radius-lg);
		height: 360px;
		object-fit: cover;
		box-shadow: var(--shadow-soft);
	}

	.overlay-card {
		position: absolute;
		bottom: -30px;
		right: 20px;
		background: rgba(255, 255, 255, 0.9);
		backdrop-filter: blur(10px);
		border-radius: var(--radius-md);
		padding: 1.4rem;
		box-shadow: 0 20px 40px rgba(8, 44, 36, 0.18);
		width: min(260px, 80%);
	}

	.overlay-card h3 {
		margin: 0 0 1rem;
		font-size: 1.1rem;
	}

	.overlay-card ul {
		margin: 0;
		padding: 0;
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		color: var(--color-soft);
	}

	.content-grid {
		display: grid;
		grid-template-columns: 320px 1fr;
		gap: 2rem;
	}

	.ingredients ul {
		margin: 0;
		padding-left: 1.1rem;
		color: var(--color-soft);
		line-height: 1.7;
	}

	.steps ol {
		margin: 0;
		padding: 0;
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: 1.4rem;
	}

	.steps li {
		display: grid;
		grid-template-columns: auto 1fr;
		gap: 1rem;
		align-items: start;
	}

	.step-index {
		width: 36px;
		height: 36px;
		border-radius: 50%;
		background: var(--gradient-leaf);
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: 700;
	}

	.steps p {
		margin: 0;
		color: var(--color-soft);
		line-height: 1.7;
	}

	.extras-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 2rem;
	}

	.tips ul {
		margin: 0;
		padding-left: 1.1rem;
		color: var(--color-soft);
		line-height: 1.6;
	}

	.comments {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.comment {
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
		padding-bottom: 1rem;
		border-bottom: 1px solid rgba(8, 44, 36, 0.08);
	}

	.comment p {
		margin: 0;
		color: var(--color-soft);
	}

	.recommended .carousel {
		display: grid;
		grid-auto-flow: column;
		grid-auto-columns: minmax(240px, 1fr);
		gap: 1.5rem;
		overflow-x: auto;
		scroll-snap-type: x mandatory;
		padding-bottom: 0.5rem;
	}

	.recommended .carousel::-webkit-scrollbar {
		height: 6px;
	}

	.recommended .carousel::-webkit-scrollbar-thumb {
		background: rgba(8, 44, 36, 0.15);
		border-radius: 999px;
	}

	.recommended .card {
		text-decoration: none;
		color: inherit;
		border-radius: var(--radius-md);
		box-shadow: 0 18px 32px rgba(8, 44, 36, 0.1);
		overflow: hidden;
		display: flex;
		flex-direction: column;
		scroll-snap-align: start;
		background: var(--color-card);
		transition:
			transform 0.2s ease,
			box-shadow 0.2s ease;
	}

	.recommended .card:hover {
		transform: translateY(-4px);
		box-shadow: 0 24px 38px rgba(8, 44, 36, 0.14);
	}

	.recommended img {
		height: 160px;
		object-fit: cover;
		width: 100%;
	}

	.card-body {
		padding: 1.4rem;
		display: flex;
		flex-direction: column;
		gap: 0.8rem;
	}

	.card-body h3 {
		margin: 0;
		font-size: 1.1rem;
	}

	.card-body p {
		margin: 0;
		color: var(--color-soft);
	}

	.tags {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
	}

	.tags span {
		background: rgba(15, 184, 114, 0.12);
		color: var(--color-forest);
		padding: 0.25rem 0.6rem;
		border-radius: 999px;
		font-size: 0.8rem;
		font-weight: 600;
	}

	.badge.warning {
		background: rgba(255, 178, 90, 0.2);
		color: #b36b05;
		padding: 0.4rem 0.9rem;
		border-radius: 999px;
		font-weight: 600;
		font-size: 0.85rem;
	}

	@media (max-width: 880px) {
		.content-grid {
			grid-template-columns: 1fr;
		}

		.overlay-card {
			position: static;
			margin-top: 1.5rem;
			width: 100%;
		}
	}

	@media (max-width: 640px) {
		.cta {
			flex-direction: column;
		}

		.media img {
			height: 260px;
		}
	}
</style>
