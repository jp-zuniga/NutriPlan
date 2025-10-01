<script>
	import { goto } from '$app/navigation';
	import ChoiceList from './ChoiceList.svelte';
	import FormBanner from './FormBanner.svelte';

	let { continue_callback } = $props();

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

	let answered = Array(questions.length).fill(null);
	let answers = $state(0);

	// Use null to mark as unanswered
	function updateQuestion(question_index, answer = null) {
		answered[question_index] = answer;
		console.log(`Question #${question_index} updated with answer ${answer}`);
		answeredQuestions();
	}

	function answeredQuestions() {
		answers = 0;
		for (let answer of answered) if (answer != null) answers++;

		console.log(`Total number of answers: ${answers}, question count: ${answered.length}`);
	}

	function passAnswers() {
		console.log(`Answers passed: ${answered}`);
		continue_callback(answered);
	}
</script>

<div class="form-body">
	<div class="questionaire">
		<div class="title">
			<div class="icon-container">
				<i class="las la-utensils"></i>
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
				answer_callback={updateQuestion}
			/>
		{/each}
		<button disabled={answers < answered.length} id="submit-button" onclick={passAnswers}
			>Continuar</button
		>
	</div>
</div>

<style>
	.questionaire {
		background-color: #f9f5ff;

		display: flex;
		flex-direction: column;
		align-items: center;

		width: 100%;
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

	.questionaire .title .icon-container i {
		color: white;
		font-size: 50px;
	}

	.questionaire .title h2,
	p {
		margin: 10px;
	}

	#submit-button {
		margin: 20px;
		width: 500px;
		background: linear-gradient(-45deg, rgba(141, 194, 111, 1) 0%, rgba(118, 184, 82, 1) 100%);
		padding: 10px 0px;
		color: white;
		font-size: 18px;
		outline: none;
		border: none;
		border-radius: 15px;
		margin-top: 15px;

		box-shadow: 10px 10px 30px rgba(0, 0, 0, 0.1);
		transition: 0.1s;
	}

	#submit-button:disabled {
		opacity: 50%;
	}

	#submit-button:not([disabled]) {
		cursor: pointer;
	}

	#submit-button:not([disabled]):hover {
		background: white;
		color: rgba(141, 194, 111, 1);
		outline: 2px solid rgba(141, 194, 111, 1);
		transform: translateY(-2px);
		box-shadow: 10px 10px 30px rgba(0, 0, 0, 0.2);
	}
</style>
