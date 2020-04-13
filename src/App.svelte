<script>
	import * as d3 from 'd3'
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

{#await promise}
	<p>...loading</p>
{:then dataset}
	<div id="main">
		<AttributesBar {dataset}/>
		<RecommendationsMain {dataset}/>
	</div>
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}

<style>
	#main {
		display: flex;
		flex-direction: row
	}
</style>