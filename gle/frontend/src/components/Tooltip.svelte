<script lang="ts">
    import { tooltips } from "$lib/tooltips.json"
    import { PUBLIC_BACKEND_URL } from "$env/static/public";

    export let displayText: string = '';
    export let displayImage: boolean = false;
    export let tooltipId: number = 0;
    export let tooltipText: string | undefined = '';

    const tooltipContent = tooltips.find(tooltip => tooltip.id === tooltipId);

    if (tooltipContent?.tooltipText) {
        tooltipText = tooltipContent.tooltipText;
    }
</script>

<div class="tooltip">
    {#if displayImage}
        <img class='display-img' src="$lib/images/info.png" alt="Info" />
    {/if}
    {displayText}
    <span class="content">
        {#if tooltipContent?.tooltipImage}
            <img class='tooltip-img' src={PUBLIC_BACKEND_URL + tooltipContent.tooltipImage} alt="Tooltip" />
        {/if}
        {tooltipText}
    </span>
</div>

<style>
    /* Tooltip container */
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black; /* If you want dots under the hoverable text */
        margin: 0.2rem 0.5rem;
    }

    /* Tooltip text */
    .content {
        visibility: hidden;
        width: 30rem;
        background-color: azure;
        border: #2c6392 solid 1px;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 2px 2px 2px 2px rgba(0, 0, 0, 0.2);

        /* Position the tooltip text */
        position: absolute;
        z-index: 1;
        bottom: -300%;
        left: 50%;
        margin-left: -15rem;

        /* Fade in tooltip */
        opacity: 0;
        transition: opacity 0.3s;
    }

    /* Tooltip arrow */
    .tooltip .content::after {
        content: "";
        position: absolute;
        top: -10%;
        left: 50%;
        margin-left: -5px;
        /* border-width: 5px; */
        /* border-style: solid; */
        /* border-color: transparent transparent #2c6392 transparent; */
    }

    /* Show the tooltip text when you mouse over the tooltip container */
    .tooltip:hover .content {
        visibility: visible;
        opacity: 1;
    }

    .display-img {
        display: inline;
        width: 1.5rem;
    }

    .tooltip-img {
        max-height: 8rem;
        margin-top: 1rem;
    }
</style>