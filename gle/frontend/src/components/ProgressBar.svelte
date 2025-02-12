<script lang="ts">
	import { progress } from "$lib/stores";

	let current: number;
	
	$: {
		progress.subscribe((val) => {
			current = (val.current/val.total)*100;
		});
	}
</script>

<div class="progress-bar">
	<div class="progress-bar-inner" style={`width: ${current}%`}></div>
</div>
<p class="progress-label">Progress: {current}%</p>

<style>
	.progress-bar {
		width: 80%;
		max-width: 800px;
		height: 20px;
		background-color: azure;
		border-radius: 5px;
		overflow: hidden;
        border: #49484a 1px solid;
	}

	.progress-bar-inner {
		height: 100%;
		background-color: #2c6392;
		transition: width 0.3s ease-out;
	}

    .progress-label {
        margin: 0.5rem;
    }
</style>
