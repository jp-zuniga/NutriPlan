<script>
	import { goto } from '$app/navigation';
	import ChoiceList from './ChoiceList.svelte';
	import FormBanner from './FormBanner.svelte';
	import FormInput from './FormInput.svelte';

	let { continue_callback } = $props();

	const questions = [
		{
			type: 'Input',
			title: 'Edad',
			input_type: 'number',
			placeholder: '28',
			validate_function: (value) => {
				if (value <= 0 || value >= 100) return false;
				else return true;
			}
		},
		{
			type: 'Input',
			title: 'Peso (kg)',
			input_type: 'number',
			placeholder: '65',
			validate_function: (value) => {
				if (value <= 0 || value >= 200) return false;
				else return true;
			}
		},
		{
			type: 'Input',
			title: 'Altura (cm)',
			input_type: 'number',
			placeholder: '165',
			validate_function: (value) => {
				if (value <= 0 || value >= 260) return false;
				else return true;
			}
		},
		{
			type: 'Choice',
			title: 'Alergias Alimentarias',
			options: [
				{ text: 'Gluten' },
				{ text: 'Lácteos' },
				{ text: 'Nueces' },
				{ text: 'Mariscos' },
				{ text: 'Huevos' },
				{ text: 'Soya' }
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
		console.log(`Medical answers passed: ${answered}`);
		continue_callback(answered);
	}
</script>

<div class="form-body">
	<div class="questionaire">
		<div class="title">
			<div class="icon-container">
				<i class="las la-file-medical-alt"></i>
			</div>
			<h2>Información Básica</h2>
			<p>Datos necesarios para crear tu plan nutricional perfecto.</p>
		</div>
		{#each questions as question, index}
			{#if question.type == 'Choice'}
				<ChoiceList
					title={question.title}
					options={question.options}
					rows={question.rows}
					group={index}
					answer_callback={updateQuestion}
				/>
			{:else if question.type == 'Input'}
				<FormInput
					title={question.title}
					placeholder={question.placeholder}
					type={question.input_type}
					group={index}
					validate_function={question.validate_function}
					answer_callback={updateQuestion}
				/>
			{/if}
		{/each}
		<button disabled={answers < answered.length} id="submit-button" onclick={passAnswers}
			>Continuar</button
		>
	</div>
</div>

<style>
	.questionaire {
		background-color: #f9f5ff;
		overflow-y: scroll;

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
		background: linear-gradient(-45deg, rgba(33, 131, 250, 1) 0%, rgba(0, 194, 116, 1) 100%);

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
