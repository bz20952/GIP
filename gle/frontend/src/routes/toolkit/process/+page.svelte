<script lang="ts">
    import { onMount } from 'svelte';
    import { getPath } from '$lib/utils';
	import { goto } from '$app/navigation';
    import { testOptions } from '$lib/stores';

    let plotPaths = new Map([
        ['time-domain', ''],
        ['forcing', ''],
        ['animate', '']
    ]);

    onMount(async () => {
        plotPaths.keys().forEach(async (endpoint: string) => {
            plotPaths = plotPaths.set(endpoint, await getPath(endpoint, $testOptions));
        });
    });

    // onMount(async () => {
    //     plotPaths.keys().forEach((plotType: string) => {
    //         plotPaths.set(plotType, getPath($testOptions, plotType));
    //     });
    // });
</script>

<svelte:head>
	<title>Signal processing</title>
	<meta name="description" content="Signal processing" />
</svelte:head>

<h1>Signal Processing</h1>

<div class="plot-container"> 
    {#if plotPaths.get('time-domain')}
        <img src={plotPaths.get('time-domain')} alt='Time-domain response' class="time-domain plot" />
    {:else}
        <i class="fa fa-spinner fa-pulse"></i>
    {/if}
    {#if plotPaths.get('forcing')}
        <img src={plotPaths.get('forcing')} alt='Forcing signal' class="forcing plot" />
    {:else}
        <i class="fa fa-spinner fa-pulse"></i>
    {/if}
    {#if plotPaths.get('animate')}
        <img src={plotPaths.get('animate')} alt='Animation' class="animation plot" />
    {:else}
        <i class="fa fa-spinner fa-pulse"></i>
    {/if}
</div>

<section>
    <div class="filter">
        <label for="filter-type">Filter type: </label>
        <select name="filter-type" bind:value={$testOptions.filterType}>
            <option value="none">None</option>
            <option value="lowPass">Low-pass</option>
            <option value="highPass">High-Pass</option>
            <option value="bandPass">Band-Pass</option>
        </select>
        <div class="freq">
            {#if $testOptions.filterType === 'lowPass'}
                <label for="cutoffFreq">Cutoff frequency (Hz): </label>
                <input type="number" name="cutoffFreq" bind:value={$testOptions.upperCutoff} />
            {:else if $testOptions.filterType === 'highPass'}
                <label for="cutoff-freq">Cutoff frequency (Hz): </label>
                <input type="number" name="cutoffFreq" bind:value={$testOptions.lowerCutoff} />
            {:else if $testOptions.filterType === 'bandPass'}
                <label for="lowerCutoff">Lower cutoff frequency (Hz): </label>
                <input type="number" name="lowerCutoff" bind:value={$testOptions.lowerCutoff}/>
                <label for="upperCutoff">Upper cutoff frequency (Hz): </label>
                <input type="number" name="upperCutoff" bind:value={$testOptions.upperCutoff}/>
            {/if}
        </div>
    </div>

    <div>
        <button class="analyse" on:click={() => goto('/toolkit/analyse')}>Analyse</button>
    </div>
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

    .plot-container {
        display: flex;
        /* flex-direction: row; */
        justify-content: center;
        align-items: center;
    }

    .plot {
        width: 40%;
        height: auto;
        margin: 0 1rem;
        box-shadow: 2px 2px 2px 2px rgba(0, 0, 0, 0.2);
        border-radius: 10px;
    }

    .filter {
        width: 100%;
    }

    .filter label {
        padding-right: 0 1rem;
    }

    .filter input {
        margin: 0 1rem;
    }

    .freq {
        margin: 1rem 0;
    }

    .freq input {
        width: 20%;
    }

    .analyse {
        margin: 1rem;
    }
</style>