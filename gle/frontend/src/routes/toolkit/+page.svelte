<script lang="ts">
	import { goto } from '$app/navigation';
	import { tools } from '$lib/stores';
	import Tooltip from '../../components/Tooltip.svelte';

	let unlockedTools = $tools.filter(tool => tool.available);
	let lockedTools = $tools.filter(tool => !tool.available);
</script>

<svelte:head>
	<title>Toolkit</title>
	<meta name="description" content="Toolkit" />
</svelte:head>

<h1>
	Welcome to your Toolkit!
</h1>

<div class="instructions">
	Here you can see all of your available tools and start new experiments.<br>
	Every experiment consists of three stages; <strong>test setup</strong>, <strong>signal processing</strong> and <strong>modal parameter identification</strong>.<br>
	By clicking the button below, you can use your available tools to gather results.<br>
</div>

<section>
	
	<button class='new-exp' on:click={() => goto('/toolkit/test')}>
		Start a new experiment!
	</button>

	<div class='tools'>
		<div class="unlocked-tools">
			<strong style="color: green;">Available tools</strong>
			<br>
			{#each unlockedTools as tool}
				<Tooltip displayText={tool.name} tooltipText={tool.description} />
				<br>
			{/each}
		</div>

		<div class="locked-tools">
			<strong style="color: orange;">Tools to unlock</strong>
			<br>
			{#each lockedTools as tool}
				<Tooltip displayText={tool.name} tooltipText={tool.description} />
				<br>
			{/each}
		</div>
	</div>
</section>

<style>
    .instructions {
        font-family: 'Segoe UI';
        font-size: 16pt;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 2px 2px 2px 2px rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        padding: 0.5rem;
        background-color: azure;
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
		min-width: 60%;
		display: flex;
		align-items: top;
		justify-content: center;
		text-align: center;
	}

	.unlocked-tools {
		margin: 2rem;
		display: inline-block;
		vertical-align: top;
		width: 50%;
		/* border: 1px solid #860e0e; */
	}

	.locked-tools {
		margin: 2rem;
		display: inline-block;
		vertical-align: top;
		width: 50%;
		/* border: 1px solid #df3333; */
	}
</style>
