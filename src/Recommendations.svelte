<script>
	import * as d3 from 'd3'
	import Draco from 'draco-vis'
	import vegaToRanking from './vegaToRanking.js'
	import dracoDataConstraints from './dracoDataConstraints.js'
	import dracoMarkConstraints from './dracoMarkConstraints.js'
	import dracoVisConstraints from './dracoVisConstraints.js'

	export let vegaSpecs = []
	export let dataset = []
	export let selectedAttributes = []
	export let recomendationCount = 9
	export let updateCount = 0

	let moreLikeThis = []
	let lessLikeThis = []
	let recommendations = []

	function getDracoConstraints() {
		if (moreLikeThis.length == 0 || lessLikeThis.length == 0) {
			return
		}

		let attrs = []

		let high = []
		let low = []

		for (let h of moreLikeThis) {
			let ranking = vegaToRanking(h['vega'])
			high.push(ranking)
			attrs = attrs.concat(Object.keys(ranking))
		}

		for (let l of lessLikeThis) {
			let ranking = vegaToRanking(l['vega'])
			low.push(ranking)
			attrs = attrs.concat(Object.keys(ranking))
		}

		attrs = new Set(attrs)

		attrs = [...attrs]

		let x1 = {}
		let x0 = {}

		for (let a of attrs) {
			x1[a] = d3.mean(low, function(d) { if (d[a]) {return d[a]}; return 0 });
			x0[a] = d3.mean(high, function(d) { if (d[a]) {return d[a]}; return 0});
		}

		var hlpair = [];
		for (var i = 0; i<high.length; i++) {
			for (var j = 0; j<low.length; j++) {
				var tmpelt = {};
				for (let k of attrs) {
					tmpelt[k] = high[i][k] - low[j][k];
				}
				hlpair[hlpair.length] = tmpelt;
			}
		}
		
		// calculate new attr
		console.log("Getting new axis vector...")
		var V = {}, Vchanged = {}, Verror = {}, norm = 0;
		for (let i of attrs) {
			V[i] = 0;
			Vchanged[i] = 0;
		}
		for (let i of attrs) {
		 V[i] = x0[i]-x1[i];
		 norm = norm + (x0[i]-x1[i])*(x0[i]-x1[i]);
		}
		let rankedConstraints = [];
		for (let i of attrs) {
			rankedConstraints.push({"attr":i, "value":V[i]})
		}
		rankedConstraints = rankedConstraints.sort(function(a,b) {return Math.abs(b["value"]) - Math.abs(a["value"]);})

		rankedConstraints = rankedConstraints.filter(function(a) {return a["value"] != 0})

		return rankedConstraints
	}

	function solveDraco() {
		let recs = recommendations

		const url = 'https://unpkg.com/wasm-clingo@0.2.2';

		const newConstraints = getDracoConstraints()
		let markConstraints = dracoMarkConstraints(newConstraints)
		let visConstraints = dracoVisConstraints(newConstraints)

		const draco = new Draco(url)
		draco.init().then(() => {
			// Get metadata about dataset
			draco.prepareData(dataset)
			const schema = draco.getSchema()
			const dataConstraints = dracoDataConstraints(selectedAttributes, schema)

			console.log(schema)

			// Create constraints based on schema
			const inputConstraints = `
				data("cereal.csv").
				num_rows(77).

				fieldtype(calories,number).
				cardinality(calories,11).

				fieldtype(protein,number).
				cardinality(protein,6).

				fieldtype(mfr,string).
				cardinality(mfr,7).

				fieldtype(shelf,number).
				cardinality(shelf,3).

				${markConstraints}

				% ====== Query constraints ======
				${visConstraints}
			`;

			console.log(inputConstraints)

			const solution = draco.solve(inputConstraints, { models: 9 });
			console.log(solution);

			recs = []

			for (let s of solution['specs']) {
				recs.push({'vega':s})
			}

			recommendations = recs
		});
	}

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
		recommendations = []

		for (let random of randomList) {
			let currentVega = vegaSpecs[random]['vega']
			let recombined = recombination(currentVega, dataset)

			if (!recombined) {
				console.log(random)
				continue
			} else {
				recommendations.push({'spec':vegaSpecs[random]['spec'],
									  'vega':recombined
									})
			}
		}
	}

	getRecombinations(vegaSpecs, dataset)

	let count = [0, 1, 2, 3, 4, 5, 6, 7, 8]

	$: for (let rec = 0; rec < recommendations.length; rec++) {
		vegaEmbed(`#vis${rec}`, recommendations[rec]['vega'])
	}

	$: if (updateCount > 0) {solveDraco()}

	function updateMore(i) {
		moreLikeThis.push(recommendations[i])
	}

	function updateLess(i) {
		lessLikeThis.push(recommendations[i])
	}
</script>

<div id="recommendationDisplay">
	{#each count as c, i}
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
