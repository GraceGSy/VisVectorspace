<script>
	import * as d3 from 'd3'
	import Recommendations from './Recommendations.svelte'

	export let dataset = []

	let promise = loadSpecs();
	let updateCount = 0

	async function loadSpecs() {
		const specs = await d3.csv(`pca_specs_binary.csv`)

		const vegaSpecs = []

		for (const s of specs) {
			let vegaFilename = s.filename
			vegaFilename = vegaFilename.replace("./", "")
			const vegaSpec = await d3.json(vegaFilename)
			vegaSpecs.push({ 'spec':s, 'vega':vegaSpec })
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
		<Recommendations {dataset} {vegaSpecs} {updateCount}/>
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