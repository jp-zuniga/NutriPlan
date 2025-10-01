<div class="heart-box">
	<img src="/assets/icons/heart.svg" alt="heart" />
</div>

<style>
	.heart-box {
		width: 30px;
		height: 30px;

		background-color: whitesmoke;
		border-radius: 10px;

		cursor: pointer;
		box-shadow: 0px 5px 5px rgba(0, 0, 0, 0.233);
		padding: 5px;

		transition: 0.1s linear;
	}

	.heart-box img {
		max-width: 100%;
		max-height: 100%;

		transition: 0.1s linear;
	}

	.heart-box:hover {
		background-color: #e44e48ff;
	}

	.heart-box:hover img {
		filter: saturate(0%) brightness(250%);
	}
</style>
