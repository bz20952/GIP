<script lang="ts">
  import { onMount } from 'svelte';
  import { feedback } from '$lib/stores';
//   import { PUBLIC_HOSTNAME } from '$env/static/public';
//   import { PUBLIC_BACKEND_PORT } from '$env/static/public';

  export let emailId;

  let feedbackText = 'There is no feedback to view for this task.';

  onMount(async () => {
    // try {
    //   const response = await fetch(`http://${PUBLIC_HOSTNAME}:${PUBLIC_BACKEND_PORT}/feedback?emailId=${emailId}`, { method: 'GET' }); // Replace with your backend URLemailId);
    //   if (response.ok) {
    //     const data = await response.json();
    //     feedbackText = data.feedback;
    //   } else {
    //     console.error('Failed to fetch feedback');
    //   }
    // } catch (error) {
    //   console.error('Error fetching feedback:', error);
    // }
    return
  });
</script>

<div class="feedback-container">
  <p>{feedbackText}</p>

  <button class="back-btn" on:click={() => $feedback = false}>Back</button>
</div>

<style>
    p {
        margin: 1rem;
        color: #333;
    }
</style>

