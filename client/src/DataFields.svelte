<script>
	import { dndzone, TRIGGERS, SHADOW_ITEM_MARKER_PROPERTY_NAME } from "svelte-dnd-action"
	import { flip } from 'svelte/animate'

	export let items = []

	let shouldIgnoreDndEvents = false;
	let dropFromOthersDisabled = true;

	// The following descriptions are provided by IMDB
	// https://www.imdb.com/interfaces/
	// principals and genre have been modified from the original dataset
	// Their descriptions reflect the modifications
	let descriptions = {"type":{type: "categorical", des:"the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)"},
						"minutes":{type: "quantitative", des:"primary runtime of the title, in minutes"},
						"rating":{type: "quantitative", des:"weighted average of all the individual user ratings"},
						"votes":{type: "quantitative", des:"number of votes the title has received"},
						"principals":{type: "quantitative", des:"total principal cast/crew for titles"},
						"genre":{type: "categorical", des:"first genre associated with the title"},
						"categorical":{type: "any", des:"type, genre"},
						"quantitative":{type: "any", des:"minutes, rating, votes, principals"}}

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
			<div class="tooltip">
				<i class="material-icons md-24 dataInfo">info</i>
				<span class="tooltiptext">{descriptions[item.name].type + ': ' + descriptions[item.name].des}</span>
			</div>
		</div>
	{/each}
</div>

<style>
	.dataField {
		height: 25px;
		margin-bottom: 10px;
		display: flex;
		cursor: move;
	}

	.field {
		align-content: middle;
		border-radius: 12px 12px 12px 12px;
    	border: steelblue solid 2px;
    	padding: 0px 10px 0px 10px;
    	width: 100%;
	}

	.dataInfo {
		opacity: 25%;
    	cursor: default;
    	margin-left: 10px;
    	cursor: default;
	}

	.tooltip {
		position: relative;
		display: flex;
		align-items: center;
	}

	/* Tooltip text */
	.tooltip .tooltiptext {
		visibility: hidden;
	    width: 200px;
	    background-color: gray;
	    color: white;
	    text-align: center;
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
	}

	/* Tooltip arrow */
	.tooltip .tooltiptext::after {
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
	.tooltip:hover .tooltiptext {
		visibility: visible;
		opacity: 1;
	}
</style>