<script lang="ts">
	import { getPath } from '$lib/utils';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
    import { tools } from '$lib/stores';
    import Highchart from '../../../components/Highchart.svelte';

    let plotPaths = new Map([
        ['dft', ''],
        ['frf-gain', ''],
        ['frf-phase', '']
    ]);

    onMount(async () => {
        plotPaths.keys().forEach(async (endpoint: string) => {
            plotPaths.set(endpoint, await getPath(endpoint));
        });
    });
</script>

<h1>Modal Parameter Identification</h1>

<div class="plot-container">
    {#if $tools.find(tool => tool.name === 'Discrete Fourier transform' && tool.available)}
        <img src={plotPaths.get('dft')} alt='Discrete Fourier transform' class="dft plot" />
    {/if}
    {#if $tools.find(tool => tool.name === 'Frequency response function' && tool.available)}
        <img src={plotPaths.get('frf-gain')} alt='Frequency response function (gain)' class="frf-gain plot" />
        <img src={plotPaths.get('frf-phase')} alt='Frequency response function (phase)' class="frf-phase plot" />
    {/if}
    <Highchart />
</div>

<section>
	<button on:click={() => goto('/')}>Return to Dashboard</button>
</section>

<style>
    h1 {
		width: 100%;
		margin: 3rem 0rem;
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

	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}
</style>