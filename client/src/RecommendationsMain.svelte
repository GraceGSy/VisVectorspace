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
		const specs = await d3.csv(`/manual_specs_one_hot_encoding.csv`, dataPreprocessor)

		const vegaSpecs = []

		for (let i in specs) {
			if (i === 'columns') { continue; }
			let s = specs[i]

			delete s.index

			// let vegaFilename = s.filename
			
			// if (!vegaFilename) { continue }
				
			// vegaFilename = 'vega_examples/' + vegaFilename
			// const vegaSpec = await d3.json(vegaFilename)
			vegaSpecs.push({ 'spec':s, 'index': i })
		}

		print(vegaSpecs.length)

		return vegaSpecs
	}

	
</script>

<div id="recommendationsMain">
	{#await promise}
		<p>...loading</p>
	{:then vegaSpecs}
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