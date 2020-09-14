<script>
	export let attributes = []

	let attributesProcessed = []

	$: {
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
		attributesProcessed = newAttributes
	}

	// let attributes = Object.keys(dataset[0])
</script>

<div id="attributesBar">
	<p><b>ATTRIBUTES</b></p>
	{#each attributesProcessed as a}
		<div key={a.join()} class="attribute">
			<div class="attributeLeft">{a[0]}</div>
			<div class="attributeRight">{a[1]}</div>
		</div>
	{/each}
</div>

<style>
	#attributesBar {
		display: flex;
		flex-direction: column;
		width: 200px;
		margin-right: 50px;
		margin-left: 25px;
	}

	.attribute {
		height: 25px;
		background: #f4f4f4;
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