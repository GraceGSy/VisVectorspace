<script>
	import Vectorspace from './Vectorspace.svelte'

	export let attributes = []
	export let allPoints = []
	export let shownPoints = []

	let attributesProcessed = []

	let markAttr = []
	let encodingAttr = []

	let attributesList = ["type","minutes","rating","votes","principals","genre"]

	$: {
		// console.log(attributes)
		let newAttributes = []
		let newMarkAttr = []
		let newEncodingAttr = []
		for (let a of attributes) {
			let feature = a[0]

			if (feature.indexOf("mark") > -1) {
				let name = "mark"
				let value = feature.slice(feature.indexOf("_") + 1)
				newMarkAttr.push([name, value])
			} else {
				let name = feature.slice(0, feature.indexOf("."))
				let value = feature.slice(feature.indexOf("_") + 1)
				if (value === "nominal") {
					value = "categorical"
				}
				newEncodingAttr.push([name, value])
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
			</div>
		{/each}
	</div>
	<div id="attributesWeights">
		<p><b>PREFERENCES</b></p>
		<p>Mark</p>
		{#each markAttr as a}
			<div key={a.join()} class="attribute">
				<div class="attributeLeft">{a[0]}</div>
				<div class="attributeRight">{a[1]}</div>
			</div>
		{/each}
		<p>Encoding</p>
		{#each encodingAttr as e}
			<div key={e.join()} class="attribute">
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
</style>