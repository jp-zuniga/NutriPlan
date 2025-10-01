const recipes = {
	'vigoron-saludable': {
		title: 'Vigorón saludable',
		tagline: 'Una versión ligera del clásico granadino con chicharrón al horno y repollo cítrico.',
		cover: 'vigoron',
		origin: 'Granada',
		time: '35 min',
		difficulty: 'Intermedia',
		calories: 430,
		macros: { protein: '28 g', carbs: '45 g', fats: '16 g' },
		tags: ['Alto en fibra', 'Sin frituras', 'Favorito de IA'],
		ingredients: [
			'500 g de yuca cocida al vapor',
			'150 g de chicharrón al horno',
			'2 tazas de repollo rallado',
			'1 zanahoria rallada',
			'2 limones criollos',
			'4 cucharadas de vinagre de caña',
			'¼ taza de cebolla morada en plumas',
			'¼ taza de menta fresca picada',
			'Sal marina y pimienta al gusto'
		],
		steps: [
			'Mezcla el repollo, la zanahoria, la cebolla y la menta con el jugo de limón y el vinagre. Deja macerar 15 minutos.',
			'Calienta el chicharrón al horno para que quede crujiente sin añadir grasa.',
			'Corta la yuca en trozos y colócala como base en cada plato.',
			'Sirve encima el curtido de repollo y finaliza con el chicharrón. Ajusta sal y pimienta.'
		],
		tips: [
			'Reemplaza el chicharrón por pollo al horno si quieres reducir grasas.',
			'Acompaña con pico de gallo de mango para añadir vitamina C.'
		],
		comments: [
			{
				user: 'Juana M.',
				city: 'Masaya',
				comment: 'Perfecta para compartir domingo en familia. El curtido queda refrescante.'
			},
			{
				user: 'Carlos A.',
				city: 'León',
				comment: 'La IA recomendó usar chicharrón al horno y funciona excelente, nada grasoso.'
			}
		]
	},
	'gallo-pinto-energizante': {
		title: 'Gallo pinto energizante',
		tagline: 'Desayuno balanceado con frijoles rojos, arroz integral y topping de huevo pochado.',
		cover: 'gallo-pinto',
		origin: 'Managua',
		time: '25 min',
		difficulty: 'Fácil',
		calories: 380,
		macros: { protein: '22 g', carbs: '52 g', fats: '9 g' },
		tags: ['Desayuno', 'Vegetariano opcional', 'Alta energía'],
		ingredients: [
			'2 tazas de arroz integral cocido',
			'2 tazas de frijoles rojos cocidos con su caldo',
			'1 cebolla blanca picada',
			'1 chile dulce picado',
			'1 cucharada de aceite de coco',
			'1 cucharadita de achiote',
			'2 huevos pochados',
			'Cilantro fresco, sal y pimienta'
		],
		steps: [
			'Sofríe la cebolla y el chile dulce en aceite de coco con el achiote.',
			'Incorpora el arroz y los frijoles con un poco de su caldo hasta integrar.',
			'Sirve con huevo pochado y cilantro fresco encima.'
		],
		tips: [
			'Cambia el huevo por aguacate para una versión vegana.',
			'Añade semillas de chía para mayor fibra.'
		],
		comments: [
			{
				user: 'Rosa F.',
				city: 'Chinandega',
				comment: 'Ideal antes de entrenar, me mantuvo llena toda la mañana.'
			},
			{
				user: 'Bryan P.',
				city: 'Estelí',
				comment: 'El toque de aceite de coco le da un aroma increíble.'
			}
		]
	},
	'sopa-queso-liviana': {
		title: 'Sopa de queso liviana',
		tagline: 'Una sopa cremosa con menos grasa, perfecta para tardes lluviosas.',
		cover: 'sopa-queso',
		origin: 'Chontales',
		time: '40 min',
		difficulty: 'Intermedia',
		calories: 320,
		macros: { protein: '18 g', carbs: '28 g', fats: '14 g' },
		tags: ['Reconfortante', 'Sin gluten', 'Ideal para cena'],
		ingredients: [
			'200 g de queso ahumado bajo en grasa',
			'1 litro de caldo de vegetales',
			'2 plátanos maduros en rodajas',
			'1 taza de leche evaporada light',
			'1 cebolla blanca',
			'2 dientes de ajo',
			'1 cucharada de achiote',
			'2 cucharadas de cilantro picado'
		],
		steps: [
			'Sofríe cebolla y ajo con achiote hasta dorar.',
			'Agrega el caldo y las rodajas de plátano, cocina 15 minutos.',
			'Incorpora la leche, hierve suave y añade el queso en cubos hasta fundir.',
			'Sazona y sirve con cilantro fresco.'
		],
		tips: [
			'Asa el queso antes de incorporarlo para potenciar sabor.',
			'Acompaña con tortillas de maíz integrales.'
		],
		comments: [
			{
				user: 'Elena Z.',
				city: 'Juigalpa',
				comment: 'Ligera pero sustanciosa, mis hijos pidieron repetición.'
			}
		]
	},
	'ensalada-chayote-verde': {
		title: 'Ensalada de chayote verde',
		tagline: 'Texturas crujientes con vinagreta de tamarindo y semillas tostadas.',
		cover: 'chayote',
		origin: 'Masaya',
		time: '20 min',
		difficulty: 'Fácil',
		calories: 280,
		macros: { protein: '10 g', carbs: '24 g', fats: '14 g' },
		tags: ['Refrescante', 'Baja en carbohidratos', 'Listo en 20 min'],
		ingredients: [
			'3 chayotes tiernos en láminas',
			'1 pepino cortado en medias lunas',
			'1 taza de tomate cherry',
			'½ taza de semillas de jícaro tostadas',
			'2 cucharadas de tamarindo concentrado',
			'2 cucharadas de miel de caña',
			'2 cucharadas de aceite de ajonjolí',
			'Hojas de hierbabuena'
		],
		steps: [
			'Mezcla el tamarindo con miel y aceite para crear la vinagreta.',
			'Integra las verduras con la vinagreta justo antes de servir.',
			'Decora con semillas tostadas y hierbabuena.'
		],
		tips: [
			'Marina el chayote con limón para suavizar su textura.',
			'Incluye queso fresco desmoronado si buscas más proteína.'
		],
		comments: [
			{
				user: 'María José',
				city: 'Masatepe',
				comment: 'Súper refrescante; la vinagreta de tamarindo es adictiva.'
			}
		]
	}
};

export function load({ params }) {
	const recipe = recipes[params.slug] ?? recipes['vigoron-saludable'];
	const recommended = Object.entries(recipes)
		.filter(([slug]) => slug !== params.slug)
		.map(([slug, info]) => ({
			slug,
			title: info.title,
			time: info.time,
			calories: info.calories,
			tags: info.tags.slice(0, 2),
			cover: info.cover
		}));

	return {
		recipe,
		recommended,
		notFound: !recipes[params.slug]
	};
}
