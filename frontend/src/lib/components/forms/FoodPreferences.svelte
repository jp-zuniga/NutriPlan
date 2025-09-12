<script>
	import { goto } from '$app/navigation';
	import ChoiceList from './ChoiceList.svelte';
	import FormBanner from './FormBanner.svelte';

	const questions = [
		{
			title: 'Tipo de alimentación',
			options: [
				{ text: 'Omnívora' },
				{ text: 'Vegana' },
				{ text: 'Vegetariana' },
				{ text: 'Pesceteriana' }
			],
			rows: 2
		},
		{
			title: 'Objetivos de Salud',
			options: [
				{ text: 'Perder peso gradualmente' },
				{ text: 'Mantener peso actual' },
				{ text: 'Ganar masa muscular' },
				{ text: 'Más energía diaria' },
				{ text: 'Mejor digestión' },
				{ text: 'Control de azucar' }
			]
		},
		{
			title: 'Nivel de Actividad',
			options: [
				{ text: 'Sedentaria', description: 'Oficina, poco ejercicio' },
				{ text: 'Ligera', description: 'Ejercicio 1-3 días/semana' },
				{ text: 'Moderada', description: 'Ejercicio 3-5 días/semana' },
				{ text: 'Activa', description: 'Ejercicio 6-7 días/semana' }
			]
		}
	];
</script>

<div class="form-body">
	<FormBanner
		form_title="Preferencias Alimenticias"
		step="1"
		stepcount="2"
		callback={() => {
			goto('/welcome');
		}}
	/>
	<div class="questionaire">
		<div class="title">
			<div class="icon-container">
				<img src="/assets/icons/utensils-solid.svg" alt="utensils" />
			</div>
			<h2>¿Cómo te gusta comer?</h2>
			<p>Selecciona tus preferencias para que tu IA nutricional te conozca mejor</p>
		</div>
		{#each questions as question, index}
			<ChoiceList
				title={question.title}
				options={question.options}
				rows={question.rows}
				group={index}
			/>
		{/each}
	</div>
</div>

<style>
	.form-body {
		width: 100vw;
		height: 100vh;

		display: grid;
		grid-template-rows: 100px 1fr;
	}

	.questionaire {
		background-color: #f9f5ff;
		overflow-y: scroll;
	}

	.questionaire .title {
		display: flex;
		flex-direction: column;

		align-items: center;
		margin-top: 40px;
	}

	.questionaire .title .icon-container {
		background: linear-gradient(-45deg, rgba(131, 77, 155, 1) 0%, rgba(208, 78, 214, 1) 100%);

		width: 75px;
		height: 75px;
		border-radius: 20px;

		box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.1);

		display: flex;
		align-items: center;
		justify-content: center;

		margin-right: 15px;
	}

	.questionaire .title .icon-container img {
		width: 50px;
		height: 50px;
	}

	.questionaire .title h2,
	p {
		margin: 10px;
	}
</style>
