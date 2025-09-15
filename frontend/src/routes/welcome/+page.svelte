<script>
	import { goto } from '$app/navigation';
	import '$lib/components/welcome/WelcomeTip.svelte';
	import WelcomeTip from '$lib/components/welcome/WelcomeTip.svelte';

	const welcome_tips = [
		{
			title: 'Recetas tradicionales nicas',
			description: 'Gallo pinto, quesillo y más con análisis nutricional',
			color: 'linear-gradient(-45deg,rgba(86, 171, 47, 1) 0%, rgba(168, 224, 99, 1) 100%)',
			icon: 'las la-utensils'
		},
		{
			title: 'IA nutricional personalizada',
			description: 'Planes basados en tu salud y preferencias',
			color: 'linear-gradient(-45deg,rgba(131, 77, 155, 1) 0%, rgba(208, 78, 214, 1) 100%)',
			icon: 'las la-brain'
		},
		{
			title: 'Objetivos de salud claros',
			description: 'Seguimiento inteligente de tu progreso',
			color: 'linear-gradient(-45deg,rgba(237, 143, 3, 1) 0%, rgba(255, 183, 94, 1) 100%)',
			icon: 'las la-bullseye'
		}
	];

	function goto_startingform() {
		goto('/forms/starting-form');
	}
</script>

<div id="welcome-screen">
	<div class="welcome-card">
		<img id="nutriplan-logo" src="/assets/images/NutriPlan.png" alt="NutriPlan Logo" />
		<hr />
		<h2>Nutrición IA para Nicaragua</h2>
		<p>
			Tu <b>chef personal con IA</b> que conoce tus<br />tradiciones y crea planes nutricionales
			únicos
		</p>
		<div id="tips">
			{#each welcome_tips as tip}
				<WelcomeTip
					title={tip.title}
					description={tip.description}
					color={tip.color}
					icon={tip.icon}
				/>
			{/each}
		</div>

		<button id="submit-button" onclick={goto_startingform}>
			<span>Crear mi plan nutricional IA</span>
		</button>
	</div>
</div>

<style>
	#welcome-screen {
		width: 100vw;
		height: 100vh;

		display: flex;

		align-items: center;
		justify-content: center;

		text-align: center;
		background-image: url('/assets/images/background.webp');
		background-size: cover;

		color: rgb(44, 44, 44);
	}

	.welcome-card {
		padding: 30px;
		background-color: white;
		border-radius: 30px;

		box-shadow: 10px 10px 30px rgba(0, 0, 0, 0.1);
	}

	#nutriplan-logo {
		height: 80px;
		width: auto;
	}

	b {
		color: green;
	}

	hr {
		border: none;
		border-top: 2px solid rgb(192, 192, 192);
	}

	#submit-button {
		width: 100%;
		background: linear-gradient(-45deg, rgba(141, 194, 111, 1) 0%, rgba(118, 184, 82, 1) 100%);
		padding: 10px 0px;
		color: white;
		font-size: 18px;
		outline: none;
		border: none;
		border-radius: 15px;
		margin-top: 15px;
		cursor: pointer;

		box-shadow: 10px 10px 30px rgba(0, 0, 0, 0.1);
		transition: 0.1s;
	}

	#submit-button:hover {
		background: white;
		color: rgba(141, 194, 111, 1);
		outline: 2px solid rgba(141, 194, 111, 1);
		transform: translateY(-2px);
		box-shadow: 10px 10px 30px rgba(0, 0, 0, 0.2);
	}

	/* #submit-button span::after {
		content: url(/assets/icons/arrow-right-solid.svg);
		display: inline-block;
		width: 20px;
		height: 20px;

		position: absolute;
		margin-left: 5px;
	} */
</style>
