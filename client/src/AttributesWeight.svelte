<script>
	import Vectorspace from './Vectorspace.svelte'
	import * as d3 from "d3"

	export let attributes = []
	export let allPoints = []
	export let shownPoints = []

	let attributesProcessed = []

	let markAttr = []
	let encodingAttr = []

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

	let attributesList = ["type","minutes","rating","votes","principals","genre"]

	$: {
		// console.log(attributes)
		let opacityScale = d3.scaleLinear()
							.domain(d3.extent(attributes.map(a => a[1])))
							.range([0.25, 1])

		let newAttributes = []
		let newMarkAttr = []
		let newEncodingAttr = []

		for (let a of attributes) {
			let feature = a[0]

			let name
			let value
			let opacity

			if (feature.indexOf("mark") > -1) {
				name = "mark"
				value = feature.slice(feature.indexOf("_") + 1)
				opacity = opacityScale(a[1])

				newMarkAttr.push([name, value, opacity])
			} else if (feature.indexOf("bin") > -1) {
				name = feature.slice(0, feature.indexOf("."))
				value = "bin"
				opacity = opacityScale(a[1])
			} else {
				name = feature.slice(0, feature.indexOf("."))
				value = feature.slice(feature.indexOf("_") + 1)
				opacity = opacityScale(a[1])

				if (value === "nominal") {
					value = "categorical"
				}
				newEncodingAttr.push([name, value, opacity])
			}
			
		}

		newMarkAttr = newMarkAttr.sort((a, b) => b[1] > a[1])
		newEncodingAttr = newEncodingAttr.sort((a, b) => b[1] > a[1])

		markAttr = newMarkAttr.slice(0, 10)
		encodingAttr = newEncodingAttr.slice(0, 10)
	}

	// let attributes = Object.keys(dataset[0])
</script>

<div id="attributesInfo">
	<div id="attributesList">
		<p><b>DATA</b></p>
		<div id="datasetName">
			<i class="material-icons md-24" id="listIcon">view_list</i>
			<p> movies90s.csv</p>
		</div>
		<p>Fields</p>
		{#each attributesList as l}
			<div key={l} class="dataField">
				<div class="field">{l}</div>
					<div class="tooltip">
					<i class="material-icons md-24 dataInfo">info</i>
					<span class="tooltiptext">{descriptions[l].type + ': ' + descriptions[l].des}</span>
				</div>
			</div>
		{/each}
	</div>
	<div id="attributesWeights">
		<p><b>PREFERENCES</b></p>
		<p>Mark</p>
		{#each markAttr as a}
			<div key={a.join()} class="attribute" style={`opacity:${a[2]}`}>
				<div class="attributeLeft">{a[0]}</div>
				<div class="attributeRight">{a[1]}</div>
			</div>
		{/each}
		<p>Encoding</p>
		{#each encodingAttr as e}
			<div key={e.join()} class="attribute" style={`opacity:${e[2]}`}>
				<div class="attributeLeft">{e[0]}</div>
				<div class="attributeRight">{e[1]}</div>
			</div>
		{/each}
		<!-- <p><b>EMBEDDINGS</b></p>
		<Vectorspace allPoints={allPoints} shownPoints={shownPoints} /> -->
	</div>
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

	#attributesWeights {
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
		flex-direction: column;
	    padding: 20px 20px 0px 15px;
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

	.attributeRight {
		border-radius: 0px 12px 12px 0px;
    	border-style: solid solid solid hidden;
	    border-color: steelblue;
	    border-width: 2px;
    	align-content: middle;
    	padding: 0px 10px 0px 5px;
    	width: 200px;
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