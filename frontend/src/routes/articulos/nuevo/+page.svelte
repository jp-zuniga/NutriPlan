<script>
	import ArticleForm from '$lib/components/ArticleForm.svelte';
</script>

<svelte:head>
	<title>Crear Artículo - NutriPlan</title>
</svelte:head>

<main class="create-article-page">
	<section class="full-width" style="background-color: #84994F; padding: 40px 0;">
		<div class="container">
			<div class="flex-center direction-col">
				<h1 class="h1 bold text-col-white mb animate-fade-in-down">Crear Artículo</h1>
				<p class="lg-p text-col-white txt-center animate-fade-in-up animate-delay-1">
					Comparte tu conocimiento sobre nutrición y bienestar
				</p>
			</div>
		</div>
	</section>

	<section class="full-width pad-50">
		<div class="container">
			<ArticleForm />
		</div>
	</section>
</main>

<style>
	.create-article-page {
		min-height: calc(100vh - 75px);
	}

	.container {
		max-width: 1000px;
		margin: 0 auto;
		padding: 0 20px;
	}
</style>
