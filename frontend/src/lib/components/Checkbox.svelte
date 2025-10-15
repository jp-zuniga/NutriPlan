<script>
	let { label, checked = false, value = $bindable('') } = $props();

	$effect(() => {
		value = checked;
	});

	function toggleCheck() {
		checked = !checked;
	}
</script>

<button class="checkbox no-pad no-border clickable no-bg flex-center gap-8" onclick={toggleCheck}>
	<div class="check soft-outline flex-center" data-selected={checked}>
		<i class="las la-square"></i>
	</div>
	<p class="md-p">
		{label}
	</p>
</button>

<style>
	.check {
		width: 20px;
		height: 20px;
		background-color: white;

		transition: 0.2s ease;
	}

	.check i {
		color: white;
	}

	.check[data-selected='true'] {
		background-color: var(--color-primary-dark);
	}
</style>
