<script>
	import { splash } from '$lib/stores';
	import { testOptions } from '$lib/stores';
</script>

<div class="splash">
	<h1 class="welcome">Welcome to the world of Gamified Engineering! 🚀</h1>
	<p>
		You are an engineer at Plane Sailing Inc who specialise in dynamics testing for aviation.
		Recently shareholders have begun to worry that the company is falling behind the competition.
		If things don't change soon, Plane Sailing might encounter rough waters.
		<br><br>
		That's where you come in.
		You are about to be given 5 challenges to demonstrate your expertise, impress clients and save the company.
		Navigate to the <a href="/help"><strong>Help</strong></a> tab for guidance on getting started.
		<br><br>
		Are you ready?
	</p>
	<input class='serial-num' type="text" placeholder="Enter your Serial Number" bind:value={$testOptions['serialNumber']}>
	{#if $testOptions['serialNumber']}
		<button class="close-btn" on:click={() => $splash=false}>Let's go.</button>
	{/if}
</div>

<style>
	.splash {
		transition: opacity 0.5s ease-out;
		position: fixed;
		top: 50%;
		text-align: center;
		left: 50%;
		transform: translate(-50%, -50%);
		background-color: azure;
		min-width: 60%;
		max-width: 100%;
		border-radius: 10px;
		padding: 1rem;
		box-shadow: 5px 5px 5px 5px rgba(0, 0, 0, 0.2);
	}

	.welcome {
		padding: 0 0 1rem 0;
	}

	.serial-num {
		margin: 1rem;
	}

	.close-btn {
		color: white;
		margin: 1rem;
		border-radius: 10px;
	}
</style>
