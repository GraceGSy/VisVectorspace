<script>
	import { createEventDispatcher } from 'svelte'

	export let dataset = []

	// let selectedAttributes = []

	let attributes = Object.keys(dataset[0])

	const dispatch = createEventDispatcher()

	function update(a) {
		// selectedAttributes = selectedAttributes.push(a)
		let element = document.getElementById(a)
		element.style.backgroundColor = "#a3ccb7"
		dispatch('attributeClicked', {
			attribute: a,
		});
	}
</script>

<div id="attributesBar">
	<p><b>ATTRIBUTES</b></p>
	{#each attributes as a}
		<button
			id={a}
			on:click={() => update(a)}>{a}</button>
	{/each}
</div>

<style>
	#attributesBar {
		display: flex;
		flex-direction: column;
		width: 150px;
		margin-right: 50px;
		background: white;
	}
</style>