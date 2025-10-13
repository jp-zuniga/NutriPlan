<script lang="ts">
	import HeartBox from './HeartBox.svelte';
	import { goto } from '$app/navigation';

	let { recipe } = $props();
	function gotoRecipe() {
		goto(`/recipes/${recipe.id}`);
	}
</script>

<div class="recipe-card grid">
	<div class="image-container">
		<img class="fit-cover no-overflow" src={recipe.image} alt={recipe.title} />
	</div>

	<div class="recipe-info">
		<div class="recipe-title">{recipe.title}</div>
		<div class="attributes">
			<div class="recipe-time">{recipe.time}</div>
			<div class="recipe-calories">
				{recipe.kcal}
			</div>
		</div>
	</div>
</div>

<!-- <div class="recipe-card hoverable">
	<div class="recipe-image-container">
		<img class="recipe-image" src={recipe.image} alt={recipe.title} />
		<div class="recipe-image-gradient"></div>
		<div class="heart-box">
			<HeartBox />
		</div>
	</div>
	<div class="recipe-info">
		<div class="recipe-title">{recipe.title}</div>
		<div class="recipe-attributes">
			<div class="recipe-time"><span>{recipe.time}</span></div>
			<div class="recipe-calories"><span>{recipe.kcal} cal</span></div>
		</div>
	</div>

	<button class="show-button" onclick={gotoRecipe}>Ver receta</button>
</div> -->

<!-- <style>
	.recipe-card {
		width: var(--recipe-card-width);
		height: var(--recipe-card-height);

		/* margin: 20px; */
		/* 
		background-color: var(--white-background);
		border-radius: var(--border-radius-1);
		box-shadow: 0px 20px 15px rgba(0, 0, 0, 0.062); */

		display: grid;
		grid-template-rows: var(--recipe-card-image-height) 1fr;

		/* transition: 0.25s; */
	}

	/* .recipe-card:hover {
		transform: translateY(-5px);
		box-shadow: 0px 20px 15px rgba(0, 0, 0, 0.1);
	} */

	.recipe-image-container {
		width: 100%;
		height: 100%;
		display: grid;

		grid-template-columns: 1fr;
		grid-template-rows: 1fr;

		position: relative;

		border-radius: inherit;
	}

	.recipe-image-container .heart-box {
		position: absolute;
		right: 5px;
		top: 5px;
	}

	.recipe-image-gradient,
	.recipe-image {
		width: 100%;
		height: 100%;

		display: block;

		grid-column: 1;
		grid-row: 1;
	}

	.recipe-image-gradient {
		background: linear-gradient(#ffffff00, var(--white-background));
	}

	.recipe-image {
		overflow: hidden;
		border-radius: inherit;
		object-fit: cover;
	}

	.recipe-info {
		padding: 20px;
	}

	.recipe-title {
		font-weight: bolder;
		font-size: 22px;
	}

	.recipe-attributes {
		display: flex;
		justify-content: space-between;
	}

	.recipe-time {
		color: gray;
	}

	.recipe-calories {
		color: gray;
	}

	.show-button {
		background-color: var(--main-color);
		border: 2px solid var(--main-color);
		padding: 5px;
		color: white;
		margin: 0px 50px;
		border-radius: 15px;
		cursor: pointer;
		transition: 0.1s;
	}

	.show-button:hover {
		color: var(--main-color);
		background-color: white;
		border-color: var(--main-color);
	}
</style> -->

<style>
	:root {
		--recipe-card-width: 250px;
		--recipe-card-height: 300px;
	}

	.recipe-card {
		width: var(--recipe-card-width);
		height: var(--recipe-card-height);
		grid-template-rows: 1fr 1fr;
	}
</style>
