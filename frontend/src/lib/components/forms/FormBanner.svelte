<script>
	import { goto } from '$app/navigation';
	let { form_title, step, stepcount, callback } = $props();

	function go_back() {
		callback();
	}
</script>

<div class="form-banner">
	<button class="back-button" aria-label="Back" onclick={go_back}>
		<i class="las la-angle-left"></i>
	</button>
	<div class="content">
		<h2 class="banner-title">{form_title}</h2>
		<p>Paso {step} de {stepcount}</p>
	</div>
</div>

<style>
	.form-banner {
		background-color: white;
		display: flex;
		align-items: center;

		z-index: 50;
		box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.05);
	}

	.form-banner .content {
		margin-left: 20px;
	}

	.form-banner .content p {
		color: gray;
	}

	.form-banner .content p,
	h2 {
		margin: 0px;
	}

	.banner-title {
		font-weight: bold;
		font-size: 20px;
	}

	.back-button {
		width: 50px;
		height: 50px;

		border: none;
		border-radius: 15px;

		display: flex;
		align-items: center;
		justify-content: center;

		margin-left: 20px;
		transition: 0.1s ease;

		cursor: pointer;
	}

	.back-button i {
		font-size: 20px;
	}
</style>
