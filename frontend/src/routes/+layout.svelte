<script>
	import favicon from '$lib/assets/favicon.svg';
	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link rel="stylesheet" href="/styles/global.css" />
	<link rel="stylesheet" href="/styles/home.css" />
</svelte:head>

{@render children?.()}
