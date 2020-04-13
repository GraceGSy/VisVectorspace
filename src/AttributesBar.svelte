<script>
	export let dataset = []

	let attributes = Object.keys(dataset[0])
</script>

<div id="attributesBar">
	<p>Attributes</p>
	{#each attributes as a}
		<button>{a}</button>
	{/each}
</div>

<style>
	#attributesBar {
		display: flex;
		flex-direction: column;
		width: 150px;
		margin-right: 50px
	}
</style>