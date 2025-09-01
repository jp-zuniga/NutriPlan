<script>
	import { goto } from '$app/navigation';
	import { gotoSearch } from './search';

	let terminoBusqueda = '';

	function buscar() {
		console.log(`Tratando de buscar: ${terminoBusqueda}`);
		if (terminoBusqueda != '') gotoSearch(terminoBusqueda);
	}
</script>

<div id="search-box">
	<input
		type="text"
		placeholder="Buscar recetas"
		bind:value={terminoBusqueda}
		on:keyup={(event) => {
			if (event.key === 'Enter') buscar();
		}}
	/>
	<button aria-label="Search" on:click={buscar}></button>
</div>

<style>
	#search-box {
		border-radius: 20px;
		width: 600px;
		background-color: rgb(235, 235, 235);

		display: flex;
		justify-content: space-between;
		align-items: center;

		transition: 0.1s linear;
	}

	#search-box:hover {
		background-color: rgb(211, 211, 211);
	}

	#search-box input {
		font-size: 14px;
		background-color: #ffffff00;
		color: #292929;
		outline: none;
		border: none;
		padding: 5px;
		margin: 5px;
		width: 100%;
		height: 100%;
	}

	#search-box button {
		width: 30px;
		height: 30px;
		margin-right: 3px;

		border: none;
		border-radius: 100%;

		background-color: var(--main-color);
		background-image: url('../assets/icons/magnifying-glass-solid-full.svg');
		background-size: 50%;
		background-position: center;
		background-repeat: no-repeat;

		transition: 0.1s linear;
		cursor: pointer;
	}
</style>
