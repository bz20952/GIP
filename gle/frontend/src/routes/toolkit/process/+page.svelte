<script lang="ts">
    import { onMount } from 'svelte';
    import { getPath } from '$lib/utils';
	import { goto } from '$app/navigation';
    import { testOptions } from '$lib/stores';

    let plotPaths = new Map([
        ['time-domain', ''],
        ['forcing', ''],
        // ['animate', '']
    ]);

    onMount(() => {
        plotPaths.keys().forEach(async (endpoint: string) => {
            plotPaths = plotPaths.set(endpoint, await getPath(endpoint, $testOptions));
        });
    });
</script>

<svelte:head>
	<title>Signal processing</title>
	<meta name="description" content="Signal processing" />
</svelte:head>

<h1>Signal Processing</h1>

<section>
    <div class="plots-container"> 
        {#if plotPaths.get('time-domain')}
            <div class="plot-container">
                <img src={plotPaths.get('time-domain')} alt='Time-domain response' class="time-domain plot" />
                <a class="fullscreen-link" href={plotPaths.get('time-domain')} target="_blank" rel="noopener noreferrer">Open fullscreen</a>
            </div>
        {:else}
            <i class="fa fa-spinner fa-pulse"></i>
        {/if}
        {#if $testOptions.excitationType !== 'Free vibration'}
            {#if plotPaths.get('forcing')}
                <div class="plot-container">
                    <img src={plotPaths.get('forcing')} alt='Forcing signal' class="forcing plot" />
                    <a class="fullscreen-link" href={plotPaths.get('forcing')} target="_blank" rel="noopener noreferrer">Open fullscreen</a>
                </div>
            {:else}
                <i class="fa fa-spinner fa-pulse"></i>
            {/if}
        {/if}
        <!-- {#if plotPaths.get('animate')}
            <div class="plot-container">
                <img src={plotPaths.get('animate')} alt='Animation' class="animation plot" />
                <a class="fullscreen-link" href={plotPaths.get('animate')} target="_blank" rel="noopener noreferrer">Open fullscreen</a>
            </div>
        {:else}
            <i class="fa fa-spinner fa-pulse"></i>
        {/if} -->
    </div>

    <!-- <div class="filter">
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
    </div> -->

    <button class="analyse" on:click={() => goto('/toolkit/analyse')}>Analyse</button>
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

    /* .filter {
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
    } */

    .analyse {
        margin: 4rem;
    }
</style>