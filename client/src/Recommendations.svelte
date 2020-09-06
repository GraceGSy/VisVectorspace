<script>
	import * as d3 from 'd3'
	import Draco from 'draco-vis'
	import vegaToRanking from './vegaToRanking.js'
	import dracoDataConstraints from './dracoDataConstraints.js'
	import dracoMarkConstraints from './dracoMarkConstraints.js'
	import dracoVisConstraints from './dracoVisConstraints.js'
	import defaultConstraints from './defaults.js'

	import getRecombinations from './getRecombinations.js'

	export let vegaSpecs = []
	export let dataset = []
	export let selectedAttributes = []
	export let recomendationCount = 9
	export let updateCount = 0

	console.log(vegaSpecs)

	// Track of user preferences
	let moreLikeThis = []
	let lessLikeThis = []

	// Current recommendations
	let recommendations = []
	// Recommendations generated from the same draco query
	let similarRecommendations = []
	// Recommendations class
	let recommendationsClass = Array(9).fill("default")

	let classifierResult

	function solveDraco(newConstraints) {
		// console.log(newConstraints)
		let recs = []

		const url = 'https://unpkg.com/wasm-clingo@0.2.2';

		// const newConstraints = getDracoConstraints()
		// console.log(newConstraints)
		let markConstraints = dracoMarkConstraints(newConstraints)
		let visConstraints = dracoVisConstraints(newConstraints)
		// let visConstraints = ''

		const draco = new Draco(url)
		return draco.init().then(() => {
			// Get metadata about dataset
			draco.prepareData(dataset)
			const schema = draco.getSchema()
			const dataConstraints = dracoDataConstraints(schema)

			// Create constraints based on schema
			const inputConstraints = `
				data("cereal.csv").
				num_rows(77).

				${dataConstraints}

				${markConstraints}

				% ====== Query constraints ======
				${visConstraints}
			`;

			const solution = draco.solve(inputConstraints, { models: recomendationCount });
			if (!solution) {
				return 
			}

			for (let s of solution['specs']) {
				recs.push({'vega':s})
			}

			similarRecommendations = []
			similarRecommendations = recs

			return recs
		})
	}

	function getSimilar(newRecommendations) {
		let result = []

		for (let nr of newRecommendations) {
			// console.log(nr)
			let individualSpecs = vegaToRanking(nr['vega'])
			let rankedSpecs = []
			for (let s of Object.keys(individualSpecs)) {
				if (individualSpecs[s] !== 0) {
					rankedSpecs.push({'attr': s, 'value': individualSpecs[s]})
				}
			}

			result.push(solveDraco(rankedSpecs))
		}
		
		return result
	}

	function selectRecommendations(similarRecommendations) {
		let allNew = []

		for (let i = 0; i < 9; i++) {
			let currentSet = JSON.parse(JSON.stringify(similarRecommendations[i]))
			if (currentSet && currentSet.length > 0) {
				currentSet = currentSet.filter(r => r)
				currentSet = currentSet.map(r => {
					r.index = i
					return r
				})
				allNew.push(currentSet)
			}
		}

		let result = []
		let setNumber = 0

		while (result.length < 9) {
			let set = allNew[setNumber % allNew.length]
			let randomIndex = Math.floor(Math.random() * (set.length))
			let selected = set[randomIndex]

			if (result.length === 0) {
				result.push(selected)
			} else {
				let isNew = true
				for (let r of result) {
					if (JSON.stringify(r.vega) === JSON.stringify(selected.vega)) {
						isNew = false
					}
				}
				if (isNew) {
					result.push(selected)
					setNumber++
				}
			}
		}

		recommendationsClass = recommendationsClass.map(r => 'default')

		return result
	}

	$: {console.log(classifierResult)
		if (typeof classifierResult !== "undefined") {
			let updatedPreferrences = []

			for (let i = 0; i < classifierResult.length; i++) {
				if (i === 1) {
					updatedPreferrences.push(vegaSpecs[i])
				}
			}

			console.log('updatedPreferrences', updatedPreferrences)

			Promise.all(getRecombinations(updatedPreferrences, dataset)).then((result) => {
				similarRecommendations = result
				recommendations = selectRecommendations(result)
			})
		}
	}

	function runClassifier() {
		let testingData = vegaSpecs.map(v => v.spec)
		let trainingData = []

		let newMore = []
		let newLess = []

		for (let i = 0; i < recommendationsClass.length; i++) {
			let r = recommendationsClass[i]
			if (r === 'more') {
				newMore.push(recommendations[i])
			} else if (r === 'less') {
				newLess.push(recommendations[i])
			}
		}

		moreLikeThis = moreLikeThis.concat(newMore)
		lessLikeThis = lessLikeThis.concat(newLess)

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

		let classifierData = {
			'training': trainingData,
			'testing': testingData
		}

		fetch(`./classifier`, {method:"POST", body:JSON.stringify(classifierData)})
			.then(d => d.text())
      		.then(d => (classifierResult = d))
	}

	$: {console.log('update count', updateCount)
		if (updateCount === 1) {
			Promise.all(getRecombinations(vegaSpecs, dataset)).then((result) => {
				similarRecommendations = result
				recommendations = selectRecommendations(result)
			})
		}
		else if (updateCount === 0) {}
		else {
			console.log('running classifier: ', updateCount)
			runClassifier()
		}}

	$: for (let rec = 0; rec < recommendations.length; rec++) {
		if (!recommendations[rec]) {continue}
		vegaEmbed(`#vis${rec}`, recommendations[rec]['vega'])
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
</script>

<div id="recommendationDisplay">
	{#each recommendations as c, i}
		<div class="vis">
			<div id="vis{i}"></div>
			<div class="buttons">
				<button class="{recommendationsClass[i] === 'more' ? 'more' : 'default'}"
						on:click={() => updateMore(i)}>
					More Like This
				</button>
				<button class="{recommendationsClass[i] === 'less' ? 'less' : 'default'}"
						on:click={() => updateLess(i)}>
					Less Like This
				</button>
			</div>
		</div>
	{/each}
</div>

<style>
	#recommendationDisplay {
		display: grid;
		grid-template-columns: repeat(3, 350px);
		grid-template-rows: repeat(3, 350px);
		grid-gap: 50px;
		margin-top: 50px
	}

	.vis {
		overflow: scroll;
	}

	.more {
		background-color: #cde09b;
	}

	.less {
		background-color: #e0a99b;
	}

	.default {
		background-color: #f4f4f4;
	}
</style>
