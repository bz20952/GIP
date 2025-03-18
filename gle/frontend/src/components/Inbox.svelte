<script lang="ts">
  import { emails } from '$lib/emails.json';
  import ResultsForm from './ResultsForm.svelte';
  import Feedback from './Feedback.svelte';
  import { showResultsForm, showFeedback, progress } from '$lib/stores';
</script>

<div class="inbox-panel">
    <h1 class="inbox-header">Messages</h1>
    <div class="message-container">
      {#each emails.slice().reverse() as email}
        {#if email.id <= $progress.current + 1}
            <div class="email">
              {#if !$showResultsForm.includes(email.id) && !$showFeedback.includes(email.id)}
                <div class="sender">{email.sender}</div>
                <div class="subject">{email.subject}</div>
                <div class="body">{email.body}</div>
                <button class="submit-btn" on:click={() => $showResultsForm = [...$showResultsForm, email.id]}>Send results</button>
                <button class="fb-btn" on:click={() => $showFeedback = [...$showFeedback, email.id]}>View feedback</button>
              {:else if $showResultsForm.includes(email.id)}
                <ResultsForm emailId={email.id}/>
              {:else if $showFeedback.includes(email.id)}
                <Feedback emailId={email.id}/>
              {/if}
            </div>
        {/if}
      {/each}
    </div>
</div>

<style>
  .inbox-header {
    font-family: 'Segoe UI';
    font-size: 20pt;
    margin: 0.5rem;
  }

  .inbox-panel {
    width: 100%;
    max-width: 1000px;
    margin: auto;
    border: 1px solid #eee;
    border-radius: 10px;
    box-shadow: 2px 2px 2px 2px rgba(0, 0, 0, 0.2);
    background-color: transparent;
    /* overflow-y: scroll; */
  }

  .message-container {
    /* padding: 10px; */
    min-height: 10rem;
    max-height: 30rem;
    /* overflow-y: auto; */
  }

  .email {
    padding: 10px;
    border-bottom: 1px solid #eee;
    border-radius: 10px;
    border: 2px solid #b2c3d3;
    margin: 1rem;
  }

  .sender {
    font-weight: bold;
  }

  .subject {
    margin-top: 5px;
    font-style: italic;
    color: #ff3e00;
  }

  .submit-btn {
    padding: 5px 10px;
    margin-top: 0.5rem;
  }
</style>
