<script>
	import * as d3 from 'd3'
	import Recommendations from './Recommendations.svelte'

	export let dataset = []
	export let selectedAttributes = []

	let promise = loadSpecs();
	let updateCount = 0

	function dataPreprocessor(d) {
		let result = {}
		for (let i = 0; i < d3.keys(d).length; i++) {
			let variableName = d3.keys(d)[i]
			if (variableName === 'filename') {
				result[variableName] = d3.values(d)[i]
			} else {
				result[variableName] = +d3.values(d)[i]
			}
		}
	    return result
	}

	async function loadSpecs() {
		const specs = await d3.csv(`/data/specs_binary.csv`, dataPreprocessor)

		const vegaSpecs = []

		for (const s of specs) {
			let vegaFilename = s.filename
			vegaFilename = vegaFilename.replace("./", "")
			const vegaSpec = await d3.json(vegaFilename)
			// vegaSpecs.push({ 'spec':s, 'vega':vegaSpec })
			vegaSpecs.push(s)
		}

		return vegaSpecs
	}

	function update() {
		updateCount++
	}
</script>

<div id="recommendationsMain">
	{#await promise}
		<p>...loading</p>
	{:then vegaSpecs}
		<div>
			<p><b>RECOMMENDATIONS</b></p>
			<button on:click={update}>Update Recommendations</button>
		</div>
		<Recommendations
			{dataset}
			{vegaSpecs}
			{selectedAttributes}
			{updateCount}/>
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}
</div>

<style>
	#recommendationsMain {
		display: flex;
		flex-direction: column;
		margin-bottom: 150px
	}
</style>