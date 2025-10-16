<script>
	import SVG_NUTRIPLAN_TRANSPARENT from '$lib/assets/nutriplan-transparent.svg';
	import { getRandomInt } from '$lib/utils/math';

	// const start = getRandomInt(0, 360);
	const start = 1;
</script>

<div class="loader-ring">
	<img src={SVG_NUTRIPLAN_TRANSPARENT} alt="nutriplan-logo" style="transform: rotate({start}deg)" />
</div>

<style>
	.loader-ring {
		display: inline-block;
		width: 80px;
		height: 80px;
		border: 5px solid rgba(0, 0, 0, 0.4);
		border-radius: 50%;
		animation: spin 1s ease infinite; /* The animation property */
	}

	/* Define the rotation animation */
	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}
</style>
