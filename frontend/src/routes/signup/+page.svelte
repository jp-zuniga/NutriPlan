<script>
	import { onMount } from 'svelte';
	import { get } from 'svelte/store';
	import { goto } from '$app/navigation';
	import Banner from '$lib/components/Banner.svelte';
	import { authUser } from '$lib/stores/auth';
	import { API_REGISTER_ENDPOINT } from '$lib/endpoints';
	import { SESSION_ACCESS_COOKIE } from '$lib/cookies';
	import RotatingNutriplan from '$lib/components/RotatingNutriplan.svelte';

	let loading = $state(false);
	let error = $state('');
	let success = $state(false);
	let form = {
		name: '',
		email: '',
		phone: '',
		password: '',
		confirm: ''
	};

	let errorfields = $state({});

	$effect(() => {
		if ($authUser !== null && $authUser !== undefined) {
			goto('/');
		}
	});

	const createFormRequest = () => {
		let formRequest = {};
		for (const question of questions) {
			formRequest[question.id] = question.value;
		}
		return formRequest;
	};

	const handleLogin = async (event) => {
		event.preventDefault();

		error = '';
		loading = true;
		success = false;

		let request = createFormRequest();

		try {
			const response = await fetch('/api/register/', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(request)
			});

			const data = await response.json();

			if (data)
				if (!response.ok) {
					error = data?.error ?? `Error accediendo a tu cuenta (HTTP ${response.status})`;
					loading = false;
					return;
				}

			console.log('User: ', data.user);
			$authUser = data.user;
			success = true;
			setTimeout(() => {
				goto('/');
			}, 600);
		} catch (err) {}
	};

	const getQuestion = (id) => questions.find((q) => q.id === id) ?? null;

	const questions = $state([
		{
			id: 'full_name',
			label: 'Nombre Completo',
			type: 'text',
			placeholder: 'Ej. María Fernanda',
			required: true,
			value: null
		},
		{
			id: 'email',
			label: 'Correo Electrónico',
			type: 'email',
			placeholder: 'tu@correo.com',
			required: true,
			value: null
		},
		{
			id: 'phone',
			label: 'Teléfono',
			type: 'tel',
			placeholder: '+505',
			required: false,
			value: null
		},
		{
			id: 'password',
			label: 'Contraseña',
			type: 'password',
			placeholder: 'Minimo 8 caracteres',
			required: true,
			value: null,
			validator: (password) => {
				if (password.length < 8) return 'La contraseña debe tener un mínimo de 8 caracteres';
				return '';
			}
		},
		{
			id: 'password_confirm',
			label: 'Confirmar contraseña',
			type: 'password',
			placeholder: '',
			required: true,
			value: null,
			validator: (password) => {
				const pass = getQuestion('password')?.value ?? '';
				if (pass !== password) return 'Las contraseñas deben coincidir';
				return '';
			}
		}
	]);
</script>

{#if $authUser !== undefined && $authUser === null}
	<main class="signup-page">
		<section class="hero">
			<div class="container hero-grid">
				<article class="copy">
					<h1>Crea tu cuenta NutriPlan</h1>
					<p>
						Personaliza tu experiencia, guarda recetas favoritas y deja que Chef Nutri IA construya
						tu plan a partir de tu historia y cultura alimentaria.
					</p>
					<ul>
						<li>✨ Planes ajustados a tu presupuesto y tiempo</li>
						<li>🍲 Recetas con ingredientes nicaragüenses</li>
						<li>📈 Seguimiento de metas y recordatorios</li>
					</ul>
				</article>
				<form class="card form" method="POST" onsubmit={handleLogin}>
					<h2>Regístrate</h2>
					<!-- <p class="no-margin" style="color: red">* (Requerido)</p> -->

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
						/>
					{/each}
					<button class="btn primary mt" type="submit" disabled={loading}>
						{#if loading}
							Creando cuenta…
						{:else}
							Crear cuenta
						{/if}
					</button>
					{#if error}
						<p id="fb-error" class="feedback error">{error}</p>
					{/if}
					{#if success}
						<p id="fb-success" class="feedback success">
							¡Cuenta creada! Preparando tu experiencia…
						</p>
					{/if}
					<p class="login-link">¿Ya tienes cuenta? <a href="/login">Inicia sesión</a></p>
				</form>
			</div>
		</section>
	</main>
{:else}
	<div class="flex-center" style="height: calc(100vh - 75px);">
		<RotatingNutriplan />
	</div>
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

	.signup-page {
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
		align-items: start;
		margin-top: 2rem;
	}

	.copy {
		display: flex;
		flex-direction: column;
		gap: 1.3rem;
	}

	.copy h1 {
		margin: 0;
		font-size: clamp(2.2rem, 3vw, 3.2rem);
	}

	.copy p {
		margin: 0;
		color: var(--color-soft);
		line-height: 1.7;
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
		gap: 1.1rem;
	}

	.form h2 {
		margin: 0;
	}

	.form input {
		width: 100%;
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

	.login-link {
		margin: 0;
		font-size: 0.95rem;
		color: var(--color-soft);
	}

	.login-link a {
		font-weight: 600;
		color: var(--color-forest);
		text-decoration: none;
	}

	@media (max-width: 640px) {
		.form {
			padding: 2rem;
		}
	}
</style>
