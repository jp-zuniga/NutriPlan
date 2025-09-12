<script>
	import { onMount } from 'svelte';

	let { title, options } = $props();

	let option_selected = null;
	let buttons = [];

	onMount(() => {
		buttons = document.getElementsByClassName('form-option');
		for (let button of buttons) console.log(button);
	});

	function optionClick(option) {
		if (option == option_selected) option_selected = null;
		else option_selected = option;

		console.log(`Handled option click event, option selected ${option}`);
		updateButtons();
	}

	function updateButtons() {
		console.log(`Updating button list: ${buttons}`);
		for (let button of buttons) {
			console.log(`Button text: ${button.textContent}`);
			if (button.classList.contains('selected')) {
				if (button.textContent == option_selected || option_selected == null)
					button.classList.remove('selected');
			} else {
				if (button.textContent == option_selected) button.classList.add('selected');
			}
		}
	}
</script>

<div class="form-choice">
	<h3>{title}</h3>
	<div class="choices">
		{#each options as option}
			<button class="form-option" onclick={() => optionClick(option)}>{option}</button>
		{/each}
	</div>
</div>

<style>
	.form-choice {
		display: flex;
		flex-direction: column;
		justify-content: left;
		width: 100%;
		margin: 20px;
	}

	.choices {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 20px;
	}

	.form-option {
		width: 100%;
		border: 2px solid white;
		background-color: white;
		box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.1);
		padding: 15px;
		border-radius: 10px;
		transition: 0.1s ease;
	}

	.form-option:hover {
		border-color: #6c40fb;
		transform: translateY(-5px);
	}

	:global(.form-option.selected:hover) {
		background-color: #5a35d0;
		border: 2px solid #5a35d0;
	}

	:global(.form-option.selected) {
		background-color: #6c40fb;
		border: 2px solid #6c40fb;
		color: white;
	}
</style>
