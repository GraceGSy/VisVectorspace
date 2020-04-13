<script>
	import * as d3 from 'd3'
	import Recommendations from './Recommendations.svelte'

	export let dataset = []

	let promise = loadSpecs();

	async function loadSpecs() {
		const specs = await d3.csv(`pca_specs_binary.csv`)

		const vegaSpecs = []

		for (const s of specs) {
			let vegaFilename = s.filename
			vegaFilename = vegaFilename.replace("./", "")
			const vegaSpec = await d3.json(vegaFilename)
			vegaSpecs.push(vegaSpec)
		}

		return vegaSpecs
	}
</script>

{#await promise}
	<p>...loading</p>
{:then vegaSpecs}
	<div id="recommendationsMain">
		<p>Recommendations</p>
		<Recommendations {dataset} {vegaSpecs}/>
	</div>
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}

<style>
	#recommendationsMain {
		display: flex;
		flex-direction: column;
	}
</style>