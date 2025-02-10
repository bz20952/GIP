<script lang="ts">
    import { onMount } from 'svelte';
    import { getPath } from '$lib/utils';
	import { goto } from '$app/navigation';

    let filterType: string = 'none';

    let plotPaths = new Map([
        ['time-domain', ''],
        ['forcing', ''],
        ['animate', '']
    ]);

    onMount(async () => {
        plotPaths.keys().forEach(async (endpoint: string) => {
            plotPaths.set(endpoint, await getPath(endpoint));
        });
    });
</script>

<h1>Signal Processing</h1>

<div class="plot-container">
    <img src={plotPaths.get('time-domain')} alt='Time-domain response' class="time-domain plot" />
    <img src={plotPaths.get('forcing')} alt='Forcing signal' class="forcing plot" />
    <img src={plotPaths.get('animate')} alt='Animation' class="animation plot" />
</div>

<section>
    <div class="filter">
        <label for="filter-type">Filter type: </label>
        <select name="filter-type" bind:value={filterType}>
            <option value="none">None</option>
            <option value="low-pass">Low-pass</option>
            <option value="high-pass">High-pass</option>
            <option value="band-pass">Band-pass</option>
        </select>
        <div class="cutoff-freq">
            {#if filterType === 'low-pass' || filterType === 'high-pass'}
                <label for="cutoff-freq">Cutoff frequency (Hz): </label>
                <input type="number" name="cutoff-freq" />
            {:else if filterType === 'band-pass'}
                    <label for="lower-cutoff">Lower cutoff frequency (Hz): </label>
                    <input type="number" name="lower-cutoff" />
                    <label for="upper-cutoff">Upper cutoff frequency (Hz): </label>
                    <input type="number" name="upper-cutoff" />
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

    .plot-container {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
    }

    .plot {
        width: 40%;
        height: auto;
        margin: 0 1rem;
    }

    .filter {
        width: 100%;
    }

    .filter label {
        padding-right: 0 1rem;
    }

    .filter input {
        background-color: azure;
        border-radius: 10px;
        margin: 0 1rem;
        border: #2c6392 solid 1px;
        color: black;
    }

    .cutoff-freq {
        margin: 1rem 0;
    }

    .cutoff-freq input {
        width: 20%;
    }

    .analyse {
        margin: 1rem;
    }
</style>