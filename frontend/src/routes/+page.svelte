<script>
	import Banner from '$lib/components/Banner.svelte';
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
			accent: 'leaf',
			icon: icon_SoupBowl
		},
		{
			title: 'Planes Nutricionales',
			description:
				'Genera un plan semanal que respete tus metas, tu actividad física y tus preferencias.',
			cta: 'Crear plan',
			accent: 'mint',
			icon: icon_Calendar
		},
		{
			title: 'Receta Rápida',
			description:
				'Escribe lo que tienes en casa y deja que nuestra IA sugiera la mejor coincidencia.',
			cta: 'Receta rápida',
			accent: 'sunrise',
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
	<section id="top" class="bg-cream flex justify-center" style="background-color: #C0C78C;">
		<div class="container regrid-cols-2 pad-20">
			<div class="content pad-20 bg-white">
				<h2>
					Descubre la <span class="p-emphasis">cocina</span>
					nicaragüense
				</h2>
				<p class="md-p mb-l">
					Tu plataforma para planear comidas nutritivas con el sabor de casa. Recibe recomendaciones
					personalizadas, recetas auténticas y acompañamiento inteligente en cada etapa.
				</p>
				<div class="button-group flex gap-24">
					<button class="btn primary">Crear mi plan nutricional</button>
					<button class="btn ghost">Explorar recetas</button>
				</div>
			</div>

			<div class="img-container img-fluid round-20 rel-pos">
				<img class="" src={ImagenVigoron} alt="vigoron" />
				<div class="card abs-pos pad-10" style="left: 15px; bottom: 15px; width: calc(100% - 30px)">
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
		<div class="container flex direction-col justify-center items-center pad-50 gap-16">
			<p class="h3">Recetas Destacadas</p>
			<div class="flex gap-16 ov-auto-x pad-10 limit-width no-shrink">
				{#each featuredRecipes as recipe}
					<RecipeCard {recipe} />
				{/each}
			</div>
		</div>
	</section>

	<section id="why-us" style="background-color: #798645;">
		<div class="container flex justify-center items-center">
			<p class="h1 text-col-white bold pad-20 txt-center">¿Por qué elegir NutriPlan?</p>
		</div>
	</section>

	<section id="categories" class="bg-soft">
		<div class="container flex direction-col justify-center items-center pad-50">
			<p class="mb-l h3">Explora por categorias</p>
			<div class="content flex wrap gap-16 justify-center items-center" id="category-roulette">
				{#each categories as category}
					<div
						class="category flex direction-col justify-center items-center round-10"
						style="background-color: {category.background_color};"
					>
						<div
							class="icon flex justify-center items-center round-5 b-shadow"
							style="background: {category.gradient}; color: white;"
						>
							{@html category.icon}
						</div>
						<p class="mt-s bold">{category.title}</p>
					</div>
				{/each}
			</div>
		</div>
	</section>
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

	#category-roulette .category {
		width: 200px;
		height: 140px;
	}

	#category-roulette .category .icon {
		width: 65px;
		height: 65px;

		font-size: 2rem;
	}
</style>
