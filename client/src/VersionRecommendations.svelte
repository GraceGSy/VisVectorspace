<script>
	import * as d3 from 'd3'
	import Recommendations from './Recommendations.svelte'

	export let dataset = []
	export let types = {}
	export let selectedAttributes = []

	let promise = loadSpecs();
	let updateCount = 0

	function dataPreprocessor(d) {
		let result = {}
		for (let i = 0; i < d3.keys(d).length; i++) {
			let variableName = d3.keys(d)[i]
			if (variableName === 'filename') {}
			else {
				result[variableName] = +d3.values(d)[i]
			}
		}
	    return result
	}

	async function loadSpecs() {
		const specs = await d3.csv(`/manual_specs_one_hot_encoding_4.csv`, dataPreprocessor)

		const vegaSpecs = []

		for (let i in specs) {
			if (i === 'columns') { continue; }
			let s = specs[i]

			delete s.index

			vegaSpecs.push({ 'spec':s })
		}

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
		width: 100%;
		display: flex;
		flex-direction: column;
	}
</style>