<script lang="ts">
	import { goto } from '$app/navigation';
  import emails from '$lib/emails.json';
  import ResultsForm from './ResultsForm.svelte';
  import Feedback from './Feedback.svelte';
  import { resultsForm, feedback } from '$lib/stores';
</script>

  <div class="inbox-panel">
      <h1 class="inbox-header">Messages</h1>
      {#each emails.emails as email}
          <div class:email class:read={email.read}>
            {#if !$resultsForm && !$feedback}
              <div class="sender">{email.sender}</div>
              <div class="subject">{email.subject}</div>
              <div class="body">{email.body}</div>
              <button class="submit-btn" on:click={() => $resultsForm = true}>Send results</button>
              <button class="fb-btn" on:click={() => $feedback = true}>View feedback</button>
            {:else if $resultsForm}
              <ResultsForm requiredResults={email.results}/>
            {:else if $feedback}
              <Feedback emailId={email.id}/>
            {/if}
          </div>
      {/each}
  </div>

<style>
  .inbox-header {
    font-family: 'Segoe UI';
    font-size: 20pt;
    margin: 0.5rem;
  }

  .inbox-panel {
    width: 100%;
    max-width: 600px;
    margin: auto;
    border: 1px solid #eee;
    border-radius: 10px;
    box-shadow: 2px 2px 2px 2px rgba(0, 0, 0, 0.2);
    overflow: hidden;
    background-color: transparent;
  }

  .email {
    padding: 10px;
    border-bottom: 1px solid #eee;
    border-radius: 10px;
    border: 1px solid #a3a6a8;
    margin: 1rem;
  }

  /* .email:hover {
    background-color: rgb(236, 241, 241);
  } */

  .email.read {
    background-color: #b4dc8d;
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
