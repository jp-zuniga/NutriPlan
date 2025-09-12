<script>
	let { title, options } = $props();
</script>

<div class="form-choice">
	<h3>{title}</h3>
	{#each options as option}
		<div class="form-option">{option}</div>
	{/each}
</div>
