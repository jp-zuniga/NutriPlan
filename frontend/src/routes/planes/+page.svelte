<script>
	import Banner from '$lib/components/Banner.svelte';

	import ImagenVigoron from '$lib/assets/vigoron.jpg';
	import PlatosTipicos from '$lib/assets/platos-tipicos.jpeg';

	const planSummaries = [
		{
			name: 'Plan activo semanal',
			goal: 'Pérdida de peso saludable',
			calories: '2,050 kcal / día',
			progress: 72,
			meals: ['Desayuno energético', 'Almuerzo tradicional', 'Cena ligera'],
			image: ImagenVigoron
		},
		{
			name: 'Rendimiento ciclismo',
			goal: 'Aumento de energía',
			calories: '2,400 kcal / día',
			progress: 45,
			meals: ['Snack pre entreno', 'Comida rica en carbohidratos', 'Smoothie nocturno'],
			image: PlatosTipicos
		}
	];

	const weeklyMacro = [
		{ day: 'L', calories: 2050, carbs: 48, protein: 26, fats: 26 },
		{ day: 'M', calories: 2100, carbs: 50, protein: 25, fats: 25 },
		{ day: 'X', calories: 1990, carbs: 46, protein: 28, fats: 26 },
		{ day: 'J', calories: 2080, carbs: 47, protein: 27, fats: 26 },
		{ day: 'V', calories: 2150, carbs: 49, protein: 26, fats: 25 },
		{ day: 'S', calories: 2220, carbs: 51, protein: 25, fats: 24 },
		{ day: 'D', calories: 1980, carbs: 45, protein: 27, fats: 28 }
	];

	const aiHighlights = [
		{
			title: 'Balance automático',
			description: 'La IA ajusta calorías y macros según tus check-ins diarios de energía y hambre.'
		},
		{
			title: 'Reemplazos inteligentes',
			description: 'Recibe sugerencias instantáneas basadas en ingredientes disponibles y temporada.'
		},
		{
			title: 'Alertas de micronutrientes',
			description: 'Identificamos deficiencias de hierro, calcio o vitamina C y proponemos recetas específicas.'
		}
	];

	const schedule = [
		{
			meal: 'Desayuno',
			recipe: 'Gallo pinto integral con huevo pochado',
			swap: 'Cambiar por batido verde'
		},
		{
			meal: 'Almuerzo',
			recipe: 'Vigorón saludable con yuca al vapor',
			swap: 'Ver opciones vegetarianas'
		},
		{
			meal: 'Cena',
			recipe: 'Sopa de queso liviana',
			swap: 'Añadir pan de elote integral'
		}
	];
</script>

<Banner />

<main class="plans">
	<section class="hero">
		<div class="container hero-inner">
			<div class="copy">
				<h1>Gestiona tus planes nutricionales personalizados</h1>
				<p>
					Crea, edita y haz seguimiento a menús diseñados por IA que combinan cocina nicaragüense con
					tus metas de salud.
				</p>
				<div class="actions">
					<a class="btn primary" href="/planificador-ia">Generar un nuevo plan</a>
					<a class="btn ghost" href="#mis-planes">Ver mis planes</a>
				</div>
			</div>
			<div class="stats card">
				<h3>Resumen semanal</h3>
				<div class="stat-row">
					<div>
						<strong>2,050 kcal</strong>
						<span>Consumo promedio</span>
					</div>
					<div>
						<strong>74%</strong>
						<span>Objetivo completado</span>
					</div>
					<div>
						<strong>+3</strong>
						<span>Recetas nuevas esta semana</span>
					</div>
				</div>
				<p class="note">Tu nutricionista recomienda mantener al menos 7 horas de sueño para optimizar resultados.</p>
			</div>
		</div>
	</section>

	<section id="mis-planes" class="saved-plans">
		<div class="container">
			<header class="section-head">
				<h2>Mis planes activos</h2>
				<p>Duplica, ajusta o comparte con tu nutricionista en un clic.</p>
			</header>
			<div class="plan-grid">
				{#each planSummaries as plan}
					<article class="plan-card">
						<img src={plan.image} alt={plan.name} />
						<div class="plan-body">
							<h3>{plan.name}</h3>
							<span class="goal">{plan.goal}</span>
							<p>{plan.calories}</p>
							<div class="progress">
								<div style={`width: ${plan.progress}%`}></div>
							</div>
							<ul>
								{#each plan.meals as meal}
									<li>{meal}</li>
								{/each}
							</ul>
							<div class="plan-actions">
								<a href="#">Ver detalle</a>
								<a href="#">Exportar</a>
							</div>
						</div>
					</article>
				{/each}
			</div>
		</div>
	</section>

	<section class="analytics">
		<div class="container analytics-grid">
			<div class="macros card">
				<h2>Balance diario</h2>
				<div class="chart">
					{#each weeklyMacro as day}
						<div class="bar">
							<span class="label">{day.day}</span>
							<div class="stack">
								<div class="segment carbs" style={`height: ${day.carbs * 1.5}px`}></div>
								<div class="segment protein" style={`height: ${day.protein * 1.5}px`}></div>
								<div class="segment fats" style={`height: ${day.fats * 1.5}px`}></div>
							</div>
							<span class="calories">{day.calories}</span>
						</div>
					{/each}
				</div>
				<p class="legend"><span class="carbs"></span>Carbohidratos <span class="protein"></span>Proteínas <span class="fats"></span>Grasas</p>
			</div>
			<div class="schedule card">
				<h2>Plan de hoy</h2>
				<ul>
					{#each schedule as item}
						<li>
							<div>
								<strong>{item.meal}</strong>
								<span>{item.recipe}</span>
							</div>
							<button type="button">{item.swap}</button>
						</li>
					{/each}
				</ul>
			</div>
		</div>
	</section>

	<section class="ai-highlights">
		<div class="container">
			<header class="section-head">
				<h2>Cómo te ayuda nuestra IA</h2>
				<p>Un copiloto nutricional que aprende de tus hábitos y preferencias.</p>
			</header>
			<div class="highlight-grid">
				{#each aiHighlights as item}
					<article>
						<h3>{item.title}</h3>
						<p>{item.description}</p>
					</article>
				{/each}
			</div>
		</div>
	</section>
</main>

<style>
	.plans {
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
		padding-top: 2rem;
	}

	.hero-inner {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 2rem;
		align-items: stretch;
	}

	.copy {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.copy h1 {
		margin: 0;
		font-size: clamp(2rem, 2.6vw, 3rem);
	}

	.copy p {
		margin: 0;
		color: var(--color-soft);
	}

	.actions {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
	}

	.stats {
		padding: 2rem;
		background: rgba(255, 255, 255, 0.88);
		backdrop-filter: blur(12px);
		border-radius: var(--radius-lg);
		box-shadow: var(--shadow-soft);
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.stats h3 {
		margin: 0;
	}

	.stat-row {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
		gap: 1rem;
	}

	.stat-row strong {
		font-size: 1.4rem;
		color: var(--color-forest);
	}

	.stat-row span {
		color: var(--color-soft);
	}

	.note {
		margin: 0;
		font-size: 0.95rem;
		color: var(--color-soft);
	}

	.plan-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 2rem;
		margin-top: 2rem;
	}

	.plan-card {
		background: rgba(255, 255, 255, 0.92);
		border-radius: var(--radius-lg);
		overflow: hidden;
		box-shadow: var(--shadow-soft);
		display: flex;
		flex-direction: column;
		transition: transform 0.2s ease, box-shadow 0.2s ease;
	}

	.plan-card:hover {
		transform: translateY(-4px);
		box-shadow: 0 28px 44px rgba(8, 44, 36, 0.18);
	}

	.plan-card img {
		width: 100%;
		height: 180px;
		object-fit: cover;
	}

	.plan-body {
		padding: 1.8rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.plan-body h3 {
		margin: 0;
	}

	.plan-body p {
		margin: 0;
		color: var(--color-soft);
	}

	.goal {
		font-weight: 600;
		color: var(--color-forest);
	}

	.progress {
		width: 100%;
		height: 8px;
		background: rgba(8, 44, 36, 0.1);
		border-radius: 999px;
		overflow: hidden;
	}

	.progress div {
		height: 100%;
		background: var(--gradient-leaf);
	}

	.plan-body ul {
		margin: 0;
		padding-left: 1rem;
		color: var(--color-soft);
		line-height: 1.6;
	}

	.plan-actions {
		display: flex;
		gap: 1rem;
		font-weight: 600;
	}

	.plan-actions a {
		text-decoration: none;
		color: var(--color-forest);
	}

	.analytics-grid {
		display: grid;
		grid-template-columns: 2fr 1fr;
		gap: 2rem;
	}

	.macros {
		padding: 2rem;
	}

	.chart {
		display: flex;
		gap: 1rem;
		align-items: flex-end;
	}

	.bar {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.6rem;
	}

	.stack {
		width: 40px;
		border-radius: 20px;
		overflow: hidden;
		background: rgba(8, 44, 36, 0.08);
		height: 240px;
		display: flex;
		flex-direction: column-reverse;
	}

	.segment {
		width: 100%;
	}

	.segment.carbs {
		background: rgba(15, 184, 114, 0.45);
	}

	.segment.protein {
		background: rgba(104, 211, 255, 0.4);
	}

	.segment.fats {
		background: rgba(255, 178, 90, 0.45);
	}

	.label {
		font-weight: 700;
	}

	.calories {
		font-size: 0.85rem;
		color: var(--color-soft);
	}

	.legend {
		display: flex;
		align-items: center;
		gap: 1rem;
		color: var(--color-soft);
		margin-top: 1.5rem;
	}

	.legend span {
		display: inline-flex;
		width: 14px;
		height: 14px;
		border-radius: 999px;
	}

	.legend .carbs {
		background: rgba(15, 184, 114, 0.45);
	}

	.legend .protein {
		background: rgba(104, 211, 255, 0.4);
	}

	.legend .fats {
		background: rgba(255, 178, 90, 0.45);
	}

	.schedule {
		padding: 2rem;
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.schedule ul {
		margin: 0;
		padding: 0;
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.schedule li {
		background: rgba(255, 255, 255, 0.75);
		border-radius: var(--radius-md);
		padding: 1.2rem 1.4rem;
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 1.5rem;
	}

	.schedule strong {
		font-size: 1.05rem;
	}

	.schedule span {
		color: var(--color-soft);
	}

	.schedule button {
		border: none;
		background: rgba(15, 184, 114, 0.15);
		color: var(--color-forest);
		font-weight: 600;
		border-radius: 999px;
		padding: 0.55rem 1rem;
		cursor: pointer;
	}

	.highlight-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
		gap: 1.5rem;
		margin-top: 2rem;
	}

	.highlight-grid article {
		background: rgba(255, 255, 255, 0.92);
		border-radius: var(--radius-md);
		padding: 1.8rem;
		box-shadow: var(--shadow-soft);
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.highlight-grid h3 {
		margin: 0;
	}

	.highlight-grid p {
		margin: 0;
		color: var(--color-soft);
	}

	@media (max-width: 960px) {
		.analytics-grid {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 640px) {
		.actions {
			flex-direction: column;
		}

		.schedule li {
			flex-direction: column;
			align-items: flex-start;
		}
	}
</style>
