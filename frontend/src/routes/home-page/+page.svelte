<script>
	import Banner from '$lib/components/Banner.svelte';
	import { onMount } from 'svelte';

	// Datos de ejemplo para recetas destacadas
	let featuredRecipes = [
		{
			id: 1,
			name: 'Gallo Pinto Nicaragüense',
			description: 'Plato tradicional a base de arroz y frijoles',
			prepTime: 25,
			calories: 320,
			image: '/placeholder-recipe-1.jpg',
			tags: ['Nica', 'Tradicional', 'Vegetariano']
		},
		{
			id: 2,
			name: 'Vigorón',
			description: 'Yuca con chicharrones y ensalada de repollo',
			prepTime: 40,
			calories: 450,
			image: '/placeholder-recipe-2.jpg',
			tags: ['Nica', 'Tradicional']
		},
		{
			id: 3,
			name: 'Ensalada de Chayote',
			description: 'Refrescante ensalada con productos locales',
			prepTime: 15,
			calories: 120,
			image: '/placeholder-recipe-3.jpg',
			tags: ['Saludable', 'Bajo en Calorías', 'Vegetariano']
		}
	];

	let searchQuery = '';
	let user = null; // Se poblaría después del login

	// Función para manejar la búsqueda
	function handleSearch() {
		if (searchQuery.trim()) {
			// Navegar a página de resultados de búsqueda
			console.log('Buscando:', searchQuery);
		}
	}

	// Efecto al montar el componente
	onMount(() => {
		// Aquí se cargarían datos reales desde la API
	});
</script>

<svelte:head>
	<title>NutriPlan - Planificación nutricional inteligente</title>
	<meta
		name="description"
		content="Planifica tu alimentación con recetas nicaragüenses adaptadas a tus necesidades y condiciones médicas"
	/>
</svelte:head>

<div class="home-container">
	<!-- Hero Section -->
	<section class="hero">
		<div class="hero-content">
			<h1 class="hero-title">
				Nutrición personalizada para <span class="highlight">nicaragüenses</span>
			</h1>
			<p class="hero-subtitle">
				Planes alimenticios adaptados a tus metas, condiciones médicas y preferencias con
				ingredientes locales
			</p>

			<div class="cta-buttons">
				{#if user}
					<a href="/plan-generator" class="btn btn-primary">Crear mi plan</a>
				{:else}
					<a href="/register" class="btn btn-primary">Comenzar ahora</a>
					<a href="/login" class="btn btn-secondary">Iniciar sesión</a>
				{/if}
			</div>
		</div>

		<div class="hero-image">
			<img src="/placeholder-hero.jpg" alt="Platos saludables nicaragüenses" />
		</div>
	</section>

	<!-- Search Section -->
	<section class="search-section">
		<div class="container">
			<h2>Encuentra recetas con lo que tengas</h2>
			<div class="search-box">
				<input
					type="text"
					placeholder="Escribe los ingredientes que tienes (ej: arroz, frijoles, plátano)..."
					bind:value={searchQuery}
					on:keypress={(e) => e.key === 'Enter' && handleSearch()}
				/>
				<button on:click={handleSearch}>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="20"
						height="20"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					>
						<circle cx="11" cy="11" r="8"></circle>
						<line x1="21" y1="21" x2="16.65" y2="16.65"></line>
					</svg>
				</button>
			</div>
			<p class="search-hint">
				O explora nuestras <a href="/recipes">recetas con filtros avanzados</a>
			</p>
		</div>
	</section>

	<!-- Features Section -->
	<section class="features">
		<div class="container">
			<h2>¿Por qué elegir NutriPlan?</h2>
			<div class="features-grid">
				<div class="feature-card">
					<div class="feature-icon">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="32"
							height="32"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						>
							<path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
						</svg>
					</div>
					<h3>Personalizado</h3>
					<p>Planes adaptados a tus objetivos, condiciones médicas y nivel de actividad</p>
				</div>

				<div class="feature-card">
					<div class="feature-icon">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="32"
							height="32"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						>
							<path
								d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"
							></path>
							<line x1="7" y1="7" x2="7.01" y2="7"></line>
						</svg>
					</div>
					<h3>Ingredientes locales</h3>
					<p>Recetas con productos nicaragüenses fáciles de encontrar</p>
				</div>

				<div class="feature-card">
					<div class="feature-icon">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="32"
							height="32"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						>
							<path
								d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"
							></path>
							<polyline points="7.5 4.21 12 6.81 16.5 4.21"></polyline>
							<polyline points="7.5 19.79 7.5 14.6 3 12"></polyline>
							<polyline points="21 12 16.5 14.6 16.5 19.79"></polyline>
							<polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
							<line x1="12" y1="22.08" x2="12" y2="12"></line>
						</svg>
					</div>
					<h3>Impulsado por IA</h3>
					<p>Generación inteligente de planes y recetas según tus preferencias</p>
				</div>
			</div>
		</div>
	</section>

	<!-- Featured Recipes -->
	<section class="featured-recipes">
		<div class="container">
			<div class="section-header">
				<h2>Recetas destacadas</h2>
				<a href="/recipes" class="view-all">Ver todas</a>
			</div>

			<div class="recipes-grid">
				{#each featuredRecipes as recipe}
					<div class="recipe-card">
						<div class="recipe-image">
							<img src={recipe.image} alt={recipe.name} />
							<div class="recipe-tags">
								{#each recipe.tags as tag}
									<span class="tag">{tag}</span>
								{/each}
							</div>
						</div>
						<div class="recipe-content">
							<h3>{recipe.name}</h3>
							<p>{recipe.description}</p>
							<div class="recipe-meta">
								<span class="prep-time">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										width="16"
										height="16"
										viewBox="0 0 24 24"
										fill="none"
										stroke="currentColor"
										stroke-width="2"
										stroke-linecap="round"
										stroke-linejoin="round"
									>
										<circle cx="12" cy="12" r="10"></circle>
										<polyline points="12 6 12 12 16 14"></polyline>
									</svg>
									{recipe.prepTime} min
								</span>
								<span class="calories">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										width="16"
										height="16"
										viewBox="0 0 24 24"
										fill="none"
										stroke="currentColor"
										stroke-width="2"
										stroke-linecap="round"
										stroke-linejoin="round"
									>
										<path
											d="M17.5 22c.83 0 1.5-.67 1.5-1.5V6c0-2.21-1.79-4-4-4S11 3.79 11 6v14.5c0 .83.67 1.5 1.5 1.5h5z"
										></path>
										<path d="M11 6H7a4 4 0 0 0-4 4v6a4 4 0 0 0 4 4h1"></path>
									</svg>
									{recipe.calories} kcal
								</span>
							</div>
							<a href={`/recipes/${recipe.id}`} class="recipe-link">Ver receta →</a>
						</div>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- How it works -->
	<section class="how-it-works">
		<div class="container">
			<h2>¿Cómo funciona NutriPlan?</h2>
			<div class="steps">
				<div class="step">
					<div class="step-number">1</div>
					<h3>Completa tu perfil</h3>
					<p>Indica tus objetivos, condiciones médicas, preferencias y nivel de actividad</p>
				</div>
				<div class="step">
					<div class="step-number">2</div>
					<h3>Genera tu plan</h3>
					<p>Nuestra IA crea un plan nutricional semanal adaptado a tus necesidades</p>
				</div>
				<div class="step">
					<div class="step-number">3</div>
					<h3>Disfruta de comidas saludables</h3>
					<p>Cocina recetas deliciosas con ingredientes locales y fáciles de encontrar</p>
				</div>
			</div>
		</div>
	</section>

	<!-- Testimonials -->
	<section class="testimonials">
		<div class="container">
			<h2>Lo que dicen nuestros usuarios</h2>
			<div class="testimonials-grid">
				<div class="testimonial">
					<div class="testimonial-content">
						<p>
							"Como persona con diabetes, NutriPlan me ha ayudado a mantener mis niveles de azúcar
							con recetas adaptadas y deliciosas."
						</p>
					</div>
					<div class="testimonial-author">
						<strong>Carlos M.</strong>
						<span>Managua</span>
					</div>
				</div>
				<div class="testimonial">
					<div class="testimonial-content">
						<p>
							"Las recetas con ingredientes locales hacen que comer saludable sea accesible y
							económico para mi familia."
						</p>
					</div>
					<div class="testimonial-author">
						<strong>María L.</strong>
						<span>León</span>
					</div>
				</div>
				<div class="testimonial">
					<div class="testimonial-content">
						<p>
							"La función de receta rápida me salva cuando no sé qué cocinar con lo que tengo en la
							despensa."
						</p>
					</div>
					<div class="testimonial-author">
						<strong>Ana R.</strong>
						<span>Granada</span>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- Final CTA -->
	<section class="final-cta">
		<div class="container">
			<h2>Comienza tu journey nutricional hoy</h2>
			<p>Únete a miles de nicaragüenses que están transformando su salud con NutriPlan</p>
			<a href="/register" class="btn btn-large">Crear mi cuenta gratis</a>
		</div>
	</section>
</div>

<style>
	/* Variables de colores */
	:global(:root) {
		--primary: #2e7d32;
		--primary-light: #4caf50;
		--primary-dark: #1b5e20;
		--secondary: #ff6f00;
		--text: #333333;
		--text-light: #666666;
		--background: #ffffff;
		--background-alt: #f8f9fa;
		--border: #e0e0e0;
		--shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
		--shadow-hover: 0 8px 15px rgba(0, 0, 0, 0.1);
	}

	/* Estilos generales */
	.home-container {
		font-family:
			'Inter',
			-apple-system,
			BlinkMacSystemFont,
			'Segoe UI',
			Roboto,
			Oxygen,
			Ubuntu,
			sans-serif;
		color: var(--text);
		line-height: 1.6;
	}

	.container {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 1.5rem;
	}

	h1,
	h2,
	h3,
	h4,
	h5,
	h6 {
		font-weight: 700;
		line-height: 1.2;
		margin-bottom: 1rem;
	}

	/* Hero Section */
	.hero {
		display: flex;
		align-items: center;
		min-height: 80vh;
		padding: 2rem 0;
		background: linear-gradient(135deg, var(--background) 0%, #f1f8e9 100%);
	}

	.hero-content {
		flex: 1;
		padding: 0 2rem;
	}

	.hero-title {
		font-size: 3.5rem;
		margin-bottom: 1.5rem;
		color: var(--text);
	}

	.highlight {
		color: var(--primary);
		position: relative;
		display: inline-block;
	}

	.highlight::after {
		content: '';
		position: absolute;
		bottom: 0;
		left: 0;
		width: 100%;
		height: 30%;
		background-color: rgba(46, 125, 50, 0.2);
		z-index: -1;
	}

	.hero-subtitle {
		font-size: 1.25rem;
		color: var(--text-light);
		margin-bottom: 2.5rem;
		max-width: 600px;
	}

	.hero-image {
		flex: 1;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.hero-image img {
		max-width: 100%;
		border-radius: 10px;
		box-shadow: var(--shadow);
	}

	.cta-buttons {
		display: flex;
		gap: 1rem;
	}

	.btn {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: 0.75rem 1.5rem;
		border-radius: 8px;
		font-weight: 600;
		text-decoration: none;
		transition: all 0.3s ease;
		border: none;
		cursor: pointer;
	}

	.btn-primary {
		background-color: var(--primary);
		color: white;
	}

	.btn-primary:hover {
		background-color: var(--primary-dark);
		transform: translateY(-2px);
		box-shadow: var(--shadow-hover);
	}

	.btn-secondary {
		background-color: transparent;
		color: var(--primary);
		border: 2px solid var(--primary);
	}

	.btn-secondary:hover {
		background-color: var(--primary);
		color: white;
		transform: translateY(-2px);
		box-shadow: var(--shadow-hover);
	}

	.btn-large {
		padding: 1rem 2rem;
		font-size: 1.1rem;
	}

	/* Search Section */
	.search-section {
		padding: 4rem 0;
		background-color: var(--background);
		text-align: center;
	}

	.search-section h2 {
		margin-bottom: 1.5rem;
	}

	.search-box {
		display: flex;
		max-width: 600px;
		margin: 0 auto 1rem;
		border-radius: 50px;
		overflow: hidden;
		box-shadow: var(--shadow);
	}

	.search-box input {
		flex: 1;
		padding: 1rem 1.5rem;
		border: none;
		font-size: 1rem;
		outline: none;
	}

	.search-box button {
		padding: 1rem 1.5rem;
		background-color: var(--primary);
		color: white;
		border: none;
		cursor: pointer;
		transition: background-color 0.3s;
	}

	.search-box button:hover {
		background-color: var(--primary-dark);
	}

	.search-hint {
		color: var(--text-light);
		font-size: 0.9rem;
	}

	.search-hint a {
		color: var(--primary);
		text-decoration: none;
	}

	.search-hint a:hover {
		text-decoration: underline;
	}

	/* Features Section */
	.features {
		padding: 5rem 0;
		background-color: var(--background-alt);
	}

	.features h2 {
		text-align: center;
		margin-bottom: 3rem;
	}

	.features-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: 2rem;
	}

	.feature-card {
		background: white;
		padding: 2rem;
		border-radius: 12px;
		text-align: center;
		box-shadow: var(--shadow);
		transition:
			transform 0.3s,
			box-shadow 0.3s;
	}

	.feature-card:hover {
		transform: translateY(-5px);
		box-shadow: var(--shadow-hover);
	}

	.feature-icon {
		margin-bottom: 1.5rem;
		color: var(--primary);
	}

	.feature-card h3 {
		margin-bottom: 1rem;
		font-size: 1.5rem;
	}

	.feature-card p {
		color: var(--text-light);
	}

	/* Featured Recipes */
	.featured-recipes {
		padding: 5rem 0;
	}

	.section-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 2.5rem;
	}

	.view-all {
		color: var(--primary);
		text-decoration: none;
		font-weight: 600;
	}

	.view-all:hover {
		text-decoration: underline;
	}

	.recipes-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: 2rem;
	}

	.recipe-card {
		background: white;
		border-radius: 12px;
		overflow: hidden;
		box-shadow: var(--shadow);
		transition:
			transform 0.3s,
			box-shadow 0.3s;
	}

	.recipe-card:hover {
		transform: translateY(-5px);
		box-shadow: var(--shadow-hover);
	}

	.recipe-image {
		position: relative;
		height: 200px;
		overflow: hidden;
	}

	.recipe-image img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		transition: transform 0.5s;
	}

	.recipe-card:hover .recipe-image img {
		transform: scale(1.05);
	}

	.recipe-tags {
		position: absolute;
		top: 1rem;
		left: 1rem;
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.tag {
		background-color: var(--primary);
		color: white;
		padding: 0.25rem 0.5rem;
		border-radius: 20px;
		font-size: 0.75rem;
		font-weight: 600;
	}

	.recipe-content {
		padding: 1.5rem;
	}

	.recipe-content h3 {
		margin-bottom: 0.5rem;
		font-size: 1.25rem;
	}

	.recipe-content p {
		color: var(--text-light);
		margin-bottom: 1rem;
	}

	.recipe-meta {
		display: flex;
		justify-content: space-between;
		margin-bottom: 1rem;
		font-size: 0.9rem;
	}

	.prep-time,
	.calories {
		display: flex;
		align-items: center;
		gap: 0.25rem;
	}

	.recipe-link {
		color: var(--primary);
		text-decoration: none;
		font-weight: 600;
		display: inline-block;
		transition: transform 0.3s;
	}

	.recipe-link:hover {
		transform: translateX(5px);
	}

	/* How it works */
	.how-it-works {
		padding: 5rem 0;
		background-color: var(--background-alt);
	}

	.how-it-works h2 {
		text-align: center;
		margin-bottom: 3rem;
	}

	.steps {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
		gap: 2rem;
	}

	.step {
		text-align: center;
		padding: 2rem;
	}

	.step-number {
		width: 50px;
		height: 50px;
		background-color: var(--primary);
		color: white;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 1.5rem;
		font-weight: 700;
		margin: 0 auto 1.5rem;
	}

	.step h3 {
		margin-bottom: 1rem;
	}

	.step p {
		color: var(--text-light);
	}

	/* Testimonials */
	.testimonials {
		padding: 5rem 0;
	}

	.testimonials h2 {
		text-align: center;
		margin-bottom: 3rem;
	}

	.testimonials-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: 2rem;
	}

	.testimonial {
		background: white;
		padding: 2rem;
		border-radius: 12px;
		box-shadow: var(--shadow);
		position: relative;
	}

	.testimonial::before {
		content: '"';
		font-size: 5rem;
		color: var(--primary-light);
		opacity: 0.2;
		position: absolute;
		top: 0.5rem;
		left: 1rem;
		line-height: 1;
	}

	.testimonial-content {
		margin-bottom: 1.5rem;
		position: relative;
		z-index: 1;
	}

	.testimonial-author {
		display: flex;
		flex-direction: column;
	}

	.testimonial-author strong {
		color: var(--primary);
	}

	.testimonial-author span {
		font-size: 0.9rem;
		color: var(--text-light);
	}

	/* Final CTA */
	.final-cta {
		padding: 5rem 0;
		background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
		color: white;
		text-align: center;
	}

	.final-cta h2 {
		margin-bottom: 1rem;
	}

	.final-cta p {
		margin-bottom: 2rem;
		opacity: 0.9;
		max-width: 600px;
		margin-left: auto;
		margin-right: auto;
	}

	.final-cta .btn-large {
		background-color: white;
		color: var(--primary);
	}

	.final-cta .btn-large:hover {
		background-color: #f0f0f0;
		transform: translateY(-2px);
		box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
	}

	/* Responsive */
	@media (max-width: 768px) {
		.hero {
			flex-direction: column;
			text-align: center;
			padding: 2rem 0;
		}

		.hero-title {
			font-size: 2.5rem;
		}

		.hero-content,
		.hero-image {
			padding: 1rem;
		}

		.cta-buttons {
			justify-content: center;
		}

		.section-header {
			flex-direction: column;
			gap: 1rem;
			text-align: center;
		}

		.steps,
		.features-grid,
		.recipes-grid,
		.testimonials-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
