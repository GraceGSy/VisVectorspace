<script>
	import Vectorspace from './Vectorspace.svelte'

	export let attributes = []
	export let allPoints = []
	export let shownPoints = []

	let attributesProcessed = []

	$: {
		console.log(attributes)
		let newAttributes = []
		for (let a of attributes) {
			let feature = a[0]

			if (feature.indexOf("mark") > -1) {
				let name = "mark"
				let value = feature.slice(feature.indexOf("_") + 1)
				newAttributes.push([name, value])
			} else {
				let name = feature.slice(0, feature.indexOf("."))
				let value = feature.slice(feature.indexOf(".") + 1)
				newAttributes.push([name, value])
			}
			
		}

		newAttributes = newAttributes.sort((a, b) => b[1] > a[1])

		attributesProcessed = newAttributes.slice(0, 10)
	}

	// let attributes = Object.keys(dataset[0])
</script>

<div id="attributesBar">
	<p><b>LEARNED ENCODINGS</b></p>
	{#each attributesProcessed as a}
		<div key={a.join()} class="attribute">
			<div class="attributeLeft">{a[0]}</div>
			<div class="attributeRight">{a[1]}</div>
		</div>
	{/each}
	<!-- <p><b>EMBEDDINGS</b></p>
	<Vectorspace allPoints={allPoints} shownPoints={shownPoints} /> -->
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
	}
</style>