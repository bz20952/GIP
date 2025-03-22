<script lang="ts">
	import { getPath } from '$lib/utils';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
    import { testOptions, tools } from '$lib/stores';

    let plotPaths = new Map()

    onMount(() => {
        $tools.filter(tool => tool.type === 'analysis').forEach(async (analysisTool) => {
            plotPaths = plotPaths.set(analysisTool.endpoint, await getPath((analysisTool.endpoint as string), $testOptions))
        })
    });
</script>

<svelte:head>
	<title>Frequency Domain Analysis</title>
	<meta name="description" content="Frequency Domain Analysis" />
</svelte:head>

<h1>Frequency Domain Analysis</h1>

<section>
    <div class="plots-container">
        {#if $tools.filter(tool => (tool.type === 'analysis' && tool.available)).length === 0}
            <h2>No tools available yet.</h2>
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
            <div class="freq">
                <i class="info">Here you can specify a range of frequencies over which you want to identify modal parameters. The smaller the range, the clearer the plots will be.</i>
                <br><br>
                <label for="lowerCutoff">Lower cutoff frequency (Hz): </label>
                <input type="number" name="lowerCutoff" bind:value={$testOptions.lowerCutoff}/>
                <br><br>
                <label for="upperCutoff">Upper cutoff frequency (Hz): </label>
                <input type="number" name="upperCutoff" bind:value={$testOptions.upperCutoff}/>
                <br><br>
                <button class='bode-and-nyquist' on:click={() => goto('/toolkit/analyse/identify')}>Identify</button>
            </div>
        {/if}
    </div>
	<!-- <button class='return' on:click={() => goto('/')}>Return to Dashboard</button> -->
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

    .freq {
        max-width: 40%;
    }
</style>