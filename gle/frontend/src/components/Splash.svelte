<script>
	import { onMount } from 'svelte';

	let visible = false;

	onMount(() => {
		visible = true;
		setTimeout(() => {
			visible = false;
		}, 2000);
	});
</script>

<style>
	.splash {
		font-size: 2rem;
		font-weight: bold;
		opacity: 0;
		transition: opacity 1s ease-out;
		position: fixed;
		top: 50%;
		text-align: center;
        text-wrap: nowrap;
		left: 50%;
		transform: translate(-50%, -50%);
	}

	.splash.visible {
		opacity: 1;
		font-size: 2rem;
	}
</style>

<div class="splash" class:visible={visible}>Welcome to the world of Gamified Engineering! 🚀</div>
