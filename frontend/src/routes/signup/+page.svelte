<script>
	import { onMount } from 'svelte';
	import { get } from 'svelte/store';
	import { goto } from '$app/navigation';
	import Banner from '$lib/components/Banner.svelte';
	import { mockSignUp, authUser } from '$lib/stores/auth';

	let loading = false;
	let error = '';
	let success = false;
	let form = {
		name: '',
		email: '',
		phone: '',
		password: '',
		confirm: ''
	};

	onMount(() => {
		const user = get(authUser);
		if (user) {
			goto('/');
		}
	});

	const handleSubmit = async (event) => {
		event.preventDefault();
		error = '';
		success = false;

		if (form.password !== form.confirm) {
			error = 'Las contraseñas no coinciden.';
			return;
		}

		loading = true;
		try {
			await mockSignUp({
				name: form.name,
				email: form.email,
				password: form.password,
				phone: form.phone
			});
			success = true;
			setTimeout(() => goto('/'), 1000);
		} catch (err) {
			error = err.message ?? 'No pudimos crear tu cuenta.';
		} finally {
			loading = false;
		}
	};

</script>

<Banner />

<main class="signup-page">
	<section class="hero">
		<div class="container hero-grid">
			<article class="copy">
				<h1>Crea tu cuenta NutriPlan</h1>
				<p>
					Personaliza tu experiencia, guarda recetas favoritas y deja que Chef Nutri IA construya tu plan
					a partir de tu historia y cultura alimentaria.
				</p>
				<ul>
					<li>✨ Planes ajustados a tu presupuesto y tiempo</li>
					<li>🍲 Recetas con ingredientes nicaragüenses</li>
					<li>📈 Seguimiento de metas y recordatorios</li>
				</ul>
			</article>
			<form class="card form" on:submit={handleSubmit}>
				<h2>Regístrate</h2>
				<label for="name">Nombre completo</label>
				<input id="name" type="text" placeholder="Ej. María Fernanda" required bind:value={form.name} />
				<label for="email">Correo electrónico</label>
				<input id="email" type="email" placeholder="tu@correo.com" required bind:value={form.email} />
				<label for="phone">Número de contacto (opcional)</label>
				<input id="phone" type="tel" placeholder="+505" bind:value={form.phone} />
				<label for="password">Contraseña</label>
				<input id="password" type="password" placeholder="Mínimo 8 caracteres" required bind:value={form.password} />
				<label for="confirm">Confirmar contraseña</label>
				<input id="confirm" type="password" required bind:value={form.confirm} />
				<button class="btn primary" type="submit" disabled={loading}>
					{#if loading}
						Creando cuenta…
					{:else}
						Crear cuenta
					{/if}
				</button>
				{#if error}
					<p class="feedback error">{error}</p>
				{/if}
				{#if success}
					<p class="feedback success">¡Cuenta creada! Preparando tu experiencia…</p>
				{/if}
				<p class="login-link">¿Ya tienes cuenta? <a href="/login">Inicia sesión</a></p>
			</form>
		</div>
	</section>
</main>

<style>
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
