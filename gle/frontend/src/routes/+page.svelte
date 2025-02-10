<script lang="ts">
	import Counter from './Counter.svelte';
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcomeFallback from '$lib/images/svelte-welcome.png';
	import Inbox from '../components/Inbox.svelte';
	import Splash from '../components/Splash.svelte';

	let timeData: string | null = null;

	async function fetchTime() {
		try {
			const response = await fetch('http://localhost:8000/time-domain');
			if (response.ok) {
				const data = await response.json();
				timeData = data.time;
			} else {
				console.error('Failed to fetch time data');
			}
		} catch (error) {
			console.error('Error fetching time data:', error);
		}
	}

	fetchTime();
</script>

<svelte:head>
	<title>Dashboard</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<!-- <Splash /> -->
</section>

<div class="inbox">
	<Inbox />
</div>

<img src="http://localhost:8000/images/sine_wave.png" alt="Welcome to Svelte" />

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
	}

	.welcome {
		display: block;
		position: relative;
		width: 100%;
		height: 0;
		padding: 0 0 calc(100% * 495 / 2048) 0;
	}

	.welcome img {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		display: block;
	}
</style>
