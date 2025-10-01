<script>
	import Banner from '$lib/components/Banner.svelte';

	const ingredientList = [
		{ name: 'Yuca', category: 'Tubérculos', kcal: 118, availability: 'Alta' },
		{ name: 'Chiltoma', category: 'Vegetales', kcal: 24, availability: 'Alta' },
		{ name: 'Queso ahumado', category: 'Lácteos', kcal: 320, availability: 'Media' }
	];

	const recipeQueue = [
		{ title: 'Indio viejo ligero', author: 'Chef Alicia', status: 'Pendiente', submitted: 'Hace 2 h' },
		{ title: 'Bowl de pinolillo', author: 'Nutri Rosa', status: 'Revisión', submitted: 'Hace 1 día' },
		{ title: 'Tostadas con frijol', author: 'Usuario comunidad', status: 'Publicado', submitted: 'Hace 3 días' }
	];

	const statusClass = {
		Pendiente: 'pending',
		'Revisión': 'review',
		Publicado: 'published'
	};

	const reports = [
		{ user: 'Carlos M.', reason: 'Lenguaje inapropiado', recipe: 'Vigorón saludable', time: 'Hace 30 min' },
		{ user: 'Ana G.', reason: 'Publicidad', recipe: 'Gallo pinto energizante', time: 'Hace 3 h' }
	];
</script>

<Banner />

<main class="admin">
	<section class="hero">
		<div class="container hero-inner">
			<div>
				<h1>Panel administrativo</h1>
				<p>Gestiona ingredientes, revisa recetas y modera comentarios de la comunidad.</p>
			</div>
			<div class="actions">
				<button class="primary" type="button">Añadir ingrediente</button>
				<button class="ghost" type="button">Crear receta destacada</button>
			</div>
		</div>
	</section>

	<section class="ingredients">
		<div class="container card">
			<header>
				<h2>Inventario de ingredientes</h2>
				<input type="text" placeholder="Buscar ingrediente" />
			</header>
			<table>
				<thead>
					<tr>
						<th>Nombre</th>
						<th>Categoría</th>
						<th>Kcal (100 g)</th>
						<th>Disponibilidad</th>
						<th></th>
					</tr>
				</thead>
				<tbody>
					{#each ingredientList as ingredient}
						<tr>
							<td>{ingredient.name}</td>
							<td>{ingredient.category}</td>
							<td>{ingredient.kcal}</td>
							<td>{ingredient.availability}</td>
							<td><a href="#">Editar</a></td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</section>

	<section class="recipes">
		<div class="container card">
			<header>
				<h2>Recetas en revisión</h2>
				<select>
					<option>Mostrar todas</option>
					<option>Pendientes</option>
					<option>Revisión</option>
					<option>Publicadas</option>
				</select>
			</header>
			<ul>
				{#each recipeQueue as item}
					<li>
						<div class="info">
							<strong>{item.title}</strong>
							<span>{item.author}</span>
						</div>
						<div class={`status ${statusClass[item.status]}`}>
							{item.status}
						</div>
						<span class="time">{item.submitted}</span>
						<div class="row-actions">
							<a href="#">Aprobar</a>
							<a href="#">Rechazar</a>
						</div>
					</li>
				{/each}
			</ul>
		</div>
	</section>

	<section class="reports">
		<div class="container card">
			<header>
				<h2>Reportes de la comunidad</h2>
				<button type="button">Ver historial completo</button>
			</header>
			<div class="report-list">
				{#each reports as report}
					<div class="report">
						<div>
							<strong>{report.user}</strong>
							<span>{report.time}</span>
						</div>
						<p>{report.reason} en <em>{report.recipe}</em></p>
						<div class="report-actions">
							<button type="button">Resolver</button>
							<button type="button" class="ghost">Ignorar</button>
						</div>
					</div>
				{/each}
			</div>
		</div>
	</section>
</main>

<style>
	.admin {
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

	.hero-inner {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 2rem;
	}

	.hero h1 {
		margin: 0 0 0.5rem;
	}

	.actions {
		display: flex;
		gap: 1rem;
		flex-wrap: wrap;
	}

	.actions .primary,
	.actions .ghost,
	.report-actions button {
		border: none;
		border-radius: 999px;
		padding: 0.65rem 1.4rem;
		font-weight: 600;
		cursor: pointer;
	}

	.actions .primary {
		background: var(--gradient-leaf);
		color: white;
		box-shadow: 0 16px 26px rgba(15, 184, 114, 0.25);
	}

	.actions .ghost,
	.report-actions .ghost {
		background: rgba(8, 44, 36, 0.08);
		color: var(--color-forest);
	}

	.card {
		background: rgba(255, 255, 255, 0.92);
		border-radius: var(--radius-lg);
		padding: 2.2rem;
		box-shadow: var(--shadow-soft);
	}

	.ingredients header,
	.recipes header,
	.reports header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 1rem;
		margin-bottom: 1.5rem;
	}

	.ingredients input {
		width: 200px;
	}

	table {
		width: 100%;
		border-collapse: collapse;
	}

	thead {
		text-align: left;
		color: var(--color-soft);
	}

	td,
th {
		padding: 0.8rem;
		border-bottom: 1px solid rgba(8, 44, 36, 0.08);
	}

	td a {
		text-decoration: none;
		font-weight: 600;
		color: var(--color-forest);
	}

	.recipes ul {
		margin: 0;
		padding: 0;
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.recipes li {
		display: grid;
		grid-template-columns: 2fr auto auto auto;
		gap: 1rem;
		align-items: center;
		padding: 1rem 0;
		border-bottom: 1px solid rgba(8, 44, 36, 0.08);
	}

	.recipes .info span {
		color: var(--color-soft);
	}

	.status {
		padding: 0.4rem 0.9rem;
		border-radius: 999px;
		font-weight: 600;
		text-transform: uppercase;
		font-size: 0.75rem;
	}

	.status.pending {
		background: rgba(255, 178, 90, 0.2);
		color: #b36b05;
	}

	.status.review {
		background: rgba(104, 211, 255, 0.25);
		color: #036089;
	}

	.status.published {
		background: rgba(15, 184, 114, 0.2);
		color: #0a6b44;
	}

	.row-actions {
		display: flex;
		gap: 0.8rem;
	}

	.row-actions a {
		text-decoration: none;
		font-weight: 600;
		color: var(--color-forest);
	}

	.time {
		color: var(--color-soft);
		font-size: 0.9rem;
	}

	.report-list {
		display: flex;
		flex-direction: column;
		gap: 1.2rem;
	}

	.report {
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
		padding-bottom: 1rem;
		border-bottom: 1px solid rgba(8, 44, 36, 0.08);
	}

	.report p {
		margin: 0;
		color: var(--color-soft);
	}

	.report em {
		font-style: normal;
		font-weight: 600;
		color: var(--color-forest);
	}

	.report-actions {
		display: flex;
		gap: 1rem;
		flex-wrap: wrap;
	}

	@media (max-width: 840px) {
		.recipes li {
			grid-template-columns: 1fr;
			align-items: flex-start;
		}

		.row-actions {
			justify-content: flex-start;
		}
	}

	@media (max-width: 640px) {
		.hero-inner {
			flex-direction: column;
			align-items: flex-start;
		}

		.actions {
			flex-direction: column;
		}

		table {
			display: block;
			overflow-x: auto;
		}
	}
</style>
