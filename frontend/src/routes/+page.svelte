<script>
	import Banner from '$lib/components/Banner.svelte';
	import { authUser } from '$lib/stores/auth';

	import ImagenVigoron from '$lib/assets/vigoron.jpg';
	import PlatosTipicos from '$lib/assets/platos-tipicos.jpeg';
	import GalloPinto from '$lib/assets/gallo-pinto.jpg';
	import SVG_AI from '$lib/assets/ai.svg';

	import icon_SoupBowl from '$lib/assets/soup-bowl.svg';
	import icon_Calendar from '$lib/assets/calendar.svg';
	import icon_RabbitFast from '$lib/assets/rabbit-fast.svg';

	const quickActions = [
		{
			title: 'Recetas',
			description:
				'Explora platos típicos, saludables y fusiones creativas para cada momento del día.',
			cta: 'Ver recetas',
			accent: 'leaf',
			icon: icon_SoupBowl
		},
		{
			title: 'Planes Nutricionales',
			description:
				'Genera un plan semanal que respete tus metas, tu actividad física y tus preferencias.',
			cta: 'Crear plan',
			accent: 'mint',
			icon: icon_Calendar
		},
		{
			title: 'Receta Rápida',
			description:
				'Escribe lo que tienes en casa y deja que nuestra IA sugiera la mejor coincidencia.',
			cta: 'Receta rápida',
			accent: 'sunrise',
			icon: icon_RabbitFast
		}
	];

	const featuredRecipes = [
		{
			title: 'Vigorón ligero',
			origin: 'Granada',
			kcal: '430 kcal',
			time: '35 min',
			rating: 4.8,
			tags: ['Popular', 'Alto en fibra'],
			image: ImagenVigoron
		},
		{
			title: 'Gallo Pinto energizante',
			origin: 'Managua',
			kcal: '380 kcal',
			time: '25 min',
			rating: 4.9,
			tags: ['Vegetariano', 'Desayuno'],
			image: GalloPinto
		},
		{
			title: 'Sopa de queso liviana',
			origin: 'Chontales',
			kcal: '320 kcal',
			time: '40 min',
			rating: 4.7,
			tags: ['Sin gluten', 'Reconfortante'],
			image: PlatosTipicos
		},
		{
			title: 'Ensalada de chayote verde',
			origin: 'Masaya',
			kcal: '280 kcal',
			time: '20 min',
			rating: 4.6,
			tags: ['Baja en carbohidratos', 'Refrescante'],
			image: PlatosTipicos
		}
	];

	const planBenefits = [
		{
			title: 'Plan semanal inteligente',
			description: 'La IA equilibra calorías, macros y tradición culinaria nica en un solo vistazo.'
		},
		{
			title: 'Sustituciones al instante',
			description: 'Intercambia recetas según ingredientes disponibles y mantén tus metas al día.'
		},
		{
			title: 'Seguimiento práctico',
			description: 'Visualiza el aporte nutricional diario y exporta tu plan para compartirlo.'
		}
	];

	const weeklyPreview = [
		{
			day: 'Lunes',
			breakfast: 'Gallo pinto integral + jugo verde',
			lunch: 'Vigorón al horno con yuca cocida',
			dinner: 'Filete de pescado criollo + ensalada cítrica'
		},
		{
			day: 'Miércoles',
			breakfast: 'Tortillas de maíz con queso fresco',
			lunch: 'Sopa de queso liviana',
			dinner: 'Pollo a la plancha con chayote salteado'
		},
		{
			day: 'Viernes',
			breakfast: 'Avena con banano caramelizado',
			lunch: 'Ensalada de chayote verde',
			dinner: 'Tacos de cerdo magro con repollo'
		}
	];

	const pantryIngredients = ['Yuca', 'Repollo', 'Limón', 'Chicharrón al horno', 'Tomate cherry'];

	const pantryMatches = [
		{
			title: 'Vigorón exprés',
			match: 86,
			missing: ['Vinagre de caña'],
			highlight: 'Listo en 20 minutos'
		},
		{
			title: 'Ensalada fresca de repollo',
			match: 72,
			missing: ['Semillas de sésamo'],
			highlight: 'Ideal para acompañar almuerzos'
		}
	];

	const communityHighlights = [
		{
			title: 'Favoritos compartidos',
			description: 'Guarda tus recetas top y descubre lo que otros nicas están cocinando.'
		},
		{
			title: 'Comentarios con propósito',
			description: 'Aprende tips de preparación y variaciones saludables de la comunidad.'
		},
		{
			title: 'Valoraciones confiables',
			description: 'Conoce el nivel de dificultad, tiempo real y calificaciones honestas.'
		}
	];

	const firstName = (name = '') => name.trim().split(' ')[0] || 'NutriChef';
</script>

<main class="home">
	<section class="hero">
		<div class="container hero-inner">
			<div class="hero-copy">
				<div class="pill no-select">
					<img src={SVG_AI} alt="ai" />
					Potenciado por IA
				</div>
				{#if $authUser}
					<span class="welcome">Hola, {firstName($authUser.name ?? $authUser.email)} 👋</span>
				{/if}
				<h1>NutriPlan, sabor y bienestar nicaragüense</h1>
				<p>
					Tu plataforma para planear comidas nutritivas con el sabor de casa. Recibe recomendaciones
					personalizadas, recetas auténticas y acompañamiento inteligente en cada etapa.
				</p>
				<div class="hero-actions">
					<a class="btn primary" href="/planes">Generar mi plan nutricional</a>
					<a class="btn ghost" href="/recetas">Explorar recetas</a>
				</div>
				<div class="hero-stats">
					<div class="stat">
						<span class="value">500+</span>
						<span class="label">Recetas locales</span>
					</div>
					<div class="stat">
						<span class="value">12k</span>
						<span class="label">Usuarios satisfechos</span>
					</div>
					<div class="stat">
						<span class="value">4.9★</span>
						<span class="label">Promedio en valoraciones</span>
					</div>
				</div>
			</div>
			<div class="hero-visual">
				<article class="hero-card main">
					<img src={ImagenVigoron} alt="Vigorón tradicional" />
					<div class="card-meta">
						<div class="meta-header">
							<span class="badge">Top nica</span>
							<span class="rating">★ 4.8</span>
						</div>
						<h3>Vigorón saludable</h3>
						<p>Yuca al vapor, chicharrón al horno y repollo cítrico.</p>
						<div class="meta-info">
							<span>430 kcal</span>
							<span>35 min</span>
						</div>
					</div>
				</article>
				<div class="hero-stack">
					<article class="mini-card">
						<img src={PlatosTipicos} alt="Platos típicos nicaragüenses" />
						<div>
							<h4>Plan semanal activo</h4>
							<span>Macros adaptados a tu rutina</span>
						</div>
					</article>
					<!-- <article class="mini-card alt">
						<div>
							<h4>Recetas compatibles</h4>
							<span>8 coincidencias con tus ingredientes</span>
						</div>
						<p>Agrega más ingredientes para afinar la búsqueda.</p>
					</article> -->
				</div>
			</div>
		</div>
	</section>

	<section class="quick-actions">
		<div class="container">
			<header class="section-head">
				<h2>Explora NutriPlan</h2>
				<p>Accede rápido a lo que necesitas: inspiración, planificación o una solución express.</p>
			</header>
			<div class="card-grid">
				{#each quickActions as action}
					<article class={`feature-card ${action.accent}`} style="color: white">
						<img src={action.icon} style="width: 35px; height: 35px" alt={action.title} />
						<!-- <span class="feature-icon">{action.icon}</span> -->
						<h3 style="color: white">{action.title}</h3>
						<p>{action.description}</p>
						<a href="#">{action.cta} →</a>
					</article>
				{/each}
			</div>
		</div>
	</section>

	<section class="featured">
		<div class="container">
			<header class="section-head" style="margin-bottom: 25px">
				<h2>Recetas destacadas de la semana</h2>
				<p>
					Curadas por nutricionistas nicas y la comunidad. Ajusta filtros para calorías, tiempo o
					preferencias.
				</p>
			</header>
			<div class="recipe-carousel">
				{#each featuredRecipes as recipe}
					<article class="recipe-card">
						<div class="image-wrap">
							<img src={recipe.image} alt={recipe.title} />
							<span class="recipe-rating">★ {recipe.rating}</span>
						</div>
						<div class="recipe-body">
							<h3>{recipe.title}</h3>
							<span class="origin">{recipe.origin}</span>
							<div class="meta">
								<span>{recipe.kcal}</span>
								<span>{recipe.time}</span>
							</div>
							<div class="tags">
								{#each recipe.tags as tag}
									<span>{tag}</span>
								{/each}
							</div>
						</div>
					</article>
				{/each}
			</div>
		</div>
	</section>

	<section class="ai-planner">
		<div class="container ai-inner">
			<div class="planner-copy">
				<h2>Generador de planes nutricionales con IA</h2>
				<p>
					Responde unas pocas preguntas sobre tu actividad física, metas y condiciones médicas para
					recibir un plan ajustado a tu día a día.
				</p>
				<ul>
					{#each planBenefits as benefit}
						<li>
							<h3>{benefit.title}</h3>
							<p>{benefit.description}</p>
						</li>
					{/each}
				</ul>
				<div class="planner-actions">
					<a class="btn primary" href="#">Comenzar evaluación</a>
					<span>Gratis y listo en menos de 3 minutos</span>
				</div>
			</div>
			<div class="planner-preview">
				<div class="preview-card">
					<h4>Vista previa semanal</h4>
					<ul>
						{#each weeklyPreview as day}
							<li>
								<span class="day">{day.day}</span>
								<div class="meals">
									<p><strong>Desayuno:</strong> {day.breakfast}</p>
									<p><strong>Almuerzo:</strong> {day.lunch}</p>
									<p><strong>Cena:</strong> {day.dinner}</p>
								</div>
							</li>
						{/each}
					</ul>
					<div class="preview-footer">
						<span>Macros balanceados • 2,000 kcal promedio</span>
					</div>
				</div>
			</div>
		</div>
	</section>

	<section class="pantry-mode">
		<div class="container pantry-inner">
			<div class="pantry-copy">
				<h2>Receta rápida: cocina con lo que tienes</h2>
				<p>
					Selecciona tus ingredientes y recibe recetas ordenadas por porcentaje de coincidencia.
					Ideal para aprovechar tu despensa sin complicaciones.
				</p>
				<div class="ingredient-chips">
					{#each pantryIngredients as ingredient}
						<span class="chip">{ingredient}</span>
					{/each}
				</div>
			</div>
			<div class="matches">
				{#each pantryMatches as match}
					<article class="match-card">
						<header>
							<h3>{match.title}</h3>
							<span>{match.highlight}</span>
						</header>
						<div class="progress">
							<div style={`width: ${match.match}%`}></div>
						</div>
						<p class="match-percent">Coincidencia del {match.match}%</p>
						<ul>
							{#each match.missing as missing}
								<li>Falta: {missing}</li>
							{/each}
						</ul>
					</article>
				{/each}
			</div>
		</div>
	</section>

	<section class="community">
		<div class="container community-inner">
			<header class="section-head">
				<h2>Comunidad y experiencias reales</h2>
				<p>Comparte tus resultados, recibe retroalimentación y construye hábitos sostenibles.</p>
			</header>
			<div class="community-grid">
				{#each communityHighlights as highlight}
					<article>
						<h3>{highlight.title}</h3>
						<p>{highlight.description}</p>
					</article>
				{/each}
				<div class="testimonial">
					<blockquote>
						“NutriPlan me ayudó a adaptar recetas tradicionales a mi plan de pérdida de peso sin
						sacrificar sabor.”
					</blockquote>
					<cite>María José • Managua</cite>
				</div>
			</div>
		</div>
	</section>

	<section class="cta-final">
		<div class="container cta-inner">
			<div>
				<h2 style="color: white">Listo para comer mejor, con sabor a Nicaragua</h2>
				<p>Crea tu cuenta gratis y comienza a recibir recomendaciones hechas a tu medida.</p>
			</div>
			<div class="cta-actions">
				<a class="btn primary" href="#">Crear cuenta gratis</a>
				<a class="btn ghost" href="#">Hablar con un nutricionista</a>
			</div>
		</div>
	</section>
</main>

<style>
	:global(body) {
		margin: 0;
		background: var(--color-cream);
		color: var(--color-ink);
		overflow-x: hidden;
	}

	.home {
		display: flex;
		flex-direction: column;
		gap: 6rem;
		padding-bottom: 6rem;
	}

	section {
		position: relative;
	}

	.container {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 1.5rem;
	}

	.section-head h2 {
		margin: 0 0 0.5rem;
		font-size: clamp(1.8rem, 2.4vw, 2.6rem);
	}

	.section-head p {
		margin: 0;
		color: var(--color-soft);
		font-size: 1rem;
		line-height: 1.6;
	}

	.hero {
		padding: 4rem 0 2rem;
	}

	.hero-inner {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		align-items: center;
		gap: 3rem;
		background: linear-gradient(135deg, rgba(246, 253, 247, 1) 0%, rgba(222, 245, 235, 0.75) 100%);
		border-radius: var(--radius-lg);
		padding: clamp(2.5rem, 4vw, 4rem);
		box-shadow: var(--shadow-soft);
		overflow: hidden;
	}

	.hero-inner::before,
	.hero-inner::after {
		content: '';
		position: absolute;
		opacity: 0.35;
		filter: blur(50px);
	}

	.hero-inner::before {
		width: 300px;
		height: 300px;
		background: var(--gradient-leaf);
		top: -100px;
		right: -80px;
	}

	.hero-inner::after {
		width: 220px;
		height: 220px;
		background: var(--gradient-mint);
		bottom: -120px;
		left: -60px;
	}

	.hero-copy {
		position: relative;
		z-index: 1;
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.hero-copy h1 {
		margin: 0;
		font-size: clamp(2.2rem, 3vw, 3.2rem);
		line-height: 1.15;
	}

	.hero-copy p {
		margin: 0;
		color: var(--color-soft);
		line-height: 1.7;
	}

	.pill {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		background: linear-gradient(
			to right,
			#8e54e9,
			#4776e6
		); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
		color: var(--color-cream);
		padding: 0.5rem 1.2rem;
		border-radius: 999px;
		font-weight: 600;
		font-size: 0.9rem;
		width: fit-content;
	}

	.welcome {
		font-family: var(--font-accent);
		font-size: 1.1rem;
		color: var(--color-forest);
		margin-top: 0.25rem;
	}

	.pill img {
		width: 18px;
		height: 18px;
	}

	.hero-actions {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
	}

	.btn {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: 0.85rem 1.6rem;
		border-radius: 999px;
		border: none;
		font-weight: 600;
		font-size: 0.98rem;
		text-decoration: none;
		cursor: pointer;
		transition:
			transform 0.25s ease,
			box-shadow 0.25s ease;
	}

	.btn.primary {
		background: var(--gradient-leaf);
		color: white;
		box-shadow: 0 15px 25px rgba(30, 164, 93, 0.3);
	}

	.btn.primary:hover {
		transform: translateY(-2px);
		box-shadow: 0 20px 30px rgba(30, 164, 93, 0.35);
	}

	.btn.ghost {
		background: rgba(255, 255, 255, 0.65);
		color: var(--color-forest);
		border: 1px solid rgba(18, 38, 33, 0.12);
	}

	.btn.ghost:hover {
		transform: translateY(-2px);
	}

	.hero-stats {
		display: flex;
		flex-wrap: wrap;
		gap: 1.5rem;
		margin-top: 0.5rem;
	}

	.stat {
		display: flex;
		flex-direction: column;
		gap: 0.2rem;
	}

	.stat .value {
		font-size: 1.6rem;
		font-weight: 700;
	}

	.stat .label {
		color: var(--color-soft);
		font-size: 0.95rem;
	}

	.hero-visual {
		position: relative;
		z-index: 1;
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.hero-card.main {
		position: relative;
		border-radius: var(--radius-lg);
		overflow: hidden;
		box-shadow: var(--shadow-soft);
		isolation: isolate;
		height: 320px;
	}

	.hero-card.main div {
		opacity: 95%;
		/* backdrop-filter: blur(30px); */
	}

	.hero-card.main h3,
	p {
		margin-bottom: 0px;
		margin-top: 0px;
	}

	.hero-card img {
		width: 100%;
		height: 320px;
		object-fit: cover;
		filter: saturate(1.05);
	}

	.hero-card.main img {
		height: 150%;
		object-fit: cover;
	}

	.card-meta {
		position: absolute;
		bottom: 1.5rem;
		left: 1.5rem;
		right: 1.5rem;
		background: rgba(255, 255, 255, 0.92);
		backdrop-filter: blur(12px);
		border-radius: var(--radius-md);
		padding: 1rem 1.2rem;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.meta-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.badge {
		background: rgba(30, 164, 93, 0.15);
		color: var(--color-forest);
		padding: 0.3rem 0.75rem;
		border-radius: 999px;
		font-size: 0.75rem;
		font-weight: 600;
	}

	.rating {
		font-weight: 600;
		color: var(--color-leaf);
	}

	.meta-info {
		display: flex;
		gap: 1rem;
		color: var(--color-soft);
		font-size: 0.9rem;
	}

	.hero-stack {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.mini-card {
		display: grid;
		grid-template-columns: 110px 1fr;
		gap: 1rem;
		align-items: center;
		background: var(--color-card);
		border-radius: var(--radius-md);
		box-shadow: 0 12px 25px rgba(18, 38, 33, 0.12);
		padding: 1rem;
	}

	.mini-card img {
		width: 100%;
		height: 90px;
		object-fit: cover;
		border-radius: var(--radius-sm);
	}

	.mini-card h4 {
		margin: 0;
		font-size: 1.05rem;
	}

	.mini-card span {
		color: var(--color-soft);
		font-size: 0.9rem;
	}

	.mini-card.alt {
		grid-template-columns: 1fr;
		background: rgba(255, 255, 255, 0.6);
	}

	.mini-card.alt p {
		margin: 0;
		color: var(--color-soft);
		font-size: 0.9rem;
	}

	.card-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
		gap: 1.5rem;
		margin-top: 2.5rem;
	}

	.feature-card {
		border-radius: var(--radius-md);
		padding: 1.8rem;
		box-shadow: 0 18px 30px rgba(18, 38, 33, 0.12);
		color: white;
		display: flex;
		flex-direction: column;
		gap: 1.2rem;
	}

	.feature-card.leaf {
		background: var(--gradient-leaf);
	}

	.feature-card.mint {
		background: var(--gradient-mint);
	}

	.feature-card.sunrise {
		background: var(--gradient-sunrise);
		color: #4f3206;
	}

	.feature-card h3 {
		margin: 0;
		font-size: 1.4rem;
	}

	.feature-card p {
		margin: 0;
		font-size: 0.95rem;
		line-height: 1.6;
	}

	.feature-card a {
		color: inherit;
		font-weight: 600;
		text-decoration: none;
	}

	.feature-icon {
		font-size: 1.6rem;
	}

	.featured .recipe-carousel {
		display: grid;
		grid-auto-flow: column;
		grid-auto-columns: minmax(240px, 1fr);
		gap: 1.5rem;
		overflow-x: auto;
		scroll-snap-type: x mandatory;
		padding-bottom: 2rem;
	}

	.featured .recipe-carousel::-webkit-scrollbar {
		height: 6px;
	}

	.featured .recipe-carousel::-webkit-scrollbar-thumb {
		background: rgba(18, 38, 33, 0.15);
		border-radius: 999px;
	}

	.recipe-card {
		background: var(--color-card);
		border-radius: var(--radius-md);
		box-shadow: 0 15px 30px rgba(18, 38, 33, 0.12);
		scroll-snap-align: start;
		overflow: hidden;
		display: flex;
		flex-direction: column;
	}

	.image-wrap {
		position: relative;
		width: 100%;
		height: 180px;
		overflow: hidden;
	}

	.image-wrap img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.recipe-rating {
		position: absolute;
		top: 0.75rem;
		right: 0.75rem;
		background: rgba(0, 0, 0, 0.6);
		color: white;
		padding: 0.35rem 0.7rem;
		border-radius: 999px;
		font-size: 0.85rem;
	}

	.recipe-body {
		padding: 1.5rem;
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.recipe-body h3 {
		margin: 0;
		font-size: 1.2rem;
	}

	.recipe-body .origin {
		color: var(--color-soft);
		font-size: 0.9rem;
	}

	.meta {
		display: flex;
		gap: 1rem;
		color: var(--color-soft);
		font-size: 0.9rem;
	}

	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 0.6rem;
	}

	.tags span {
		background: rgba(30, 164, 93, 0.12);
		color: var(--color-forest);
		padding: 0.25rem 0.75rem;
		border-radius: 999px;
		font-size: 0.8rem;
		font-weight: 600;
	}

	.ai-planner {
		padding: 1rem 0;
	}

	.ai-inner {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 3rem;
		align-items: start;
	}

	.planner-copy {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.planner-copy p {
		margin: 0;
		color: var(--color-soft);
		line-height: 1.7;
	}

	.planner-copy ul {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 1.2rem;
	}

	.planner-copy li {
		background: var(--color-card);
		border-radius: var(--radius-md);
		padding: 1.2rem 1.4rem;
		box-shadow: 0 12px 25px rgba(18, 38, 33, 0.1);
	}

	.planner-copy h3 {
		margin: 0 0 0.4rem;
		font-size: 1.1rem;
	}

	.planner-actions {
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
	}

	.planner-actions span {
		color: var(--color-soft);
		font-size: 0.9rem;
	}

	.planner-preview {
		display: flex;
		justify-content: center;
	}

	.preview-card {
		width: min(100%, 360px);
		background: rgba(255, 255, 255, 0.88);
		backdrop-filter: blur(10px);
		border-radius: var(--radius-md);
		padding: 1.8rem 1.6rem;
		box-shadow: var(--shadow-soft);
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.preview-card h4 {
		margin: 0;
		font-size: 1.2rem;
	}

	.preview-card ul {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.preview-card li {
		display: grid;
		grid-template-columns: 80px 1fr;
		gap: 0.75rem;
	}

	.day {
		font-weight: 700;
		color: var(--color-forest);
	}

	.meals p {
		margin: 0;
		color: var(--color-soft);
		font-size: 0.9rem;
		line-height: 1.5;
	}

	.preview-footer {
		text-align: center;
		font-size: 0.9rem;
		color: var(--color-forest);
		background: rgba(30, 164, 93, 0.15);
		padding: 0.75rem 1rem;
		border-radius: var(--radius-sm);
		font-weight: 600;
	}

	.pantry-inner {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 3rem;
		align-items: start;
	}

	.pantry-copy {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.pantry-copy p {
		margin: 0;
		color: var(--color-soft);
		line-height: 1.7;
	}

	.ingredient-chips {
		display: flex;
		flex-wrap: wrap;
		gap: 0.75rem;
	}

	.chip {
		background: rgba(18, 38, 33, 0.08);
		padding: 0.55rem 1.1rem;
		border-radius: 999px;
		font-weight: 600;
		font-size: 0.9rem;
	}

	.matches {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.match-card {
		background: var(--color-card);
		border-radius: var(--radius-md);
		padding: 1.5rem;
		box-shadow: 0 15px 30px rgba(18, 38, 33, 0.12);
		position: relative;
	}

	.match-card header {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		gap: 1rem;
		margin-bottom: 1rem;
	}

	.match-card h3 {
		margin: 0;
		font-size: 1.15rem;
	}

	.match-card header span {
		color: var(--color-soft);
		font-size: 0.9rem;
	}

	.progress {
		width: 100%;
		height: 8px;
		background: rgba(18, 38, 33, 0.08);
		border-radius: 999px;
		overflow: hidden;
		margin-bottom: 0.75rem;
	}

	.progress div {
		height: 100%;
		background: var(--gradient-leaf);
	}

	.match-percent {
		margin: 0 0 0.5rem;
		font-weight: 600;
		color: var(--color-forest);
	}

	.match-card ul {
		margin: 0;
		padding-left: 1.1rem;
		color: var(--color-soft);
		font-size: 0.9rem;
		line-height: 1.6;
	}

	.community-inner {
		display: flex;
		flex-direction: column;
		gap: 2.5rem;
	}

	.community-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
		gap: 1.8rem;
	}

	.community-grid article,
	.testimonial {
		background: var(--color-card);
		border-radius: var(--radius-md);
		padding: 1.6rem;
		box-shadow: 0 15px 30px rgba(18, 38, 33, 0.12);
	}

	.community-grid h3 {
		margin: 0 0 0.6rem;
		font-size: 1.2rem;
	}

	.community-grid p {
		margin: 0;
		color: var(--color-soft);
		line-height: 1.6;
	}

	.testimonial blockquote {
		margin: 0 0 1rem;
		font-style: italic;
		line-height: 1.6;
	}

	.testimonial cite {
		font-weight: 600;
		color: var(--color-forest);
	}

	.cta-final {
		padding: 0 0 2rem;
	}

	.cta-inner {
		background: var(--gradient-leaf);
		border-radius: var(--radius-lg);
		padding: clamp(2.5rem, 4vw, 3.5rem);
		color: white;
		display: flex;
		flex-direction: column;
		gap: 2rem;
		align-items: flex-start;
		box-shadow: var(--shadow-soft);
	}

	.cta-inner h2 {
		margin: 0 0 0.5rem;
		font-size: clamp(2rem, 2.6vw, 2.8rem);
	}

	.cta-inner p {
		margin: 0;
		font-size: 1rem;
		line-height: 1.6;
	}

	.cta-actions {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
	}

	.cta-actions .btn.ghost {
		background: rgba(255, 255, 255, 0.2);
		color: white;
		border-color: rgba(255, 255, 255, 0.4);
	}

	@media (max-width: 900px) {
		.hero-inner::before,
		.hero-inner::after {
			display: none;
		}

		.hero-card img {
			height: 250px;
		}

		.preview-card li {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 640px) {
		.hero-actions,
		.cta-actions {
			flex-direction: column;
		}

		.hero-stats {
			gap: 1rem;
		}

		.hero-copy h1 {
			font-size: 2rem;
		}

		.card-grid {
			grid-template-columns: 1fr;
		}

		.featured .recipe-carousel {
			grid-auto-columns: 80%;
		}
	}
</style>
