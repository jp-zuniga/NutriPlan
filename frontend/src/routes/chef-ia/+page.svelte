<script>
	import Banner from '$lib/components/Banner.svelte';

	import SVG_AI from '$lib/assets/ai.svg';

	const features = [
		{
			title: 'Planificación consciente',
			description: 'Equilibra macros, tradiciones locales y tus objetivos en menos de un minuto.'
		},
		{
			title: 'Relevancia en tiempo real',
			description: 'La IA aprende de tus check-ins diarios y ajusta porciones, snacks y compras.'
		},
		{
			title: 'Contexto cultural',
			description: 'Recomendaciones basadas en ingredientes nicaragüenses disponibles en tu zona.'
		}
	];

	const assistants = [
		{
			name: 'Chef tradicional',
			description: 'Proteínas magras, granos enteros y sazón criolla.',
			tag: 'Sabores clásicos'
		},
		{
			name: 'Coach activo',
			description: 'Snacks energéticos, timing de carbohidratos y hidratación.',
			tag: 'Rendimiento'
		},
		{
			name: 'Nutri familiar',
			description: 'Menús para compartir, porciones balanceadas y economía local.',
			tag: 'Compartir'
		}
	];
</script>

<main class="chef-ia">
	<section class="hero">
		<div class="container hero-grid">
			<div class="copy">
				<span class="badge">Inteligencia culinaria nica</span>
				<h1>Conoce a Chef Nutri IA</h1>
				<p>
					Un asistente diseñado para transformar tus datos en planes deliciosos, sostenibles y
					auténticamente nicaragüenses. Sin recetas genéricas: todo se adapta a ti.
				</p>
				<div class="actions">
					<a class="btn primary" href="/planificador-ia">Crear mi plan</a>
					<a class="btn ghost" href="/planificador-ia">Ver evaluación</a>
				</div>
			</div>
			<div class="assistant card">
				<div class="avatar">
					<img src={SVG_AI} alt="Chef IA" />
				</div>
				<div class="message">
					<h2>Hola, soy Chef Nutri</h2>
					<p>Estoy listo para analizar tus preferencias y generar un plan sabroso y equilibrado.</p>
					<ul>
						<li>✅ Ajusto por presupuesto y tiempo</li>
						<li>✅ Sugerencias con ingredientes locales</li>
						<li>✅ Plan semanal + lista de compras</li>
					</ul>
				</div>
			</div>
		</div>
	</section>

	<section class="features">
		<div class="container">
			<header class="section-head">
				<h2>Lo que hace diferente a nuestra IA</h2>
				<p>Inteligencia alimentada con recetas nicas, datos nutricionales y feedback de la comunidad.</p>
			</header>
			<div class="feature-grid">
				{#each features as feature}
					<article class="card">
						<h3>{feature.title}</h3>
						<p>{feature.description}</p>
					</article>
				{/each}
			</div>
		</div>
	</section>

	<section class="assistants">
		<div class="container">
			<header class="section-head">
				<h2>Elige tu compañero ideal</h2>
				<p>Cada modo de Chef Nutri IA prioriza un estilo distinto según tus objetivos.</p>
			</header>
			<div class="assist-grid">
				{#each assistants as item}
					<article class="card">
						<span class="tag">{item.tag}</span>
						<h3>{item.name}</h3>
						<p>{item.description}</p>
						<a href="/planificador-ia">Activar modo</a>
					</article>
				{/each}
			</div>
		</div>
	</section>
</main>

<style>
	.chef-ia {
		display: flex;
		flex-direction: column;
		gap: 4.5rem;
		padding-bottom: 5rem;
	}

	.container {
		max-width: 1080px;
		margin: 0 auto;
		padding: 0 1.5rem;
	}

	.hero-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 2.5rem;
		align-items: center;
		margin-top: 2rem;
	}

	.copy .badge {
		display: inline-flex;
		align-items: center;
		padding: 0.4rem 1rem;
		border-radius: 999px;
		background: rgba(15, 184, 114, 0.15);
		color: var(--color-forest);
		font-weight: 600;
		margin-bottom: 1rem;
	}

	.copy h1 {
		margin: 0;
		font-size: clamp(2.3rem, 3vw, 3.4rem);
	}

	.copy p {
		margin: 1rem 0 0;
		color: var(--color-soft);
		line-height: 1.7;
	}

	.actions {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		margin-top: 1.5rem;
	}

	.assistant {
		display: grid;
		grid-template-columns: 120px 1fr;
		gap: 1.2rem;
		align-items: center;
		padding: 2rem;
	}

	.avatar {
		display: flex;
		align-items: center;
		justify-content: center;
		background: rgba(15, 184, 114, 0.1);
		border-radius: var(--radius-md);
		padding: 1rem;
	}

	.avatar img {
		width: 72px;
		height: 72px;
	}

	.message h2 {
		margin: 0 0 0.75rem;
	}

	.message p {
		margin: 0 0 0.75rem;
		color: var(--color-soft);
	}

	.message ul {
		margin: 0;
		padding-left: 1.1rem;
		color: var(--color-soft);
		line-height: 1.5;
	}

	.feature-grid,
	.assist-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
		gap: 1.5rem;
		margin-top: 2rem;
	}

	.feature-grid .card,
	.assist-grid .card {
		padding: 1.8rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.assist-grid a {
		font-weight: 600;
		text-decoration: none;
		color: var(--color-forest);
	}

	@media (max-width: 640px) {
		.assistant {
			grid-template-columns: 1fr;
			text-align: left;
		}
	}
</style>
