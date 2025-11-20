<script lang="ts">
	import { goto } from '$app/navigation';
	import { toReadableDate } from '$lib/utils/date';

	let { article } = $props();

	function gotoArticle() {
		goto(`/articulos/${article.slug}`);
	}

	// Calcular extracto si no existe
	function getExcerpt(content, maxLength = 150) {
		if (article.excerpt) return article.excerpt;
		const text = content.replace(/[#*`_\[\]()]/g, '').trim();
		return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
	}
</script>

<button
	class="article-card flex direction-col bg-white soft-outline no-border pad-20 hoverable animate-fade-in-up b-shadow"
	onclick={gotoArticle}
	aria-roledescription="Open Article"
>
	<div class="article-header mb">
		<h3 class="lg-p bold txt-left mb-s">{article.title}</h3>
		<div class="article-meta flex direction-col gap-4 sm-p p-ghost">
			<span class="author">
				<i class="las la-user"></i>
				{article.author.name || 'NutriPlan'}
			</span>
			<span class="date">
				<i class="las la-calendar"></i>
				{toReadableDate(article.created_at)}
			</span>
			{#if article.reading_time}
				<span class="reading-time">
					<i class="las la-clock"></i>
					{article.reading_time} min
				</span>
			{/if}
		</div>
	</div>

	<p class="article-excerpt md-p p-ghost txt-left no-overflow">
		{getExcerpt(article.text)}
	</p>

	<div class="article-footer mt flex items-center justify-between">
		<span class="read-more sm-p p-emphasis">
			Leer más <i class="las la-arrow-right"></i>
		</span>
	</div>
</button>

<style>
	.article-card {
		width: 300px;
		height: 250px;
		cursor: pointer;
		transition:
			transform 0.2s ease,
			box-shadow 0.2s ease,
			background 0.2s ease;
		text-align: left;
	}

	.article-card:hover,
	.article-card:focus {
		background-color: var(--color-soft-white);
		outline: 1px solid rgba(0, 0, 0, 0.3);
		transform: translateY(-3px);
		box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
	}

	.article-header h3 {
		line-height: 1.3;
		color: var(--color-forest);
		transition: color 0.2s ease;
	}

	.article-card:hover h3 {
		color: var(--color-primary-dark);
	}

	.article-meta {
		flex-wrap: wrap;
	}

	.article-meta span {
		display: flex;
		align-items: center;
		gap: 4px;
	}

	.article-excerpt {
		line-height: 1.6;
		flex-grow: 1;
	}

	.read-more {
		font-weight: 600;
		transition: transform 0.2s ease;
	}

	.article-card:hover .read-more {
		transform: translateX(5px);
	}

	.read-more i {
		transition: transform 0.2s ease;
	}

	.article-card:hover .read-more i {
		transform: translateX(3px);
	}
</style>
