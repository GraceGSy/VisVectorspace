<script>
	import * as d3 from 'd3'
	import AttributesBar from './AttributesBar.svelte'
	import RecommendationsMain from './RecommendationsMain.svelte'

	let rand = -1;
	function getRand() {
		fetch("./classifier/api?param1=1&param1=2")
	}

	let selectedAttributes = []
	let promise = loadData();

	function getType(row) {
		const result = {}

		for (let attr of Object.keys(row)) {
			const value = row[attr]
			if (isNaN(parseFloat(value))) {
				result[attr] ='string'
			} else {
				result[attr] ='number'
			}
		}

		return result
	}

	async function loadData() {
		const dataset = await d3.csv(`cereal.csv`)

		const firstRow = dataset[0]

		const types = getType(firstRow)

		return {"dataset":dataset, "types":types}
	}

	function updateAttributes(event) {
		let attribute = event.detail.attribute
		
		if (selectedAttributes.includes(attribute)) {}
		else {
			selectedAttributes.push(attribute)
			selectedAttributes = selectedAttributes
		}
	}
</script>

<div id="main" style="padding: '20px'">
	{#await promise}
		<p>...loading</p>
	{:then dataset}
			<!-- <AttributesBar
				on:attributeClicked={updateAttributes}
				dataset={dataset["dataset"]}/> -->
			<RecommendationsMain
				dataset = {dataset["dataset"]}
				types = {dataset["types"]}
				{selectedAttributes}/>
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}
</div>

<style>
	#main {
		display: flex;
		flex-direction: row
	}
</style>