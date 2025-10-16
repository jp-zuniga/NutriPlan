<script lang="ts">
	import { goto } from '$app/navigation';
	import { extractDirectImage } from '$lib/utils/images';

	let { recipe } = $props();
	function gotoRecipe() {
		goto(`/receta	s/${recipe.slug}`);
	}
</script>

<button
	class="recipe-card grid no-gap bg-white soft-outline no-border no-pad hoverable"
	onclick={gotoRecipe}
	aria-roledescription="Open Recipe"
>
	<div class="image-container no-overflow rel-pos">
		<img
			class="fit-cover full-size"
			src={extractDirectImage(recipe.primary_image)}
			alt={recipe.name}
		/>
		<div
			class="star-rating abs-pos bg-white pad-5 sm-p flex items-center justify-center"
			style="top: 5px; right: 5px; gap: 3px;"
		>
			<i class="las la-star p-emphasis no-ul"></i>
			{recipe.rating_avg}
		</div>
	</div>

	<div class="recipe-info pad-20 flex direction-col gap-8 txt-left">
		<div class="recipe-title bold md-p">{recipe.name}</div>
		<div class="attributes flex gap-8 wrap">
			{#if recipe.total_time}
				<div class="recipe-time p-ghost sm-p">
					<i class="las la-stopwatch"></i>
					{recipe.total_time} minutos
				</div>
			{/if}
			{#if recipe.servings}
				<div class="recipe-portions p-ghost sm-p">
					{#if recipe.servings == 1}
						<i class="las la-user"></i>
					{:else if recipe.servings <= 3}
						<i class="las la-user-friends"></i>
					{:else}
						<i class="las la-users"></i>
					{/if}
					{recipe.servings} porciones
				</div>
			{/if}

			{#if recipe.calories_per_serving}
				<div class="recipe-calories p-ghost sm-p">
					<i class="las la-fire-alt"></i>
					{recipe.calories_per_serving * 1} calorías (por porción)
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
