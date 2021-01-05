<script>
	import * as d3 from 'd3'

	export let allPoints = []
	export let shownPoints = []

	let scaleColor = d3.scaleLinear()
				    .domain([-1, 0, 1])
				    .range(["red", "white", "green"])

	$: {let svg = d3.select("#vectorspace")
		let scaleX = d3.scaleLinear()
						.domain(d3.extent(allPoints, d => d.umapX))
						.range([10, 190])
		let scaleY = d3.scaleLinear()
						.domain(d3.extent(allPoints, d => d.umapY))
						.range([10, 190])

		svg.select("#points")
			.selectAll(".point")
			.data(allPoints)
			.join("circle")
			.attr("class", "point")
			.attr("cx", d => scaleX(d.umapX))
			.attr("cy", d => scaleY(d.umapY))
			.attr("r", 2)
			.attr("fill", d => scaleColor(d.label))
			.attr("stroke", "grey")
			.attr("stroke-width", "0.5px")

		let shown = shownPoints.map(d => d.spec)

		console.log("rendering selected...")

		svg.select("#selected")
			.selectAll(".selectedPoint")
			.data(shown)
			.join("circle")
			.attr("class", "selectedPoint")
			.attr("cx", d => scaleX(d.umapX))
			.attr("cy", d => scaleY(d.umapY))
			.attr("r", 2)
			.attr("fill", d => scaleColor(d.label))
			.attr("stroke", "black")
			.attr("stroke-width", "2px")
	}

	// let attributes = Object.keys(dataset[0])
</script>

<div>
	<svg id="vectorspace" width="200px" height="200px">
		<g id="points"/>
		<g id="selected"/>
	</svg>
</div>

<style>
</style>