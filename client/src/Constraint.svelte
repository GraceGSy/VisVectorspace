<script>
	import { dndzone, TRIGGERS, SHADOW_ITEM_MARKER_PROPERTY_NAME } from "svelte-dnd-action"
	import { flip } from 'svelte/animate'

	export let items = []
	export let attributeType
	export let updateCount
	// export let setValue

	$: console.log("items", items)

	let shouldIgnoreDndEvents = false;
	let aggregates = ["-", "bin", "min", "max", "mean", "median", "sum"]
	let selected = ""

	let descriptions = {"type":"categorical",
						"minutes":"quantitative",
						"rating":"quantitative",
						"votes":"quantitative",
						"principals":"quantitative",
						"genre":"categorical"}

	const flipDurationMs = 200

	function handleConsider(e) {
        items = e.detail.items;
    }

    function handleFinalize(e) {

    	let mostRecent = e.detail.info.id

    	for (let i of e.detail.items) {
    		if (i.id == mostRecent) {
    			items = [i]
    			updateCount++
    			// setValue = i.id
    		}
    	}
    }

    function onChange(item, a) {
    	// console.log('updating items...', item)
    	// let itemName= item.name

    	item.aggregate = a
    	items = [...items]
    	updateCount++
    }

    function removeItem() {
    	if (items.length != 0) {
    		items = []
    		updateCount++
    	}
    }

</script>

<div class="attribute">
	<div class="attributeLeft">{attributeType}</div>
	<div class="attributeRight"
		use:dndzone={{items, flipDurationMs}}
		on:consider={handleConsider}
		on:finalize={handleFinalize}>
		{#each items as item(item.id)}
			<div>{item.name ? item.name : ''}</div>
			{#if descriptions[item.name] == "quantitative"}
				<div class="tooltip">
					<i class="material-icons md-24">expand_more</i>
					<div class="tooltipcontent">
						{#each aggregates as a}
							<label class="aggOption">
								<input type="radio"
										value={a}
										checked={item.aggregate===a}
										on:change={() => onChange(item, a)} />
								<p class="aggValue">{a}</p>
							</label>
						{/each}
					</div>
				</div>
			{/if}
		{/each}
	</div>
	<i class="material-icons md-24 dataInfo"
		on:click={removeItem}>delete</i>
</div>

<style>
	.attribute {
		height: 25px;
		margin-bottom: 10px;
		display: flex;
	}

	.attributeLeft {
		border-radius: 12px 0px 0px 12px;
    	border: steelblue solid 2px;
    	align-content: middle;
    	padding: 0px 5px 0px 10px;
	}

	.attributeRight {
		border-radius: 0px 12px 12px 0px;
    	border-style: solid solid solid hidden;
	    border-color: steelblue;
	    border-width: 2px;
    	align-content: middle;
    	padding: 0px 0px 0px 5px;
	    width: 200px;
	    display: flex;
	    justify-content: space-between;
	}

	.aggOption {
		display: flex;
		align-items: center;
	}

	.dataInfo {
		opacity: 25%;
    	cursor: default;
    	margin-left: 10px;
    	cursor: pointer;
	}

	/* Hard coded alignment values */
	.aggValue {
		margin-left: 5px;
		margin-top: 7px;
		line-height: 0.5em;
	}

	.tooltip {
		position: relative;
		display: flex;
		align-items: center;
	}

	/* Tooltip text */
	.tooltip .tooltipcontent {
		visibility: hidden;
	    width: 200px;
	    background-color: gray;
	    color: white;
	    padding: 20px;
	    border-radius: 6px;
	    position: absolute;
	    z-index: 1;
	    /* top: -2px; */
	    left: 120%;
	    opacity: 0;
	    transition: opacity 0.3s;
	    /* height: 80px; */
	    font-size: 12px;
	    opacity: 0.6;
	    display: grid;
	    grid-template-columns: repeat(2, auto);
	    grid-template-rows: repeat(4, auto);
	}

	/* Tooltip arrow */
	.tooltip .tooltipcontent::after {
		content: " ";
		position: absolute;
		top: 50%;
		right: 100%; /* To the left of the tooltip */
		margin-top: -5px;
		border-width: 5px;
		border-style: solid;
		border-color: transparent gray transparent transparent;
	}

	/* Show the tooltip text when you mouse over the tooltip container */
	.tooltip:hover .tooltipcontent {
		visibility: visible;
		opacity: 1;
	}
</style>