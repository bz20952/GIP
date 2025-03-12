<script lang="ts">
    import { showResultsForm, progress } from "$lib/stores";
    import { removeItemAll } from "$lib/utils";
    import { emails } from "$lib/emails.json";
    import { tooltips } from "$lib/tooltips.json"
    import type { Email, Result } from "$lib/types";
    import Tooltip from "./Tooltip.svelte";

    export let emailId: number;
    const currentEmail = emails.find((email) => email.id === emailId) as Email;   
    const requiredResults = currentEmail?.results;
    const currentResult = requiredResults.find((result) => $progress.currentTask.currentSubtask.subtaskId === result.subtaskId) as Result;
    const currentTooltip = tooltips.find(tooltip => tooltip.id === currentResult.tooltipId);

    let submitted: boolean = false;

    function handleSubmit(event: Event) {
        submitted = true;
        $progress.currentTask.currentSubtask.feedbackStage = Math.min($progress.currentTask.currentSubtask.feedbackStage + 1, currentResult.feedback.length);
        $progress.currentTask.currentSubtask.attempts += 1;
        const formData = new FormData(event.target as HTMLFormElement);
        $progress.currentTask.currentSubtask.answer = formData.get(currentResult.name);
    }
</script>

<form on:submit|preventDefault={handleSubmit}>
    <div class="field">
        <label for={currentResult.name}>{currentResult.name}: </label>
        {#if currentResult.inputType === 'select'}
            <select name={currentResult.name} id={currentResult.name} bind:value={$progress.currentTask.currentSubtask.answer} required>
                {#each currentResult.options as option}
                    <option value={option}>{option}</option>
                {/each}
            </select>
        {:else if currentResult.inputType === 'text'}
            <input type="text" id={currentResult.name} name={currentResult.name} bind:value={$progress.currentTask.currentSubtask.answer} required>
        {:else if currentResult.inputType === 'number'}
            <input type="number" id={currentResult.name} name={currentResult.name} bind:value={$progress.currentTask.currentSubtask.answer} required>
        {:else if currentResult.inputType === 'none'}
            <i>This answer is read automatically.</i>
        {/if}
        <span>{currentResult.unit}<Tooltip displayImage={true} tooltipText={currentTooltip?.tooltipText} tooltipImage={currentTooltip?.tooltipImage}/></span>
    </div>
    <div class='btns'>
        <button class="back-btn" on:click={() => $showResultsForm = removeItemAll($showResultsForm, emailId)}>Back</button>
        <button class="submit-btn" type="submit">Submit</button>
        {#if submitted}
            <p class="success">Results submitted successfully!</p>
        {/if}
    </div>
</form>

<style>
    form {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .field {
        margin: 0.2rem 0;
    }

    label {
        margin-bottom: 0.5rem;
        margin-right: 1rem;
    }

    .btns {
        margin-top: 0.5rem;
    }

    .success {
        margin-top: 0.5rem;
        color: green;
    }
</style>
