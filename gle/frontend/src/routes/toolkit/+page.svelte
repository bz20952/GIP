<script lang="ts">
	import { goto } from '$app/navigation';
	import { tools } from '$lib/stores';

	let unlockedTools = $tools.filter(tool => tool.available).map(tool => tool.name);
	let lockedTools = $tools.filter(tool => !tool.available).map(tool => tool.name);
</script>

<svelte:head>
	<title>Toolkit</title>
	<meta name="description" content="Toolkit" />
</svelte:head>

<h1>
	Welcome to your Toolkit!
</h1>

<div class="sb-container">
	<ul>
		<li>Here you can see all of your available tools and start new experiments.</li>
		<li>Every experiment consists of three stages; test setup, signal processing and modal analysis.</li>
		<li>By clicking the button below, you can use your available tools to gather results.</li>
	</ul>
</div>

<section>
	
	<button class='new-exp' on:click={() => goto('/toolkit/test')}>
		Start a new experiment!
	</button>

	<div class='tools'>
		<div class="unlocked-tools">
			<strong>Available tools:</strong>
			<ul>
				{#each unlockedTools as tool}
					<li>{tool}</li>
				{/each}
			</ul>
		</div>

		<div class="locked-tools">
			<strong>Tools to unlock:</strong>
			<ul>
				{#each lockedTools as tool}
					<li>{tool}</li>
				{/each}
			</ul>
		</div>
	</div>
</section>

<style>
	.sb-container {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

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

	button {
        margin: 2rem;
        display: flex;
        justify-content: center;
        align-content: center;
        padding: 0.5rem 1rem;
    }

	.tools {
		background-color: transparent;
		border-radius: 10px;
		box-shadow: 2px 2px 2px 2px rgba(0, 0, 0, 0.2);
		max-width: 80%;
		display: flex;
		align-items: top;
		justify-content: center;
	}

	.unlocked-tools {
		margin: 2rem;
		display: inline-block;
		vertical-align: top;
	}

	.locked-tools {
		margin: 2rem;
		display: inline-block;
		vertical-align: top;
	}
	
	ul {
		list-style: square;
	}
</style>
