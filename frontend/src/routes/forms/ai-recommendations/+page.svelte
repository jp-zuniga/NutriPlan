<script>
	import { onMount } from 'svelte';
	import { formAnswers } from '$lib/stores/formAnswers.js';
	import { writable } from 'svelte/store';
	import { AI_API_ENDPOINT } from '$lib/endpoints';

	// Chat state
	let messages = $state([
		{
			sender: 'ai',
			text: '¡Hola! Estoy aquí para recomendarte recetas personalizadas. ¿En qué te gustaría enfocarte hoy?'
		}
	]);
	let userInput = $state('');
	let loading = $state(false);
	let messagesContainer;

	$effect(() => {
		messages;
		loading;

		if (messagesContainer) {
			messagesContainer.scrollTo({
				top: messagesContainer.scrollHeight,
				behavior: 'smooth'
			});
		}
	});

	// Generate prompt from formAnswers
	function buildPrompt(answers) {
		const { foodAnswers, medicalAnswers } = answers;
		let prompt = 'Basado en mis preferencias alimenticias: ';
		prompt += foodAnswers?.join(', ') || 'N/A';
		prompt += '. Perfil de salud: ';
		prompt += medicalAnswers?.join(', ') || 'N/A';
		prompt += '. ¿Qué recetas me recomiendas?';
		return prompt;
	}

	// Send message to AI (placeholder)
	async function sendMessage() {
		if (!userInput.trim()) return;

		messages = [...messages, { sender: 'user', text: userInput }];
		loading = true;

		// Build prompt from form answers
		let prompt;
		formAnswers.subscribe((answers) => {
			prompt = buildPrompt(answers) + ' ' + userInput;
		})();

		const messageToAI = userInput;
		userInput = '';
		// Placeholder fetch
		fetch(AI_API_ENDPOINT, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				message: messageToAI
			})
		})
			.then((response) => {
				return response.json();
			})
			.then((data) => {
				let display_text = data.answer
					? data.answer
					: 'Hubo un error al comunicarse con el servidor';

				messages = [
					...messages,
					{
						sender: 'ai',
						text: display_text
					}
				];
				loading = false;
			});
		// setTimeout(() => {
		// 	messages = [
		// 		...messages,
		// 		{
		// 			sender: 'ai',
		// 			text: 'Esta es una respuesta simulada basada en tu mensaje: ' + messageToAI
		// 		}
		// 	];
		// 	loading = false;
		// }, 1200);
	}
</script>

<div class="ai-recommendations-page">
	<div class="header">
		<h1>Recomendaciones Inteligentes</h1>
		<p>Recibe sugerencias personalizadas de recetas según tus preferencias y perfil de salud.</p>
	</div>
	<div class="chatbox">
		<div class="messages" bind:this={messagesContainer}>
			{#each messages as msg}
				<div class="message {msg.sender}">
					<span>{msg.text}</span>
				</div>
			{/each}
			{#if loading}
				<div class="message ai loading">
					<span>Generando respuesta...</span>
				</div>
			{/if}
		</div>
		<form class="input-row" on:submit|preventDefault={sendMessage}>
			<input
				type="text"
				bind:value={userInput}
				placeholder="Escribe tu mensaje..."
				autocomplete="off"
			/>
			<button type="submit" aria-label="Enviar mensaje" disabled={loading || !userInput.trim()}>
				<svg
					width="24"
					height="24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
					><path d="M22 2L11 13"></path><path d="M22 2L15 22L11 13L2 9L22 2Z"></path></svg
				>
			</button>
		</form>
	</div>
</div>

<style>
	.ai-recommendations-page {
		min-height: 100vh;
		background: linear-gradient(120deg, #f8fafc 0%, #e0e7ff 100%);
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 0;
	}
	.header {
		margin-top: 48px;
		text-align: center;
	}
	.header h1 {
		font-size: 2.5rem;
		font-weight: 700;
		color: #3b82f6;
		margin-bottom: 0.5rem;
	}
	.header p {
		color: #64748b;
		font-size: 1.2rem;
	}
	.chatbox {
		background: #fff;
		box-shadow: 0 8px 32px rgba(60, 72, 100, 0.12);
		border-radius: 24px;
		width: 100%;
		max-width: 480px;
		margin: 32px auto;
		padding: 32px 24px 24px 24px;
		display: flex;
		flex-direction: column;
		gap: 16px;
	}
	.messages {
		flex: 1;
		overflow-y: scroll;
		max-height: 340px;
		margin-bottom: 12px;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}
	.input-row button {
		display: flex;
		justify-content: center;
		align-items: center;
	}
	.message {
		padding: 12px 18px;
		border-radius: 18px;
		max-width: 80%;
		word-break: break-word;
		font-size: 1rem;
		line-height: 1.5;
		box-shadow: 0 2px 8px rgba(60, 72, 100, 0.06);
	}
	.message.user {
		align-self: flex-end;
		background: linear-gradient(90deg, #3b82f6 0%, #6366f1 100%);
		color: #fff;
	}
	.message.ai {
		align-self: flex-start;
		background: #e0e7ff;
		color: #334155;
	}
	.message.loading {
		font-style: italic;
		opacity: 0.7;
	}
	.input-row {
		display: flex;
		gap: 8px;
		align-items: center;
	}
	.input-row input {
		flex: 1;
		padding: 12px 16px;
		border-radius: 16px;
		border: 1px solid #cbd5e1;
		font-size: 1rem;
		outline: none;
		transition: border 0.2s;
	}
	.input-row input:focus {
		border-color: #6366f1;
	}
	.input-row button {
		background: linear-gradient(90deg, #6366f1 0%, #3b82f6 100%);
		color: #fff;
		border: none;
		border-radius: 50%;
		width: 44px;
		height: 44px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: background 0.2s;
	}
	.input-row button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}
</style>
