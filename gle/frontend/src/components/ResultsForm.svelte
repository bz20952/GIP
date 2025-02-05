<script lang="ts">
    import { showResultsForm, progress } from "$lib/stores";
    import { removeItemAll } from "$lib/utils.ts";
    import { emails } from "$lib/emails.json";

    export let emailId: number;
    const currentEmail = emails.find((email) => email.id === emailId) as any;
    const currentTask = $progress.tasks.find((task) => task.emailId === emailId) as any;
    const requiredResults = currentEmail?.results as Array<any>; 

    let submitted: boolean = false;

    function handleSubmit(event: Event) {
        submitted = true;
        currentTask.feedbackStage = Math.min(currentTask.feedbackStage + 1, 3);  // Move to the next feedback stage after each submission (max feedback stage = 3)
        const formData = new FormData(event.target as HTMLFormElement);
        let i = 0;  // Answer indexer
        requiredResults?.forEach((result) => {
            currentTask.answers[i] = formData.get(result.name);
            i += 1;
        })
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
