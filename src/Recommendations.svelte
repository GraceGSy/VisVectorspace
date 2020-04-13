<script>
	import * as d3 from 'd3'

	export let vegaSpecs = []
	export let dataset = []

	function getMappings(encoding, typedVariables) {
		let originalVars = {}

		for (let channel in encoding) {
			let channelVar = encoding[channel]['field']
			let channelType = encoding[channel]['type']

			if (!originalVars[channelVar]) {
				originalVars[channelVar] = new Set([])
			}

			for (let newVar in typedVariables[channelType]) {
				originalVars[channelVar].add(typedVariables[channelType][newVar])
			}
		}

		for (let variable in originalVars) {
			originalVars[variable] = Array.from(originalVars[variable])
		}

		return originalVars
	}

	function getEncodings2(encoding, typedVariables, dataset) {
		let newEncodings = [encoding]
		let possibleEncodings = getMappings(encoding, typedVariables)

		for (let originalVar in possibleEncodings) {
			let tempEncodings = []

			if (possibleEncodings[originalVar].length == 0) {
				console.log(`no possible mappings for ${originalVar}`)
				return
			}

			for (let v in possibleEncodings[originalVar]) {
				let vName = possibleEncodings[originalVar][v]
				let currentEncodings = JSON.parse(JSON.stringify(newEncodings))
				currentEncodings = currentEncodings.map(function(x) {
					for (let channel in x) {
						if (x[channel]['field'] === originalVar) {
							x[channel]['field'] = vName
							if (x[channel]['scale'] && x[channel]['scale']['domain']) {
								x[channel]['scale']['domain'] = d3.extent(dataset, d => d[vName])
							}
						}

						if (x[channel]['axis'] && x[channel]['axis']['title']) {
							delete x[channel]['axis']['title']
						}

						if (x[channel]['legend'] && x[channel]['legend']['title']) {
							delete x[channel]['legend']['title']
						}
					}
					return x
				})
				tempEncodings = tempEncodings.concat(currentEncodings)
			}

			newEncodings = tempEncodings
		}

		return newEncodings
	}

	function recombination(spec, dataset) {
		if (spec['title']) {
			delete spec['title']
		}

		if (spec['transform']) {
			delete spec['transform']
		}
		let variable_types = {}

		// abstract this later
		let typed_variables = {'quantitative':['calories', 'protein', 'fat',
												'sodium', 'fiber', 'carbo',
												'sugars', 'potass', 'vitamins',
												'weight', 'cups', 'rating'],
								'nominal':['name', 'mfr'],
								'ordinal':['shelf']}

		let allEncodings = getEncodings2(spec['encoding'], typed_variables, dataset)

		if (!allEncodings) {return}

		//////// RETURN MORE THAN ONE ////////
		//////////////////////////////////////
		// let newSpecs = []

		// for (let i = 1; i < 4; i++) {
		// 	let copySpec = JSON.parse(JSON.stringify(spec))
		// 	copySpec['encoding'] = allEncodings[i]
		// 	copySpec['data']['values'] = data
		// 	newSpecs.push(copySpec)
		// }

		// return newSpecs
		//////////////////////////////////////
		//////// RETURN MORE THAN ONE ////////

		let copySpec = JSON.parse(JSON.stringify(spec))
		copySpec['encoding'] = allEncodings[1]
		copySpec['data']['values'] = dataset
		delete copySpec['data']['url']

		return copySpec	
	}

	function getRecombinations(vegaSpecs, dataset) {
		let randomList = [7, 18, 142, 20, 212, 251, 213, 300, 272]
		let recommendations = []

		for (let random of randomList) {
			let currentSpec = vegaSpecs[random]
			let recombined = recombination(currentSpec, dataset)

			if (!recombined) {
				console.log(random)
				continue
			} else {
				recommendations.push(recombined)
			}

			// if (recommendations.length == 9) {
			// 	console.log(recommendations)
			// 	return recommendations
			// }
		}

		return recommendations
	}

	let recommendations = getRecombinations(vegaSpecs, dataset)

	let count = [0, 1, 2, 3, 4, 5, 6, 7, 8]

	for (let rec = 0; rec < recommendations.length; rec++) {
		vegaEmbed(`#vis${rec}`, recommendations[rec])
	}
</script>

<div id="recommendationDisplay">
	{#each count as c, i}
		<div id="vis{i}"></div>
	{/each}
</div>