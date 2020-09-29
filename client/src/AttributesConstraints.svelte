<script>
	export let selectedMark
	export let channelSelections

	import * as d3 from 'd3'
	let marks = ['', 'area','bar','point', 'line','rect','tick']

	let channels = ['x','y','color','size','shape']

	let accepted_types = ['type_quantitative', 'type_nominal']

	let variable_types = {'name': 'number', 'mfr': 'string', 'type': 'string', 'calories': 'number', 'protein': 'number', 'fat': 'number', 'sodium': 'number', 'fiber': 'number', 'carbo': 'number', 'sugars': 'number', 'potass': 'number', 'vitamins': 'number', 'shelf': 'number', 'weight': 'number', 'cups': 'number', 'rating': 'number'}

	let variables = [''].concat(accepted_types).concat(Object.keys(variable_types).map(v => 'field_' + v))
</script>

<div id="attributesBar">
	<p><b>ENCODINGS</b></p>
	<p>mark</p>
	<div class="attribute">
		<div class="attributeLeft">mark</div>
		<select id="mark-dropdown" class="attributeRight" bind:value={selectedMark}>
			{#each marks as m}
				<option value={m}>{m}</option>
			{/each}
		</select>
	</div>
	<p>channel</p>
	
	{#each channels as c}
		<div class="attribute">
			<div class="attributeLeft">{c}</div>
			<select id="mark-dropdown" class="attributeRight" bind:value={channelSelections[c]}>
				{#each variables as v}
					<option value={v}>{v}</option>
				{/each}
			</select>
		</div>
	{/each}
	
</div>

<style>
	#attributesBar {
		display: flex;
	    flex-direction: column;
	    width: 200px;
	    padding-right: 50px;
	    padding-left: 25px;
	    margin-right: 25px;
	    background: white;
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

	.attributeRight {
		border-radius: 0px 12px 12px 0px;
    	border-style: solid solid solid hidden;
	    border-color: steelblue;
	    border-width: 2px;
    	align-content: middle;
    	padding: 0px 10px 0px 5px;
    	height: 25px;
	}
</style>