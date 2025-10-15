<script>
	import favicon from '$lib/assets/favicon.svg';
	import { authUser } from '$lib/stores/auth.js';
	import Banner from '$lib/components/Banner.svelte';
	import { NIGHTLY_BUILD } from '$lib/endpoints.js';

	let { data, children } = $props();

	$effect(() => {
		console.log(`Data: ${JSON.stringify(data.user)}`);
		authUser.set(data.user);
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link rel="stylesheet" href="/styles/global.css" />
	<link rel="stylesheet" href="/styles/home.css" />
	<link rel="stylesheet" href="/styles/responsive.css" />
	<link
		rel="stylesheet"
		href="https://maxst.icons8.com/vue-static/landings/line-awesome/line-awesome/1.3.0/css/line-awesome.min.css"
	/>
	{#if NIGHTLY_BUILD}
		<title>NutriPlan</title>
	{:else}
		<title>NutriPlan (nightly)</title>
	{/if}
</svelte:head>

<Banner />
{@render children?.()}
