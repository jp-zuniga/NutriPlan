<script>
	import { page } from '$app/stores';
	import { API_ARTICLES_ENDPOINT } from '$lib/endpoints';
	import { toReadableDate } from '$lib/utils/date';
	import RotatingNutriplan from '$lib/components/RotatingNutriplan.svelte';
	import { marked } from 'marked';

	const article_slug = $state($page.params.slug);

	let loading = $state(true);
	let article = $state(null);

	const get_article = async () => {
		loading = true;

		try {
			const response = await fetch(`${API_ARTICLES_ENDPOINT}${article_slug}`, {
				method: 'GET'
			});

			console.log(`Article response: ${response}`);

			if (response.ok) {
				const data = await response.json();
				article = data;
				console.log('Article data:', article);
			} else {
				article = null;
			}
		} catch (error) {
			console.error('Error fetching article:', error);
			article = null;
		}

		loading = false;
	};

	// Calcular tiempo de lectura estimado
	function calculateReadingTime(content) {
		if (!content) return 0;
		const wordsPerMinute = 200;
		const words = content.trim().split(/\s+/).length;
		return Math.ceil(words / wordsPerMinute);
	}

	get_article();
</script>

<svelte:head>
	{#if article}
		<title>{article.title} - NutriPlan</title>
	{:else}
		<title>Artículo - NutriPlan</title>
	{/if}
</svelte:head>

{#if !loading}
	<main id="article" class="mb animate-fade-in-up">
		{#if article}
			<!-- Breadcrumb -->
			<section class="full-width">
				<div class="container md flex direction-col mt-l">
					<div id="trail" class="flex full-width items-center gap-8">
						<a href="/articulos" class="no-ul p-ghost">Artículos</a>
						<i class="las la-angle-right"></i>
						<a href="/articulos/{article.slug}" class="no-ul p-emphasis">{article.title}</a>
					</div>
				</div>
			</section>

			<!-- Article Header -->
			<section id="article-header" class="full-width">
				<div class="container md flex direction-col">
					<h1 class="h1 bold mb">{article.title}</h1>

					<div class="article-meta flex items-center gap-24 mb-l p-ghost">
						<div class="author flex items-center gap-8">
							<i class="las la-user"></i>
							<span>{article.author.name || 'NutriPlan'}</span>
						</div>
						<div class="date flex items-center gap-8">
							<i class="las la-calendar"></i>
							<span>{toReadableDate(article.created_at)}</span>
						</div>
						<!-- {#if article.reading_time}
							<div class="reading-time flex items-center gap-8">
								<i class="las la-clock"></i>
								<span>{article.reading_time} min de lectura</span>
							</div>
						{:else}
							<div class="reading-time flex items-center gap-8">
								<i class="las la-clock"></i>
								<span>{calculateReadingTime(article.text)} min de lectura</span>
							</div>
						{/if}	 -->
					</div>

					{#if article.updated_at && article.updated_at !== article.created_at}
						<p class="sm-p p-ghost">
							Última actualización: {toReadableDate(article.updated_at)}
						</p>
					{/if}

					<hr class="full-width soft mt" />
				</div>
			</section>

			<!-- Article Content -->
			<section id="article-content" class="full-width mb-l">
				<div class="container md pad-20 soft-outline bg-white">
					<div class="markdown-content">
						{@html marked(article.text)}
					</div>
				</div>
			</section>

			<!-- Back to articles -->
			<section class="full-width mb-l mt-l">
				<div class="container md flex-center mt-l">
					<a href="/articulos" class="btn ghost">
						<i class="las la-arrow-left"></i>
						Volver a artículos
					</a>
				</div>
			</section>
		{:else}
			<div class="flex-center full-size" style="height: calc(100vh - 75px);">
				<div class="flex direction-col items-center gap-16">
					<p class="p-ghost h2">404</p>
					<p class="p-ghost lg-p">Artículo no encontrado</p>
					<a href="/articulos" class="btn primary">Ver todos los artículos</a>
				</div>
			</div>
		{/if}
	</main>
{:else}
	<div class="flex-center full-size" style="height: calc(100vh - 75px);">
		<RotatingNutriplan />
	</div>
{/if}

<style>
	#article-header {
		background: var(--color-soft-white);
		padding-block: 40px;
	}

	.article-meta {
		flex-wrap: wrap;
		font-size: 0.95rem;
	}

	/* Estilos para contenido markdown */
	.markdown-content {
		font-family: var(--font-base);
		line-height: 1.8;
		color: var(--color-forest);
		max-width: 100%;
	}

	.markdown-content :global(h1),
	.markdown-content :global(h2),
	.markdown-content :global(h3),
	.markdown-content :global(h4),
	.markdown-content :global(h5),
	.markdown-content :global(h6) {
		font-family: var(--font-display);
		font-weight: 700;
		margin-top: 2rem;
		margin-bottom: 1rem;
		line-height: 1.3;
		color: var(--color-forest);
	}

	.markdown-content :global(h1) {
		font-size: 2.5rem;
	}
	.markdown-content :global(h2) {
		font-size: 2rem;
		border-bottom: 2px solid var(--color-soft-gray);
		padding-bottom: 0.5rem;
	}
	.markdown-content :global(h3) {
		font-size: 1.5rem;
	}
	.markdown-content :global(h4) {
		font-size: 1.25rem;
	}

	.markdown-content :global(p) {
		margin-bottom: 1.5rem;
		font-size: 1.1rem;
	}

	.markdown-content :global(a) {
		color: var(--color-primary-dark);
		text-decoration: underline;
		transition: color 0.2s ease;
	}

	.markdown-content :global(a:hover) {
		color: var(--color-emphasis);
	}

	.markdown-content :global(ul),
	.markdown-content :global(ol) {
		margin-left: 2rem;
		margin-bottom: 1.5rem;
	}

	.markdown-content :global(li) {
		margin-bottom: 0.5rem;
		line-height: 1.7;
	}

	.markdown-content :global(blockquote) {
		border-left: 4px solid var(--color-primary-dark);
		padding-left: 1.5rem;
		margin: 2rem 0;
		font-style: italic;
		color: var(--color-soft);
		background: var(--color-soft-white);
		padding: 1rem 1.5rem;
		border-radius: 4px;
	}

	.markdown-content :global(code) {
		background: var(--color-soft-gray);
		padding: 0.2rem 0.4rem;
		border-radius: 4px;
		font-family: 'Courier New', monospace;
		font-size: 0.9em;
	}

	.markdown-content :global(pre) {
		background: var(--color-soft-gray-darker);
		padding: 1.5rem;
		border-radius: 8px;
		overflow-x: auto;
		margin: 2rem 0;
	}

	.markdown-content :global(pre code) {
		background: none;
		padding: 0;
		border-radius: 0;
	}

	.markdown-content :global(img) {
		max-width: 100%;
		height: auto;
		border-radius: 8px;
		margin: 2rem 0;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	}

	.markdown-content :global(table) {
		width: 100%;
		border-collapse: collapse;
		margin: 2rem 0;
	}

	.markdown-content :global(th),
	.markdown-content :global(td) {
		border: 1px solid var(--color-soft-gray);
		padding: 0.75rem;
		text-align: left;
	}

	.markdown-content :global(th) {
		background: var(--color-soft-gray);
		font-weight: 600;
	}

	.markdown-content :global(hr) {
		border: none;
		border-top: 2px solid var(--color-soft-gray);
		margin: 3rem 0;
	}

	.markdown-content :global(strong) {
		font-weight: 700;
		color: var(--color-forest);
	}

	.markdown-content :global(em) {
		font-style: italic;
	}
</style>
