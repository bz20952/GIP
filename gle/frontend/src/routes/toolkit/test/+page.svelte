<script lang="ts">
    import { goto } from '$app/navigation';
    import { tools } from '$lib/stores';
    import { testOptions } from '$lib/stores';

    let showSpinner = false;

    const locations = ['0', 'l/4', 'l/2', '3l/4', 'l'];

    function limitAccelSelection(event: Event) {
        const checkboxes = document.querySelectorAll('.checkbox-row input[type="checkbox"]');
        const checkedCount = Array.from(checkboxes).filter(checkbox => (checkbox as HTMLInputElement).checked).length;
        
        if (checkedCount > 3) {
            (event.target as HTMLInputElement).checked = false;
        } else if (checkedCount < 1) {
            (event.target as HTMLInputElement).checked = true;
        }
    }
</script>

<svelte:head>
	<title>Test Setup</title>
	<meta name="description" content="Test setup" />
</svelte:head>

<h1>Test Setup</h1>

<div class="instructions">
    You can position up to 3 accelerometers on the beam. The excitation location can be selected by moving the shaker icon <img class='demo-icon' src="$lib/images/speaker.png" alt="Shaker" />.
</div>

<section class="experiment">
    <div class="checkbox-row">
        <input class='accelerometer' type="checkbox" bind:checked={$testOptions['accelerometers']['A0']} on:change={limitAccelSelection} />
        <input class='accelerometer' type="checkbox" bind:checked={$testOptions['accelerometers']['A1']} on:change={limitAccelSelection} />
        <input class='accelerometer' type="checkbox" bind:checked={$testOptions['accelerometers']['A2']} on:change={limitAccelSelection} />
        <input class='accelerometer' type="checkbox" bind:checked={$testOptions['accelerometers']['A3']} on:change={limitAccelSelection} />
        <input class='accelerometer' type="checkbox" bind:checked={$testOptions['accelerometers']['A4']} on:change={limitAccelSelection} />
    </div>

    <img class="beam" src="$lib/images/beam.png" alt="Free-free beam" />

    <div class="shaker-slider">
        <input type="range" min=0 max={locations.length - 1} step=1 bind:value={$testOptions['shakerPosition']}/>
    </div>

    <div class="extra-params">
        <div class="excitation-type">
            <label for="excitation-type">Excitation type:</label>
            <select name="excitation-type" id="excitation-type" bind:value={$testOptions['excitationType']}>
                {#each $tools as tool}
                    {#if tool.available && tool.type === "excitation"}
                        <option value={tool.name}>{tool.name}</option>
                    {/if}
                {/each}
            </select>
            {#if $testOptions['excitationType'] === 'Hammer testing'}
                <label for="tip-hardness">Tip hardness:</label>
                <select name="tip-hardness" id="tip-hardness" bind:value={$testOptions['tipHardness']}>
                    <option value='Soft'>Soft</option>
                    <option value='Hard'>Hard</option>
                </select>
            {/if}
        </div>

        <div class="sampling-slider">
            <label for="sampling-freq">Sampling frequency: <strong>{$testOptions['samplingFreq']} Hz</strong></label>
            <input type="range" min="512" max="2048" step="512" bind:value={$testOptions['samplingFreq']} />
        </div>
    </div>

    <button class="run-test" on:click={() => goto('/toolkit/process')}>Run Test</button>
    {#if showSpinner}
        <div class="fa spinner"></div>
    {/if}
</section>

<style>
    h1 {
        font-family: 'Segoe UI', sans-serif;;
        /* -webkit-text-stroke: 1px #2c6392; */
        margin: 0.5rem;
    }

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

    .demo-icon {
        height: 1.5em;
        display: inline;
    }

    section {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .checkbox-row {
        display: flex;
        width: 100%;
        gap: 21%;
        margin: 5rem 0 1rem 0;
        justify-content: center;
        align-items: center;
    }

    .accelerometer {
        cursor: pointer;
        border-radius: 10%;
        border-color: #2c6392;
    }

    .shaker-slider {
        display: flex;
        width: 100%;
        margin: 2rem 0 1rem 0;
        justify-content: center;
        align-items: center;
    }

    .shaker-slider input[type="range"] {
        width: 100%;
        -webkit-appearance: none;
        background: transparent;
    }

    .shaker-slider input[type="range"]::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        height: 60px;
        width: 60px;
        background-image: url('$lib/images/speaker.png');
        background-size: cover;
        cursor: pointer;
    }

    .extra-params {
        width: 100%;
    }

    .excitation-type {
        margin: 1rem;
    }

    .excitation-type select {
        background-color: azure;
        border-radius: 10px;
        margin: 0 1rem;
        border: #2c6392 solid 1px;
    }

    .sampling-slider {
        width: 80%;
        margin: 2rem 0 2rem 1rem;
    }

    .sampling-slider label {
        padding: 0 2rem 0 0;
    }

    .sampling-slider input[type="range"] {
        -webkit-appearance: none;
        padding: 1px;
        width: 50%;
        border-radius: 5px;
        background-color: azure;
        border: 1px solid #2c6392;
        justify-content: center;
        align-items: center;
    }

    .sampling-slider input[type="range"]::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        height: 16px;
        width: 16px;
        border-radius: 25%;
        background-color: #2c6392;
        background-size: cover;
        cursor: pointer;
    }

    .run-test {
        margin: 1rem;
        width: 10%;
        display: flex;
        justify-content: center;
        align-content: center;
        padding: 0.5rem 0;
    }
</style>