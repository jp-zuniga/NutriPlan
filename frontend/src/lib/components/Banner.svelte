<script>
	const links = [
		{
			text: 'Home',
			link: '#'
		},

		{
			text: 'Recetas',
			link: '#'
		},

		{
			text: 'Plan Nutricional',
			link: '#'
		},

		{
			text: 'Planes',
			link: '#'
		},

		{
			text: 'Contactanos',
			link: '#'
		}
	];
</script>

<div class="banner">
	<div id="logo">
		<img src="/assets/images/NutriPlan.png" alt="NutriPlan logo" />
	</div>
	<div id="links">
		{#each links as link}
			<a href={link.link}><span>{link.text}</span></a>
		{/each}
	</div>
	<div id="user"></div>
</div>

<style>
	.banner {
		height: 100px;
		box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);

		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.banner #logo img {
		height: 70px;
	}

	.banner #links {
		width: 50%;
		height: 100%;

		display: flex;
		justify-content: space-evenly;
	}

	.banner #links a {
		width: 100%;
		height: 100%;

		display: flex;
		justify-content: center;
		align-items: center;

		text-decoration: none;
		color: black;
	}

	.banner #links a:hover {
		background-color: rgba(0, 0, 0, 0.1);
	}
</style>
