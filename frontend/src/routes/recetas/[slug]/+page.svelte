<script>
	import { page } from '$app/stores';
	import StarRating from '$lib/components/StarRating.svelte';
	import { API_RECIPES_ENDPOINT } from '$lib/endpoints';
	import { getRecipe } from '$lib/utils/recipes';
	import { toReadableDate } from '$lib/utils/date';
	import { extractDirectImage } from '$lib/utils/images';
	import { authUser } from '$lib/stores/auth';
	import RotatingNutriplan from '$lib/components/RotatingNutriplan.svelte';
	import { marked } from 'marked';

	const recipe_slug = $state($page.params.slug);

	let loading = $state(true);
	let recipe = $state(null);
	let reviews = $state(null);

	const get_recipe = async () => {
		loading = true;

		const data = await getRecipe(recipe_slug);
		if (data != null) {
			recipe = data.recipe;
			reviews = data.reviews;

			console.log('Recipe data: ', recipe);
		}

		loading = false;
	};

	// Star rating functionality
	let star_preview = $state(0);
	let star_count = $state(0);

	const fill_color = '#C86F56';
	const unfill_color = 'gray';

	const star_meanings = [
		'No me lo pude comer',
		'No me gustó',
		'Estaba OK',
		'Me gustó',
		'Me encantó'
	];

	let user_review = $state('');

	const fast_reviews = [
		['No funcionó', 'Faltaban ingredientes'],
		['Las instrucciones no son claras', 'Necesita mejorar', 'No sabía rico'],
		['Faltaba un paso', 'Demasiado dificil'],
		['Estaba bien', 'Necesita mas sabor', 'Talvez la intente de nuevo'],
		['Me encantó!', 'Muy buen sabor', 'Facil de hacer', 'Valió la pena el esfuerzo']
	];

	get_recipe();
</script>

<svelte:head>
	{#if recipe}
		<title>{recipe.name}</title>
	{/if}
</svelte:head>

{#if !loading}
	<main id="recipe" class="mb">
		{#if recipe}
			<section class="full-width">
				<div class="container md flex direction-col mt-l mb-l">
					<div id="trail" class="flex full-width items-center gap-8">
						<a href="/recetas" class="no-ul p-ghost">Recetas</a>
						<i class="las la-angle-right"></i>
						<a href="/recetas/{recipe.slug}" class="no-ul p-emphasis">{recipe.name}</a>
					</div>
				</div>
			</section>

			<section>
				<div class="container md flex direction-col">
					<p class="h2 bold">{recipe.name}</p>
					<p class="md-p p-ghost mb">{recipe.description}</p>

					<hr class="full-width soft" />
					<div id="rating-info" class="flex items-center justify-between pad-10">
						<div id="star-rating" class="flex-center gap-8">
							{#if recipe.rating_avg != null}
								<StarRating count={recipe.rating_avg} />
								<p class="md-p p-emphasis">{recipe.rating_avg}</p>
								<a class="p-ghost md-p" href="#reviews">
									({recipe.rating_count}
									{recipe.rating_count == 1 ? 'reseña' : 'reseñas'})
								</a>
							{:else}
								<StarRating count={recipe.rating_avg} />
								<p class="md-p">Sin reseñas</p>
							{/if}
						</div>

						<div id="time-to-cook" class="flex-center gap-8">
							<i class="las la-stopwatch"></i>
							{recipe.total_time} minutos
						</div>

						<div id="portions" class="flex-center gap-8">
							{#if recipe.servings == 1}
								<i class="las la-user"></i>
							{:else if recipe.servings <= 3}
								<i class="las la-user-friends"></i>
							{:else}
								<i class="las la-users"></i>
							{/if}

							{recipe.servings}
							{recipe.servings == 1 ? 'porción' : 'porciones'}
						</div>
					</div>
					<hr class="full-width soft" />

					<div class="time-info flex items-center mb">
						<p class="md-p p-ghost">Ultima Actualización:&nbsp;</p>
						<p class="md-p p-emphasis no-ul">{toReadableDate(recipe.updated_at)}</p>
					</div>

					<div class="pad-50">
						<img
							src={extractDirectImage(recipe.main_image_url)}
							class="full-size no-overflow"
							alt={recipe.name}
						/>
					</div>
				</div>
			</section>

			<section id="ingredients">
				<div class="container md flex-begin direction-col">
					<p class="h2 bold">Ingredientes</p>
					<div class="container md flex direction-col">
						<ul>
							{#each recipe.ingredients as amount}
								<li>
									{amount.amount}
									{amount.unit}
									de
									{amount.ingredient.name}
								</li>
							{/each}
						</ul>
					</div>
				</div>
			</section>

			<section id="instructions">
				{#if recipe.instructions}
					<div class="container md flex-begin direction-col mb">
						<p class="h2 bold">Instrucciones</p>
						<p class="instructions">
							{@html marked(recipe.instructions)}
						</p>
					</div>
				{/if}
			</section>

			<section id="review">
				<div class="container md flex direction-col">
					<p class="h2 bold">
						Reseñas
						{#if recipe.rating_count}
							({recipe.rating_count})
						{/if}
					</p>
					<p class="md-p p-ghost mb-l">
						Revisa nuestras <a href="#" class="ul-emphasis bold">normas de comunidad</a> acerca de las
						reseñas.
					</p>

					<div class="pad-20" style="background-color: #9EBC8A">
						<div class="flex direction-col bg-white b-shadow pad-20">
							<p class="h3 bold mb">{recipe.name}</p>

							<div class="flex items-center gap-16 mb">
								<div class="flex direction-col border-right" style="padding-right: 20px;">
									<p class="lg-p">Mi puntuación</p>
									<div class="flex">
										{#each { length: 5 } as _, i}
											<!-- svelte-ignore a11y_click_events_have_key_events -->
											<i
												class="las la-star clickable"
												onmouseenter={() => {
													star_preview = i + 1;
												}}
												onmouseleave={() => {
													star_preview = 0;
												}}
												onclick={() => {
													star_count = i + 1;
												}}
												role="button"
												tabindex="0"
												style="color: {star_preview >= i + 1 || star_count >= i + 1
													? fill_color
													: unfill_color}; font-size: 30px;"
											></i>
										{/each}
									</div>
								</div>

								<p class="lg-p p-ghost">
									{#if star_preview != 0}
										{star_meanings[star_preview - 1]}
									{:else if star_count != 0}
										{star_meanings[star_count - 1]}
									{/if}
								</p>
							</div>

							<p class="lg-p">Mi reseña</p>
							<div class="fast-reviews flex wrap gap-8 pad-5">
								{#if star_count != 0}
									{#each fast_reviews[star_count - 1] as fast_review}
										<button
											class="bg-soft-gray clickable hoverable pad-10 md-p no-border"
											onclick={() => {
												user_review = fast_review;
											}}
										>
											{fast_review}
										</button>
									{/each}
								{/if}
							</div>
							<textarea
								placeholder="¿Que pensaste de esta receta?"
								class="pad-10 mb"
								bind:value={user_review}
							></textarea>

							<div class="flex items-center gap-16">
								<button
									class="btn ghost"
									onclick={() => {
										star_count = 0;
										user_review = '';
									}}>Cancelar</button
								>
								<button
									class="btn primary"
									disabled={user_review == '' || star_count == 0 || $authUser == null}
									>Enviar</button
								>
							</div>

							{#if $authUser == null}
								<p class="md-p p-emphasis no-ul mt">
									Debes crear una cuenta para poder escribir una reseña. <a href="/signup"
										>Hazlo aqui</a
									>
								</p>
							{/if}
						</div>
					</div>
				</div>
			</section>

			<section id="reviews">
				<div class="container md flex direction-col reviews mt gap-16">
					<div class="separator txt-center">
						<hr class="soft" />
						{#if reviews.length != 0}
							<p class="p-ghost">{reviews.length} reseña(s)</p>
						{:else}
							<p class="p-ghost">No hay reseñas!</p>
						{/if}

						<hr class="soft" />
					</div>

					{#each reviews as review}
						<div class="review flex direction-col gap-8 bg-soft-gray pad-20">
							<div class="user flex items-center gap-8">
								<div
									class="pic flex-center"
									style="width: 30px; height: 30px; background-color: gray; border-radius: 50%"
								>
									<i class="las la-user-alt text-col-white" style="font-size: 20px;"></i>
								</div>

								Anónimo
							</div>
							<div class="flex gap-16 items-center">
								<StarRating count={review.rating} />
								<p class="sm-p p-ghost">{toReadableDate(review.created_at)}</p>
							</div>
							{#if review.comment}
								<p class="lg-p">{review.comment}</p>
							{/if}
						</div>
					{/each}
				</div>
			</section>
		{:else}
			<div class="flex-center full-size" style="height: calc(100vh - 75px);">
				<p class="p-ghost lg-p">404, receta no encontrada</p>
			</div>
		{/if}
	</main>
{:else}
	<div class="flex-center full-size" style="height: calc(100vh - 75px);">
		<RotatingNutriplan />
	</div>
{/if}
