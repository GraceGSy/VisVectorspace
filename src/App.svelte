<script>
	import * as d3 from 'd3'
	// import Draco from 'draco-vis'
	import AttributesBar from './AttributesBar.svelte'
	import RecommendationsMain from './RecommendationsMain.svelte'

	let promise = loadData();

	async function loadData() {
		const dataset = await d3.csv(`cereal.csv`)

		return dataset
	}

	// function handleClick() {
	// 	promise = loadData();
	// }
</script>

<!-- <button on:click={handleClick}>
	generate random number
</button> -->

<div id="main">
	{#await promise}
		<p>...loading</p>
	{:then dataset}
			<AttributesBar {dataset}/>
			<RecommendationsMain {dataset}/>
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