<script lang="ts">
  import { onMount } from 'svelte';
  import { showFeedback, progress, tools, testOptions } from '$lib/stores';
  import { removeItemAll } from '$lib/utils';
  import { emails } from '$lib/emails.json';
  import Noti from './Noti.svelte';
	import type { Email, Tool, Feedback, Result, TestOptions } from '$lib/types';

  export let emailId: number;
  const currentEmail = emails.find((email) => email.id === emailId) as Email;  

  let feedbackText = {
    message: 'There is no feedback yet.',
    colour: 'black'
  };
  let showNotification: boolean = false;

  // On mounting this component, we compare the submitted answers to the correct answers and feed back accordingly.
  onMount(async () => {
      const result = currentEmail.results.find((result: Result) => result.subtaskId === $progress.currentTask.currentSubtask.subtaskId) as Result;
      const feedbackStage = result.feedback.find((feedback: Feedback) => feedback.stage === $progress.currentTask.currentSubtask.feedbackStage) as Feedback;

      if (result.inputType === 'text' || result.inputType === 'select') {
        if ($progress.currentTask.currentSubtask.answer === result.answer) {
          $progress.currentTask.currentSubtask.correct = true;
        }
      } else if (result.inputType === 'number') {
        // Acceptable answer margin of +- 10%
        let upper_bound = 1.1*(result.answer as number);
        let lower_bound = 0.9*(result.answer as number);
        if ($progress.currentTask.currentSubtask.answer as number >= lower_bound && $progress.currentTask.currentSubtask.answer as number <= upper_bound) {
          $progress.currentTask.currentSubtask.correct = true;
        }
      } else if (result.inputType === 'none') {
        Object.keys(result.answer).forEach((key) => {
          if (result.answer[key] === $testOptions[key as keyof TestOptions]) {
            $progress.currentTask.currentSubtask.correct = true;
          }
        })
      }

      if ($progress.currentTask.currentSubtask.correct) {
        feedbackText = {
          message: result.praise,
          colour: 'green'
        }
      } else {
        feedbackText = {
          message: feedbackStage.message as string,
          colour: 'red'
        }
      }

      // If all answers are correct or maximum feedback stage is reached, move to the next task and update progress and tools accordingly
      if ($progress.currentTask.currentSubtask.subtaskId === currentEmail.results.length) {
        if ($progress.currentTask.currentSubtask.correct || $progress.currentTask.currentSubtask.feedbackStage === result.feedback.length){
          $progress.current = Math.max(emailId, $progress.current); // Update progress
          $progress.currentTask.emailId += 1;
          $progress.currentTask.currentSubtask.subtaskId = 1;
          $progress.currentTask.currentSubtask.feedbackStage = 0;
          $progress.currentTask.currentSubtask.answer = undefined;
          $progress.currentTask.currentSubtask.correct = false;

          // Update tools with new unlocked ones
          currentEmail.unlocks.forEach((tool: string) => {
            const unlockedTool: Tool | undefined = $tools.find((t) => t.name === tool);
            if (unlockedTool) {
              unlockedTool.available = true;
            }
          });
          showNotification = true;
        }
      } else if ($progress.currentTask.currentSubtask.correct || $progress.currentTask.currentSubtask.feedbackStage === result.feedback.length) {
        $progress.currentTask.currentSubtask.subtaskId += 1;
        $progress.currentTask.currentSubtask.feedbackStage = 0;
        $progress.currentTask.currentSubtask.answer = undefined;
        $progress.currentTask.currentSubtask.correct = false;
      }
  });
</script>

<!-- {#if showNotification}
  <Noti />
{/if} -->
<div class="feedback-container">
  <p style="color: {feedbackText.colour}">{feedbackText.message}</p>
  <button class="back-btn" on:click={() => $showFeedback = removeItemAll($showFeedback, emailId)}>Back</button>
</div>

<style>
    p {
        margin: 1rem;
        color: #333;
    }
</style>

