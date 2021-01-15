<script>
	import { dndzone, TRIGGERS, SHADOW_ITEM_MARKER_PROPERTY_NAME } from "svelte-dnd-action"
	import { flip } from 'svelte/animate'

	export let items = []
	export let attributeType
	export let updateCount
	// export let setValue

	let shouldIgnoreDndEvents = false;

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


</script>

<div class="attribute">
	<div class="attributeLeft">{attributeType}</div>
	<div class="attributeRight"
		use:dndzone={{items, flipDurationMs}}
		on:consider={handleConsider}
		on:finalize={handleFinalize}>
		{#each items as item(item.id)}
			<div>{item.name ? item.name : ''}</div>
		{/each}
	</div>
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
    	padding: 0px 10px 0px 5px;
    	width: 200px;
	}
</style>