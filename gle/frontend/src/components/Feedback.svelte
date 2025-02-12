<script lang="ts">
  import { onMount } from 'svelte';
  import { showFeedback, progress, tools } from '$lib/stores';
  import { removeItemAll } from '$lib/utils';
  import { emails } from '$lib/emails.json';
  import Noti from './Noti.svelte';
	import type { Email, Task, Tool, Feedback } from '$lib/types';

  export let emailId: number;
  const currentEmail = emails.find((email) => email.id === emailId) as Email;
  const currentTask = $progress.tasks.find((task) => task.emailId === emailId) as Task;

  let feedbackText = 'There is no feedback yet for this task.';
  let showNotification: boolean = false;

  // On mounting this component, we compare the submitted answers to the correct answers and feed back accordingly.
  onMount(async () => {
      let correctAnswerCount: number = 0;
      let i = 0;

      const feedbackStage: Feedback | undefined = currentEmail.feedback.find((feedback: Feedback) => feedback.stage === currentTask.feedbackStage);
      currentTask.answers.forEach((answer: number) => {
        // Acceptable answer margin of +- 10%
        let upper_bound = 1.1*currentEmail.results[i].answer;
        let lower_bound = 0.9*currentEmail.results[i].answer;
        if (answer >= lower_bound && answer <= upper_bound) {
          correctAnswerCount += 1;
        } else {
          feedbackText = feedbackStage?.message as string;
        }
        i += 1;
      })

      // If all answers are correct or maximum feedback stage is reached, move to the next task and update progress and tools accordingly
      if (correctAnswerCount === currentEmail.results.length || feedbackStage?.stage === 3) {
        if (correctAnswerCount === currentEmail.results.length) {
          feedbackText = 'Well done!';  // Change this to be more encouraging
        }
        $progress.current = Math.max(emailId, $progress.current); // Update progress

        // Update tools with new unlocked ones
        currentEmail.unlocks.forEach((tool: string) => {
          const unlockedTool: Tool | undefined = $tools.find((t) => t.name === tool);
          if (unlockedTool) {
            unlockedTool.available = true;
          }
        });

        showNotification = true;
      }
  });
</script>

<!-- {#if showNotification}
  <Noti />
{/if} -->
<div class="feedback-container">
  <p>{feedbackText}</p>
  <button class="back-btn" on:click={() => $showFeedback = removeItemAll($showFeedback, emailId)}>Back</button>
</div>

<style>
    p {
        margin: 1rem;
        color: #333;
    }
</style>

