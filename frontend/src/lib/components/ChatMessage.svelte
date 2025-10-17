<script>
	import SVG_AI from '$lib/assets/ai.svg';

	let { message } = $props();

	const isUser = message.role === 'user';
	const isAssistant = message.role === 'assistant';

	// Simple markdown parser para texto básico
	function parseMarkdown(text) {
		if (!text) return '';

		// Bold
		text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
		// Italic
		text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
		// Line breaks
		text = text.replace(/\n/g, '<br>');

		return text;
	}

	function formatTime(timestamp) {
		if (!timestamp) return '';
		const date = new Date(timestamp);
		return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
	}
</script>

<div class="message-wrapper {isUser ? 'user-message' : 'assistant-message'}">
	{#if isAssistant}
		<div class="message-avatar">
			<img src={SVG_AI} alt="Chefcito" />
		</div>
	{/if}

	<div class="message-content {isUser ? 'user-bubble' : 'assistant-bubble'}">
		{#if isAssistant}
			<div class="message-header">
				<span class="message-sender">Chefcito</span>
				{#if message.timestamp}
					<span class="message-time">{formatTime(message.timestamp)}</span>
				{/if}
			</div>
		{/if}

		<div class="message-text">
			{@html parseMarkdown(message.content)}
		</div>

		{#if message.recipes && message.recipes.length > 0}
			<div class="message-suggestions">
				<p class="sm-p bold">Recetas sugeridas:</p>
				<div class="flex gap-8 wrap">
					{#each message.recipes as recipeId}
						<a href="/recetas/{recipeId}" class="chip">
							<i class="las la-utensils"></i>
							Receta #{recipeId}
						</a>
					{/each}
				</div>
			</div>
		{/if}

		{#if message.ingredients && message.ingredients.length > 0}
			<div class="message-suggestions">
				<p class="sm-p bold">Ingredientes mencionados:</p>
				<div class="flex gap-8 wrap">
					{#each message.ingredients as ingredient}
						<span class="chip">{ingredient}</span>
					{/each}
				</div>
			</div>
		{/if}

		{#if isUser && message.timestamp}
			<div class="message-time-user">{formatTime(message.timestamp)}</div>
		{/if}
	</div>
</div>

<style>
	.message-wrapper {
		display: flex;
		gap: 0.75rem;
		margin-bottom: 1.5rem;
		max-width: 100%;
	}

	.user-message {
		justify-content: flex-end;
	}

	.assistant-message {
		justify-content: flex-start;
	}

	.message-avatar {
		width: 36px;
		height: 36px;
		border-radius: 50%;
		background: var(--gradient-leaf);
		padding: 0.5rem;
		flex-shrink: 0;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.message-avatar img {
		width: 100%;
		height: 100%;
		filter: brightness(0) invert(1);
	}

	.message-content {
		max-width: 70%;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.user-bubble {
		background: var(--gradient-leaf);
		color: white;
		padding: 1rem 1.25rem;
		border-radius: var(--radius-md);
		border-bottom-right-radius: 0.25rem;
	}

	.assistant-bubble {
		background: white;
		color: var(--color-forest);
		padding: 1rem 1.25rem;
		border-radius: var(--radius-md);
		border-bottom-left-radius: 0.25rem;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
	}

	.message-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.5rem;
		padding-bottom: 0.5rem;
		border-bottom: 1px solid var(--color-soft-gray);
	}

	.message-sender {
		font-weight: 600;
		color: var(--color-forest);
		font-size: 0.9rem;
	}

	.message-time {
		font-size: 0.75rem;
		color: var(--color-soft);
	}

	.message-time-user {
		font-size: 0.75rem;
		color: rgba(255, 255, 255, 0.8);
		text-align: right;
		margin-top: 0.25rem;
	}

	.message-text {
		line-height: 1.6;
		word-wrap: break-word;
	}

	.user-bubble .message-text {
		color: white;
	}

	.message-suggestions {
		margin-top: 0.75rem;
		padding-top: 0.75rem;
		border-top: 1px solid var(--color-soft-gray);
	}

	.message-suggestions p {
		margin: 0 0 0.5rem 0;
		color: var(--color-soft);
	}

	.chip {
		display: inline-flex;
		align-items: center;
		gap: 0.25rem;
		padding: 0.375rem 0.75rem;
		background: var(--color-soft-stone);
		color: var(--color-forest);
		border-radius: var(--radius-sm);
		font-size: 0.875rem;
		font-weight: 500;
		text-decoration: none;
		transition: all 0.2s ease;
	}

	.chip:hover {
		background: var(--color-leaf);
		color: white;
		transform: translateY(-1px);
	}

	.chip i {
		font-size: 1rem;
	}

	@media (max-width: 768px) {
		.message-content {
			max-width: 85%;
		}

		.message-avatar {
			width: 32px;
			height: 32px;
		}
	}
</style>
