<script>
	import { onMount, tick } from 'svelte';
	import { get } from 'svelte/store';
	import { goto } from '$app/navigation';
	import Banner from '$lib/components/Banner.svelte';
	import { authUser } from '$lib/stores/auth';
	import { json } from '@sveltejs/kit';
	import { API_LOGIN_ENDPOINT } from '$lib/endpoints';

	const highlights = [
		'Accede a tus planes y recetas guardadas',
		'Recibe recomendaciones de IA adaptadas a tu progreso',
		'Comparte tu evolución con tu nutricionista'
	];

	let loading = $state(false);
	let error = $state('');
	let success = $state(false);

	onMount(() => {
		$effect(() => {
			if ($authUser != null) {
				goto('/');
			}
		});
	});

	const createFormRequest = () => {
		let formRequest = {};
		for (const question of questions) {
			formRequest[question.id] = question.value;
		}
		return formRequest;
	};

	const handleSubmit = async (event) => {
		event.preventDefault();

		if (loading) return;

		error = '';
		success = false;
		loading = true;

		// Fuerza un re-render
		await tick();

		let request = createFormRequest();

		try {
			const response = await fetch('/api/login', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(request)
			});

			const data = await response.json();
			console.log('Data: ', data);

			if (data)
				if (!response.ok) {
					error = data?.error ?? `Error accediendo a tu cuenta (HTTP ${response.status})`;
					loading = false;
					return;
				}

			success = true;
			console.log('User: ', data.user);
			$authUser = data.user;

			setTimeout(() => {
				goto('/');
			}, 1000);
		} catch (err) {
			error = err;
		}

		loading = false;
	};

	const questions = $state([
		{
			id: 'email',
			label: 'Correo Electrónico',
			type: 'email',
			placeholder: 'tu@correo.com',
			required: true,
			value: null
		},
		{
			id: 'password',
			label: 'Contraseña',
			type: 'password',
			placeholder: '••••••••',
			required: true,
			value: null
			// validator: (password) => {
			// 	if (password.length < 8) return 'La contraseña debe tener un mínimo de 8 caracteres';
			// 	return '';
			// }
		}
	]);
</script>

{#if $authUser !== undefined && $authUser === null}
	<main class="login">
		<section class="hero">
			<div class="container hero-grid">
				<article class="copy">
					<h1>Inicia sesión en NutriPlan</h1>
					<p>
						Retoma tus planes personalizados, sincroniza tus recetas favoritas y continúa tu camino
						hacia un bienestar con sabor nicaragüense.
					</p>
					<ul>
						{#each highlights as item}
							<li>{item}</li>
						{/each}
					</ul>
				</article>
				<form class="card form" onsubmit={handleSubmit}>
					<h2>Bienvenido de vuelta</h2>
					{#each questions as question}
						<label for={question.id}
							>{question.label}
							{#if question.required}
								<span style="color: red">*</span>
							{/if}
						</label>
						<input
							name={question.id}
							type={question.type}
							placeholder={question.placeholder}
							required={question.required}
							bind:value={question.value}
							oninput={(event) => {
								const error = question.validator ? question.validator(event.target.value) : '';
								event.target.setCustomValidity(error || '');
							}}
							disabled={loading}
						/>
					{/each}
					<div class="form-row">
						<label class="remember">
							<input name="remember" type="checkbox" /> Recuérdame
						</label>
						<a href="#">¿Olvidaste tu contraseña?</a>
					</div>
					<button class="btn primary" type="submit" disabled={loading}>
						{#if loading}
							Cargando…
						{:else}
							Ingresar
						{/if}
					</button>
					<!-- {#if error}
					<p class="feedback error">{error}</p>
				{/if}
				{#if showSuccess}
					<p class="feedback success">¡Bienvenido! Redirigiendo…</p>
				{/if} -->
					{#if error}
						<p id="fb-error" class="feedback error">{error}</p>
					{/if}
					{#if success}
						<p id="fb-success" class="feedback success">
							¡Sesión Iniciada! Preparando tu experiencia…
						</p>
					{/if}
					<p class="signup">
						¿Aún no tienes cuenta? <a href="/signup">Regístrate aquí</a>
					</p>
				</form>
			</div>
		</section>
	</main>
{/if}

<style>
	input {
		transition: 0.25s ease;
	}

	input:user-invalid {
		background-color: #ffd0ce;
	}

	#fb-error,
	#fb-success {
		width: 100%;
		padding: 5px;
		font-size: 15px;
		text-align: center;
		color: rgb(0, 0, 0);
		border-radius: 15px;
	}

	#fb-error {
		border: 2px solid rgb(255, 0, 0);
		background-color: rgba(255, 0, 0, 0.35);
	}

	#fb-success {
		border: 2px solid rgb(0, 255, 0);
		background-color: rgba(0, 255, 0, 0.35);
	}

	.login {
		display: flex;
		flex-direction: column;
		gap: 4rem;
		padding-bottom: 4rem;
	}

	.container {
		max-width: 960px;
		margin: 0 auto;
		padding: 0 1.5rem;
	}

	.hero-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 2.5rem;
		align-items: stretch;
		margin-top: 2rem;
	}

	.copy {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.copy h1 {
		margin: 0;
		font-size: clamp(2.1rem, 3vw, 3rem);
	}

	.copy p {
		margin: 0;
		color: var(--color-soft);
	}

	.copy ul {
		margin: 0;
		padding-left: 1.1rem;
		color: var(--color-soft);
		line-height: 1.6;
	}

	.form {
		padding: 2.4rem 2.6rem;
		display: flex;
		flex-direction: column;
		gap: 1.2rem;
	}

	.form h2 {
		margin: 0;
	}

	.form-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 1rem;
		font-size: 0.95rem;
	}

	.remember {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		color: var(--color-soft);
	}

	.form button {
		margin-top: 0.5rem;
	}

	.feedback {
		margin: 0;
		font-size: 0.92rem;
	}

	.feedback.error {
		color: #b3261e;
	}

	.feedback.success {
		color: var(--color-forest);
	}

	.form a {
		color: var(--color-forest);
		text-decoration: none;
		font-weight: 600;
	}

	.signup {
		margin: 0;
		font-size: 0.95rem;
		color: var(--color-soft);
	}

	@media (max-width: 640px) {
		.form {
			padding: 2rem;
		}

		.form-row {
			flex-direction: column;
			align-items: flex-start;
		}
	}
</style>
