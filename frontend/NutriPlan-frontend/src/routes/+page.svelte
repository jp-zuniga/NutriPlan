<script>
	class Receta {
		constructor(nombre, imagen, tiempo, reseñas, favorita) {
			this.nombre = nombre;
			this.tiempo = tiempo;
			this.reseñas = reseñas;
			this.favorita = favorita;
			this.imagen = imagen;
		}
	}

	const user_name = 'Mauricio';
	const recomendadas = [
		new Receta(
			'Dedos de Pollo',
			'https://assets.tmecosys.com/image/upload/t_web_rdp_recipe_584x480_1_5x/img/recipe/ras/Assets/162ADE57-4E13-4FA2-9A36-E408323336AE/Derivates/19f90d7d-7a1b-40f4-b912-d9f8bb9d2fbb.jpg',
			120,
			47,
			false
		)
	];
</script>

<div id="body">
	<div id="search-bar">
		<div id="bar-title"></div>
		<div id="search-box">
			<input type="text" placeholder="Buscar recetas" />
			<button aria-label="Search"></button>
		</div>
		<div id="bar-left">
			<div><b>Hola,</b> {user_name}</div>
		</div>
	</div>
	<div id="sidebar">
		<ul>
			<li>My Account</li>
			<li>New Recipes</li>
			<li>Favorites</li>
			<li>Log out</li>
		</ul>
	</div>
	<div id="main-content">
		<div class="tab">Recomendado</div>
		<hr />

		<!-- Tarjeta por defecto para recetas -->
		{#each recomendadas as receta}
			<div class="recipe-card">
				<div class="recipe-image-container">
					<img class="recipe-image" src={receta.imagen} alt={receta.nombre} />
					<div class="recipe-image-gradient"></div>
				</div>
				<div class="recipe-info">
					<div class="recipe-title">{receta.nombre}</div>
					<div class="recipe-time"><span>{receta.tiempo} min</span></div>
				</div>
			</div>
		{/each}
	</div>
</div>
