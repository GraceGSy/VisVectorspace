<script>
	import * as d3 from 'd3'
	import Draco from 'draco-vis'

	export let vegaSpecs = []
	export let dataset = []
	export let recomendationCount = 9
	export let updateCount = 0

	let moreLikeThis = []
	let lessLikeThis = []
	let recommendations = []

	function getDracoConstraints(updateCount) {
		if (moreLikeThis.length == 0 || lessLikeThis.length == 0) {
			return
		}

		for (var i = 0; i<attrNo; i++) {
			x1[attr[i]] = d3.mean(low, function(d) { return d["coord"][aainttr[i]]});
			x0[attr[i]] = d3.mean(high, function(d) { return d["coord"][attr[i]]});
		}

		var hlpair = [];
		for (var i = 0; i<high.length; i++) {
			for (var j = 0; j<low.length; j++) {
				var tmpelt = {};
				for (var k = 0; k<attrNo; k++) {
					tmpelt[attr[k]] = high[i]["coord"][attr[k]] - low[j]["coord"][attr[k]];
				}
				hlpair[hlpair.length] = tmpelt;
			}
		}
		
		// calculate new attr
		console.log("Getting new axis vector...")
		var V = {}, Vchanged = {}, Verror = {}, norm = 0;
		for (var i = 0; i<attrNo; i++) {
			V[attr[i]] = 0;
			Vchanged[attr[i]] = 0;
		}
		for (var i = 0; i<attrNo; i++) {
		 V[attr[i]] = x0[attr[i]]-x1[attr[i]];
		 norm = norm + (x0[attr[i]]-x1[attr[i]])*(x0[attr[i]]-x1[attr[i]]);
		}
		var VV = [];
		for (var i = 0; i<attrNo; i++) {
			VV[i] = {"attr":attr[i], "value":V[attr[i]]};
		}
		VV.sort(function(a,b) {return Math.abs(b["value"]) - Math.abs(a["value"]);});
	}

	function solveDraco() {
		let recs = recommendations

		const url = 'https://unpkg.com/wasm-clingo@0.2.2';

		const draco = new Draco(url)
		draco.init().then(() => {
			// Get metadata about dataset
			draco.prepareData(dataset)
			const schema = draco.getSchema()

			// Create constraints based on schema
			const constraints = `
				data("cereal.csv").
				num_rows(77).

				fieldtype(mfr,string).
				cardinality(mfr,7).

				fieldtype(calories,number).
				cardinality(calories,11).

					% ====== Query constraints ======
					encoding(e0).
					:- not field(e0,mfr).

					encoding(e1).
					:- not field(e1,calories).
			`;

			const solution = draco.solve(constraints, { models: 9 });
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
		moreLikeThis.append(recommendations[i])
	}

	function updateLess(i) {
		lessLikeThis.append(recommendations[i])
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
