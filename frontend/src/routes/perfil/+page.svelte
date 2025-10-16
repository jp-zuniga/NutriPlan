<script>
	import Banner from '$lib/components/Banner.svelte';
	import { authUser, redirectIfNull } from '$lib/stores/auth';

	import ImagenVigoron from '$lib/assets/vigoron.jpg';
	import GalloPinto from '$lib/assets/gallo-pinto.jpg';
	import PlatosTipicos from '$lib/assets/platos-tipicos.jpeg';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import RotatingNutriplan from '$lib/components/RotatingNutriplan.svelte';

	$effect(() => {
		if ($authUser === null) goto('/login');
	});

	const user = {
		name: 'María Fernanda',
		location: 'Managua, Nicaragua',
		age: 29,
		goal: 'Definir músculo',
		activity: 'Entrenamiento funcional 4x por semana',
		conditions: ['Intolerancia a la lactosa', 'Dolores de hombro'],
		favorites: [
			{ title: 'Vigorón saludable', image: ImagenVigoron, calories: '430 kcal' },
			{ title: 'Gallo pinto energizante', image: GalloPinto, calories: '380 kcal' },
			{ title: 'Sopa de queso liviana', image: PlatosTipicos, calories: '320 kcal' }
		]
	};

	const preferences = {
		ingredients: ['Chayote', 'Mango verde', 'Quinoa', 'Queso ahumado light'],
		restrictions: ['Sin lactosa', 'Limitar sodio'],
		tags: ['Alta proteína', 'Cenas ligeras', 'Batch cooking']
	};

	const progress = [
		{ metric: 'Peso', value: '62 kg', change: '-1.2 kg en 30 días' },
		{ metric: 'Circunferencia cintura', value: '72 cm', change: '-3 cm' },
		{ metric: 'Energía', value: '8/10', change: '↑ mejoró 2 puntos' }
	];

	const community = [
		{
			name: 'Daniela R.',
			recipe: 'Ensalada de chayote verde',
			comment: 'Agregué pepitoria tostada para más proteína. Quedó brutal.'
		},
		{
			name: 'Chef Luis',
			recipe: 'Sopa de queso liviana',
			comment: 'Sella el queso en sartén antiadherente para intensificar sabor.'
		}
	];

	const account = {
		email: 'maria.fernanda@nutriplan.com',
		phone: '+505 8888 9900',
		memberSince: 'Abril 2023',
		plan: 'NutriPlan Pro',
		timezone: 'GMT-6 Managua'
	};

	const notifications = [
		{ label: 'Recordatorios de comidas y agua', key: 'meals', enabled: true },
		{ label: 'Nuevas recetas sugeridas', key: 'recipes', enabled: true },
		{ label: 'Alertas de comunidad y comentarios', key: 'community', enabled: false }
	];

	const integrations = [
		{ name: 'Google Calendar', status: 'Sincronizado' },
		{ name: 'Salud iOS', status: 'Pendiente de activar' },
		{ name: 'Garmin Connect', status: 'Sincronizado' }
	];
</script>

{#if $authUser !== undefined && $authUser !== null}
	<main class="profile">
		<section class="hero">
			<div class="container hero-grid">
				<article class="card profile-card">
					<h1>{$authUser?.first_name ?? 'Sin Nombre'} {$authUser?.last_name ?? ''}</h1>
					<p class="location">{user.location}</p>
					<ul class="summary">
						<li><strong>Edad:</strong> {$authUser?.age ?? user.age}</li>
						<li><strong>Meta:</strong> {$authUser?.goal ?? user.goal}</li>
						<li><strong>Actividad:</strong> {$authUser?.activity ?? user.activity}</li>
					</ul>
					<div class="conditions">
						<h3>Condiciones a considerar</h3>
						<ul>
							{#each user.conditions as condition}
								<li>{condition}</li>
							{/each}
						</ul>
					</div>
					<div class="actions">
						<a class="btn primary" href="/planificador-ia">Actualizar evaluación IA</a>
						<a class="btn ghost" href="#">Compartir con nutricionista</a>
					</div>
				</article>
				<section class="card tracker">
					<h2>Seguimiento de progreso</h2>
					<div class="metrics">
						{#each progress as item}
							<div>
								<strong>{item.metric}</strong>
								<span class="value">{item.value}</span>
								<span class="change">{item.change}</span>
							</div>
						{/each}
					</div>
				</section>
			</div>
		</section>

		<section class="preferences">
			<div class="container prefs-grid">
				<article class="card">
					<h2>Ingredientes preferidos</h2>
					<div class="chips">
						{#each preferences.ingredients as ingredient}
							<span class="chip">{ingredient}</span>
						{/each}
					</div>
				</article>
				<article class="card">
					<h2>Restricciones</h2>
					<ul>
						{#each preferences.restrictions as restriction}
							<li>{restriction}</li>
						{/each}
					</ul>
				</article>
				<article class="card">
					<h2>Etiquetas preferidas</h2>
					<div class="chips">
						{#each preferences.tags as tag}
							<span class="chip">{tag}</span>
						{/each}
					</div>
				</article>
			</div>
		</section>

		<section class="favorites">
			<div class="container">
				<header class="section-head">
					<h2>Recetas favoritas</h2>
					<p>Tu top 3 más cocinado, listos para agregar al plan de esta semana.</p>
				</header>
				<div class="favorite-grid">
					{#each user.favorites as favorite}
						<article class="card">
							<img src={favorite.image} alt={favorite.title} />
							<div class="body">
								<h3>{favorite.title}</h3>
								<p>{favorite.calories}</p>
								<a href="/recetas">Ver receta</a>
							</div>
						</article>
					{/each}
				</div>
			</div>
		</section>

		<section class="community">
			<div class="container community-grid">
				<article class="card">
					<h2>Actividad reciente</h2>
					<ul>
						<li>Guardaste el plan "Activa AM" hace 2 días.</li>
						<li>Registraste 3 comidas completadas hoy.</li>
						<li>La IA sugirió 2 nuevas recetas según tus ingredientes.</li>
					</ul>
				</article>
				<article class="card">
					<h2>Interacciones de la comunidad</h2>
					{#each community as entry}
						<div class="entry">
							<strong>{entry.name}</strong>
							<span>{entry.recipe}</span>
							<p>{entry.comment}</p>
						</div>
					{/each}
				</article>
			</div>
		</section>

		<section class="account">
			<div class="container account-grid">
				<article class="card account-form">
					<h2>Datos de cuenta</h2>
					<form>
						<div class="field-row">
							<div>
								<label for="email">Correo</label>
								<input id="email" type="email" value={$authUser?.email ?? account.email} readonly />
							</div>
							<div>
								<label for="phone">Teléfono</label>
								<input id="phone" type="tel" value={$authUser?.phone ?? account.phone} readonly />
							</div>
						</div>
						<div class="field-row">
							<div>
								<label for="plan">Plan actual</label>
								<input id="plan" type="text" value={$authUser?.plan ?? account.plan} readonly />
							</div>
							<div>
								<label for="timezone">Zona horaria</label>
								<input
									id="timezone"
									type="text"
									value={$authUser?.timezone ?? account.timezone}
									readonly
								/>
							</div>
						</div>
						<div class="meta">
							<span>Miembro desde {$authUser?.memberSince ?? account.memberSince}</span>
							<button class="btn ghost" type="button">Actualizar contraseña</button>
						</div>
					</form>
				</article>
				<article class="card notifications">
					<h2>Preferencias de notificación</h2>
					<ul>
						{#each notifications as item}
							<li>
								<span>{item.label}</span>
								<label class="toggle">
									<input type="checkbox" checked={item.enabled} />
									<span></span>
								</label>
							</li>
						{/each}
					</ul>
				</article>
				<article class="card integrations">
					<h2>Integraciones y dispositivos</h2>
					<ul>
						{#each integrations as integration}
							<li>
								<div>
									<strong>{integration.name}</strong>
									<span>{integration.status}</span>
								</div>
								<a href="#">Gestionar</a>
							</li>
						{/each}
					</ul>
				</article>
			</div>
		</section>
	</main>
{:else}
	<div class="flex-center" style="height: calc(100vh - 75px);">
		<RotatingNutriplan />
	</div>
{/if}

<style>
	.profile {
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

	.hero-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: 2.5rem;
	}

	.profile-card {
		display: flex;
		flex-direction: column;
		gap: 1.3rem;
		padding: 2.5rem;
	}

	.profile-card h1 {
		margin: 0;
	}

	.location {
		margin: 0;
		color: var(--color-soft);
	}

	.summary {
		margin: 0;
		padding-left: 1.1rem;
		color: var(--color-soft);
		line-height: 1.7;
	}

	.conditions ul {
		margin: 0;
		padding-left: 1.1rem;
		color: var(--color-soft);
		line-height: 1.6;
	}

	.actions {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
	}

	.tracker {
		padding: 2.5rem;
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.metrics {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
		gap: 1.5rem;
	}

	.metrics div {
		background: rgba(255, 255, 255, 0.85);
		border-radius: var(--radius-md);
		padding: 1.2rem;
		box-shadow: var(--shadow-soft);
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
	}

	.metrics strong {
		font-size: 1.1rem;
	}

	.value {
		font-weight: 700;
	}

	.change {
		color: var(--color-soft);
		font-size: 0.9rem;
	}

	.prefs-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
		gap: 2rem;
	}

	.prefs-grid .card {
		padding: 2rem;
		display: flex;
		flex-direction: column;
		gap: 1.2rem;
	}

	.prefs-grid ul {
		margin: 0;
		padding-left: 1.1rem;
		color: var(--color-soft);
		line-height: 1.6;
	}

	.chips {
		display: flex;
		flex-wrap: wrap;
		gap: 0.6rem;
	}

	.account-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
		gap: 2rem;
	}

	.account-form form {
		display: flex;
		flex-direction: column;
		gap: 1.4rem;
	}

	.account-form .field-row {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
		gap: 1rem;
	}

	.account-form input {
		width: 100%;
	}

	.account-form .meta {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 1rem;
		color: var(--color-soft);
		font-size: 0.9rem;
	}

	.notifications ul,
	.integrations ul {
		margin: 0;
		padding: 0;
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.notifications li,
	.integrations li {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 1rem;
	}

	.notifications span {
		font-weight: 600;
		color: var(--color-forest);
	}

	.toggle {
		position: relative;
		width: 40px;
		height: 22px;
		display: inline-flex;
		align-items: center;
	}

	.toggle input {
		opacity: 0;
		width: 0;
		height: 0;
	}

	.toggle span {
		position: absolute;
		cursor: pointer;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(8, 44, 36, 0.2);
		border-radius: 999px;
		transition: background 0.2s ease;
	}

	.toggle span::before {
		content: '';
		position: absolute;
		height: 16px;
		width: 16px;
		left: 4px;
		top: 3px;
		background: #fff;
		border-radius: 50%;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
		transition: transform 0.2s ease;
	}

	.toggle input:checked + span {
		background: var(--gradient-leaf);
	}

	.toggle input:checked + span::before {
		transform: translateX(18px);
	}

	.integrations li div {
		display: flex;
		flex-direction: column;
		gap: 0.2rem;
	}

	.integrations li span {
		color: var(--color-soft);
		font-size: 0.9rem;
	}

	.integrations a {
		font-weight: 600;
		text-decoration: none;
		color: var(--color-forest);
	}

	.favorite-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
		gap: 1.5rem;
		margin-top: 2rem;
	}

	.favorite-grid .card {
		overflow: hidden;
		display: flex;
		flex-direction: column;
	}

	.favorite-grid img {
		width: 100%;
		height: 160px;
		object-fit: cover;
	}

	.favorite-grid .body {
		padding: 1.4rem;
		display: flex;
		flex-direction: column;
		gap: 0.8rem;
	}

	.favorite-grid a {
		font-weight: 600;
		color: var(--color-forest);
		text-decoration: none;
	}

	.community-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 2rem;
	}

	.community-grid .card {
		padding: 2rem;
		display: flex;
		flex-direction: column;
		gap: 1.2rem;
	}

	.community-grid ul {
		margin: 0;
		padding-left: 1.1rem;
		color: var(--color-soft);
		line-height: 1.6;
	}

	.entry {
		display: flex;
		flex-direction: column;
		gap: 0.3rem;
		padding-bottom: 1rem;
		border-bottom: 1px solid rgba(8, 44, 36, 0.08);
	}

	.entry span {
		font-weight: 600;
		color: var(--color-forest);
	}

	.entry p {
		margin: 0;
		color: var(--color-soft);
	}

	@media (max-width: 640px) {
		.actions {
			flex-direction: column;
		}

		.account-form .field-row {
			grid-template-columns: 1fr;
		}

		.account-form .meta {
			flex-direction: column;
			align-items: flex-start;
		}
	}
</style>
