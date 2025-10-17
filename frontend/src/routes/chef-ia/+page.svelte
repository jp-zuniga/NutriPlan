<script>
	import { onMount } from 'svelte';
	import Banner from '$lib/components/Banner.svelte';
	import ChatMessage from '$lib/components/ChatMessage.svelte';
	import ChatInput from '$lib/components/ChatInput.svelte';
	import RotatingNutriplan from '$lib/components/RotatingNutriplan.svelte';
	import SVG_AI from '$lib/assets/ai.svg';
	import { API_CHEFCITO_CHAT_ENDPOINT } from '$lib/endpoints';
	import { authenticatedFetch, JSONRequest } from '$lib/utils/fetch';

	let messages = $state([]);
	let loading = $state(false);
	let error = $state('');
	let userInput = $state('');
	let messagesContainer;

	const allSuggestedQuestions = [
		'¿Qué puedo cocinar con yuca y queso?',
		'¿Cómo hago un gallo pinto saludable?',
		'Dame una receta rápida para el desayuno',
		'Recomiéndame un platillo típico bajo en calorías',
		'¿Qué receta puedo hacer en 30 minutos?',
		'Ayúdame a planear una cena nicaragüense',
		'Necesito ideas para meal prep semanal',
		'¿Cómo sustituir ingredientes en recetas tradicionales?',
		'¿Qué platillo puedo hacer con plátano maduro?',
		'Dame opciones vegetarianas de comida nica',
		'¿Cómo hacer un nacatamal más ligero?',
		'Recetas con frijoles rojos y arroz'
	];

	// Seleccionar 4 preguntas aleatorias
	let randomQuestions = $state([]);

	onMount(() => {
		randomQuestions = allSuggestedQuestions.sort(() => Math.random() - 0.5).slice(0, 4);
	});

	const scrollToBottom = () => {
		if (messagesContainer) {
			setTimeout(() => {
				messagesContainer.scrollTop = messagesContainer.scrollHeight;
			}, 100);
		}
	};

	const sendMessage = async (text) => {
		if (!text || !text.trim()) return;

		const messageText = text.trim();

		// Agregar mensaje del usuario
		messages = [
			...messages,
			{
				role: 'user',
				content: messageText,
				timestamp: new Date()
			}
		];

		scrollToBottom();
		loading = true;
		error = '';

		try {
			const response = await fetch('/api/chef-ia/', JSONRequest({ message: messageText }));

			if (!response.ok) {
				const data = await response.json();
				throw new Error(data?.message ?? 'Error en la respuesta del servidor');
			}

			const data = (await response.json()).data;
			console.log(data);

			if (data == null) throw new Error('Hubo un error obteniendo la respuesta de chefcito');

			// Agregar respuesta de Chefcito
			messages = [
				...messages,
				{
					role: 'assistant',
					content: data.reply || 'No recibí respuesta de Chefcito.',
					recipes: data.recipes || [],
					ingredients: data.ingredients || [],
					timestamp: new Date()
				}
			];

			scrollToBottom();
		} catch (err) {
			error = err ?? 'No pude conectarme con Chefcito. Intentá de nuevo.';
			console.error('Error al enviar mensaje:', err);
		} finally {
			loading = false;
		}
	};
</script>

<svelte:head>
	<title>Chefcito - Tu Asistente Culinario IA | NutriPlan</title>
</svelte:head>

<main class="chat-page">
	<header class="chat-header">
		<div class="header-content">
			<div class="header-avatar">
				<img src={SVG_AI} alt="Chefcito" />
			</div>
			<div class="header-text">
				<h1 class="h2 bold no-margin">Chefcito</h1>
				<p class="sm-p p-ghost no-margin">Tu asistente culinario nicaragüense</p>
			</div>
		</div>
	</header>

	<div class="messages-container" bind:this={messagesContainer}>
		{#if messages.length === 0}
			<div class="welcome-screen">
				<div class="welcome-icon">
					<img src={SVG_AI} alt="Chefcito" />
				</div>
				<h2 class="h2 bold text-col-1">¡Hola! Soy Chefcito</h2>
				<p class="md-p text-col-2">
					Tu asistente culinario personal. Pregúntame sobre recetas, ingredientes, planificación de
					comidas o consejos de cocina. Estoy aquí para ayudarte a cocinar rico y saludable al
					estilo nica.
				</p>

				<div class="suggested-section">
					<h3 class="h4 bold text-col-1 mb">Preguntas para empezar:</h3>
					<div class="suggestions-grid">
						{#each randomQuestions as question}
							<button class="suggestion-btn card hoverable" onclick={() => sendMessage(question)}>
								<i class="las la-comment-dots"></i>
								<span>{question}</span>
							</button>
						{/each}
					</div>
				</div>
			</div>
		{:else}
			<div class="messages-list">
				{#each messages as message}
					<ChatMessage {message} />
				{/each}

				{#if loading}
					<div class="typing-indicator">
						<div class="typing-avatar">
							<img src={SVG_AI} alt="Chefcito" />
						</div>
						<div class="typing-bubble card">
							<span class="typing-text">Chefcito está escribiendo</span>
							<div class="typing-dots">
								<span></span>
								<span></span>
								<span></span>
							</div>
						</div>
					</div>
				{/if}

				{#if error}
					<div class="error-message card">
						<i class="las la-exclamation-triangle"></i>
						<p>{error}</p>
						<button class="btn ghost sm" onclick={() => (error = '')}> Cerrar </button>
					</div>
				{/if}
			</div>
		{/if}
	</div>

	<div class="input-container">
		<div class="input-wrapper">
			<ChatInput
				bind:value={userInput}
				onSend={sendMessage}
				disabled={loading}
				placeholder="Pregúntame sobre recetas, ingredientes o tips de cocina..."
			/>
		</div>
	</div>
</main>

<style>
	.chat-page {
		display: flex;
		flex-direction: column;
		height: calc(100vh - 80px);
		background: var(--color-soft-white);
		position: relative;
	}

	.chat-header {
		background: white;
		border-bottom: 1px solid var(--color-soft-gray);
		padding: 1rem 0;
		flex-shrink: 0;
	}

	.header-content {
		max-width: 1000px;
		margin: 0 auto;
		padding: 0 1.5rem;
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	.header-avatar {
		width: 48px;
		height: 48px;
		border-radius: 50%;
		background: var(--gradient-leaf);
		padding: 0.75rem;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	.header-avatar img {
		width: 100%;
		height: 100%;
		filter: brightness(0) invert(1);
	}

	.header-text h1 {
		color: var(--color-forest);
	}

	.messages-container {
		flex: 1;
		overflow-y: auto;
		overflow-x: hidden;
		scroll-behavior: smooth;
	}

	.welcome-screen {
		max-width: 700px;
		margin: 0 auto;
		padding: 3rem 1.5rem;
		text-align: center;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.5rem;
	}

	.welcome-icon {
		width: 120px;
		height: 120px;
		border-radius: 50%;
		background: var(--gradient-leaf);
		padding: 2rem;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: var(--shadow-soft);
	}

	.welcome-icon img {
		width: 100%;
		height: 100%;
		filter: brightness(0) invert(1);
	}

	.welcome-screen h2 {
		margin: 0;
	}

	.welcome-screen > p {
		max-width: 500px;
		margin: 0;
		line-height: 1.6;
	}

	.suggested-section {
		width: 100%;
		margin-top: 2rem;
	}

	.suggestions-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 1rem;
		margin-top: 1rem;
	}

	.suggestion-btn {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 1rem 1.25rem;
		background: white;
		border: 2px solid var(--color-soft-gray);
		border-radius: var(--radius-md);
		text-align: left;
		cursor: pointer;
		transition: all 0.2s ease;
		color: var(--color-forest);
		font-size: 0.95rem;
		line-height: 1.4;
	}

	.suggestion-btn i {
		font-size: 1.5rem;
		color: var(--color-leaf);
		flex-shrink: 0;
	}

	.suggestion-btn:hover {
		border-color: var(--color-leaf);
		background: var(--color-soft-stone);
		transform: translateY(-2px);
	}

	.messages-list {
		max-width: 900px;
		margin: 0 auto;
		padding: 2rem 1.5rem;
	}

	.typing-indicator {
		display: flex;
		gap: 0.75rem;
		margin-bottom: 1.5rem;
	}

	.typing-avatar {
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

	.typing-avatar img {
		width: 100%;
		height: 100%;
		filter: brightness(0) invert(1);
	}

	.typing-bubble {
		padding: 1rem 1.25rem;
		border-radius: var(--radius-md);
		border-bottom-left-radius: 0.25rem;
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.typing-text {
		color: var(--color-soft);
		font-size: 0.9rem;
	}

	.typing-dots {
		display: flex;
		gap: 0.25rem;
	}

	.typing-dots span {
		width: 6px;
		height: 6px;
		border-radius: 50%;
		background: var(--color-soft);
		animation: typing 1.4s infinite;
	}

	.typing-dots span:nth-child(2) {
		animation-delay: 0.2s;
	}

	.typing-dots span:nth-child(3) {
		animation-delay: 0.4s;
	}

	@keyframes typing {
		0%,
		60%,
		100% {
			transform: translateY(0);
			opacity: 0.5;
		}
		30% {
			transform: translateY(-10px);
			opacity: 1;
		}
	}

	.error-message {
		max-width: 600px;
		margin: 0 auto 1.5rem;
		padding: 1rem 1.25rem;
		background: rgba(239, 68, 68, 0.1);
		border: 1px solid rgba(239, 68, 68, 0.2);
		border-radius: var(--radius-md);
		display: flex;
		align-items: center;
		gap: 0.75rem;
		color: #dc2626;
	}

	.error-message i {
		font-size: 1.5rem;
		flex-shrink: 0;
	}

	.error-message p {
		flex: 1;
		margin: 0;
	}

	.input-container {
		background: white;
		border-top: 1px solid var(--color-soft-gray);
		flex-shrink: 0;
	}

	.input-wrapper {
		max-width: 900px;
		margin: 0 auto;
	}

	@media (max-width: 768px) {
		.chat-page {
			height: calc(100vh - 70px);
		}

		.header-content {
			padding: 0 1rem;
		}

		.header-avatar {
			width: 40px;
			height: 40px;
			padding: 0.625rem;
		}

		.welcome-screen {
			padding: 2rem 1rem;
		}

		.welcome-icon {
			width: 100px;
			height: 100px;
			padding: 1.5rem;
		}

		.suggestions-grid {
			grid-template-columns: 1fr;
		}

		.messages-list {
			padding: 1.5rem 1rem;
		}
	}
</style>
