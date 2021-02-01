import Draco from 'draco-vis'
import vegaToRanking from './vegaToRanking.js'
import dracoDataConstraints from './dracoDataConstraints.js'
import dracoMarkConstraints from './dracoMarkConstraints.js'
import dracoVisConstraints from './dracoVisConstraints.js'
import * as d3 from 'd3'

function solveDraco(newConstraints, dataset) {
	// console.log(newConstraints)
	let recs = []

	const url = 'https://unpkg.com/wasm-clingo@0.2.2'
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

		console.log(inputConstraints)

		const solution = draco.solve(inputConstraints, { models: 4 });

		// console.log(solution)
		if (!solution) {
			// console.log('no solution')
			return []
		}

		for (let [i, s] of solution['specs'].entries()) {
			s.width = 270
			s.height = 270
			recs.push({'vega':s, 'uid': 'id' + (new Date().valueOf()) + '_' + i})
		}

		return recs
	})
}

function getTests(index, vegaSpecs, dataset) {
	// console.log('spec', vegaSpecs[index])
	let encoding = vegaSpecs[index].spec

	let constraints = []
	for (let s of Object.keys(encoding)) {
		if (s.includes("filename")) { continue; }
		else if (s.includes("none")) { continue; }
		else if (encoding[s] !== 0) {
			constraints.push({'attr': s, 'value': encoding[s]})
		}
	}
	
	return solveDraco(constraints, dataset)
}


function getRandom(min, max) {	
	let value = Math.floor(Math.random() * (max - min) + min)
	return value
}

export default function getRecombinations(vegaSpecs, dataset) {
	let selectedIndices = new Set()
	let allDracoRecommendations = []
	let count = 4

	while (allDracoRecommendations.length < count) {
		let newIndex = getRandom(0, vegaSpecs.length)

		if (!selectedIndices.has(newIndex)) {
			selectedIndices.add(newIndex)
			let newRecommendations = getTests(newIndex, vegaSpecs, dataset)
			allDracoRecommendations.push(newRecommendations)
		}
	}

	// console.log(allDracoRecommendations)

	return allDracoRecommendations
}