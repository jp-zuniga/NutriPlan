<script>
	import LogoFavicon from '$lib/assets/favicon.svg';
</script>

<footer class="site-footer bg-white">
	<div class="container pad-50">
		<div class="footer-content regrid-cols-4 gap-32">
			<!-- Brand Section -->
			<div class="footer-brand animate-fade-in-up">
				<div class="brand flex items-center gap-4 mb">
					<img src={LogoFavicon} alt="NutriPlan logo" />
					<div class="flex direction-col">
						<span class="title md-p bold" style="font-family: 'Montserrat'">NUTRIPLAN</span>
						<span class="subtitle sm-p p-ghost" style="font-family: 'Montserrat'; font-size:10px"
							>COME MEJOR, VIVE MEJOR</span
						>
					</div>
				</div>
				<p class="md-p p-ghost mb">
					Tu plataforma para planear comidas nutritivas con el sabor auténtico de Nicaragua. Recetas
					tradicionales adaptadas para una vida saludable.
				</p>
				<div class="social-links flex gap-16">
					<a
						href="javascript:void(0)"
						class="social-link flex-center round-10 hover-lift"
						style="width: 40px; height: 40px; background: var(--color-soft-gray);"
						aria-label="Síguenos en Facebook"
					>
						<i class="lab la-facebook-f text-col-1"></i>
					</a>
					<a
						href="javascript:void(0)"
						class="social-link flex-center round-10 hover-lift"
						style="width: 40px; height: 40px; background: var(--color-soft-gray);"
						aria-label="Síguenos en Instagram"
					>
						<i class="lab la-instagram text-col-1"></i>
					</a>
					<a
						href="javascript:void(0)"
						class="social-link flex-center round-10 hover-lift"
						style="width: 40px; height: 40px; background: var(--color-soft-gray);"
						aria-label="Síguenos en Twitter"
					>
						<i class="lab la-twitter text-col-1"></i>
					</a>
					<a
						href="javascript:void(0)"
						class="social-link flex-center round-10 hover-lift"
						style="width: 40px; height: 40px; background: var(--color-soft-gray);"
						aria-label="Síguenos en YouTube"
					>
						<i class="lab la-youtube text-col-1"></i>
					</a>
				</div>
			</div>

			<!-- Quick Links -->
			<div class="footer-links animate-fade-in-up animate-delay-1">
				<h3 class="h3 bold mb">Enlaces Rápidos</h3>
				<ul class="link-list">
					<li><a href="/" class="md-p p-ghost no-ul hover-lift">Inicio</a></li>
					<li><a href="/recetas" class="md-p p-ghost no-ul hover-lift">Recetas</a></li>
					<li><a href="/planes" class="md-p p-ghost no-ul hover-lift">Planes Nutricionales</a></li>
					<li><a href="/receta-rapida" class="md-p p-ghost no-ul hover-lift">Receta Rápida</a></li>
					<li><a href="/chef-ia" class="md-p p-ghost no-ul hover-lift">Chef IA</a></li>
				</ul>
			</div>

			<!-- Community -->
			<div class="footer-community animate-fade-in-up animate-delay-2">
				<h3 class="h3 bold mb">Comunidad</h3>
				<ul class="link-list">
					<li><a href="/perfil" class="md-p p-ghost no-ul hover-lift">Mi Perfil</a></li>
					<li>
						<a href="javascript:void(0)" class="md-p p-ghost no-ul hover-lift">Recetas Favoritas</a>
					</li>
					<li>
						<a href="javascript:void(0)" class="md-p p-ghost no-ul hover-lift">Compartir Receta</a>
					</li>
					<li>
						<a href="javascript:void(0)" class="md-p p-ghost no-ul hover-lift">Foro de Usuarios</a>
					</li>
					<li><a href="javascript:void(0)" class="md-p p-ghost no-ul hover-lift">Eventos</a></li>
				</ul>
			</div>

			<!-- Support -->
			<div class="footer-support animate-fade-in-up animate-delay-3">
				<h3 class="h3 bold mb">Soporte</h3>
				<ul class="link-list">
					<li><a href="/acerca" class="md-p p-ghost no-ul hover-lift">Acerca de Nosotros</a></li>
					<li>
						<a href="javascript:void(0)" class="md-p p-ghost no-ul hover-lift">Centro de Ayuda</a>
					</li>
					<li><a href="javascript:void(0)" class="md-p p-ghost no-ul hover-lift">Contacto</a></li>
					<li>
						<a href="javascript:void(0)" class="md-p p-ghost no-ul hover-lift">Términos de Uso</a>
					</li>
					<li>
						<a href="javascript:void(0)" class="md-p p-ghost no-ul hover-lift"
							>Política de Privacidad</a
						>
					</li>
				</ul>
			</div>
		</div>

		<!-- Footer Bottom -->
		<div
			class="footer-bottom flex justify-between items-center mt-l pt-20 border-top animate-fade-in-up animate-delay-4"
		>
			<p class="md-p p-ghost">© 2024 NutriPlan. Todos los derechos reservados.</p>
			<p class="md-p p-ghost">
				Hecho con <i class="las la-heart p-emphasis"></i> en Nicaragua
			</p>
		</div>
	</div>
</footer>

<style>
	.site-footer {
		border-top: 1px solid var(--color-soft-gray);
		background: var(--color-soft-white);
	}

	.footer-content {
		margin-bottom: 40px;
	}

	.brand img {
		width: 40px;
		height: 40px;
	}

	.link-list {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.link-list li {
		margin-bottom: 12px;
	}

	.link-list a {
		transition:
			color 0.2s ease,
			transform 0.2s ease;
	}

	.link-list a:hover {
		color: var(--color-primary-dark);
		transform: translateX(5px);
	}

	.social-link {
		transition:
			background 0.2s ease,
			transform 0.2s ease;
	}

	.social-link:hover {
		background: var(--color-primary-dark) !important;
		transform: translateY(-2px);
	}

	.social-link:hover i {
		color: white !important;
	}

	.border-top {
		border-top: 1px solid var(--color-soft-gray);
	}

	@media (max-width: 768px) {
		.footer-content {
			grid-template-columns: 1fr;
			gap: 24px;
		}

		.footer-bottom {
			flex-direction: column;
			gap: 16px;
			text-align: center;
		}
	}
</style>
