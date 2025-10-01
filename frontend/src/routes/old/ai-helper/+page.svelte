<script>
	import { AI_API_ENDPOINT } from '$lib/endpoints';
	import { preventDefault } from 'svelte/legacy';
	import showdown from 'showdown';

	const user = 'Mauricio';
	const firstLetter = user.trim()[0];

	const ai_model = 'Gemini 2.5 Pro';
	const bot_name = 'Nonna';

	let messages = $state([]);
	let userInput = $state();

	let loading = $state(false);
	let messagesContainer = $state();

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

	const converter = new showdown.Converter();

	function markdownToHtml(text) {
		return converter.makeHtml(text);
	}

	// Send message to AI
	async function sendMessage() {
		if (!userInput.trim()) return;

		messages = [...messages, { sender: 'user', text: userInput }];
		loading = true;

		const messageToAI = userInput;
		userInput = '';
		// Placeholder fetch
		fetch(AI_API_ENDPOINT, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				message: messageToAI,
				user_id: user
			}),
			signal: AbortSignal.timeout(50000)
		})
			.then((response) => {
				return response.json();
			})
			.then((data) => {
				if (!data.answer) throw 'No se encontro una respuesta';
				// Parsear de markdown a HTML
				const parsedAnswer = markdownToHtml(data.answer);

				messages = [
					...messages,
					{
						sender: 'ai',
						text: parsedAnswer
					}
				];
				loading = false;
			})
			.catch((error) => {
				const displayText = 'Hubo un error comunicandose con el servidor: ' + error;

				messages = [
					...messages,
					{
						sender: 'ai',
						text: displayText
					}
				];
				loading = false;
			});
	}
</script>

<div id="page-body">
	<!-- Banner -->
	<div id="banner">
		<div class="botname">
			<div class="logo">
				<i class="lab la-cloudsmith"></i>
			</div>
			<span id="bot-name">{bot_name}</span>
			<span id="model">{ai_model}</span>
		</div>
		<div class="user-container">{firstLetter}</div>
	</div>

	<!-- Chatbox -->
	<div id="chatbox-section">
		<div id="chatbox">
			<div class="message-container" bind:this={messagesContainer}>
				{#if messages.length == 0}
					<h2>Buenas tardes, {user}<br />En que te puedo ayudar?</h2>
				{:else}
					{#each messages as message}
						<div class="message {message.sender}"><span>{@html message.text}</span></div>
					{/each}

					{#if loading}
						<div class="message ai loading">
							<span>Generando respuesta...</span>
						</div>
					{/if}
				{/if}
			</div>
			<div class="input-box">
				<textarea
					type="text"
					disabled={loading}
					placeholder="Pregunta lo que quieras"
					bind:value={userInput}
					onkeypress={(event) => {
						if (event.key == 'Enter' && !event.shiftKey) {
							event.preventDefault();
							sendMessage();
						}
					}}
				></textarea>
				<!-- <button id="input-submit" onclick={sendMessage}>
					<i class="las la-arrow-up"></i>
				</button> -->
			</div>
		</div>
	</div>
</div>

<style>
	#page-body {
		display: grid;
		grid-template-rows: 100px 1fr 100px;

		width: 100vw;
		height: 100vh;

		background-color: #efedec;
	}

	#chatbox-section {
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	#chatbox {
		height: 100%;
		width: 50%;

		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.input-box {
		width: 75%;
		height: 125px;
	}

	.input-box textarea {
		width: 100%;
		height: 100%;

		padding: 20px;
		border-radius: 20px;
		border: none;
		outline: 7px solid rgba(0, 0, 0, 0.1);

		resize: none;
	}

	.message-container {
		padding: 10px;
		width: 75%;
		min-height: 200px;
		max-height: 450px;
		margin-bottom: 50px;
		overflow-y: auto;
	}

	.message {
		width: 100%;
		display: flex;
		margin-bottom: 5px;
	}

	.message.user {
		justify-content: end;
	}

	.message span {
		padding: 10px;
		border-radius: 15px;
	}

	.message.user span {
		max-width: 75%;
		border-radius: 15px 2px 15px 15px;
		background: linear-gradient(152deg, rgba(56, 239, 125, 0.5) 0%, rgba(0, 242, 96, 0.5) 100%);
	}

	.message-container h2 {
		color: rgb(20, 20, 20);
		font-size: 30px;
		text-align: center;
		font-weight: 600;
	}

	.input-box textarea::placeholder {
		color: rgb(138, 138, 138);
	}

	#banner {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 25px;
	}

	.botname {
		display: flex;
		align-items: center;
	}

	.botname .logo {
		width: 40px;
		height: 40px;
		border-radius: 25px;
		border: 2px solid rgb(65, 65, 65);

		display: flex;
		align-items: center;
		justify-content: center;

		background: linear-gradient(152deg, rgba(74, 74, 74, 1) 0%, rgba(0, 0, 0, 1) 100%);
	}

	.botname .logo i {
		font-size: 25px;
		color: white;
	}

	.botname #bot-name {
		margin-left: 10px;
		font-weight: 500;
		font-size: 25px;
		color: rgb(20, 20, 20);
		user-select: none;
	}

	.botname #model {
		margin-left: 15px;
		font-weight: 500;
		font-size: 12px;
		color: rgb(20, 20, 20);
		padding: 5px;

		background: linear-gradient(152deg, rgba(0, 195, 84, 0.3) 0%, rgba(0, 162, 99, 0.3) 100%);
		outline: 1px solid rgb(0, 195, 84);
		border-radius: 8px;
		color: rgb(43, 43, 43);

		user-select: none;
	}

	.user-container {
		width: 40px;
		height: 40px;
		background-color: rgba(0, 0, 0, 0.1);
		border-radius: 20px;

		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
