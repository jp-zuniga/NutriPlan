<script>
	import ChoiceList from './ChoiceList.svelte';
	import FormBanner from './FormBanner.svelte';

	const questions = [
		{
			title: 'Tipo de alimentación',
			options: ['Omnívora', 'Vegana', 'Vegetariana', 'Pesceteriana']
		}
	];
</script>

<div class="form-body">
	<FormBanner form_title="Preferencias Alimenticias" step="1" stepcount="2" />
	<div class="questionaire">
		{#each questions as question}
			<ChoiceList title={question.title} options={question.options} />
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
		background-color: #F9F5FF;
	}
</style>
