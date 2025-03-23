<script lang="ts">
	import { getPath } from '$lib/utils';
	import { onMount } from 'svelte';
    import { testOptions, tools } from '$lib/stores';
    import { goto } from '$app/navigation';

    let plotPaths = new Map()

    onMount(() => {
        $tools.filter(tool => tool.type === 'identification').forEach(async (analysisTool) => {
            plotPaths = plotPaths.set(analysisTool.endpoint, await getPath((analysisTool.endpoint as string), $testOptions))
        })
    });
</script>

<svelte:head>
	<title>Modal Parameter Identification</title>
	<meta name="description" content="Modal parameter identification" />
</svelte:head>

<h1>Modal Parameter Identification</h1>

<section>
    <div class="plots-container">
        {#if $tools.filter(tool => (tool.type === 'identification' && tool.available)).length === 0}
            <h2>No identification tools available yet.</h2>
        {:else if $testOptions.excitationType === 'Free vibration'}
            <h2>No forcing measurements available yet.</h2>
        {:else}
            {#each plotPaths.keys() as toolEndpoint}
                {#if $tools.find(tool => tool.endpoint == toolEndpoint)?.available}
                    {#if plotPaths.get(toolEndpoint)}
                        <div class="plot-container">
                            <img src={plotPaths.get(toolEndpoint)} alt={toolEndpoint} class="plot" />
                            <a class="fullscreen-link" href={plotPaths.get(toolEndpoint)} target="_blank" rel="noopener noreferrer">Open fullscreen</a>
                        </div>
                    {:else}
                        <i class="fa fa-spinner fa-pulse"></i>
                    {/if}
                {/if}
            {/each}
        {/if}
    </div>
    <button class='back' on:click={() => goto('/toolkit/analyse')}>Back</button>
</section>

<style>
    h1 {
		width: 100%;
		margin: 3rem 0rem;
	}

    section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

    .fa-spinner {
        font-size: 2rem;
        padding: 0 2rem;
    }

	.plots-container {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        width: 150%;
    }

    .plot-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0 2rem;
        width: 40rem;
    }

    .fullscreen-link {
        margin: 1rem;
    }

    .plot {
        width: 100%;
        height: auto;
        box-shadow: 2px 2px 2px 2px rgba(0, 0, 0, 0.2);
        border-radius: 10px;
    }

    .back {
        margin: 4rem;
    }
</style>