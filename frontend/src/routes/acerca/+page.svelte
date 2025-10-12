<script>
	import Banner from '$lib/components/Banner.svelte';

	const faq = [
		{
			question: '¿Qué es NutriPlan?',
			answer:
				'NutriPlan es una plataforma nutricional enfocada en la gastronomía nicaragüense que combina IA y asesoría humana para crear planes personalizados.'
		},
		{
			question: '¿Cómo se generan las recomendaciones?',
			answer:
				'Analizamos tus objetivos, actividad física, preferencias y condiciones médicas. Con IA proponemos recetas y planes que puedes ajustar manualmente.'
		},
		{
			question: '¿Puedo compartir mis planes?',
			answer:
				'Sí, exporta tu plan en PDF, compártelo con tu nutricionista o sincronízalo con tu calendario personal.'
		}
	];

	const contact = [
		{ label: 'Correo', value: 'hola@nutriplan.com.ni' },
		{ label: 'Teléfono', value: '+505 2222 3344' },
		{ label: 'Dirección', value: 'Managua, Nicaragua' }
	];
</script>


<main class="about">
	<section class="intro">
		<div class="container">
			<h1>Sobre NutriPlan</h1>
			<p>
				Promovemos el bienestar a través de recetas nicaragüenses autenticadas por nutricionistas y
				potenciadas con IA. Creemos en la alimentación consciente, local y accesible.
			</p>
			<div class="pillars">
				<article class="card">
					<h2>Recetas con identidad</h2>
					<p>Rescatamos platillos tradicionales y los adaptamos a distintos objetivos nutricionales.</p>
				</article>
				<article class="card">
					<h2>IA con propósito</h2>
					<p>Modelos propios que aprenden de tus hábitos y respetan tus preferencias.</p>
				</article>
				<article class="card">
					<h2>Comunidad activa</h2>
					<p>Usuarios, chefs y expertos compartiendo experiencias, consejos y motivación.</p>
				</article>
			</div>
		</div>
	</section>

	<section class="faq">
		<div class="container faq-grid">
			<article class="card">
				<h2>Preguntas frecuentes</h2>
				<div class="qa">
					{#each faq as item}
						<div>
							<h3>{item.question}</h3>
							<p>{item.answer}</p>
						</div>
					{/each}
				</div>
			</article>
			<article class="card contact">
				<h2>Contacto</h2>
				<ul>
					{#each contact as item}
						<li>
							<strong>{item.label}</strong>
							<span>{item.value}</span>
						</li>
					{/each}
				</ul>
				<button type="button">Agenda una demo</button>
			</article>
		</div>
	</section>
</main>

<style>
	.about {
		display: flex;
		flex-direction: column;
		gap: 4.5rem;
		padding-bottom: 5rem;
	}

	.container {
		max-width: 960px;
		margin: 0 auto;
		padding: 0 1.5rem;
	}

	.intro h1 {
		margin: 2rem 0 0.5rem;
		font-size: clamp(2.2rem, 3vw, 3rem);
	}

	.intro p {
		margin: 0 0 2rem;
		color: var(--color-soft);
	}

	.pillars {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
		gap: 1.5rem;
	}

	.pillars .card {
		padding: 1.8rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.faq-grid {
		display: grid;
		grid-template-columns: 3fr 2fr;
		gap: 2rem;
	}

	.qa {
		display: flex;
		flex-direction: column;
		gap: 1.2rem;
	}

	.qa h3 {
		margin: 0;
	}

	.qa p {
		margin: 0;
		color: var(--color-soft);
	}

	.contact ul {
		margin: 0;
		padding: 0;
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.contact strong {
		font-size: 0.95rem;
	}

	.contact span {
		color: var(--color-soft);
	}

	.contact button {
		margin-top: 1.5rem;
		border: none;
		background: var(--gradient-leaf);
		color: white;
		padding: 0.75rem 1.4rem;
		border-radius: 999px;
		font-weight: 600;
		cursor: pointer;
		box-shadow: 0 16px 26px rgba(15, 184, 114, 0.25);
	}

	@media (max-width: 720px) {
		.faq-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
