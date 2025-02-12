<script lang="ts">
    export let displayText;
    export let tooltipText;
</script>

<li class="tooltip">{displayText}
    <span class="tooltiptext">{tooltipText}</span>
</li>

<style>
    /* Tooltip container */
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black; /* If you want dots under the hoverable text */
        margin: 0.2rem 0rem;
    }

    /* Tooltip text */
    .tooltip .tooltiptext {
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
        bottom: 125%;
        left: 50%;
        margin-left: -15rem;

        /* Fade in tooltip */
        opacity: 0;
        transition: opacity 0.3s;
    }

    /* Tooltip arrow */
    .tooltip .tooltiptext::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #2c6392 transparent transparent transparent;
    }

    /* Show the tooltip text when you mouse over the tooltip container */
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>