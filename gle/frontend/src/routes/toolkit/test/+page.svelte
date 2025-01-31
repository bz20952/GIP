<!-- Ideally this will have some customisable test setup animation of the beam. Where:
- Accelerometers can be placed.
- Excitation location can be selected.
- Excitation type can be selected.
- Sampling frequency can be selected. -->

<script lang="ts">
    import { goto } from '$app/navigation';
    import beam from '$lib/images/beam.png';
    import speaker from '$lib/images/speaker.png';
    import { tools } from '$lib/stores';

    let accel1: boolean = false;
    let accel2: boolean = false;
    let accel3: boolean = false;
    let accel4: boolean = false;
    let accel5: boolean = false;
    let shakerPosition: number;
    let samplingFreq: number;

    function limitAccelSelection(event: Event) {
        const checkboxes = document.querySelectorAll('.checkbox-row input[type="checkbox"]');
        const checkedCount = Array.from(checkboxes).filter(checkbox => (checkbox as HTMLInputElement).checked).length;
        
        if (checkedCount > 3) {
            (event.target as HTMLInputElement).checked = false;
        }
    }
</script>

<svelte:head>
	<title>Test Setup</title>
	<meta name="description" content="Test setup" />
</svelte:head>

<h1>Test Setup</h1>

<div class="instructions">
    You can position up to 3 accelerometers on the beam. The excitation location can be selected by moving the shaker icon <img class='demo-icon' src={speaker} alt="Shaker" />.
</div>

<section class="experiment">
    <div class="checkbox-row">
        <input class='accelerometer' type="checkbox" bind:checked={accel1} on:change={limitAccelSelection} />
        <input class='accelerometer' type="checkbox" bind:checked={accel2} on:change={limitAccelSelection} />
        <input class='accelerometer' type="checkbox" bind:checked={accel3} on:change={limitAccelSelection} />
        <input class='accelerometer' type="checkbox" bind:checked={accel4} on:change={limitAccelSelection} />
        <input class='accelerometer' type="checkbox" bind:checked={accel5} on:change={limitAccelSelection} />
    </div>

    <img class="beam" src={beam} alt="Free-free beam" />

    <div class="shaker-slider">
        <input type="range" min="1" max="5" step="1" bind:value={shakerPosition}/>
    </div>

    <div class="excitation-type">
        <label for="excitation-type">Excitation type: </label>
        <select name="excitation-type" id="excitation-type">
            {#each $tools as tool}
                {#if tool.available && tool.type === "excitation"}
                    <option value={tool.name}>{tool.name}</option>
                {/if}
            {/each}
        </select>
    </div>

    <div class="sampling-slider">
        <label for="sampling-freq">Sampling frequency: <strong>{samplingFreq} kHz</strong></label>
        <input type="range" min="100" max="600" step="100" bind:value={samplingFreq} />
    </div>

    <button class="run-test" on:click={() => goto('/toolkit/process')}>Run Test</button>
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

    .excitation-type {
        margin: 1rem;
    }

    .excitation-type select {
        background-color: azure;
        border-radius: 10px;
        margin: 0 1rem;
    }

    .sampling-slider {
        display: flex;
        width: 100%;
        margin: 2rem 0;
        justify-content: center;
        align-items: center;
    }

    .sampling-slider label {
        padding: 0 2rem;
    }

    .sampling-slider input[type="range"] {
        -webkit-appearance: none;
        padding: 1px 0;
        width: 50%;
        border-radius: 5px;
        background-color: azure;
        border: 1px solid #2c6392;
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
        background-color: #2c6392;
        border-radius: 10px;
        color: white;
        margin: 1rem;
        width: 10%;
        display: flex;
        justify-content: center;
        align-content: center;
        padding: 0.5rem 0;
    }

    .run-test:hover {
        background-color: #3b76a9;
    }
</style>