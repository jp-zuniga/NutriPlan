<script>
	import Banner from '$lib/components/Banner.svelte';
	import Footer from '$lib/components/Footer.svelte';
	import { authUser } from '$lib/stores/auth';

	import ImagenVigoron from '$lib/assets/vigoron.jpg';
	import PlatosTipicos from '$lib/assets/platos-tipicos.jpeg';
	import GalloPinto from '$lib/assets/gallo-pinto.jpg';
	import SVG_AI from '$lib/assets/ai.svg';
	import SVG_STAR from '$lib/assets/star.svg';

	import icon_SoupBowl from '$lib/assets/soup-bowl.svg';
	import icon_Calendar from '$lib/assets/calendar.svg';
	import icon_RabbitFast from '$lib/assets/rabbit-fast.svg';
	import RecipeCard from '$lib/components/RecipeCard.svelte';
	import RotatingNutriplan from '$lib/components/RotatingNutriplan.svelte';
	import { API_RECIPES_ENDPOINT } from '$lib/endpoints';

	let recipe_loading = $state(true);
	let recipeResults = $state([]);
	const resolveResults = async (page) => {
		recipe_loading = true;

		recipeResults = [];

		const response = await fetch(API_RECIPES_ENDPOINT, {
			method: 'GET'
		});

		if (response.ok) {
			const data = await response.json();
			console.log(data);
			recipeResults = data.slice(0, 4);
			recipe_loading = false;
			return;
		}

		recipeResults = null;

		recipe_loading = false;
	};

	let results = $state(null);
	resolveResults();

	const categories = [
		{
			title: 'Desayuno',
			icon: '<i class="las la-coffee"></i>',
			gradient: '#A9C46C',
			background_color: 'rgba(164,180,101,0.1)'
		},
		{
			title: 'Almuerzo',
			icon: '<i class="las la-drumstick-bite"></i>',
			gradient: 'rgb(169, 74, 74)',
			background_color: 'rgba(169, 74, 74, 0.1)'
		},
		{
			title: 'Cena',
			icon: '<i class="las la-utensils"></i>',
			gradient: 'rgb(106, 156, 137)',
			background_color: 'rgba(106, 156, 137, 0.1)'
		},
		{
			title: 'Postres',
			icon: '<i class="las la-cookie"></i>',
			gradient: 'rgb(185, 148, 112)',
			background_color: 'rgba(185, 148, 112, 0.1)'
		}
	];

	const quickActions = [
		{
			title: 'Recetas',
			description:
				'Explora platos típicos, saludables y fusiones creativas para cada momento del día.',
			cta: 'Ver recetas',
			cta_link: '/recetas',
			accent: 'leaf',
			background: 'rgb(119, 178, 84)',
			icon: icon_SoupBowl
		},
		{
			title: 'Planes Nutricionales',
			description:
				'Genera un plan semanal que respete tus metas, tu actividad física y tus preferencias.',
			cta: 'Crear plan',
			cta_link: '/planes',
			accent: 'mint',
			background: 'rgb(133, 169, 143)',
			icon: icon_Calendar
		},
		{
			title: 'Receta Rápida',
			description:
				'Escribe lo que tienes en casa y deja que nuestra IA sugiera la mejor coincidencia.',
			cta: 'Receta rápida',
			cta_link: '/receta-rapida',
			accent: 'sunrise',
			background: 'rgb(202, 115, 115)',
			icon: icon_RabbitFast
		}
	];

	const featuredRecipes = [
		{
			title: 'Vigorón ligero',
			origin: 'Granada',
			kcal: '430 kcal',
			time: '35 min',
			rating: 4.8,
			tags: ['Popular', 'Alto en fibra'],
			image: ImagenVigoron
		},
		{
			title: 'Gallo Pinto energizante',
			origin: 'Managua',
			kcal: '380 kcal',
			time: '25 min',
			rating: 4.9,
			tags: ['Vegetariano', 'Desayuno'],
			image: GalloPinto
		},
		{
			title: 'Sopa de queso liviana',
			origin: 'Chontales',
			kcal: '320 kcal',
			time: '40 min',
			rating: 4.7,
			tags: ['Sin gluten', 'Reconfortante'],
			image: PlatosTipicos
		},
		{
			title: 'Ensalada de chayote verde',
			origin: 'Masaya',
			kcal: '280 kcal',
			time: '20 min',
			rating: 4.6,
			tags: ['Baja en carbohidratos', 'Refrescante'],
			image: 'https://tipsparatuviaje.com/wp-content/uploads/2020/01/carne-en-vaho-2.jpg'
		}
	];

	const planBenefits = [
		{
			title: 'Plan semanal inteligente',
			description: 'La IA equilibra calorías, macros y tradición culinaria nica en un solo vistazo.'
		},
		{
			title: 'Sustituciones al instante',
			description: 'Intercambia recetas según ingredientes disponibles y mantén tus metas al día.'
		},
		{
			title: 'Seguimiento práctico',
			description: 'Visualiza el aporte nutricional diario y exporta tu plan para compartirlo.'
		}
	];

	const weeklyPreview = [
		{
			day: 'Lunes',
			breakfast: 'Gallo pinto integral + jugo verde',
			lunch: 'Vigorón al horno con yuca cocida',
			dinner: 'Filete de pescado criollo + ensalada cítrica'
		},
		{
			day: 'Miércoles',
			breakfast: 'Tortillas de maíz con queso fresco',
			lunch: 'Sopa de queso liviana',
			dinner: 'Pollo a la plancha con chayote salteado'
		},
		{
			day: 'Viernes',
			breakfast: 'Avena con banano caramelizado',
			lunch: 'Ensalada de chayote verde',
			dinner: 'Tacos de cerdo magro con repollo'
		}
	];

	const pantryIngredients = ['Yuca', 'Repollo', 'Limón', 'Chicharrón al horno', 'Tomate cherry'];

	const pantryMatches = [
		{
			title: 'Vigorón exprés',
			match: 86,
			missing: ['Vinagre de caña'],
			highlight: 'Listo en 20 minutos'
		},
		{
			title: 'Ensalada fresca de repollo',
			match: 72,
			missing: ['Semillas de sésamo'],
			highlight: 'Ideal para acompañar almuerzos'
		}
	];

	const communityHighlights = [
		{
			title: 'Favoritos compartidos',
			description: 'Guarda tus recetas top y descubre lo que otros nicas están cocinando.'
		},
		{
			title: 'Comentarios con propósito',
			description: 'Aprende tips de preparación y variaciones saludables de la comunidad.'
		},
		{
			title: 'Valoraciones confiables',
			description: 'Conoce el nivel de dificultad, tiempo real y calificaciones honestas.'
		}
	];

	const firstName = (name = '') => name.trim().split(' ')[0] || 'NutriChef';
</script>

<div class="home flex direction-col items-center no-overflow">
	<section
		id="hero"
		class="bg-cream flex justify-center gradient-animation"
		style="background: linear-gradient(135deg, #C0C78C 0%, #A9C46C 50%, #798645 100%);"
	>
		<div class="container regrid-cols-2 pad-20">
			<div class="content pad-20 bg-white hover-lift animate-fade-in-left">
				<h1 class="h1 mb">
					Descubre la cocina
					<span class="p-emphasis">nicaragüense</span>
				</h1>
				<p class="lg-p mb-l p-ghost">
					Tu plataforma para planear comidas nutritivas con el sabor de casa. Recibe recomendaciones
					personalizadas, recetas auténticas y acompañamiento inteligente en cada etapa.
				</p>
				<div class="button-group flex gap-24">
					<a class="btn primary hover-glow animate-scale-in animate-delay-1" href="/planes"
						>Crear mi plan nutricional</a
					>
					<a class="btn ghost hover-scale animate-scale-in animate-delay-2" href="/recetas"
						>Explorar recetas</a
					>
				</div>
			</div>

			<div class="img-container img-fluid round-20 rel-pos animate-fade-in-right animate-delay-1">
				<img class="hover-scale" src={ImagenVigoron} alt="vigoron" />
				<div
					class="card abs-pos pad-10 hover-lift animate-slide-in-up animate-delay-2"
					style="left: 15px; bottom: 15px; width: calc(100% - 30px)"
				>
					<p class="bold">Vigorón Saludable</p>
					<p>Yuca al vapor, chicharrón al horno y repollo cítrico.</p>
					<div class="flex justify-between">
						<div class="info flex sm-p gap-8 p-ghost">
							<p>420 kcal</p>
							<p>35 min</p>
						</div>
						<div class="stars">
							<i class="las la-star p-emphasis no-ul"></i>
							4.9
						</div>
					</div>
				</div>
			</div>
		</div>
	</section>

	<section id="star-recipes" class="bg-soft-gray">
		<div class="container flex-center direction-col pad-50 gap-16">
			<div class="flex-center direction-col animate-fade-in-up">
				<p class="h2 bold">Recetas Destacadas</p>
				<p class="p-ghost">Las favoritas de nuestra comunidad</p>
			</div>
			<div
				class="flex gap-16 ov-auto-x pad-10 limit-width no-shrink animate-fade-in-up animate-delay-1"
			>
				{#if !recipe_loading}
					{#each recipeResults as recipe, index}
						<div class="animate-fade-in-up" style="animation-delay: {(index + 2) * 0.1}s;">
							<RecipeCard {recipe} />
						</div>
					{/each}
				{:else}
					<div class="full-size flex-center">
						<RotatingNutriplan />
					</div>
				{/if}
			</div>
		</div>
	</section>

	<section id="why-us" style="background-color: #798645;">
		<div class="container flex-center">
			<p class="h1 text-col-white bold pad-20 txt-center animate-fade-in-down">
				¿Por qué elegir NutriPlan?
			</p>
		</div>
	</section>

	<section id="benefits" class="bg-white">
		<div class="container flex-center direction-col pad-50">
			<div class="flex-center direction-col mb-l animate-fade-in-up">
				<h2 class="h2 bold mb">Beneficios únicos de NutriPlan</h2>
				<p class="lg-p p-ghost txt-center">
					Descubre lo que nos hace diferentes en el mundo de la nutrición nicaragüense
				</p>
			</div>

			<div class="content flex-center wrap gap-24">
				<div
					class="benefit-card pad-20 round-15 bg-soft-gray hover-lift animate-fade-in-up animate-delay-1"
					style="width: 300px; min-height: 200px;"
				>
					<div
						class="benefit-icon flex-center round-10 mb"
						style="width: 60px; height: 60px; background: var(--gradient-leaf);"
					>
						<i class="las la-brain text-col-white" style="font-size: 24px;"></i>
					</div>
					<h3 class="h3 bold mb">Plan semanal inteligente</h3>
					<p class="md-p p-ghost">
						La IA equilibra calorías, macros y tradición culinaria nica en un solo vistazo.
					</p>
				</div>

				<div
					class="benefit-card pad-20 round-15 bg-soft-gray hover-lift animate-fade-in-up animate-delay-2"
					style="width: 300px; min-height: 200px;"
				>
					<div
						class="benefit-icon flex-center round-10 mb"
						style="width: 60px; height: 60px; background: var(--gradient-mint);"
					>
						<i class="las la-exchange-alt text-col-white" style="font-size: 24px;"></i>
					</div>
					<h3 class="h3 bold mb">Sustituciones al instante</h3>
					<p class="md-p p-ghost">
						Intercambia recetas según ingredientes disponibles y mantén tus metas al día.
					</p>
				</div>

				<div
					class="benefit-card pad-20 round-15 bg-soft-gray hover-lift animate-fade-in-up animate-delay-3"
					style="width: 300px; min-height: 200px;"
				>
					<div
						class="benefit-icon flex-center round-10 mb"
						style="width: 60px; height: 60px; background: var(--gradient-sunrise);"
					>
						<i class="las la-chart-line text-col-white" style="font-size: 24px;"></i>
					</div>
					<h3 class="h3 bold mb">Seguimiento práctico</h3>
					<p class="md-p p-ghost">
						Visualiza el aporte nutricional diario y exporta tu plan para compartirlo.
					</p>
				</div>

				<div
					class="benefit-card pad-20 round-15 bg-soft-gray hover-lift animate-fade-in-up animate-delay-4"
					style="width: 300px; min-height: 200px;"
				>
					<div
						class="benefit-icon flex-center round-10 mb"
						style="width: 60px; height: 60px; background: linear-gradient(135deg, #C86F56 0%, #ff6b6b 100%);"
					>
						<i class="las la-heart text-col-white" style="font-size: 24px;"></i>
					</div>
					<h3 class="h3 bold mb">Recetas auténticas</h3>
					<p class="md-p p-ghost">
						Platos tradicionales nicaragüenses adaptados para una alimentación saludable.
					</p>
				</div>

				<div
					class="benefit-card pad-20 round-15 bg-soft-gray hover-lift animate-fade-in-up animate-delay-5"
					style="width: 300px; min-height: 200px;"
				>
					<div
						class="benefit-icon flex-center round-10 mb"
						style="width: 60px; height: 60px; background: linear-gradient(135deg, #6C9073 0%, #9EBC8A 100%);"
					>
						<i class="las la-users text-col-white" style="font-size: 24px;"></i>
					</div>
					<h3 class="h3 bold mb">Comunidad activa</h3>
					<p class="md-p p-ghost">
						Conecta con otros nicaragüenses que comparten tu pasión por comer bien.
					</p>
				</div>

				<div
					class="benefit-card pad-20 round-15 bg-soft-gray hover-lift animate-fade-in-up animate-delay-5"
					style="width: 300px; min-height: 200px;"
				>
					<div
						class="benefit-icon flex-center round-10 mb"
						style="width: 60px; height: 60px; background: linear-gradient(135deg, #4cd4aa 0%, #68d3ff 100%);"
					>
						<i class="las la-star text-col-white" style="font-size: 24px;"></i>
					</div>
					<h3 class="h3 bold mb">Valoraciones confiables</h3>
					<p class="md-p p-ghost">
						Calificaciones honestas de la comunidad para ayudarte a elegir lo mejor.
					</p>
				</div>
			</div>
		</div>
	</section>

	<section id="all-in-one">
		<div class="container flex-center direction-col pad-50">
			<p class="h3 bold animate-fade-in-up">Todo en un solo lugar</p>
			<p class="mb-l p-ghost md-p animate-fade-in-up animate-delay-1">
				Accede rápido a lo que necesitas: inspiración, planificación o una solución express.
			</p>
			<div class="content flex-center wrap gap-24">
				{#each quickActions as action, index}
					<div
						class="quick-action pad-20 round-5 hover-lift animate-fade-in-up"
						style="width: 300px; height: 200px; background-color: {action.background}; animation-delay: {(index +
							2) *
							0.1}s;"
					>
						<img src={action.icon} alt={action.title} style="width: 50px; height: 50px;" />
						<p class="lg-p bold text-col-white">{action.title}</p>
						<p class="md-p text-col-white mb">{action.description}</p>

						<!-- <a href={action.cta_link} class="no-ul text-col-white">{action.cta}</a> -->
					</div>
				{/each}
			</div>
		</div>
	</section>

	<section id="testimonials" class="bg-soft-gray">
		<div class="container flex-center direction-col pad-50">
			<div class="flex-center direction-col mb-l animate-fade-in-up">
				<h2 class="h2 bold mb">Lo que dicen nuestros usuarios</h2>
				<p class="lg-p p-ghost txt-center">
					Testimonios reales de nicaragüenses que transformaron su alimentación
				</p>
			</div>

			<div class="content flex-center wrap gap-24">
				<div
					class="testimonial-card pad-20 round-15 bg-white hover-lift animate-fade-in-up animate-delay-1"
					style="width: 350px; min-height: 200px;"
				>
					<div class="flex items-center gap-16 mb">
						<div
							class="avatar full-round text-col-white flex-center"
							style="width: 50px; height: 50px; background: var(--gradient-leaf);"
						>
							<span class="bold">MC</span>
						</div>
						<div>
							<p class="bold">María Carmen</p>
							<p class="sm-p p-ghost">Managua</p>
						</div>
						<div class="stars ml-auto">
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
						</div>
					</div>
					<p class="md-p">
						"NutriPlan me ayudó a mantener mis tradiciones culinarias pero de forma más saludable.
						El vigorón que preparo ahora es igual de delicioso pero con menos calorías."
					</p>
				</div>

				<div
					class="testimonial-card pad-20 round-15 bg-white hover-lift animate-fade-in-up animate-delay-2"
					style="width: 350px; min-height: 200px;"
				>
					<div class="flex items-center gap-16 mb">
						<div
							class="avatar full-round text-col-white flex-center"
							style="width: 50px; height: 50px; background: var(--gradient-mint);"
						>
							<span class="bold">CR</span>
						</div>
						<div>
							<p class="bold">Carlos Roberto</p>
							<p class="sm-p p-ghost">Granada</p>
						</div>
						<div class="stars ml-auto">
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
						</div>
					</div>
					<p class="md-p">
						"La función de receta rápida es increíble. Escribo lo que tengo en la cocina y me
						sugiere platos nicas que puedo hacer. ¡Genial para estudiantes!"
					</p>
				</div>

				<div
					class="testimonial-card pad-20 round-15 bg-white hover-lift animate-fade-in-up animate-delay-3"
					style="width: 350px; min-height: 200px;"
				>
					<div class="flex items-center gap-16 mb">
						<div
							class="avatar full-round text-col-white flex-center"
							style="width: 50px; height: 50px; background: var(--gradient-sunrise);"
						>
							<span class="bold">AL</span>
						</div>
						<div>
							<p class="bold">Ana Lucía</p>
							<p class="sm-p p-ghost">León</p>
						</div>
						<div class="stars ml-auto">
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
						</div>
					</div>
					<p class="md-p">
						"Mi plan semanal se adapta perfectamente a mi rutina de ejercicio. La IA entiende mis
						necesidades y me da opciones que realmente puedo seguir."
					</p>
				</div>

				<div
					class="testimonial-card pad-20 round-15 bg-white hover-lift animate-fade-in-up animate-delay-4"
					style="width: 350px; min-height: 200px;"
				>
					<div class="flex items-center gap-16 mb">
						<div
							class="avatar full-round text-col-white flex-center"
							style="width: 50px; height: 50px; background: linear-gradient(135deg, #C86F56 0%, #ff6b6b 100%);"
						>
							<span class="bold">JM</span>
						</div>
						<div>
							<p class="bold">José Manuel</p>
							<p class="sm-p p-ghost">Masaya</p>
						</div>
						<div class="stars ml-auto">
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
						</div>
					</div>
					<p class="md-p">
						"Como chef, aprecio la autenticidad de las recetas. NutriPlan respeta nuestras
						tradiciones pero las hace más nutritivas. ¡Excelente trabajo!"
					</p>
				</div>

				<div
					class="testimonial-card pad-20 round-15 bg-white hover-lift animate-fade-in-up animate-delay-5"
					style="width: 350px; min-height: 200px;"
				>
					<div class="flex items-center gap-16 mb">
						<div
							class="avatar full-round text-col-white flex-center"
							style="width: 50px; height: 50px; background: linear-gradient(135deg, #6C9073 0%, #9EBC8A 100%);"
						>
							<span class="bold">SR</span>
						</div>
						<div>
							<p class="bold">Sofía Raquel</p>
							<p class="sm-p p-ghost">Chontales</p>
						</div>
						<div class="stars ml-auto">
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
						</div>
					</div>
					<p class="md-p">
						"La comunidad es lo mejor. Comparto mis recetas familiares y aprendo de otros. Es como
						tener una cocina nicaragüense virtual."
					</p>
				</div>

				<div
					class="testimonial-card pad-20 round-15 bg-white hover-lift animate-fade-in-up animate-delay-5"
					style="width: 350px; min-height: 200px;"
				>
					<div class="flex items-center gap-16 mb">
						<div
							class="avatar full-round text-col-white flex-center"
							style="width: 50px; height: 50px; background: linear-gradient(135deg, #4cd4aa 0%, #68d3ff 100%);"
						>
							<span class="bold">DR</span>
						</div>
						<div>
							<p class="bold">Diego Rafael</p>
							<p class="sm-p p-ghost">Rivas</p>
						</div>
						<div class="stars ml-auto">
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
							<i class="las la-star p-emphasis"></i>
						</div>
					</div>
					<p class="md-p">
						"Perdí 15 libras en 3 meses siguiendo los planes de NutriPlan. Lo mejor es que nunca me
						aburrí porque siempre hay variedad de platos nicas."
					</p>
				</div>
			</div>
		</div>
	</section>

	<!-- <section id="categories" style="background-color: #FAF1E6">
		<div class="container flex-center direction-col pad-50">
			<p class="mb-l h3">Explora por categorias</p>
			<div class="content flex wrap gap-16 justify-center items-center" id="category-roulette">
				{#each categories as category}
					<div
						class="category flex-center direction-col round-10"
						style="background-color: {category.background_color};"
					>
						<div
							class="icon flex-center round-5 b-shadow"
							style="background: {category.gradient}; color: white;"
						>
							{@html category.icon}
						</div>
						<p class="mt-s">{category.title}</p>
					</div>
				{/each}
			</div>
		</div>
	</section> -->

	<section id="metrics" class="bg-white">
		<div class="container flex-center direction-col pad-50">
			<div class="flex-center direction-col mb-l animate-fade-in-up">
				<h2 class="h2 bold mb">NutriPlan en números</h2>
				<p class="lg-p p-ghost txt-center">Los resultados hablan por sí solos</p>
			</div>

			<div class="content flex-center wrap gap-32">
				<div
					class="metric-card pad-20 round-15 bg-soft-gray hover-lift animate-fade-in-up animate-delay-1"
					style="width: 200px; min-height: 150px;"
				>
					<div
						class="metric-icon flex-center round-10 mb"
						style="width: 60px; height: 60px; background: var(--gradient-leaf); margin: 0 auto;"
					>
						<i class="las la-utensils text-col-white" style="font-size: 24px;"></i>
					</div>
					<h3 class="h1 bold txt-center mb" style="color: var(--color-primary-dark);">500+</h3>
					<p class="md-p p-ghost txt-center">Recetas nicaragüenses</p>
				</div>

				<div
					class="metric-card pad-20 round-15 bg-soft-gray hover-lift animate-fade-in-up animate-delay-2"
					style="width: 200px; min-height: 150px;"
				>
					<div
						class="metric-icon flex-center round-10 mb"
						style="width: 60px; height: 60px; background: var(--gradient-mint); margin: 0 auto;"
					>
						<i class="las la-users text-col-white" style="font-size: 24px;"></i>
					</div>
					<h3 class="h1 bold txt-center mb" style="color: var(--color-primary-dark);">2,500+</h3>
					<p class="md-p p-ghost txt-center">Usuarios activos</p>
				</div>

				<div
					class="metric-card pad-20 round-15 bg-soft-gray hover-lift animate-fade-in-up animate-delay-3"
					style="width: 200px; min-height: 150px;"
				>
					<div
						class="metric-icon flex-center round-10 mb"
						style="width: 60px; height: 60px; background: var(--gradient-sunrise); margin: 0 auto;"
					>
						<i class="las la-calendar text-col-white" style="font-size: 24px;"></i>
					</div>
					<h3 class="h1 bold txt-center mb" style="color: var(--color-primary-dark);">8,000+</h3>
					<p class="md-p p-ghost txt-center">Planes creados</p>
				</div>

				<div
					class="metric-card pad-20 round-15 bg-soft-gray hover-lift animate-fade-in-up animate-delay-4"
					style="width: 200px; min-height: 150px;"
				>
					<div
						class="metric-icon flex-center round-10 mb"
						style="width: 60px; height: 60px; background: linear-gradient(135deg, #C86F56 0%, #ff6b6b 100%); margin: 0 auto;"
					>
						<i class="las la-star text-col-white" style="font-size: 24px;"></i>
					</div>
					<h3 class="h1 bold txt-center mb" style="color: var(--color-primary-dark);">4.8</h3>
					<p class="md-p p-ghost txt-center">Rating promedio</p>
				</div>
			</div>
		</div>
	</section>

	<section id="join">
		<div class="container flex-center direction-col pad-50">
			<p class="h1 text-col-white bold animate-fade-in-up">Empieza tu viaje culinario hoy</p>
			<p class="lg-p text-col-white mb-l animate-fade-in-up animate-delay-1">
				Únete a miles de nicaragüenses que ya transformaron su forma de comer con recetas saludables
				y deliciosas
			</p>

			<a href="/signup" class="btn ghost mb-l hover-glow animate-scale-in animate-delay-2"
				>Registrate!</a
			>
			<p class="md-p text-col-white animate-fade-in-up animate-delay-3">
				Ya tienes una cuenta? <a href="/login" class="bold text-col-white">Inicia Sesión</a>
			</p>
		</div>
	</section>

	<Footer />
</div>

<style>
	.home section {
		/* Vertical padding */
		width: 100%;
	}

	img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	/*
	#category-roulette .category {
		width: 200px;
		height: 140px;
	}

	#category-roulette .category .icon {
		width: 65px;
		height: 65px;

		font-size: 2rem;
	}
		*/

	section#join {
		background:
			radial-gradient(
				circle,
				transparent 20%,
				#626f47 20%,
				#626f47 80%,
				transparent 80%,
				transparent
			),
			radial-gradient(
					circle,
					transparent 20%,
					#626f47 20%,
					#626f47 80%,
					transparent 80%,
					transparent
				)
				50px 50px,
			linear-gradient(#708051 8px, transparent 8px) 0 -4px,
			linear-gradient(90deg, #708051 8px, transparent 8px) -4px 0;
		background-color: #626f47;
		background-size:
			100px 100px,
			100px 100px,
			50px 50px,
			50px 50px;
	}
</style>
