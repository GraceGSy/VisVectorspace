<script>
	import * as d3 from 'd3'
	import Draco from 'draco-vis'
	import vegaToRanking from './vegaToRanking.js'
	import defaultConstraints from './defaults.js'

	import getRecombinations from './getRecombinations.js'

	import AttributesWeight from './AttributesWeight.svelte'

	export let participant = -1
	export let allParticipantInfo = {}

	export let vegaSpecs = []
	export let dataset = []
	export let selectedAttributes = []
	export let recommendationCount = 4

	// true if updating recommendations from server
	let loading = false
	
	let updateCount = 0

	// Track of user preferences
	let moreLikeThis = []
	let lessLikeThis = []
	let maybeLikeThis = []

	// Current recommendations
	let recommendations = []
	// Recommendations generated from the same draco query
	let similarRecommendations = []
	// Recommendations class
	let recommendationsClass = Array(recommendationCount).fill("default")

	let classifierResult

	let pinned = []
	let currentPinned = []

	let attributesWeight = []

	let visVectors = []

	let allPoints = []
	let shownPoints = []

	let sessionData = []

	$: visVectors = vegaSpecs

	function getRandom(count, choices) {
		if (choices.length < count) {
			return choices
		}

		let numChoices = choices.length
		let chosen = new Set()
		while (chosen.size < count) {
			let randomIndex = Math.floor(Math.random() * Math.floor(numChoices))

			chosen.add(randomIndex)
		}

		let result = []
		for (let i of Array.from(chosen)) {
			result.push(choices[i])
		}

		// console.log(result)

		return result
	}

	function selectRecommendations(recommendationSets) {
		similarRecommendations = recommendationSets

		let result = []
		let setNumber = 0

		for (let set of similarRecommendations) {
			let randomIndex = Math.floor(Math.random() * (set.length))
			let selected = set[randomIndex]

			result.push(selected)
		}

		recommendationsClass = recommendationsClass.map(r => 'default')
		recommendations = result

		loading = false
	}

	function runClassifier() {
		loading = true

		let testingData = visVectors.map(v => v.spec)
		let trainingData = []

		let moreLikeThis = []
		let lessLikeThis = []
		let maybeLikeThis = []

		let date = new Date()

		for (let i = 0; i < recommendationsClass.length; i++) {
			let r = recommendationsClass[i]
			if (r === 'more') {
				moreLikeThis = moreLikeThis.concat(similarRecommendations[i])
				sessionData = sessionData.concat({"seen": recommendations[i], "label": "more", "date": date})
				// maybeLikeThis = maybeLikeThis.concat(similarRecommendations[i])
			} else if (r === 'less') {
				lessLikeThis.push(recommendations[i])
				sessionData = sessionData.concat({"seen": recommendations[i], "label": "less", "date": date})
			} else {
				// maybeLikeThis.push(recommendations[i])
				sessionData = sessionData.concat({"seen": recommendations[i], "label": "none", "date": date})
			}
		}

		// If no user feedback provided
		if (moreLikeThis.length === 0 && lessLikeThis.length  === 0) {
			Promise.all(getRecombinations(vegaSpecs, dataset)).then((result) => {
				selectRecommendations(result)
			})
			return
		}

		// moreLikeThis = moreLikeThis.concat(newMore)
		// lessLikeThis = lessLikeThis.concat(newLess)
		// maybeLikeThis = maybeLikeThis.concat(newMaybe)

		for (let m of moreLikeThis) {
			let newM = m.vega.encoding
			newM.label = 1
			newM['mark_'+m.vega.mark] = 1
			trainingData.push(newM)
		}
		for (let l of lessLikeThis) {
			let newL = l.vega.encoding
			newL.label = -1
			newL['mark_'+l.vega.mark] = 1
			trainingData.push(newL)
		}
		// for (let mb of maybeLikeThis) {
		// 	let newMb = mb.vega.encoding
		// 	newMb.label = 0
		// 	newMb['mark_'+mb.vega.mark] = 1
		// 	trainingData.push(newMb)
		// }

		// for (let set of similarRecommendations) {
		// 	for (let s of set) {
		// 		let newS = s.vega.encoding
		// 		newS.label = 0
		// 		newS['mark'] = s.vega.mark
		// 		trainingData.push(newS)
		// 	}
		// }

		// console.log(testingData.length)

		let classifierData = {
			'training': trainingData,
			'testing': testingData
		}

		fetch(`./kneighbors`, {method:"POST", body:JSON.stringify(classifierData)})
			.then(d => d.text())
      		.then(d => {
      			// console.log(d)
      			let result = JSON.parse(d)

      			// console.log("result", result)
      			let newPrediction = result["predictions"]
      			let newDataset = result["newData"].map((d, i) => {d.label = newPrediction[i]; return d})
      			let newVectors = []

      			for (let d of newDataset) {
      				let s = d

					delete s.index

					newVectors.push({ 'spec':s })
      			}

      			// We keep only the most recent 200 visualizations
      			if (newVectors.length > 200) {
      				let difference = newVectors.length - 200
      				newVectors = newVectors.slice(difference, newVectors.length)
      			}

      			visVectors = newVectors

      			// let preferred = result["pred"]
      			let updatedLikes = []
      			let updatedMaybe = []
      			let updatedNo = []

				for (let i = 0; i < newDataset.length; i++) {
					let current = newDataset[i]
					if (current.label > 0) {
						updatedLikes.push(newVectors[i])
					} else if (current.label === 0) {
						updatedMaybe.push(newVectors[i])
					} else {
						updatedNo.push(newVectors[i])
					}
				}

				let updatedPreferrences

				if (updatedLikes.length == 0) {
					if (updatedMaybe.length < recommendationCount) {
						updatedPreferrences = getRandom(4, updatedNo)
					} else {
						updatedPreferrences = getRandom(4, updatedMaybe)
					}
				} else {
					// Introduce some randomness by including parts of the vectorspace
					// Not yet explored
					let randomMaybe = getRandom(2, updatedMaybe)
					let randomYes = getRandom(2, updatedLikes)
					updatedPreferrences = randomYes.concat(randomMaybe)
				}

				allPoints = newDataset
				shownPoints = updatedPreferrences

				let attributes = Object.keys(newDataset[0])
				let attributeMeans = []

				for (let a of attributes) {
					if (a.indexOf("label") > -1 || a.indexOf("umapX") > -1 || a.indexOf("umapY") > -1) {
						continue
					}
					let attributeValues = newDataset.map(d => {
						if (d[a] == 1) {
							return d.label
						}
						return 0
					})
					attributeMeans.push([a, d3.mean(attributeValues)])
				}

				attributesWeight = attributeMeans.filter(d => d[1] > 0)

				Promise.all(getRecombinations(updatedPreferrences, dataset)).then((result) => {
					selectRecommendations(result)
				})
      		})
	}

	$: {console.log('update count', updateCount)
		if (updateCount === 0) {
			Promise.all(getRecombinations(vegaSpecs, dataset)).then((result) => {
				selectRecommendations(result)
			})
		}
		else {
			console.log('running classifier: ', updateCount)
			runClassifier()
		}}

	$: for (let rec = 0; rec < recommendations.length; rec++) {
		if (!recommendations[rec]) {continue}
		vegaEmbed(`#vis${rec}`, recommendations[rec]['vega'], {actions:false})
	}

	// Update 'moreLikeThis' array
	function updateMore(i) {
		// Liking items is disabled if new recommendations are loading
		if (loading) { return }

		// If items already in moreLikeThis, remove
		let current = recommendationsClass[i]
		if (current === 'more') {
			recommendationsClass[i] = 'default'
		} else {
			recommendationsClass[i] = 'more'
		}
	}

	// Update 'lessLikeThis' array
	function updateLess(i) {
		// Disliking items is disabled if new recommendations are loading
		if (loading) { return }

		// If items already in lessLikeThis, remove
		let current = recommendationsClass[i]
		if (current === 'less') {
			recommendationsClass[i] = 'default'
		} else {
			recommendationsClass[i] = 'less'
		}
	}

	function update() {
		updateCount++
	}

	function reset() {
		recommendationsClass = recommendationsClass.map(r => 'default')
		moreLikeThis = []
		lessLikeThis = []
		maybeLikeThis = []
	}

	$: for (let p = 0; p < pinned.length; p++) {
		if (!pinned[p]) {continue}
		vegaEmbed(`#pin${p}`, pinned[p]['vega'], {actions:false})
	}

	function pin(i) {
		// Pinning is disabled if new recommendations are loading
		if (loading) { return }

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
	}

	function showPin() {
		// Showing pins is disabled if new recommendations are loading
		if (loading) { return }

		document.getElementById("pinnedDrawer").style.width = "450px"
	}

	function closePin() {
		// Hiding pins is disabled if new recommendations are loading
		if (loading) { return }

		document.getElementById("pinnedDrawer").style.width = "0px"
	}

	function exportJSON() {
		// Downloading is disabled if new recommendations are loading
		if (loading) { return }

		let allData = {"participant": allParticipantInfo,
						"session": sessionData}

		var filename = `sessionData_${participant}.json`
		var element = document.createElement('a');
		element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(allData)))
		element.setAttribute('download', filename)

		element.style.display = 'none'
		document.body.appendChild(element)

		element.click()

		document.body.removeChild(element)
	}

</script>

<div id="overall">
	<div class:showLoader="{loading}"
		class:hideLoader="{!loading}"
		class="loader">
		<div class="spinner"></div>
	</div>
	<AttributesWeight attributes={attributesWeight}
						allPoints={allPoints}
						shownPoints={shownPoints}/>
	<div id="recommendations">
		<div id="menu">
			<p class="title1"><b>RECOMMENDATIONS</b></p>
			<button on:click={update}>UPDATE RECOMMENDATIONS</button>
			<button on:click={showPin}>PINNED</button>
			<button id="exportJSON" on:click={exportJSON} class="btn">DOWNLOAD</button>
		</div>
		<div id="recommendationDisplay">
			{#each recommendations as c, i}
				<div class="vis">
					<div class="buttons">
						<button class="{recommendationsClass[i] === 'more' ? 'more' : 'default'}"
								on:click={() => updateMore(i)}>
							More Like This
						</button>
						<button class="{recommendationsClass[i] === 'less' ? 'less' : 'default'}"
								on:click={() => updateLess(i)}>
							Less Like This
						</button>
						<div class:isPinned="{recommendations[i] && currentPinned.indexOf(recommendations[i].uid) > -1}"
							 class="pinButton"
							 on:click={() => pin(i)}>
							<i class="material-icons-outlined md-24">push_pin</i>
						</div>
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
		<a id="closeButton" on:click={closePin}>&times;</a>
		<div id="pinnedDisplay">
			{#each pinned as p, i}
				<div id="pin{i}"></div>
			{/each}
		</div>
	</div>
</div>

<style>
	#overall {
		display: flex;
		background: #f3f3f3;
		width: 100%;
		overflow: scroll;
	}

	.showLoader {
		display: flex;
	}

	.hideLoader {
		display: none;
	}

	.loader {
		width: 100vw;
		height: 100%;
		position: fixed;
		z-index: 100;
		opacity: 0.2;
		background-color: gray;
	    align-items: center;
	    justify-content: center;
	}

	.spinner {
		border: 16px solid #f3f3f3;
		border-radius: 50%;
		border-top: 16px solid #3498db;
		width: 80px;
		height: 80px;
		-webkit-animation: spin 2s linear infinite; /* Safari */
		animation: spin 2s linear infinite;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	#recommendations {
		padding-top: 20px;
		margin-bottom: 20px
	}

	/*#recommendationDisplay {
		display: grid;
		grid-template-columns: repeat(3, 350px);
		grid-template-rows: repeat(3, 350px);
		grid-gap: 15px;
		margin-top: 50px;
	}*/

	#recommendationDisplay {
		display: grid;
		grid-template-columns: repeat(2, 480px);
		grid-template-rows: repeat(2, 460px);
		grid-gap: 15px;
		margin-top: 50px;
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
		padding-top: 30px;
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
		max-width: 480px
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
		width: 28px;
    	height: 28px;
    	color: gray;
    	cursor: pointer;
    	transition: transform 0.5s;
	}

	.isPinned {
		color: green;
	    transform: rotate(45deg);
	    transition: transform 0.5s;
	}

	.more {
		background-color: #cde09b;
		margin-right: 0.5em;
	}

	.less {
		background-color: #e0a99b;
		margin-right: 0.5em;
	}

	.default {
		background-color: #f4f4f4;
		margin-right: 0.5em;
	}

	.vegaContainer {
		height: 400px;
		overflow: scroll;
	    background: white;
	    display: flex;
	    flex-direction: column;
	}
</style>
