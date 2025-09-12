<script>
	let { title, description, color, icon } = $props();
</script>

<div class="recipe-tip">
	<div class="image-container" style="background: {color};">
		<img src={icon} alt="Icon" />
	</div>
	<div class="text-container">
		<h3>{title}</h3>
		<p>{description}</p>
	</div>
</div>

<style>
	.recipe-tip {
		display: flex;
		align-items: center;

		text-align: left;

		margin: 15px;
		font-size: 13px;
	}

	.image-container {
		width: 50px;
		height: 50px;
		border-radius: 20px;

		box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.1);

		display: flex;
		align-items: center;
		justify-content: center;

		margin-right: 15px;
	}

	.image-container img {
		width: 30px;
		height: 30px;
	}

	h3 {
		margin: 0px;
	}

	p {
		margin: 0px;
	}
</style>
