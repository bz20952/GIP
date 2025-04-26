<svelte:head>
	<title>Help</title>
	<meta name="description" content="Help" />
</svelte:head>

<h1>User guide</h1>

<section>
	<div class="summary">
		Watch <a href="https://youtu.be/CW5EYQ-pZUc" target="_blank">this video</a> for a visual how-to guide.
		Or keep reading for a quick summary.
	</div>

	<div class='written-guide'>
		<!-- <i><strong>TL;DR</strong></i> -->
		<ul>
			<li>Try to avoid refreshing the page as this will reset the game and your progress.</li>
			<li>View your current tasks on your <a href="/">Dashboard</a>. There are five tasks in total.</li>
			<li>View your progress at the bottom of any page at any time.</li>
			<li>To start a task, navigate to the <a href="/toolkit">Toolkit</a>. Hovering over a tool will reveal a short description.</li>
			<li>In order to complete a task, click <strong>Send results</strong> under the message and enter one or more numerical answers obtained from your experiment.</li>
			<li>In order to check whether or not you have completed the task successfully, click <strong>View feedback</strong>. If you have completed the task successfully, a new task will appear.</li>
		</ul>	
	</div>
	<div class="closing">If you come across any issues, please ask one of the research team for help. All feedback is very helpful to us in improving and maintaing this tool!</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	h1 {
		width: 100%;
		margin-top: 3rem;
	}

	.summary {
        font-family: 'Segoe UI';
        font-size: 16pt;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 2px 2px 2px 2px rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        padding: 1rem;
        background-color: azure;
    }

	.written-guide {
		margin: 2rem;
	}

	ul {
		list-style: square;
	}

	li {
		padding: 0.5rem;
	}

	.closing {
		text-align: center;
		font-size: 18pt;
		margin: 2rem 0rem;
	}
</style>
