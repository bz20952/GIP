<script lang="ts">
    import { resultsForm } from "$lib/stores";

    export let requiredResults;

    let submitted: boolean = false;

    function handleSubmit(event: Event) {
        submitted = true;
        return event
    }
</script>

<form on:submit|preventDefault={handleSubmit}>
    {#each requiredResults as result}
        <div class="field">
            <label for={result.name}>{result.name}: </label>
            <input type="text" id={result.name} name={result.name} required>
            <span>{result.unit}</span>
        </div>
    {/each}
    <div class='btns'>
        <button class="back-btn" on:click={() => $resultsForm = false}>Back</button>
        <button class="submit-btn" type="submit">Submit</button>
        {#if submitted}
            <p>Results submitted successfully!</p>
        {/if}
    </div>
</form>

<style>
    form {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    label {
        margin-bottom: 0.5rem;
    }

    input[type="text"] {
        color: black;
        padding: 0.5rem;
        font-size: 1rem;
        margin-bottom: 1rem;
        border-radius: 10px;
    }

    .btns {
        margin-top: 0.5rem;
    }
</style>
