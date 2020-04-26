<script>
	import * as d3 from 'd3'
	import Draco from 'draco-vis'
	import vegaToRanking from './vegaToRanking.js'
	import dracoDataConstraints from './dracoDataConstraints.js'
	import dracoMarkConstraints from './dracoMarkConstraints.js'
	import dracoVisConstraints from './dracoVisConstraints.js'
	import defaultConstraints from './defaults.js'

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

	// Initialize constraint weights
	// let constraintWeights = []

	// update constraints
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

		// Remove duplicates
		attrs = new Set(attrs)

		// Convert back to array
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
		console.log(newConstraints)
		let markConstraints = dracoMarkConstraints(newConstraints)
		let visConstraints = dracoVisConstraints(newConstraints)

		const draco = new Draco(url)
		draco.init().then(() => {
			// Get metadata about dataset
			draco.prepareData(dataset)
			const schema = draco.getSchema()
			const dataConstraints = dracoDataConstraints(schema)

			console.log(schema)

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

			const solution = draco.solve(inputConstraints, { models: recomendationCount });
			console.log(solution);

			recs = []

			for (let s of solution['specs']) {
				recs.push({'vega':s})
			}

			recommendations = recs
		});
	}

	let count = [0, 1, 2, 3, 4, 5, 6, 7, 8]

	$: if (updateCount > 0) {solveDraco()}

	$: for (let rec = 0; rec < recommendations.length; rec++) {
		vegaEmbed(`#vis${rec}`, recommendations[rec]['vega'])
	}

	function updateMore(i) {
		moreLikeThis.push(recommendations[i])
	}

	function updateLess(i) {
		lessLikeThis.push(recommendations[i])
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
