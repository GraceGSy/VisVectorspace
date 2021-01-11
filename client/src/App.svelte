<script>
	import * as d3 from 'd3'
	import AttributesBar from './AttributesBar.svelte'
	import VersionRecommendations from './VersionRecommendations.svelte'
	import VersionConstraintSolver from './VersionConstraintSolver.svelte'

	let versionChoice = null

	let version = null

	let participant = null
	let participantOrder = ['constraintSolver', 'constraintLearner',
							'constraintSolver', 'constraintSolver',
							'constraintSolver', 'constraintLearner',
							'constraintSolver', 'constraintLearner',
							'constraintLearner', 'constraintSolver',
							'constraintLearner', 'constraintLearner']

	let ageRange = null
	let tools = null
	let experience = null

	let allParticipantInfo = {}
	let start = false

	let rand = -1;
	function getRand() {
		fetch("./classifier/api?param1=1&param1=2")
	}

	let selectedAttributes = []
	let promise = loadData();

	function getType(row) {
		const result = {}

		for (let attr of Object.keys(row)) {
			const value = row[attr]
			if (isNaN(parseFloat(value))) {
				result[attr] ='string'
			} else {
				result[attr] ='number'
			}
		}

		return result
	}

	function dataPreprocessor(d) {
		let result = {}
		for (let i = 0; i < d3.keys(d).length; i++) {
			let variableName = d3.keys(d)[i]
			if (variableName === 'tconst' || variableName === "title" || variableName === 'year') {}
			else if (variableName === 'type' || variableName === "genre") {
				result[variableName] = d3.values(d)[i]
			}
			else {
				result[variableName] = +d3.values(d)[i]
			}
		}
	    return result
	}

	async function loadData() {
		const dataset = await d3.csv(`movies.csv`, dataPreprocessor)

		// console.log(dataset)

		const firstRow = dataset[0]

		const types = getType(firstRow)

		return {"dataset":dataset, "types":types}
	}

	function updateAttributes(event) {
		let attribute = event.detail.attribute
		
		if (selectedAttributes.includes(attribute)) {}
		else {
			selectedAttributes.push(attribute)
			selectedAttributes = selectedAttributes
		}
	}

	function load() {
		if (participant && ageRange && ageRange != "<18" && experience) {
			allParticipantInfo = {"age": ageRange,
								  "tools": tools,
								  "experience": experience}
			start = true
		}
	}
</script>

<div style="padding: '20px'">
	
	<!--<div id="versioning">
		<label class="versionOption">
			<input type=radio bind:group={version} value={"constraintSolver"}>
			Constraint Solver
		</label>
		<label class="versionOption">
			<input type=radio bind:group={version} value={"constraintLearner"}>
			Constraint Learner
		</label>
	</div>-->
	<div id="main">
		{#await promise}
			<p>...loading</p>
		{:then dataset}
			{#if start && participantOrder[participant - 1] === "constraintSolver"}
				<VersionConstraintSolver
					dataset = {dataset["dataset"]}
					types = {dataset["types"]}
					{selectedAttributes}
					{allParticipantInfo}/>
			{:else if start && participantOrder[participant - 1] === "constraintLearner"}
				<!-- <AttributesBar
					on:attributeClicked={updateAttributes}
					dataset={dataset["dataset"]}/> -->
				<VersionRecommendations
					dataset = {dataset["dataset"]}
					types = {dataset["types"]}
					{selectedAttributes}
					{participant}
					{allParticipantInfo}/>
			{:else}
				<div id="chooseVersion">
					<div id="demographics">
						<div id="participantID">
							Participant ID:
							<input class="inputBox" bind:value={participant}>
						</div>
						<div id="participantAge">
							<p class="inputContent">Please select your age range:</p>
							<label class="inputBox">
								<input type=radio bind:group={ageRange} value={"<18"}>
								Less than 18
							</label>
							<label class="inputBox">
								<input type=radio bind:group={ageRange} value={"18-24"}>
								18 to 24 (inclusive)
							</label>
							<label class="inputBox">
								<input type=radio bind:group={ageRange} value={"25-29"}>
								25 to 29 (inclusive)
							</label>
							<label class="inputBox">
								<input type=radio bind:group={ageRange} value={"30-34"}>
								30 to 34 (inclusive)
							</label>
							<label class="inputBox">
								<input type=radio bind:group={ageRange} value={">=35"}>
								35 or greater
							</label>
						</div>
						<div id="participantTools">
							<p class="inputContent">Please list the visualization tools you have used in the last 30 days (comma separated):</p>
							<input id="toolsInput" class="inputBox" bind:value={tools}>
						</div>
						<div id="participantExperience">
							<p class="inputContent">In the last 30 days how often have used visualization tools?</p>
							<label class="inputBox">
								<input type=radio bind:group={experience} value={"0"}>
								Never
							</label>
							<label class="inputBox">
								<input type=radio bind:group={experience} value={"1-2"}>
								1-2 times
							</label>
							<label class="inputBox">
								<input type=radio bind:group={experience} value={"3-5"}>
								3-5 times
							</label>
							<label class="inputBox">
								<input type=radio bind:group={experience} value={"5-10"}>
								5-10 times
							</label>
							<label class="inputBox">
								<input type=radio bind:group={experience} value={">10"}>
								More than 10 times
							</label>
						</div>
						<!-- <label class="versionOption">
							<input type=radio bind:group={version} value={"constraintSolver"}>
							Constraint Solver
						</label>
						<label class="versionOption">
							<input type=radio bind:group={version} value={"constraintLearner"}>
							Constraint Learner
						</label> -->
						<button id="beginButton" on:click={load}>BEGIN</button>
					</div>
				</div>
			{/if}
		{:catch error}
			<p style="color: red">{error.message}</p>
		{/await}
	</div>
</div>

<style>
	#main {
		display: flex;
		flex-direction: row
	}

	#chooseVersion {
		width: 100vw;
		height: 100vh;
		display: flex;
		justify-content: center;
		align-items: center
	}

	#demographics {}

	#versioning {
		display: flex;
		padding: 10px 0px 20px 20px;
	}

	#toolsInput {
		width: 100%;
	}

	.versionOption {
		margin-right: 20px;
	}

	.inputBox {
		margin-bottom: 10px
	}

	.inputContent {
		margin-top: 25px;
		margin-bottom: 10px
	}

	#beginButton {
		margin-top: 25px;
	}
</style>