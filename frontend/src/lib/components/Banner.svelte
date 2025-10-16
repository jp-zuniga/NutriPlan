<script>
	import { authUser } from '$lib/stores/auth';
	import LogoFavicon from '$lib/assets/favicon.svg';
	import { goto } from '$app/navigation';
	import RotatingNutriplan from './RotatingNutriplan.svelte';

	let navLinks = $state([
		{ text: 'Inicio', href: '/' },
		{ text: 'Recetas', href: '/recetas' },
		{ text: 'Planes', href: '/planes' },
		{ text: 'Receta rápida', href: '/receta-rapida' },
		{ text: 'Chef IA', href: '/chef-ia' },
		{ text: 'Perfil', href: ($authUser !== undefined && $authUser !== null) ? '/perfil' : '/login' }
	]);

	let menuOpen = $state(false);

	const toggleMenu = () => {
		menuOpen = !menuOpen;
	};

	const closeMenu = () => {
		menuOpen = false;
	};

	const handleLogout = () => {
		goto('/api/logout/');
		closeMenu();
	};

	function initials(name = '') {
		return name
			.trim()
			.split(' ')
			.filter(Boolean)
			.map((part) => part[0])
			.slice(0, 2)
			.join('')
			.toUpperCase();
	}
</script>

<nav class="site-nav flex-center bg-white">
	<div class="nav-inner flex items-center justify-between rel-pos">
		<!-- Brand logo -->
		<a href="/" class="brand flex items-center no-ul gap-8" onclick={closeMenu}>
			<img src={LogoFavicon} alt="NutriPlan logo" />
			<div class="flex direction-col">
				<span class="title md-p bold">NutriPlan</span>
				<span class="subtitle sm-p p-ghost">Come mejor, vive mejor</span>
			</div>
		</a>

		<!-- Normal navbar -->
		<div class="nav-links flex-center gap-32 high-res">
			{#each navLinks as link}
				<a href={link.href} class="nav-link no-ul md-p"><span>{link.text}</span></a>
			{/each}
		</div>

		<!-- Sign in -->
		<div class="sign-in flex-center gap-16 high-res">
			{#if $authUser !== undefined && $authUser !== null}
				<div class="user-pill flex-center gap-16 pill pad-10 bg-white b-shadow">
					<span class="avatar full-round text-col-white flex-center"
						>{initials($authUser.first_name || $authUser.email)}</span
					>
					<div class="user-info flex direction-col">
						<p class="md-p bold no-margin">{$authUser.first_name} {$authUser.last_name}</p>
						<p class="md-p p-ghost no-margin">{$authUser.email}</p>
					</div>
					<button class="btn ghost" onclick={handleLogout}>Salir</button>
				</div>
			{:else if $authUser === null}
				<a href="/login" class="btn ghost">Ingresar</a>
				<a href="/signup" class="btn primary">Regístrate</a>
			{/if}
		</div>

		<!-- Toolbar -->
		<button
			type="button"
			class="low-res toolbar flex direction-col justify-between no-border no-pad"
			data-open={menuOpen}
			onclick={toggleMenu}
			aria-label="Toggle menu"
		>
			<span></span>
			<span></span>
			<span></span>
		</button>
	</div>

	<!-- Menu -->
	<div
		class="menu flex-center direction-col abs-pos low-res full-width soft-outline"
		data-open={menuOpen}
	>
		{#each navLinks as link}
			<a
				href={link.href}
				class="nav-link no-ul md-p full-width txt-center pad-10"
				onclick={closeMenu}><span>{link.text}</span></a
			>
		{/each}
	</div>
</nav>

<style>
	:root {
		--navbar-height: 75px;
	}

	.nav-inner {
		width: 90%;
	}

	.site-nav {
		position: sticky;
		top: 0;
		height: var(--navbar-height);
		z-index: 100;
		backdrop-filter: blur(16px);
		background: rgba(255, 255, 255, 0.82);
		border-bottom: 1px solid rgba(8, 44, 36, 0.08);
		box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
	}

	.sign-in {
		width: 300px;
	}

	.brand {
		width: 190px;
	}

	.brand img {
		width: 48px;
		height: 48px;
	}

	.user-pill .avatar {
		background: #73946b;
		background: linear-gradient(138deg, rgba(115, 148, 107, 1) 0%, rgba(3, 167, 145, 1) 50%);

		width: 40px;
		height: 40px;
	}

	.user-pill button {
		border-radius: 999px;
		padding: 10px;
	}

	.user-info p {
		margin: -4px 0px;
	}

	.nav-link,
	.nav-link span {
		transition: 0.2s ease;
	}

	.nav-link:hover span {
		transform: translateY(-3px);
		font-weight: bold;
	}

	.toolbar {
		width: 40px;
		height: 30px;

		cursor: pointer;
		background: none;
	}

	.toolbar span {
		width: 100%;
		border: 1px solid rgba(0, 0, 0, 0.5);
		transition: 0.2s ease;
	}

	.toolbar[data-open='true'] span:nth-child(1) {
		transform: translateY(14px) rotate(45deg);
	}

	.toolbar[data-open='true'] span:nth-child(2) {
		opacity: 0;
	}

	.toolbar[data-open='true'] span:nth-child(3) {
		transform: translateY(-14px) rotate(-45deg);
	}

	.menu {
		top: var(--navbar-height);
		background: white;
		display: none;
		opacity: 0%;
		transform: translateY(-10px);
		transition: 0.2s ease;
	}

	.menu[data-open='true'] {
		display: flex;
		opacity: 90%;
		transform: translateY(0px);
	}

	.menu a:hover {
		background: rgba(0, 0, 0, 0.1);
	}

	@media (max-width: 1200px) {
		.high-res {
			display: none;
		}
	}

	@media (min-width: 1200px) {
		.low-res {
			display: none;
		}
	}

	/* .user-pill button:hover {
		background: rgb(240, 240, 240);
	} */
</style>
