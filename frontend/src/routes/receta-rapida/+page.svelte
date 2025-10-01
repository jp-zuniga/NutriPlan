<script>
	import Banner from '$lib/components/Banner.svelte';

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
</script>

<Banner />

<main class="pantry-mode">
	<section class="hero">
		<div class="container hero-inner">
			<div class="copy">
				<h1>Receta rápida: cocinar con lo que tienes</h1>
				<p>
					Selecciona ingredientes disponibles y obtén recetas ordenadas por porcentaje de coincidencia,
					tiempo y perfil nutricional.
				</p>
			</div>
			<form class="input-card">
				<label for="ingredient">Agregar ingrediente</label>
				<div class="input-row">
					<input id="ingredient" type="text" placeholder="Ej. chiltoma, queso fresco, papaya" />
					<button type="button">Añadir</button>
				</div>
				<div class="chips">
					{#each pantry as item}
						<span class="chip">{item}</span>
					{/each}
					<button type="button" class="ghost">Limpiar lista</button>
				</div>
				<div class="preferences">
					<label><input type="checkbox" checked /> Incluir solo opciones saludables</label>
					<label><input type="checkbox" /> Mostrar recetas veganas</label>
					<label><input type="checkbox" /> Filtrar por menos de 30 minutos</label>
				</div>
			</form>
		</div>
	</section>

	<section class="results">
		<div class="container">
			<header class="section-head">
				<h2>Resultados sugeridos por IA</h2>
				<p>Ordenados por coincidencia, impacto nutricional y popularidad en Nicaragua.</p>
			</header>
			<div class="result-grid">
				{#each suggestions as suggestion}
					<article class="card result">
						<div class="header">
							<h3>{suggestion.recipe}</h3>
							<span class="match">Coincidencia {suggestion.match}%</span>
						</div>
						<div class="meta">
							<span>{suggestion.time}</span>
							<span>{suggestion.steps} pasos</span>
							<span>{suggestion.health}</span>
						</div>
						<div class="progress">
							<div style={`width: ${suggestion.match}%`}></div>
						</div>
						<ul class="missing">
							{#each suggestion.missing as item}
								<li>Falta: {item}</li>
							{/each}
						</ul>
						<div class="actions">
							<a href="/recetas">Ver receta base</a>
							<a href="#">Generar versión personalizada</a>
						</div>
					</article>
				{/each}
			</div>
		</div>
	</section>

	<section class="smart-tips">
		<div class="container tips-grid">
			<article class="card summary">
				<h2>Optimiza tu despensa</h2>
				<p>
					Obtén recomendaciones priorizando ingredientes nicaragüenses, reduce desperdicios y conecta con
					proveedores locales.
				</p>
				<a class="btn primary" href="/planificador-ia">Sincronizar con mi plan</a>
			</article>
			<article class="card checklist">
				<h3>Consejos rápidos</h3>
				<ul>
					{#each smartTips as tip}
						<li>{tip}</li>
					{/each}
				</ul>
			</article>
		</div>
	</section>
</main>

<style>
	.pantry-mode {
		display: flex;
		flex-direction: column;
		gap: 4.5rem;
		padding-bottom: 5rem;
	}

	.container {
		max-width: 1000px;
		margin: 0 auto;
		padding: 0 1.5rem;
	}

	.hero-inner {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 2.5rem;
		align-items: start;
	}

	.copy h1 {
		margin: 0;
		font-size: clamp(2.1rem, 3vw, 3rem);
	}

	.copy p {
		margin: 1rem 0 0;
		color: var(--color-soft);
	}

	.input-card {
		background: rgba(255, 255, 255, 0.92);
		border-radius: var(--radius-lg);
		padding: 2.5rem;
		box-shadow: var(--shadow-soft);
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.input-row {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 1rem;
	}

	.input-row button {
		background: var(--gradient-leaf);
		color: white;
		border: none;
		border-radius: 999px;
		padding: 0 1.6rem;
		font-weight: 600;
		cursor: pointer;
	}

	.chips {
		display: flex;
		flex-wrap: wrap;
		gap: 0.8rem;
	}

	.chips .ghost {
		border: none;
		background: rgba(8, 44, 36, 0.08);
		color: var(--color-forest);
		border-radius: 999px;
		padding: 0.5rem 1rem;
		font-weight: 600;
		cursor: pointer;
	}

	.preferences {
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
		color: var(--color-soft);
	}

	.results .result-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
		gap: 1.8rem;
		margin-top: 2rem;
	}

	.result {
		padding: 1.8rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.result .header {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		gap: 1rem;
	}

	.match {
		font-weight: 700;
		color: var(--color-forest);
	}

	.meta {
		display: flex;
		flex-wrap: wrap;
		gap: 0.6rem;
		color: var(--color-soft);
		font-weight: 600;
	}

	.progress {
		height: 8px;
		background: rgba(8, 44, 36, 0.08);
		border-radius: 999px;
		overflow: hidden;
	}

	.progress div {
		height: 100%;
		background: var(--gradient-leaf);
	}

	.missing {
		margin: 0;
		padding-left: 1.1rem;
		color: var(--color-soft);
		line-height: 1.6;
	}

	.actions {
		display: flex;
		justify-content: space-between;
		align-items: center;
		flex-wrap: wrap;
		gap: 1rem;
		font-weight: 600;
	}

	.actions a {
		text-decoration: none;
		color: var(--color-forest);
	}

	.tips-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 2rem;
		align-items: stretch;
	}

	.summary {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.checklist {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.checklist ul {
		margin: 0;
		padding-left: 1.1rem;
		color: var(--color-soft);
		line-height: 1.6;
	}

	@media (max-width: 640px) {
		.input-row {
			grid-template-columns: 1fr;
		}

		.actions {
			justify-content: flex-start;
		}
	}
</style>
