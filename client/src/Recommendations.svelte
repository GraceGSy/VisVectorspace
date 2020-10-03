<script>
	import * as d3 from 'd3'
	import Draco from 'draco-vis'
	import vegaToRanking from './vegaToRanking.js'
	import defaultConstraints from './defaults.js'

	import getRecombinations from './getRecombinations.js'

	import AttributesWeight from './AttributesWeight.svelte'

	export let vegaSpecs = []
	export let dataset = []
	export let selectedAttributes = []
	export let recomendationCount = 9
	
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
	let recommendationsClass = Array(9).fill("default")

	let classifierResult

	let pinned = []

	let attributesWeight = []

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
	}

	function runClassifier() {
		let testingData = vegaSpecs.map(v => v.spec)
		let trainingData = []

		let newMore = []
		let newLess = []
		let newMaybe = []

		for (let i = 0; i < recommendationsClass.length; i++) {
			let r = recommendationsClass[i]
			if (r === 'more') {
				newMore.push(recommendations[i])
			} else if (r === 'less') {
				newLess.push(recommendations[i])
			} else {
				newMaybe.push(recommendations[i])
			}
		}

		// If no user feedback provided
		if (newMore.length === 0 && newLess.length  === 0) {
			Promise.all(getRecombinations(vegaSpecs, dataset)).then((result) => {
				selectRecommendations(result)
			})
			return
		}

		moreLikeThis = moreLikeThis.concat(newMore)
		lessLikeThis = lessLikeThis.concat(newLess)
		maybeLikeThis = maybeLikeThis.concat(newMaybe)

		for (let m of moreLikeThis) {
			let newM = m.vega.encoding
			newM.label = 1
			newM['mark'] = m.vega.mark
			trainingData.push(newM)
		}
		for (let l of lessLikeThis) {
			let newL = l.vega.encoding
			newL.label = -1
			newL['mark'] = l.vega.mark
			trainingData.push(newL)
		}
		for (let mb of maybeLikeThis) {
			let newMb = mb.vega.encoding
			newMb.label = 0
			newMb['mark'] = mb.vega.mark
			trainingData.push(newMb)
		}

		console.log(testingData)

		let classifierData = {
			'training': trainingData,
			'testing': testingData
		}

		fetch(`./classifier`, {method:"POST", body:JSON.stringify(classifierData)})
			.then(d => d.text())
      		.then(d => {
      			let result = JSON.parse(d)

      			attributesWeight = result["feature_wts"]

      			let preferred = result["pred"]
      			let updatedLikes = []
      			let updatedMaybe = []
      			let updatedNo = []

				for (let i = 0; i < preferred.length; i++) {
					if (preferred[i] === 1) {
						updatedLikes.push(vegaSpecs[i])
					} else if (preferred[i] === 0) {
						updatedMaybe.push(vegaSpecs[i])
					} else {
						updatedNo.push(vegaSpecs[i])
					}
				}

				let updatedPreferrences

				console.log('recommended... ', updatedLikes.length)

				if (updatedLikes.length < 9) {
					updatedPreferrences = updatedLikes.concat(updatedMaybe)
					if (updatedPreferrences.length < 9) {
						updatedPreferrences = updatedPreferrences.concat(updatedNo)
					}
				} else {
					updatedPreferrences = updatedLikes
				}

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
		pinned = pinned.concat([recommendations[i]])
	}

	function showPin() {
		document.getElementById("pinnedDrawer").style.width = "450px"
	}

	function closePin() {
		document.getElementById("pinnedDrawer").style.width = "0px"
	}
</script>

<div id="overall">
	<AttributesWeight attributes={attributesWeight}/>
	<div id="recommendations">
		<div id="menu">
			<p><b>RECOMMENDATIONS</b></p>
			<button on:click={update}>UPDATE RECOMMENDATIONS</button>
			<button on:click={reset}>RESET</button>
			<button on:click={showPin}>PINNED</button>
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
						<div class="pinButton" on:click={() => pin(i)}>
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
		background: #f4f4f4;
		padding-right: 25px;
	}

	#recommendationDisplay {
		display: grid;
		grid-template-columns: repeat(3, 350px);
		grid-template-rows: repeat(3, 350px);
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
		max-width: 420px
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
		height: 322px;
		overflow: scroll;
	    background: white;
	    display: flex;
	    flex-direction: column;
	}
</style>
