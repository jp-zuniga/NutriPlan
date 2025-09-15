<script>
	import { goto } from '$app/navigation';
	import FormBanner from '$lib/components/forms/FormBanner.svelte';
	import FoodPreferences from '$lib/components/forms/FoodPreferences.svelte';
	import MedicalInfo from '$lib/components/forms/MedicalInfo.svelte';
	import { formAnswers } from '$lib/stores/formAnswers.js';

	let foodAnswers = null;
	let medicalAnswers = null;

	const form_steps = ['Preferencias alimenticias', 'Perfil de Salud'];
	let current_form = 1;
	let form_questionaire;

	function reset_scroll() {
		if (form_questionaire) form_questionaire.scrollTop = 0;
	}

	function go_back() {
		if (current_form <= 1) goto('/welcome');
		else current_form--;
		reset_scroll();
	}

	function onFoodContinue(answers) {
		foodAnswers = answers;
		formAnswers.update((fa) => ({ ...fa, foodAnswers }));
		current_form++;
		reset_scroll();
	}

	function onMedicalContinue(answers) {
		medicalAnswers = answers;
		formAnswers.update((fa) => ({ ...fa, medicalAnswers }));
		goto('/forms/ai-recommendations');
		reset_scroll();
	}
</script>

<div class="form">
	<FormBanner
		form_title={form_steps[current_form - 1]}
		step={current_form}
		stepcount={form_steps.length}
		callback={go_back}
	/>
	<div class="form-container" bind:this={form_questionaire}>
		{#if current_form == 1}
			<FoodPreferences continue_callback={onFoodContinue} />
		{:else if current_form == 2}
			<MedicalInfo continue_callback={onMedicalContinue} />
		{:else}
			<h2>404, Form not Found</h2>
		{/if}
	</div>
</div>

<style>
	.form {
		width: 100vw;
		height: 100vh;

		display: grid;
		grid-template-rows: 100px 1fr;
	}

	.form-container {
		overflow-y: scroll;
	}
</style>
