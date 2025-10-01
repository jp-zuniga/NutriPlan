<script>
	import Banner from '$lib/components/Banner.svelte';

	const steps = [
		{ number: 1, title: 'Perfil', description: 'Edad, objetivo y nivel de actividad física.' },
		{ number: 2, title: 'Preferencias', description: 'Ingredientes favoritos, restricciones y cultura alimentaria.' },
		{ number: 3, title: 'Resultados', description: 'Plan semanal editable y métricas en tiempo real.' }
	];

	const activities = ['Sedentario', 'Ligero', 'Moderado', 'Intenso'];
	const goals = ['Perder peso', 'Mantener', 'Ganar masa muscular', 'Mejorar energía'];

	const preview = [
		{ day: 'Lunes', meals: ['Gallo pinto integral', 'Vigorón saludable', 'Sopa de queso liviana'] },
		{ day: 'Miércoles', meals: ['Smoothie verde tropical', 'Filete de pescado criollo', 'Ensalada de chayote'] },
		{ day: 'Viernes', meals: ['Avena con cacao', 'Indio viejo balanceado', 'Tacos de frijol'] }
	];

	const insights = [
		{
			title: 'Balance diario',
			detail: 'Tu plan mantiene 40% carbohidratos, 30% proteínas y 30% grasas saludables.'
		},
		{
			title: 'Temporada actual',
			detail: 'Se priorizan ingredientes frescos como chayote, mango verde y queso ahumado.'
		},
		{
			title: 'Recomendación de expertos',
			detail: 'Añade 2 litros de agua diarios y 2 snacks ricos en fibra para potenciar saciedad.'
		}
	];
</script>

<Banner />

<main class="planner">
	<section class="hero">
		<div class="container hero-grid">
			<div class="copy">
				<h1>Genera tu plan nutricional con IA en minutos</h1>
				<p>
					Nuestra IA combina recetas tradicionales nicaragüenses con tus necesidades nutricionales.
					Completa los pasos y obtén un plan listo para editar y compartir.
				</p>
				<div class="steps">
					{#each steps as step}
						<div class="step">
							<span>{step.number}</span>
							<h3>{step.title}</h3>
							<p>{step.description}</p>
						</div>
					{/each}
				</div>
			</div>
			<form class="card form">
				<h2>Configura tu plan</h2>
				<label for="age">Edad</label>
				<input id="age" type="number" min="12" max="90" placeholder="32" />
				<label for="goal">Meta principal</label>
				<select id="goal">
					{#each goals as goal}
						<option>{goal}</option>
					{/each}
				</select>
				<label for="activity">Actividad física</label>
				<select id="activity">
					{#each activities as activity}
						<option>{activity}</option>
					{/each}
				</select>
				<label for="restrictions">Restricciones o condiciones médicas</label>
				<textarea id="restrictions" rows="3" placeholder="Hipertensión, alergia a mariscos, etc."></textarea>
				<div class="form-actions">
					<button type="button" class="primary">Generar plan</button>
					<button type="button" class="ghost">Guardar borrador</button>
				</div>
			</form>
		</div>
	</section>

	<section class="preview">
		<div class="container preview-grid">
			<article class="card weekly">
				<h2>Vista previa semanal</h2>
				<div class="table">
					{#each preview as day}
						<div class="row">
							<strong>{day.day}</strong>
							<ul>
								{#each day.meals as meal}
									<li>{meal}</li>
								{/each}
							</ul>
							<button type="button">Reemplazar</button>
						</div>
					{/each}
				</div>
			</article>
			<article class="card metrics">
				<h2>Resumen nutricional</h2>
				<ul>
					<li><span>Calorías diarias:</span> 2,050 kcal</li>
					<li><span>Proteínas:</span> 130 g</li>
					<li><span>Carbohidratos:</span> 210 g</li>
					<li><span>Grasas saludables:</span> 68 g</li>
				</ul>
				<div class="insights">
					{#each insights as insight}
						<div>
							<h3>{insight.title}</h3>
							<p>{insight.detail}</p>
						</div>
					{/each}
				</div>
			</article>
		</div>
	</section>

	<section class="cta">
		<div class="container cta-card">
			<div>
				<h2>¿Listo para recibir un plan ajustado a tu vida?</h2>
				<p>Compártelo con tu nutricionista, imprime tu lista de compras o sincroniza con tu calendario.</p>
			</div>
			<div class="cta-actions">
				<a class="btn primary" href="/planes">Ver mis planes</a>
				<a class="btn ghost" href="/recetas">Añadir recetas favoritas</a>
			</div>
		</div>
	</section>
</main>

<style>
	.planner {
		display: flex;
		flex-direction: column;
		gap: 5rem;
		padding-bottom: 5rem;
	}

	.container {
		max-width: 1080px;
		margin: 0 auto;
		padding: 0 1.5rem;
	}

	.hero {
		padding-top: 2rem;
	}

	.hero-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
		gap: 2.5rem;
		align-items: start;
	}

	.copy {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.copy h1 {
		margin: 0;
		font-size: clamp(2.1rem, 3vw, 3.2rem);
	}

	.copy p {
		margin: 0;
		color: var(--color-soft);
		line-height: 1.7;
	}

	.steps {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
		gap: 1rem;
	}

	.step {
		background: rgba(255, 255, 255, 0.85);
		border-radius: var(--radius-md);
		padding: 1.5rem;
		box-shadow: var(--shadow-soft);
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
	}

	.step span {
		width: 40px;
		height: 40px;
		border-radius: 50%;
		background: var(--gradient-leaf);
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: 700;
	}

	.step h3 {
		margin: 0;
		font-size: 1.1rem;
	}

	.step p {
		margin: 0;
		color: var(--color-soft);
		font-size: 0.95rem;
	}

	.form {
		padding: 2.5rem;
		gap: 1.2rem;
		display: flex;
		flex-direction: column;
	}

	.form h2 {
		margin: 0;
	}

	.form textarea {
		resize: vertical;
	}

	.form-actions {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
	}

	.form-actions .primary {
		background: var(--gradient-leaf);
		color: white;
		border: none;
		border-radius: 999px;
		padding: 0.75rem 1.6rem;
		font-weight: 600;
		cursor: pointer;
		box-shadow: 0 16px 26px rgba(15, 184, 114, 0.28);
	}

	.form-actions .ghost {
		border: none;
		background: rgba(8, 44, 36, 0.08);
		color: var(--color-forest);
		border-radius: 999px;
		padding: 0.75rem 1.6rem;
		font-weight: 600;
		cursor: pointer;
	}

	.preview-grid {
		display: grid;
		grid-template-columns: 2fr 1fr;
		gap: 2rem;
	}

	.weekly {
		padding: 2.2rem;
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.table {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.row {
		background: rgba(255, 255, 255, 0.8);
		border-radius: var(--radius-md);
		padding: 1.2rem 1.4rem;
		display: grid;
		grid-template-columns: 100px 1fr auto;
		gap: 1rem;
		align-items: center;
	}

	.row ul {
		margin: 0;
		padding-left: 1rem;
		color: var(--color-soft);
		line-height: 1.6;
	}

	.row button {
		border: none;
		background: rgba(104, 211, 255, 0.2);
		color: var(--color-forest);
		padding: 0.55rem 1rem;
		border-radius: 999px;
		font-weight: 600;
		cursor: pointer;
	}

	.metrics {
		padding: 2.2rem;
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.metrics ul {
		margin: 0;
		padding: 0;
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: 0.8rem;
		color: var(--color-soft);
	}

	.metrics li span {
		font-weight: 600;
		color: var(--color-forest);
	}

	.insights {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.insights h3 {
		margin: 0;
		font-size: 1rem;
	}

	.insights p {
		margin: 0;
		color: var(--color-soft);
		font-size: 0.95rem;
	}

	.cta-card {
		background: var(--gradient-leaf);
		color: white;
		border-radius: var(--radius-lg);
		padding: clamp(2.5rem, 4vw, 3.5rem);
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		box-shadow: var(--shadow-soft);
	}

	.cta-card h2 {
		margin: 0;
	}

	.cta-card p {
		margin: 0;
		font-size: 1.05rem;
	}

	.cta-actions {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
	}

	@media (max-width: 900px) {
		.preview-grid {
			grid-template-columns: 1fr;
		}

		.row {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 640px) {
		.form-actions {
			flex-direction: column;
		}

		.cta-actions {
			flex-direction: column;
		}
	}
</style>
