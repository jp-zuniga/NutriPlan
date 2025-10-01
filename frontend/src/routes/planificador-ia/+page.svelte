<script>
	import { onDestroy } from 'svelte';
	import Banner from '$lib/components/Banner.svelte';

	import ImagenVigoron from '$lib/assets/vigoron.jpg';
	import PlatosTipicos from '$lib/assets/platos-tipicos.jpeg';

	const activityOptions = ['Sedentario', 'Ligero', 'Moderado', 'Intenso'];
	const goalOptions = ['Bajar de peso', 'Mantener peso', 'Aumentar masa muscular', 'Mejorar salud general'];
	const conditionOptions = ['Diabetes', 'Hipertensión', 'Colesterol alto', 'Problemas renales'];
	const dietOptions = ['Omnívora', 'Vegetariana', 'Vegana', 'Pescetariana', 'Keto / baja en carbohidratos', 'Mediterránea'];
	const budgetOptions = ['Bajo', 'Medio', 'Alto'];
	const cookingTimeOptions = ['Rápido (< 20 min)', 'Intermedio (30 – 45 min)', 'Sin límite'];
	const mealsPerDayOptions = ['3 comidas', '4 comidas', '5 comidas', 'Flexible'];
	const kitchenAccessOptions = ['Cocina completa', 'Solo estufa', 'Solo microondas', 'Espacio compartido'];

	const generatedPlan = {
		summary: [
			'Plan adaptado a tu objetivo de bajar 3 kg en 8 semanas con énfasis en fibra y proteínas magras.',
			'Se priorizan ingredientes locales como yuca, frijoles rojos, maíz y queso ahumado ligero.',
			'Las cenas se mantienen ligeras para favorecer descanso y control de glucosa.'
		],
		macros: {
			calories: '2,050 kcal',
			protein: '130 g',
			carbs: '230 g',
			fats: '58 g'
		},
		week: [
			{
				day: 'Lunes',
				meals: [
					'Gallo pinto integral con huevo pochado',
					'Ensalada de chayote verde con pollo a la plancha',
					'Sopa de queso liviana con tortillas integrales'
				],
				snack: 'Batido verde de espinaca, piña y hierbabuena'
			},
			{
				day: 'Miércoles',
				meals: [
					'Avena con cacao, banano y semillas de jícaro',
					'Vigorón saludable con curtido cítrico',
					'Filete de pescado criollo + ensalada de mango verde'
				],
				snack: 'Tostadas de maíz con frijoles molidos y pico de gallo'
			},
			{
				day: 'Viernes',
				meals: [
					'Smoothie de papaya y avena con semillas de chía',
					'Indio viejo ligero acompañado de ensalada verde',
					'Tacos de frijol rojo y chiltoma con queso fresco light'
				],
				snack: 'Brochetas de fruta tropical con limón y menta'
			}
		],
		shopping: ['Frijoles rojos', 'Yuca fresca', 'Queso ahumado light', 'Chayote', 'Hierbas frescas', 'Quinoa', 'Filete de pescado blanco'],
		adaptations: [
			'Reemplaza el queso en cenas por tofu marinado si quieres una versión vegana.',
			'Agrega 10 minutos de caminata después de la cena al menos 4 veces por semana.',
			'Programa recordatorios de hidratación cada 3 horas.'
		]
	};

	let stage = 'form';
	let timeoutId;

	const handleSubmit = (event) => {
		event.preventDefault();
		stage = 'loading';
		clearTimeout(timeoutId);
		timeoutId = setTimeout(() => {
			stage = 'result';
		}, 2000);
	};

	const resetPlanner = () => {
		clearTimeout(timeoutId);
		stage = 'form';
	};

	onDestroy(() => {
		clearTimeout(timeoutId);
	});
</script>

<Banner />

<main class="planner">
	<section class="intro">
		<div class="container intro-inner">
			<div class="copy">
				<h1>Chef Nutri IA</h1>
				<p>
					Completa el formulario y deja que nuestra IA combine nutrición, sabor nica y tus objetivos
					personales. En segundos tendrás un plan ajustado a tu realidad.
				</p>
			</div>
			<div class="visual card">
				<img src={ImagenVigoron} alt="Plan nutrido" />
				<div class="overlay">
					<strong>Plan inteligente</strong>
					<span>Se actualiza con tus avances cada semana</span>
				</div>
			</div>
		</div>
	</section>

	{#if stage === 'form'}
		<section class="form-section">
			<div class="container">
				<form class="card planner-form" on:submit={handleSubmit}>
					<h2>Completa tu evaluación personalizada</h2>
					<p class="hint">Tu información permanecerá privada y solo se usará para sugerencias nutricionales.</p>

					<div class="form-grid">
						<fieldset>
							<legend>🧑‍⚕️ Datos personales y de salud</legend>
							<div class="field-row">
								<div>
									<label for="age">Edad</label>
									<input id="age" type="number" min="12" max="99" placeholder="32" required />
								</div>
								<div>
									<label for="sex">Sexo</label>
									<select id="sex" required>
										<option value="">Selecciona</option>
										<option>Mujer</option>
										<option>Hombre</option>
										<option>No especificar</option>
									</select>
								</div>
							</div>
							<div class="field-row">
								<div>
									<label for="weight">Peso actual (kg)</label>
									<input id="weight" type="number" step="0.1" placeholder="62" />
								</div>
								<div>
									<label for="height">Estatura (cm)</label>
									<input id="height" type="number" placeholder="168" />
								</div>
							</div>
							<label for="activity">Nivel de actividad</label>
							<select id="activity" required>
								<option value="">Selecciona una opción</option>
								{#each activityOptions as option}
									<option>{option}</option>
								{/each}
							</select>
							<div class="goal-grid">
								<p>Objetivo principal</p>
								{#each goalOptions as goal}
									<label class="selectable">
										<input type="radio" name="goal" value={goal} required />
										<span>{goal}</span>
									</label>
								{/each}
							</div>
							<div class="checkbox-group">
								<p>Condiciones médicas relevantes</p>
								{#each conditionOptions as condition}
									<label class="selectable">
										<input type="checkbox" value={condition} />
										<span>{condition}</span>
									</label>
								{/each}
							</div>
							<label for="other-condition">Otras condiciones</label>
							<textarea id="other-condition" rows="2" placeholder="Describe cualquier otra condición"></textarea>
							<label for="allergies">Alergias alimentarias</label>
							<textarea id="allergies" rows="2" placeholder="Ej. maní, mariscos, lactosa"></textarea>
						</fieldset>

						<fieldset>
							<legend>🍴 Preferencias alimentarias</legend>
							<p>Tipo de dieta preferida</p>
							<div class="checkbox-group">
								{#each dietOptions as diet}
									<label class="selectable">
										<input type="radio" name="diet" value={diet} />
										<span>{diet}</span>
									</label>
								{/each}
								<label class="selectable">
									<input type="radio" name="diet" value="Otra" />
									<span>Otra (especificar)</span>
								</label>
							</div>
							<textarea rows="2" placeholder="Detalla otra dieta si aplica"></textarea>
							<label for="likes">Alimentos que disfrutas</label>
							<textarea id="likes" rows="2" placeholder="Ej. chiltoma, aguacate, quinua"></textarea>
							<label for="dislikes">Alimentos que deseas evitar</label>
							<textarea id="dislikes" rows="2" placeholder="Lista o razones"></textarea>
							<label for="availability">Disponibilidad de ingredientes locales</label>
							<textarea
								id="availability"
								rows="2"
								placeholder="Ej. frijoles rojos, maíz blanco, plátano, queso ahumado"
							></textarea>
						</fieldset>

						<fieldset>
							<legend>🎯 Expectativas y contexto</legend>
							<label for="expectations">Expectativa de resultados</label>
							<textarea id="expectations" rows="2" placeholder="Ej. perder 3 kg en 2 meses"></textarea>
							<div class="field-row">
								<div>
									<label for="budget">Presupuesto para alimentación</label>
									<select id="budget">
										<option value="">Selecciona</option>
										{#each budgetOptions as option}
											<option>{option}</option>
										{/each}
									</select>
								</div>
								<div>
									<label for="time">Tiempo disponible para cocinar</label>
									<select id="time">
										<option value="">Selecciona</option>
										{#each cookingTimeOptions as option}
											<option>{option}</option>
										{/each}
									</select>
								</div>
							</div>
							<label for="meals">Cantidad de comidas al día</label>
							<select id="meals">
								<option value="">Selecciona</option>
								{#each mealsPerDayOptions as option}
									<option>{option}</option>
								{/each}
							</select>
							<label for="kitchen">Acceso a cocina</label>
							<select id="kitchen">
								<option value="">Selecciona</option>
								{#each kitchenAccessOptions as option}
									<option>{option}</option>
								{/each}
							</select>
						</fieldset>

						<fieldset>
							<legend>👥 Funciones sociales y hábitos</legend>
							<div class="field-row">
								<div class="question">
									<p>¿Compartes tus comidas con la familia?</p>
									<label class="selectable">
										<input type="radio" name="family" value="Si" />
										<span>Sí</span>
									</label>
									<label class="selectable">
										<input type="radio" name="family" value="No" />
										<span>No</span>
									</label>
								</div>
								<div class="question">
									<p>¿Abierto a recetas nuevas tradicionales o fusión?</p>
									<label class="selectable">
										<input type="radio" name="new-recipes" value="Si" />
										<span>Sí</span>
									</label>
									<label class="selectable">
										<input type="radio" name="new-recipes" value="No" />
										<span>No</span>
									</label>
								</div>
							</div>
							<label for="history">Historial alimenticio (opcional)</label>
							<textarea id="history" rows="3" placeholder="Describe lo que sueles comer en un día"></textarea>
						</fieldset>
					</div>

					<div class="actions">
						<button class="btn primary" type="submit">Generar plan nutricional</button>
						<p class="disclaimer">Recibirás tu plan en menos de 10 segundos.</p>
					</div>
				</form>
			</div>
		</section>
	{:else if stage === 'loading'}
		<section class="loading">
			<div class="container">
				<div class="card loading-card">
					<div class="spinner"></div>
					<h2>Generando tu plan…</h2>
					<p>Chef Nutri IA está equilibrando macros, cultura nica y tus preferencias.</p>
				</div>
			</div>
		</section>
	{:else}
		<section class="result">
			<div class="container result-grid">
				<article class="card summary">
					<h2>Tu plan personalizado está listo</h2>
					<ul>
						{#each generatedPlan.summary as item}
							<li>{item}</li>
						{/each}
					</ul>
					<div class="macros">
						<div>
							<span>Calorías</span>
							<strong>{generatedPlan.macros.calories}</strong>
						</div>
						<div>
							<span>Proteínas</span>
							<strong>{generatedPlan.macros.protein}</strong>
						</div>
						<div>
							<span>Carbohidratos</span>
							<strong>{generatedPlan.macros.carbs}</strong>
						</div>
						<div>
							<span>Grasas</span>
							<strong>{generatedPlan.macros.fats}</strong>
						</div>
					</div>
					<div class="result-actions">
						<button class="btn ghost" type="button" on:click={resetPlanner}>Editar respuestas</button>
						<a class="btn primary" href="/planes">Añadir al panel de planes</a>
					</div>
				</article>
				<section class="card week">
					<h2>Vista semanal destacada</h2>
					<div class="week-grid">
						{#each generatedPlan.week as day}
							<article>
								<header>
									<h3>{day.day}</h3>
									<img src={PlatosTipicos} alt={day.day} />
								</header>
								<ul>
									{#each day.meals as meal}
										<li>{meal}</li>
									{/each}
								</ul>
								<p class="snack"><strong>Snack sugerido:</strong> {day.snack}</p>
							</article>
						{/each}
					</div>
				</section>
				<section class="card extras">
					<h2>Checklist y ajustes</h2>
					<div class="list-block">
						<h3>Lista de compras clave</h3>
						<ul>
							{#each generatedPlan.shopping as item}
								<li>{item}</li>
							{/each}
						</ul>
					</div>
					<div class="list-block">
						<h3>Recomendaciones IA</h3>
						<ul>
							{#each generatedPlan.adaptations as item}
								<li>{item}</li>
							{/each}
						</ul>
					</div>
				</section>
			</div>
		</section>
	{/if}
</main>

<style>
	.planner {
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

	.intro-inner {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 2.5rem;
		align-items: center;
		margin-top: 2rem;
	}

	.copy h1 {
		margin: 0;
		font-size: clamp(2.2rem, 3vw, 3.4rem);
	}

	.copy p {
		margin: 1rem 0 0;
		color: var(--color-soft);
		line-height: 1.7;
	}

	.visual {
		position: relative;
		overflow: hidden;
	}

	.visual img {
		width: 100%;
		height: 280px;
		object-fit: cover;
		border-radius: var(--radius-lg);
	}

	.visual .overlay {
		position: absolute;
		bottom: 1.2rem;
		left: 1.2rem;
		right: 1.2rem;
		background: rgba(255, 255, 255, 0.92);
		border-radius: var(--radius-md);
		padding: 0.9rem 1rem;
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
		box-shadow: 0 18px 32px rgba(8, 44, 36, 0.18);
	}

	.visual strong {
		font-size: 1.1rem;
	}

	.visual span {
		color: var(--color-soft);
		font-size: 0.9rem;
	}

	.form-section .planner-form {
		display: flex;
		flex-direction: column;
		gap: 2rem;
		padding: 2.5rem;
	}

	.planner-form h2 {
		margin: 0;
	}

	.hint {
		margin: 0;
		color: var(--color-soft);
		font-size: 0.95rem;
	}

	.form-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
		gap: 1.8rem;
	}

	fieldset {
		border: 1px solid rgba(8, 44, 36, 0.08);
		border-radius: var(--radius-md);
		padding: 1.5rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		background: rgba(255, 255, 255, 0.9);
	}

	legend {
		padding: 0 0.5rem;
		font-weight: 700;
		color: var(--color-forest);
	}

	.field-row {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
		gap: 1rem;
	}

	.goal-grid,
	.checkbox-group {
		display: flex;
		flex-wrap: wrap;
		gap: 0.75rem;
	}

	.selectable {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 0.9rem;
		border-radius: 999px;
		border: 1px solid rgba(8, 44, 36, 0.12);
		cursor: pointer;
		background: rgba(255, 255, 255, 0.85);
		transition: background 0.2s ease, border-color 0.2s ease;
	}

	.selectable input {
		accent-color: var(--color-leaf);
	}

	.selectable:hover {
		border-color: rgba(15, 184, 114, 0.4);
		background: rgba(15, 184, 114, 0.1);
	}

	.question {
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
	}

	.question p {
		margin: 0;
		font-weight: 600;
	}

	.actions {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		align-items: flex-start;
	}

	.disclaimer {
		margin: 0;
		color: var(--color-soft);
		font-size: 0.9rem;
	}

	.loading {
		padding: 2rem 0 4rem;
	}

	.loading-card {
		max-width: 420px;
		margin: 0 auto;
		padding: 2.5rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.2rem;
	}

	.spinner {
		width: 48px;
		height: 48px;
		border-radius: 50%;
		border: 4px solid rgba(15, 184, 114, 0.2);
		border-top-color: var(--color-leaf);
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	.result-grid {
		display: grid;
		grid-template-columns: minmax(260px, 1fr) minmax(280px, 1fr);
		gap: 2rem;
		align-items: start;
	}

	.summary ul {
		margin: 0;
		padding-left: 1.1rem;
		color: var(--color-soft);
		line-height: 1.6;
	}

	.macros {
		display: grid;
		grid-template-columns: repeat(2, minmax(100px, 1fr));
		gap: 1rem;
		margin-top: 1.5rem;
	}

	.macros span {
		color: var(--color-soft);
		font-size: 0.9rem;
	}

	.macros strong {
		font-size: 1.3rem;
	}

	.result-actions {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		margin-top: 2rem;
	}

	.week {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.week-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 1.2rem;
	}

	.week-grid article {
		background: rgba(255, 255, 255, 0.9);
		border-radius: var(--radius-md);
		padding: 1.2rem;
		display: flex;
		flex-direction: column;
		gap: 0.8rem;
	}

	.week-grid header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 0.8rem;
	}

	.week-grid img {
		width: 56px;
		height: 56px;
		object-fit: cover;
		border-radius: 50%;
	}

	.week-grid ul {
		margin: 0;
		padding-left: 1.1rem;
		color: var(--color-soft);
		line-height: 1.5;
	}

	.snack {
		margin: 0;
		color: var(--color-forest);
		font-size: 0.9rem;
	}

	.extras {
		display: flex;
		flex-direction: column;
		gap: 1.2rem;
	}

	.list-block h3 {
		margin: 0 0 0.6rem;
		font-size: 1rem;
	}

	.list-block ul {
		margin: 0;
		padding-left: 1.1rem;
		color: var(--color-soft);
		line-height: 1.6;
	}

	@media (max-width: 960px) {
		.result-grid {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 720px) {
		.form-grid {
			grid-template-columns: 1fr;
		}

		.field-row {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 640px) {
		.form-section .planner-form {
			padding: 2rem;
		}

		.result-actions {
			flex-direction: column;
		}
	}
</style>
