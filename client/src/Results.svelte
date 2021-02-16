<script>
	import * as d3 from 'd3'

	let promise = loadData();
	let participantVis = {"constraintLearner": [],
						"constraintSolver": []}

	async function loadData() {
		const dataset = await d3.json(`allPinned.json`)

		let splitData = {"constraintLearner": [],
						"constraintSolver": []}

		for (let d of dataset) {
			if (d.systemType === "constraintLearner") {
				splitData["constraintLearner"].push([d.vis1, d.vis2, d.vis3, d.vis4, d.vis5])
			} else {
				splitData["constraintSolver"].push([d.vis1, d.vis2, d.vis3, d.vis4, d.vis5])
			}
		}

		// const firstRow = dataset[0]

		// const types = getType(firstRow)

		participantVis = splitData

		return splitData
	}

	$: for (let i = 0; i < participantVis["constraintLearner"].length; i++) {
		let participant = participantVis["constraintLearner"][i]
		for (let j = 0; j < 5; j++) {
			let vis = participant[j]["vega"]["vega"]
			vis.width = 150
			vis.height = 150
			vegaEmbed(`#learnervis${i}${j}`, vis, {actions:false})
		}
	}

	$: for (let i = 0; i < participantVis["constraintSolver"].length; i++) {
		let participant = participantVis["constraintSolver"][i]
		for (let j = 0; j < 5; j++) {
			let vis = participant[j]["pinned"]["vega"]
			vis.width = 150
			vis.height = 150
			vegaEmbed(`#solvervis${i}${j}`, vis, {actions:false})
		}
	}

</script>

<div id="overall">
	{#await promise}
		<p>...loading</p>
	{:then splitData}
		<div id="learner">
			<h3>Constraint Learners</h3>
			{#each Array(6) as participant, i}
				<div class="participantContainer">
					{#each Array(5) as vega, j}
						<div class="vegaContainer">
							<div id="learnervis{i}{j}"></div>
						</div>
					{/each}
				</div>
			{/each}
		</div>
		<div id="solver">
			<h3>Constraint Solver</h3>
			{#each Array(6) as participant, i}
				<div class="participantContainer">
					{#each Array(5) as vega, j}
						<div class="vegaContainer">
							<div id="solvervis{i}{j}"></div>
						</div>
					{/each}
				</div>
			{/each}
		</div>
	{/await}
</div>

<style>
	#overall {
		width: 100vw;
		height: 100vh;
	}

	.participantContainer {
		width: 100%;
		display: flex;
	}
</style>
