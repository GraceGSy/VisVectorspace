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

	// Track of user preferences
	let moreLikeThis = []
	let lessLikeThis = []

	// Current recomendations
	let recommendations = []
	let similarRecommendations = []

	let classifierResult

	function solveDraco(newConstraints) {
		console.log(newConstraints)
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

			// console.log(schema)

			// Create constraints based on schema
			const inputConstraints = `
				data("cereal.csv").
				num_rows(77).

				${dataConstraints}

				${markConstraints}

				% ====== Query constraints ======
				${visConstraints}
			`;

			// console.log(inputConstraints)

			const solution = draco.solve(inputConstraints, { models: recomendationCount });
			if (!solution) {
				console.log(solution, newConstraints)
				return 
			}

			for (let s of solution['specs']) {
				recs.push({'vega':s})
			}

			similarRecommendations = []
			similarRecommendations = recs

			console.log(recs)

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

	// function getAllSimilar(newRecommendations) {
	// 	// let individualSpecs = vegaToRanking(vegaSpec)
		
	// 	Promise.all(getSimilar(newRecommendations)).then((result) => {
	// 		return 
	// 		// console.log('here', result)
	// 	})
	// }

	$: {console.log(classifierResult)
		if (typeof classifierResult !== "undefined") {
			let updatedPreferrences = []

			for (let i = 0; i < classifierResult.length; i++) {
				if (i === 1) {
					updatedPreferrences.push(dataset[i])
				}
			}

			Promise.all(getRecombinations(vegaSpecs, updatedPreferrences)).then((result) => {
				similarRecommendations = result
			})
		}
	}

	function runClassifier() {
		let testingData = vegaSpecs.map(v => v.spec)
		let trainingData = []

		for (let m of moreLikeThis) {
			let newM = m.vega.encoding
			newM.label = 1
			newM['mark_' + m.vega.mark] = 1
			trainingData.push(newM)
		}
		for (let l of lessLikeThis) {
			let newL = l.vega.encoding
			newL.label = -1
			newL['mark_' + l.vega.mark] = 1
			trainingData.push(newL)
		}

		console.log('updated', trainingData)

		let classifierData = {
			'training': trainingData,
			'testing': testingData
		}

		fetch(`./classifier`, {method:"POST", body:JSON.stringify(classifierData)})
			.then(d => d.text())
      		.then(d => (classifierResult = d))
	}

	$: {recommendations = similarRecommendations.map(r => {
			if (r.length === 0) {
				return
			}
			return r[0]
		})
	}

	$: {if (updateCount === 1) {
			console.log(dataset)
			Promise.all(getRecombinations(vegaSpecs, dataset)).then((result) => {
				similarRecommendations = result
			})
			// let newRecommendations = getRecombinations(vegaSpecs, dataset)
			// getAllSimilar(newRecommendations)
			// recommendations = newRecommendations
		}
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
		moreLikeThis = moreLikeThis.concat(similarRecommendations[i])
		console.log(moreLikeThis)
	}

	// Update 'lessLikeThis' array
	function updateLess(i) {
		lessLikeThis = lessLikeThis.concat(similarRecommendations[i])
	}
</script>

<div id="recommendationDisplay">
	{#each recommendations as c, i}
		<div class="vis">
			<div id="vis{i}"></div>
			<div class="buttons">
				<button on:click={() => updateMore(i)}>
					More Like This
				</button>
				<button on:click={() => updateLess(i)}>
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
</style>
