<script>
	// Svelte 5 runes style, matching your snippet:
	let { count = 0 } = $props(); // e.g., 0..5, can be decimal

	const star_count = 5;
	const fill_color = '#C86F56';
	const unfill_color = 'gray';
	const size = 22; // px

	let value = $state();
	let stars = $state();

	$effect(() => {
		value = Math.max(0, Math.min(count, star_count));
		stars = Array.from({ length: star_count });
	});

	function pctAt(i) {
		const p = (value - i) * 100;
		return Math.max(0, Math.min(100, p));
	}
</script>

<div class="stars flex" aria-label={`Rating: ${value} de ${star_count}`}>
	{#each stars as _, i}
		<span class="star rel-pos" style="font-size:{size}px">
			<!-- base (unfilled) -->
			<i class="las la-star base" style="color:{unfill_color}"></i>
			<!-- overlay (filled) clipped by width -->
			<span class="fill no-overflow abs-pos" style="width:{pctAt(i)}%; top: 0px; left: 0px;">
				<i class="las la-star" style="color:{fill_color}"></i>
			</span>
		</span>
	{/each}
</div>
