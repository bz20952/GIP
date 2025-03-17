<script lang="ts">
  import { onMount } from 'svelte';
  import { showFeedback, progress, tools, testOptions } from '$lib/stores';
  import { removeItemAll, sendApiRequest } from '$lib/utils';
  import { emails } from '$lib/emails.json';
  import Noti from './Noti.svelte';
	import type { Email, Tool, Feedback, Result, TestOptions, DisplayMessage } from '$lib/types';

  export let emailId: number;
  const email = emails.find((email) => email.id === emailId) as Email;  
  const result = email.results.find((result: Result) => result.subtaskId === $progress.currentTask.currentSubtask.subtaskId) as Result;
  
  let showNotification: boolean = false;

  // On mounting this component, we compare the submitted answers to the correct answers and feed back accordingly.
  onMount(() => {
      if (emailId === $progress.currentTask.emailId) {

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

        const feedbackStage = result.feedback.find((feedback: Feedback) => feedback.stage === $progress.currentTask.currentSubtask.feedbackStage) as Feedback;
        if ($progress.currentTask.currentSubtask.correct) {
          progress.update(store => {
            return {
              ...store,
              displayMessage: $progress.displayMessage.map(item =>
                item.emailId === emailId
                  ? { emailId: emailId, colour: 'green', message: result.praise }
                  : item
              )
            }
          })
        } else {
          progress.update(store => {
            return {
              ...store,
              displayMessage: $progress.displayMessage.map(item =>
                item.emailId === emailId
                  ? { emailId: emailId, colour: 'red', message: feedbackStage.message }
                  : item
              )
            }
          })
        }

        // If all answers are correct or maximum feedback stage is reached, move to the next task and update progress and tools accordingly
        if ($progress.currentTask.currentSubtask.subtaskId === email.results.length) {

          // The following should only be called when the last subtask in a task has been completed
          if ($progress.currentTask.currentSubtask.correct || ($progress.currentTask.emailId !== emails.length && $progress.currentTask.currentSubtask.feedbackStage === result.feedback.length)) {

            // Stop tracking if final task is complete
            if ($progress.currentTask.emailId === emails.length) {
              sendApiRequest('stop-tracking', 'POST', { serialNumber: $testOptions.serialNumber, subtaskId: $progress.currentTask.currentSubtask.subtaskId, timestamp: Math.floor(Date.now() / 1000), attempts: $progress.currentTask.currentSubtask.attempts });
            };

            $progress.current = Math.max(emailId, $progress.current); // Update progress
            $progress.currentTask.emailId += 1;
            $progress.currentTask.currentSubtask.subtaskId = 1;
            $progress.currentTask.currentSubtask.feedbackStage = 0;
            $progress.currentTask.currentSubtask.attempts = 0;
            $progress.currentTask.currentSubtask.answer = undefined;
            $progress.currentTask.currentSubtask.correct = false;

            // Update tools with new unlocked ones
            email.unlocks.forEach((tool: string) => {
              const unlockedTool: Tool | undefined = $tools.find((t) => t.name === tool);
              if (unlockedTool) {
                unlockedTool.available = true;
              }
            });
            showNotification = true;  // Notify user of new task

            // If has just moved onto final task, start tracking subtask one of final task
            if ($progress.currentTask.emailId === emails.length) {
              sendApiRequest('start-tracking', 'POST', { serialNumber: $testOptions.serialNumber, subtaskId: $progress.currentTask.currentSubtask.subtaskId, timestamp: Math.floor(Date.now() / 1000) });
            } ;
          }
      } else if ($progress.currentTask.currentSubtask.correct || ($progress.currentTask.emailId !== emails.length && $progress.currentTask.currentSubtask.feedbackStage === result.feedback.length)) {
        if ($progress.currentTask.emailId === emails.length) {
          sendApiRequest('stop-tracking', 'POST', { serialNumber: $testOptions.serialNumber, subtaskId: $progress.currentTask.currentSubtask.subtaskId, timestamp: Math.floor(Date.now() / 1000), attempts: $progress.currentTask.currentSubtask.attempts });
        };

        $progress.currentTask.currentSubtask.subtaskId += 1;
        $progress.currentTask.currentSubtask.feedbackStage = 0;
        $progress.currentTask.currentSubtask.attempts = 0;
        $progress.currentTask.currentSubtask.answer = undefined;
        $progress.currentTask.currentSubtask.correct = false;

        // Tracking time to complete each of the tasks in task 5
        if ($progress.currentTask.emailId === emails.length) {
          sendApiRequest('start-tracking', 'POST', { serialNumber: $testOptions.serialNumber, subtaskId: $progress.currentTask.currentSubtask.subtaskId, timestamp: Math.floor(Date.now() / 1000) });
        };
      }
    }
  });  
</script>

{#if showNotification && $progress.currentTask.emailId <= emails.length}
  <Noti />
{/if}
<div class="feedback-container">
  <p style="color: {($progress.displayMessage.find(emailFb => emailFb.emailId === emailId) as DisplayMessage).colour}">{($progress.displayMessage.find(emailFb => emailFb.emailId === emailId) as DisplayMessage).message}</p>
  {#if (emailId < $progress.currentTask.emailId)}
    <p><i>You have completed all tasks in this message.</i></p>
  {:else}
    <p><i>You have completed {$progress.currentTask.currentSubtask.subtaskId-1}/{email.results.length} tasks in this message.</i></p>
    <button class="back-btn" on:click={() => $showFeedback = removeItemAll($showFeedback, emailId)}>Back</button>
  {/if}
</div>

<style>
    p {
        margin: 1rem;
        color: #333;
    }
</style>

