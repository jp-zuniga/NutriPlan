<script>
	let { title, type, placeholder, group, validate_function, answer_callback } = $props();

	let input = $state('');
	let valid_value = $state(null);

	function optionClick(index) {
		valid_value = validate_function(input);

		if (valid_value) answer_callback(group, input);
		else answer_callback(group, null);
	}
</script>

<div class="form-choice">
	<h3>{title}</h3>
	<div class="form-input">
		<input
			class={valid_value === false ? 'invalid' : ''}
			bind:value={input}
			{type}
			{placeholder}
			onkeyup={optionClick}
		/>
	</div>
</div>

<style>
	.form-choice {
		display: flex;
		flex-direction: column;
		justify-content: left;
		margin: 20px;
		width: 80%;
	}

	.form-input input {
		text-align: left;
		font-size: 18px;
		width: 100%;
		border: 2px solid white;
		background-color: white;
		box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.1);
		padding: 15px;
		border-radius: 10px;
		transition: 0.1s ease;

		outline-color: #6c40fb;

		display: flex;
		flex-direction: column;
	}

	.form-choice input.invalid {
		background-color: pink;
	}

	.form-input input:focus {
		outline: 2px solid #6c40fb;
		transform: translateY(-5px);
	}
</style>
