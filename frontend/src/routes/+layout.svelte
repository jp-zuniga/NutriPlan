<script>
	import favicon from '$lib/assets/favicon.svg';
	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link rel="stylesheet" href="/styles/global.css" />
	<link rel="stylesheet" href="/styles/home.css" />
	<link
		rel="stylesheet"
		href="https://maxst.icons8.com/vue-static/landings/line-awesome/line-awesome/1.3.0/css/line-awesome.min.css"
	/>
	<title>NutriPlan</title>
</svelte:head>

{@render children?.()}
