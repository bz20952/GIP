<script>
  export let emails = [
    { sender: 'Alice', subject: 'Meeting Reminder', snippet: 'Don\'t forget we have a meeting...', read: false },
    { sender: 'Bob', subject: 'Project Update', snippet: 'The project is moving along...', read: true },
    { sender: 'Carol', subject: 'Dinner Invitation', snippet: 'Would you like to join us...', read: false }
  ];
</script>

<div class="inbox-panel">
    <h1 class="inbox-header">Inbox</h1>
    {#each emails as email}
        <div class:email class:read={email.read}>
            <div class="sender">{email.sender}</div>
            <div class="subject">{email.subject}</div>
            <div class="snippet">{email.snippet}</div>
        </div>
    {/each}
</div>

<style>
  .inbox-panel {
    width: 100%;
    max-width: 600px;
    margin: auto;
    border: 1px solid #ccc;
    border-radius: 4px;
    overflow: hidden;
  }

  .email {
    padding: 10px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
  }

  .email:last-child {
    border-bottom: none;
  }

  .email.read {
    background-color: #f9f9f9;
  }

  .sender {
    font-weight: bold;
  }

  .subject {
    margin-top: 5px;
  }

  .snippet {
    margin-top: 5px;
    color: #666;
  }
</style>
