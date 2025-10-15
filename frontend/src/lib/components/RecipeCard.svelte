<script lang="ts">
	import { goto } from '$app/navigation';

	let { recipe } = $props();
	function gotoRecipe() {
		goto(`/recipes/${recipe.id}`);
	}
</script>

<button
	class="recipe-card grid no-gap bg-white soft-outline no-border no-pad hoverable"
	onclick={gotoRecipe}
	aria-roledescription="Open Recipe"
>
	<div class="image-container no-overflow rel-pos">
		<img class="fit-cover full-size" src={recipe.image} alt={recipe.title} />
		<div
			class="star-rating abs-pos bg-white pad-5 sm-p flex items-center justify-center"
			style="top: 5px; right: 5px; gap: 3px;"
		>
			<i class="las la-star p-emphasis no-ul"></i>
			{recipe.rating}
		</div>
	</div>

	<div class="recipe-info pad-20 flex direction-col gap-8 txt-left">
		<div class="recipe-title bold md-p">{recipe.title}</div>
		<div class="attributes flex gap-16">
			{#if recipe.time}
				<div class="recipe-time p-ghost sm-p">
					<i class="las la-stopwatch"></i>
					{recipe.time}
				</div>
			{/if}
			{#if recipe.kcal}
				<div class="recipe-calories p-ghost sm-p">
					{recipe.kcal}
				</div>
			{/if}
			{#if recipe.portions}
				<div class="recipe-portions p-ghost sm-p">
					<i class="las la-user"></i>
					{recipe.portions}
				</div>
			{/if}
		</div>

		<div class="tags flex wrap gap-8">
			{#each recipe.tags as tag}
				<span class="sm-p p-ghost bg-soft-gray-darker pad-5 round-5">{tag}</span>
			{/each}
		</div>
	</div>
</button>

<style>
	:root {
		--recipe-card-width: 250px;
		--recipe-card-height: 350px;
	}

	.recipe-card {
		width: var(--recipe-card-width);
		height: var(--recipe-card-height);

		min-width: var(--recipe-card-width);
		min-height: var(--recipe-card-height);

		grid-template-rows: 3fr 2fr;
		cursor: pointer;

		transition: 0.25s ease;
	}

	.recipe-card:hover,
	.recipe-card:focus {
		background-color: var(--color-soft-white);
		outline: 1px solid rgba(0, 0, 0, 0.5);
	}
</style>
