<script lang="ts">
	import Inbox from '../components/Inbox.svelte';
	import Splash from '../components/Splash.svelte';
	import { splash } from '$lib/stores';
</script>

<svelte:head>
	<title>Dashboard</title>
	<meta name="description" content="Dashboard" />
</svelte:head>

{#if $splash}
	<Splash />
{/if}

<!-- <h1>
	Plane Sailing Inc.
</h1> -->

<section>
	<img src='$lib/images/logo.png' alt='Plane Sailing Inc.' />
	<Inbox />
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	h1 {
		width: 100%;
		margin: 3rem 0rem;
	}

	img {
		margin: 1rem 0 0 0;
		height: 15em;
		width: auto;
	}
</style>
