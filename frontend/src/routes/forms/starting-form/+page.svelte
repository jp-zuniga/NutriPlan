<script>
	import { goto } from '$app/navigation';
	import FormBanner from '$lib/components/forms/FormBanner.svelte';
	import FoodPreferences from '$lib/components/forms/FoodPreferences.svelte';
	import MedicalInfo from '$lib/components/forms/MedicalInfo.svelte';

	const form_steps = ['Preferencias alimenticias', 'Perfil de Salud'];
	const form_objects = [
		`<FoodPreferences
			continue_callback={() => {
				current_form++;
			}}
		/>`
	];
	let current_form = $state(1);

	function go_back() {
		if (current_form <= 1) goto('/welcome');
		else current_form--;
	}
</script>

<div class="form">
	<FormBanner
		form_title={form_steps[current_form - 1]}
		step={current_form}
		stepcount={form_steps.length}
		callback={go_back}
	/>
	<div class="form-container">
		{#if current_form == 1}
			<FoodPreferences
				continue_callback={() => {
					current_form++;
				}}
			/>
		{:else if current_form == 2}
			<MedicalInfo
				continue_callback={() => {
					goto('/home');
				}}
			/>
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
