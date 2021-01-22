<script>
	import * as d3 from 'd3'
	import Draco from 'draco-vis'

	import AttributesConstraints from './AttributesConstraints.svelte'
	import dracoDataConstraints from './dracoDataConstraints.js'

	export let dataset = []
	export let types = {}
	export let selectedAttributes = []
	
	let updateCount = 0

	let pinned = []
	let currentPinned = []

	let attributesConstraints = []

	let recommendations = []

	let sessionData = []

	// Track user constraints
	let selectedMark
	const channelDefaults = {"x":[], "y":[], "color":[], "size":[], "shape":[]}
	let channelSelections = JSON.parse(JSON.stringify(channelDefaults))

	function solveDraco(markConstraints, visConstraints, dataset) {
		// console.log(newConstraints)
		let recs = []

		const url = 'https://unpkg.com/wasm-clingo@0.2.2'

		const draco = new Draco(url)
		return draco.init().then(() => {
			// Get metadata about dataset
			draco.prepareData(dataset)
			const schema = draco.getSchema()
			const dataConstraints = dracoDataConstraints(schema)

			// Create constraints based on schema
			const inputConstraints = `
				data("movies.csv").
				num_rows(77).

				${dataConstraints}

				${markConstraints}

				% ====== Query constraints ======
				${visConstraints}
			`;

			console.log(inputConstraints)

			const solution = draco.solve(inputConstraints, { models: 4 });
			
			// console.log("solution", solution)
			
			if (!solution) {
				console.log('no solution')
				recommendations = []
				return []
			}

			// console.log("solution", solution)

			for (let [i, s] of solution['specs'].entries()) {
				s.width = 270
				s.height = 270
				recs.push({'vega':s, 'uid': 'id' + (new Date().valueOf()) + '_' + i})
			}

			console.log(recs)

			recommendations = recs

			sessionData.push({"markConstraints":selectedMark,
							  "visConstraints":channelSelections,
							  "recommendations": recs,
							  "date": new Date()})

			// console.log(recommendations)
		})
	}

	function getRecommendations() {
		let markConstraints = selectedMark === '' ? '' : `mark(${selectedMark}).`

		let visConstraints = []
		// console.log(channelSelections)

		let encodingCount = 0
		for (let c of Object.keys(channelSelections)) {
			if (channelSelections[c].length == 0) {continue}

			let channelValue = channelSelections[c][0].name

			if (channelValue === "categorical") { channelValue = "nominal" }

			// console.log(c, channelValue)

			if (channelValue && channelValue != '') {
				let newConstraint = `encoding(e${encodingCount}).:- not channel(e${encodingCount}, ${c}).`
				
				if (channelValue == "quantitative" || channelValue == "nominal") {
					// Get channel
					newConstraint = newConstraint + `:- not type(e${encodingCount}, ${channelValue}).`

				} else {
					// Get field
					newConstraint = newConstraint + `:- not field(e${encodingCount}, ${channelValue}).`

					let agg = channelSelections[c][0].aggregate

					if (agg === "bin") {
						newConstraint = newConstraint + `:- not bin(e${encodingCount}, 10).`
					} else if (agg != "-") {
						newConstraint = newConstraint + `:- not aggregate(e${encodingCount}, ${agg}).`
					}
				}

				visConstraints.push(newConstraint)
				encodingCount++
			}
		}

		visConstraints = visConstraints.join('\n\n')

		solveDraco(markConstraints, visConstraints, dataset)
	}

	$: {console.log('update count', updateCount)
		if (updateCount === 0) {}
		else {
			getRecommendations()
		}}

	$: for (let rec = 0; rec < recommendations.length; rec++) {
		if (!recommendations[rec]) {continue}
		vegaEmbed(`#vis${rec}`, recommendations[rec]['vega'], {actions:false})
	}

	// $: if (channelSelections || selectedMark) {
	// 	console.log(channelSelections, selectedMark)
	// 	updateCount++
	// }

	// function update() {
	// 	updateCount++
	// }

	function reset() {
		selectedMark = ''
		channelSelections = JSON.parse(JSON.stringify(channelDefaults))
		updateCount++
	}

	$: for (let p = 0; p < pinned.length; p++) {
		if (!pinned[p]) {continue}
		vegaEmbed(`#pin${p}`, pinned[p]['vega'], {actions:false})
	}

	function pin(i) {
		// Pinning is disabled if new recommendations are loading
		let selectedUid = recommendations[i].uid
		let pinnedIndex = currentPinned.indexOf(selectedUid)
		if (pinnedIndex === -1) {
			currentPinned = [...currentPinned, selectedUid]
			pinned = pinned.concat([recommendations[i]])

			let date = new Date()
			sessionData = sessionData.concat({"pinned": recommendations[i], "label": "pinned", "date": date})
		} else {
			currentPinned.splice(pinnedIndex, 1)
			currentPinned = currentPinned

			let newPinned = []

			for (let p of pinned) {
				if (p.uid === selectedUid) {
					continue
				} else {
					newPinned.push(p)
				}
			}

			pinned = newPinned

			let date = new Date()
			sessionData = sessionData.concat({"pinned": recommendations[i], "label": "unpinned", "date": date})
		}

		console.log(currentPinned)
	}

	function togglePin() {
		if (document.getElementById("pinnedDrawer").style.width === "450px") {
			document.getElementById("pinnedDrawer").style.width = "0px"
		} else {
			document.getElementById("pinnedDrawer").style.width = "450px"
		}
	}

	// function showPin() {
	// 	document.getElementById("pinnedDrawer").style.width = "450px"
	// }

	// function closePin() {
	// 	document.getElementById("pinnedDrawer").style.width = "0px"
	// }

	function exportJSON() {
		var filename = "sessionData.json"
		var element = document.createElement('a');
		element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(sessionData)))
		element.setAttribute('download', filename)

		element.style.display = 'none'
		document.body.appendChild(element)

		element.click()

		document.body.removeChild(element)
	}
</script>

<div id="overall">
	<AttributesConstraints bind:selectedMark={selectedMark}
							bind:channelSelections={channelSelections}
							bind:updateCount={updateCount} />
	<div id="recommendations">
		<div id="menu">
			<p><b>RECOMMENDATIONS</b></p>
			<!-- <button>UPDATE RECOMMENDATIONS</button> -->
			<div id="menuOptions">
				<button id="pinnedButton" on:click={togglePin}>PINNED</button>
				<button on:click={reset}>RESET</button>
				<button id="exportJSON" on:click={exportJSON} class="btn">DOWNLOAD</button>
			</div>
		</div>
		<div id="recommendationDisplay">
			{#each recommendations as c, i}
				<div class="vis">
					<div class:isPinned="{recommendations[i] && currentPinned.indexOf(recommendations[i].uid) > -1}"
						class="pinButton"
						on:click={() => pin(i)}>
						<i class="material-icons-outlined md-24">push_pin</i>
						</div>
					<div class="vegaContainer">
						<div id="vis{i}"></div>
					</div>
				</div>
			{/each}
		</div>
	</div>
	<div id="pinnedDrawer">
		<p id="pinnedText"><b>PINNED</b></p>
		<!-- <a id="closeButton" on:click={closePin}>&times;</a> -->
		<div id="pinnedDisplay">
			{#each pinned as p, i}
				<div id="pin{i}" class="pinned"></div>
			{/each}
		</div>
	</div>
</div>

<style>
	#overall {
		display: flex;
		background: #f3f3f3;
		width: 100%;
	}

	#menuOptions {
		display: flex;
		width: 100%;
	}

	#pinnedButton {
		margin-right: auto;
	}

	#exportJSON {
		margin-left: 5px;
	}

	#recommendations {
		padding-top: 20px;
		margin-bottom: 20px
	}

	#recommendationDisplay {
		display: grid;
		grid-template-columns: repeat(2, 480px);
		grid-template-rows: repeat(2, 460px);
		grid-gap: 15px;
		margin-top: 50px
	}

	#pinnedDrawer {
		height: 100%;
		width: 0;
		position: fixed;
		z-index: 1001;
		top: 0;
		right: 0;
		overflow: scroll;
		transition: 0.5s;
		padding-top: 20px;
		background: white;
		box-shadow: 195px 8px 10px -5px rgba(0,0,0,0.2), 0px 16px 24px 2px rgba(0,0,0,0.14), 0px 6px 30px 5px rgba(0,0,0,0.12);
	}

	#pinnedText {
		margin-left: 30px;
	}

	#pinnedDisplay {
		display: flex;
		flex-direction: column;
		gap: 30px;
		margin-left: 30px;
		max-width: 500px;
		padding-bottom: 30px;
	}

	.pinned {
		height: 400px;
		overflow: scroll;
	}

	#closeButton {
		position: absolute;
		top: 0;
		right: 25px;
		font-size: 36px;
		margin-left: 50px;
		cursor: pointer;
	}

	.vis {
		overflow: scroll;
	    background: white;
	    display: flex;
	    flex-direction: column;
	    padding: 15px;
	}

	.buttons {
		display: flex;
		flex-direction: row;
		margin-bottom: 20px;
	}

	.pinButton {
		margin-left: auto;
		margin-bottom: 20px;
		width: 28px;
    	height: 28px;
    	color: gray;
    	cursor: pointer;
	}

	.isPinned {
		color: green;
	    transform: rotate(45deg);
	    transition: transform 0.5s;
	}

	.vegaContainer {
		height: 400px;
		overflow: scroll;
	    background: white;
	    display: flex;
	    flex-direction: column;
	}
</style>
