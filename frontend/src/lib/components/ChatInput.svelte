<script>
	let {
		value = $bindable(''),
		onSend = () => {},
		disabled = false,
		placeholder = 'Escribe tu pregunta aquí...'
	} = $props();

	let textareaElement;

	const handleKeydown = (e) => {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			handleSubmit();
		}
	};

	const handleSubmit = () => {
		const text = value.trim();
		if (!text || disabled) return;

		onSend(text);
		value = '';

		// Reset textarea height
		if (textareaElement) {
			textareaElement.style.height = 'auto';
		}
	};

	const adjustHeight = () => {
		if (textareaElement) {
			textareaElement.style.height = 'auto';
			textareaElement.style.height = Math.min(textareaElement.scrollHeight, 150) + 'px';
		}
	};
</script>

<div class="chat-input-container">
	<textarea
		bind:this={textareaElement}
		bind:value
		onkeydown={handleKeydown}
		oninput={adjustHeight}
		{placeholder}
		{disabled}
		rows="1"
		class="chat-textarea"
	></textarea>

	<button
		onclick={handleSubmit}
		disabled={disabled || !value.trim()}
		class="send-button"
		aria-label="Enviar mensaje"
	>
		{#if disabled}
			<i class="las la-circle-notch la-spin"></i>
		{:else}
			<i class="las la-paper-plane"></i>
		{/if}
	</button>
</div>

<style>
	.chat-input-container {
		display: flex;
		gap: 0.75rem;
		padding: 1rem;
		background: white;
		border-top: 1px solid var(--color-soft-gray);
		align-items: flex-end;
	}

	.chat-textarea {
		flex: 1;
		padding: 0.875rem 1rem;
		border: 2px solid var(--color-soft-gray);
		border-radius: var(--radius-md);
		font-size: 1rem;
		font-family: var(--font-base);
		resize: none;
		max-height: 150px;
		min-height: 48px;
		transition: border-color 0.2s ease;
		line-height: 1.5;
	}

	.chat-textarea:focus {
		outline: none;
		border-color: var(--color-leaf);
	}

	.chat-textarea:disabled {
		background: var(--color-soft-gray);
		cursor: not-allowed;
	}

	.send-button {
		width: 48px;
		height: 48px;
		background: var(--gradient-leaf);
		border: none;
		border-radius: var(--radius-md);
		color: white;
		font-size: 1.25rem;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.2s ease;
		flex-shrink: 0;
	}

	.send-button:hover:not(:disabled) {
		background: var(--color-primary-dark);
		transform: translateY(-2px);
	}

	.send-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
		transform: none;
	}

	.send-button i {
		transition: transform 0.2s ease;
	}

	.send-button:hover:not(:disabled) i {
		transform: translateX(2px);
	}

	@media (max-width: 768px) {
		.chat-input-container {
			padding: 0.75rem;
			gap: 0.5rem;
		}

		.chat-textarea {
			padding: 0.75rem;
			font-size: 0.95rem;
		}

		.send-button {
			width: 44px;
			height: 44px;
		}
	}
</style>

