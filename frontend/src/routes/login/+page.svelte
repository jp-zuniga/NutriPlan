<script>
	import { onMount } from 'svelte';
	import { get } from 'svelte/store';
	import { goto } from '$app/navigation';
	import Banner from '$lib/components/Banner.svelte';
	import { mockLogin, authUser } from '$lib/stores/auth';

	const highlights = [
		'Accede a tus planes y recetas guardadas',
		'Recibe recomendaciones de IA adaptadas a tu progreso',
		'Comparte tu evolución con tu nutricionista'
	];

	let loading = false;
	let error = '';
	let showSuccess = false;
	let form = {
		email: '',
		password: ''
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
		showSuccess = false;
		loading = true;

		try {
			await mockLogin(form);
			showSuccess = true;
			setTimeout(() => goto('/'), 900);
		} catch (err) {
			error = err.message ?? 'No se pudo iniciar sesión.';
		} finally {
			loading = false;
		}
	};

</script>

<Banner />

<main class="login">
	<section class="hero">
		<div class="container hero-grid">
			<article class="copy">
				<h1>Inicia sesión en NutriPlan</h1>
				<p>
					Retoma tus planes personalizados, sincroniza tus recetas favoritas y continúa tu camino hacia un
					bienestar con sabor nicaragüense.
				</p>
				<ul>
					{#each highlights as item}
						<li>{item}</li>
					{/each}
				</ul>
			</article>
			<form class="card form" on:submit={handleSubmit}>
				<h2>Bienvenido de vuelta</h2>
				<label for="email">Correo electrónico</label>
				<input
					id="email"
					type="email"
					placeholder="tu@correo.com"
					required
					bind:value={form.email}
				/>
				<label for="password">Contraseña</label>
				<input
					id="password"
					type="password"
					placeholder="••••••••"
					required
					bind:value={form.password}
				/>
				<div class="form-row">
					<label class="remember">
						<input type="checkbox" /> Recuérdame
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
				{#if error}
					<p class="feedback error">{error}</p>
				{/if}
				{#if showSuccess}
					<p class="feedback success">¡Bienvenido! Redirigiendo…</p>
				{/if}
				<p class="signup">
					¿Aún no tienes cuenta? <a href="/signup">Regístrate aquí</a>
				</p>
			</form>
		</div>
	</section>
</main>

<style>
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
