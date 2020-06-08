<script>
	import * as d3 from 'd3'
	// import Draco from 'draco-vis'
	import AttributesBar from './AttributesBar.svelte'
	import RecommendationsMain from './RecommendationsMain.svelte'

	let rand = -1;
	function getRand() {
		fetch("./classifier/api?param1=1&param1=2")
	}


	let selectedAttributes = []
	let promise = loadData();

	async function loadData() {
		const dataset = await d3.csv(`cereal.csv`)

		return dataset
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

<div id="main">
	<!-- <h1>Your number is {rand}!</h1> -->
	<!-- <button on:click={getRand}>Get a random number</button> -->
	{#await promise}
		<p>...loading</p>
	{:then dataset}
			<AttributesBar
				on:attributeClicked={updateAttributes}
				{dataset}/>
			<RecommendationsMain
				{selectedAttributes}
				{dataset}/>
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