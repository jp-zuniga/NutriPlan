<script>
	import { authUser, logout } from '$lib/stores/auth';

	const navLinks = [
		{ text: 'Inicio', href: '/' },
		{ text: 'Recetas', href: '/recetas' },
		{ text: 'Planes', href: '/planes' },
		{ text: 'Receta rápida', href: '/receta-rapida' },
		{ text: 'Chef IA', href: '/chef-ia' },
		{ text: 'Comunidad', href: '/perfil' }
	];

	let menuOpen = false;

	const toggleMenu = () => {
		menuOpen = !menuOpen;
	};

	const closeMenu = () => {
		menuOpen = false;
	};

	const handleLogout = () => {
		logout();
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

<nav class="site-nav" data-open={menuOpen}>
	<div class="nav-inner">
		<a class="brand" href="/" on:click={closeMenu}>
			<img src="/assets/images/NutriPlan.png" alt="NutriPlan logo" />
			<div class="brand-copy">
				<span class="title">NutriPlan</span>
				<span class="subtitle">Come mejor, vive mejor</span>
			</div>
		</a>
		<button class="menu-toggle" type="button" on:click={toggleMenu} aria-expanded={menuOpen}>
			<span></span>
			<span></span>
			<span></span>
		</button>
		<div class="nav-links" class:open={menuOpen}>
			{#each navLinks as link}
				<a href={link.href} on:click={closeMenu}>{link.text}</a>
			{/each}
		</div>
		<div class="nav-cta">
			{#if $authUser}
				<div class="user-pill">
					<span class="avatar">{initials($authUser.name || $authUser.email)}</span>
					<div class="user-info">
						<strong>{$authUser.name ?? 'Usuario NutriPlan'}</strong>
						<span>{$authUser.email}</span>
					</div>
					<button type="button" on:click={handleLogout}>Salir</button>
				</div>
			{:else}
				<a class="ghost" href="/login">Ingresar</a>
				<a class="primary" href="/signup">Regístrate</a>
			{/if}
		</div>
	</div>
</nav>

<style>
	.site-nav {
		position: sticky;
		top: 0;
		z-index: 100;
		backdrop-filter: blur(16px);
		background: rgba(255, 255, 255, 0.82);
		border-bottom: 1px solid rgba(8, 44, 36, 0.08);
	}

	.nav-inner {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0.75rem 1.5rem;
		display: flex;
		align-items: center;
		gap: 1.5rem;
	}

	.brand {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		text-decoration: none;
		color: inherit;
	}

	.brand img {
		height: 48px;
		width: 48px;
		object-fit: contain;
	}

	.brand-copy {
		display: flex;
		flex-direction: column;
		line-height: 1.1;
	}

	.brand-copy .title {
		font-family: var(--font-display, 'Alegreya Sans', sans-serif);
		font-weight: 700;
		font-size: 1.2rem;
		color: var(--color-forest, #05463a);
	}

	.brand-copy .subtitle {
		font-size: 0.8rem;
		color: var(--color-soft, #587a6a);
	}

	.menu-toggle {
		background: none;
		border: none;
		padding: 0;
		width: 42px;
		height: 42px;
		display: none;
		flex-direction: column;
		justify-content: center;
		gap: 6px;
		cursor: pointer;
	}

	.menu-toggle span {
		display: block;
		height: 3px;
		width: 100%;
		background: var(--color-forest, #05463a);
		border-radius: 999px;
		transition: transform 0.3s ease, opacity 0.3s ease;
	}

	.site-nav[data-open='true'] .menu-toggle span:nth-child(1) {
		transform: translateY(9px) rotate(45deg);
	}

	.site-nav[data-open='true'] .menu-toggle span:nth-child(2) {
		opacity: 0;
	}

	.site-nav[data-open='true'] .menu-toggle span:nth-child(3) {
		transform: translateY(-9px) rotate(-45deg);
	}

	.nav-links {
		display: flex;
		gap: 1.5rem;
		align-items: center;
	}

	.nav-links a {
		text-decoration: none;
		font-weight: 600;
		color: var(--color-soft, #587a6a);
		font-size: 0.98rem;
		transition: color 0.2s ease, transform 0.2s ease;
	}

	.nav-links a:hover {
		color: var(--color-forest, #05463a);
		transform: translateY(-2px);
	}

	.nav-cta {
		margin-left: auto;
		display: flex;
		align-items: center;
		gap: 0.9rem;
	}

	.nav-cta a {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: 0.55rem 1.2rem;
		border-radius: 999px;
		text-decoration: none;
		font-weight: 600;
		font-size: 0.95rem;
		transition: transform 0.2s ease, box-shadow 0.2s ease;
	}

	.nav-cta .ghost {
		background: rgba(8, 44, 36, 0.05);
		color: var(--color-forest, #05463a);
	}

	.nav-cta .ghost:hover {
		transform: translateY(-2px);
	}

	.nav-cta .primary {
		background: var(--gradient-leaf, linear-gradient(135deg, #0fb872 0%, #53d5a5 100%));
		color: white;
		box-shadow: 0 12px 24px rgba(15, 184, 114, 0.28);
	}

	.nav-cta .primary:hover {
		transform: translateY(-2px);
		box-shadow: 0 18px 28px rgba(15, 184, 114, 0.32);
	}

	.user-pill {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		background: rgba(255, 255, 255, 0.9);
		border-radius: 999px;
		padding: 0.4rem 0.8rem 0.4rem 0.4rem;
		box-shadow: 0 12px 24px rgba(8, 44, 36, 0.12);
	}

	.avatar {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 36px;
		height: 36px;
		border-radius: 50%;
		background: var(--gradient-mint);
		color: white;
		font-weight: 700;
	}

	.user-info {
		display: flex;
		flex-direction: column;
		line-height: 1.1;
	}

	.user-info strong {
		font-size: 0.95rem;
	}

	.user-info span {
		color: var(--color-soft);
		font-size: 0.8rem;
	}

	.user-pill button {
		border: none;
		background: rgba(8, 44, 36, 0.08);
		color: var(--color-forest);
		padding: 0.3rem 0.8rem;
		border-radius: 999px;
		font-weight: 600;
		cursor: pointer;
		transition: transform 0.2s ease;
	}

	.user-pill button:hover {
		transform: translateY(-1px);
	}

	@media (max-width: 960px) {
		.nav-inner {
			padding: 0.75rem 1rem;
		}

		.nav-links {
			position: absolute;
			top: 100%;
			left: 0;
			right: 0;
			background: rgba(255, 255, 255, 0.95);
			flex-direction: column;
			padding: 1.5rem;
			gap: 1rem;
			border-bottom: 1px solid rgba(8, 44, 36, 0.08);
			opacity: 0;
			pointer-events: none;
			transform: translateY(-10px);
			transition: opacity 0.25s ease, transform 0.25s ease;
		}

		.nav-links.open {
			opacity: 1;
			pointer-events: auto;
			transform: translateY(0);
		}

		.nav-cta {
			gap: 0.6rem;
		}

		.menu-toggle {
			display: inline-flex;
			margin-left: auto;
		}
	}

	@media (max-width: 640px) {
		.user-pill {
			padding: 0.4rem 0.6rem 0.4rem 0.4rem;
		}

		.user-pill button {
			padding: 0.3rem 0.65rem;
		}
	}
</style>
