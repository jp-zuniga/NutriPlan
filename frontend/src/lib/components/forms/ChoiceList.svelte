<script>
	let { title, description, options, rows = 1, group } = $props();

	let selectedIndex = $state(null);

	function optionClick(index) {
		selectedIndex = selectedIndex === index ? null : index;
	}
</script>

<div class="form-choice">
	<h3>{title}</h3>
	<div class="choices" style="grid-template-columns: repeat({rows}, 1fr);">
		{#each options as option, index}
			<button
				class="form-option {selectedIndex === index ? 'selected' : ''}"
				onclick={() => optionClick(index)}
				type="button"
			>
				{option.text}
				{#if option.description}
					<span>{option.description}</span>
				{/if}
			</button>
		{/each}
	</div>
</div>

<style>
	.form-choice {
		display: flex;
		flex-direction: column;
		justify-content: left;
		margin: 20px;
	}

	.choices {
		display: grid;
		gap: 20px;
	}

	.form-option {
		text-align: left;
		font-size: 18px;
		width: 100%;
		border: 2px solid white;
		background-color: white;
		box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.1);
		padding: 15px;
		border-radius: 10px;
		transition: 0.1s ease;

		display: flex;
		flex-direction: column;
	}

	.form-option:hover {
		border-color: #6c40fb;
		transform: translateY(-5px);
	}

	.form-option.selected {
		background-color: #6c40fb;
		border: 2px solid #6c40fb;
		color: white;
	}

	.form-option.selected:hover {
		background-color: #5a35d0;
		border: 2px solid #5a35d0;
	}

	.form-option span {
		color: inherit;
		opacity: 60%;
		font-size: 15px;
	}
</style>
