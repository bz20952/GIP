<script lang="ts">
    import { onMount } from 'svelte';
    import { sendApiRequest } from '$lib/api';
    import { PUBLIC_HOSTNAME, PUBLIC_BACKEND_PORT } from '$env/static/public';
	import { goto } from '$app/navigation';

    let filterType: string = 'none';
    let timeDomainPlotPath: string;
    let animationPath: string;

    onMount(async () => {
        await getTimeDomainPlotPath();
        console.log(timeDomainPlotPath);
        await getAnimationPath();
    });

    async function getTimeDomainPlotPath() {
        const result = await sendApiRequest('time-domain', 'GET', {});
        timeDomainPlotPath = `http://${PUBLIC_HOSTNAME}:${PUBLIC_BACKEND_PORT}/images/${result.message}`;
    };

    async function getAnimationPath() {
        const result = await sendApiRequest('animate', 'GET', {});
        animationPath = `http://${PUBLIC_HOSTNAME}:${PUBLIC_BACKEND_PORT}/images/${result.message}`;
    };
</script>

<h1>Signal Processing</h1>

<div class="plot-container">
    <img src={timeDomainPlotPath} alt='Time domain plot' class="time-domain" />
    <img src={timeDomainPlotPath} alt='Animation' class="animation" />
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
                <label for="cutoff-freq">Cutoff frequency: </label>
                <input type="number" name="cutoff-freq" />
            {:else if filterType === 'band-pass'}
                    <label for="lower-cutoff">Lower cutoff frequency: </label>
                    <input type="number" name="lower-cutoff" />
                    <label for="upper-cutoff">Upper cutoff frequency: </label>
                    <input type="number" name="upper-cutoff" />
            {/if}
        </div>
    </div>

    <div>
        <button class="dft" on:click={() => goto('/toolkit/analyse')}>Compute DFT</button>
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

    .time-domain {
        width: 40%;
        height: auto;
        margin: 0 1rem;
    }

    .animation {
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

    .dft {
        margin: 1rem;
    }
</style>