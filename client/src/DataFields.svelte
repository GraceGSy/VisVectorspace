<script>
	import { dndzone, TRIGGERS, SHADOW_ITEM_MARKER_PROPERTY_NAME } from "svelte-dnd-action"
	import { flip } from 'svelte/animate'

	export let items = []

	let shouldIgnoreDndEvents = false;
	let dropFromOthersDisabled = true

	const flipDurationMs = 200

	function handleConsider(e) {
        console.warn(`got consider ${JSON.stringify(e.detail, null, 2)}`);
        const {trigger, id} = e.detail.info;
        if (trigger === TRIGGERS.DRAG_STARTED) {
            console.warn(`copying ${id}`);
            const idx = items.findIndex(item => item.id === id);
            const newId = `${id}_copy_${Math.round(Math.random()*100000)}`;
						// the line below was added in order to be compatible with version svelte-dnd-action 0.7.4 and above 
					  e.detail.items = e.detail.items.filter(item => !item[SHADOW_ITEM_MARKER_PROPERTY_NAME]);
            e.detail.items.splice(idx, 0, {...items[idx], id: newId});
            items = e.detail.items;
            shouldIgnoreDndEvents = true;
        }
        else if (!shouldIgnoreDndEvents) {
            items = e.detail.items;
        }
        else {
            items = [...items];
        }
    }

    function handleFinalize(e) {
        items = e.detail.items;
    }

</script>


<div use:dndzone={{items, flipDurationMs, dropFromOthersDisabled}}
	on:consider={handleConsider}
	on:finalize={handleFinalize}>
	{#each items as item(item.id)}
		<div key={item.name} class="dataField" animate:flip={{duration:flipDurationMs}}>
			<div class="field">{item.name}</div>
		</div>
	{/each}
</div>

<style>
	#datasetName {
		display: flex;
		font-size: 11px;
		align-items: center;
	}

	#listIcon {
		font-size: 16px;
		margin-right: 2px;
	}

	#attributesInfo {
		display: flex;
	}

	#attributesConstraints {
		display: flex;
		flex-direction: column;
		width: 175px;
		padding: 20px 50px 0px 15px;
	    margin-right: 25px;
		background: #f3f3f3;
		border-right: 2px solid white;
	}

	#attributesList {
		display: flex;
		height: 100%;
		flex-direction: column;
	    padding: 20px 50px 0px 15px;
	    margin-right: 25px;
		background: white;
	}

	.dataField {
		height: 25px;
		margin-bottom: 10px;
		display: flex;
	}

	.field {
		align-content: middle;
		border-radius: 12px 12px 12px 12px;
    	border: steelblue solid 2px;
    	padding: 0px 10px 0px 10px;
    	width: 100%;
	}

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

	#mark-dropdown {
		height: 25px;
		width: 200px;
	}

	.attributeRight {
		border-radius: 0px 12px 12px 0px;
    	border-style: solid solid solid hidden;
	    border-color: steelblue;
	    border-width: 2px;
    	align-content: middle;
    	padding: 0px 10px 0px 5px;
	}
</style>