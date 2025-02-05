<script lang='ts'>
    import { onMount } from 'svelte';
    import WindowsNotify from '$lib/sounds/Windows Notify.wav';

    const message = 'New message!';

    let visible = true;

    onMount(() => {
        const audio = new Audio(WindowsNotify);
        audio.play();
        setTimeout(() => {
            visible = false;
        }, 3000); // fade out after 3 seconds
    });
</script>

<div class="notification {visible ? 'visible' : ''}">
    <strong>{message}</strong>
</div>

<style>
    .notification {
        position: fixed;
        top: -100px;
        right: 10px;
        max-width: 200px;
        color: #2c6392;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        border-radius: 10px;
        border: #2c6392 solid 1px;
        padding: 10px;
        background-color: azure;
        transition: top 0.8s ease-in-out;
        box-shadow: 2px 2px 2px 2px rgba(0, 0, 0, 0.2);
    }

    .visible {
        top: 10px; /* Drop-in position */
    }
</style>
