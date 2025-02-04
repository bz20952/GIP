<script lang="ts">
	import Counter from './Counter.svelte';
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcomeFallback from '$lib/images/svelte-welcome.png';
	import Inbox from '../components/Inbox.svelte';
	import Splash from '../components/Splash.svelte';
	import ProgressBar from '../components/ProgressBar.svelte';
</script>

<svelte:head>
	<title>Dashboard</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<h1>
	Welcome to the world of Gamified Engineering! 🚀
</h1>

<section>
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
</style>
