export default function(constraints) {
	if (!constraints) {return ''}

	let channels = ['x', 'y', 'row', 'column', 'color', 'size', 'shape', 'text']

	let encodingCount = 0

	let allConstraints = []

	for (let c of channels) {

		let relevant = constraints.filter(function(a) {return a['attr'].startsWith(c)})

		if (relevant.length != 0) {

			let newConstraint = `encoding(e${encodingCount}).:- not channel(e${encodingCount}, ${c}).`

			for (let r of relevant) {
				let attr = r['attr']

				// If there are datatype preferences
				if (attr.includes('.type')) {

					// Get type
					let type = attr.slice(attr.indexOf('type')+5)

					if (r['value'] > 0) {
						// 'moreLikeThis' type
						newConstraint = newConstraint + `:- not type(e${encodingCount}, ${type}).`
					}
				}

				// If there are field preferences
				if (attr.includes('.field')) {

					// Get field
					let field = attr.slice(attr.indexOf('field')+6)

					if (r['value'] > 0) {
						// 'moreLikeThis' field
						newConstraint = newConstraint + `:- not field(e${encodingCount}, ${field}).`
					} else {
						// 'lessLikeThis' field
						newConstraint = newConstraint + `:- field(e${encodingCount}, ${field}).`
					}
					
				}

				// If there are aggregate preferences
				if (attr.includes('.aggregate')) {

					// Get aggregate
					let agg = attr.slice(attr.indexOf('aggregate')+10)

					console.log(agg)

					if (r['value'] > 0) {
						// 'moreLikeThis' field
						newConstraint = newConstraint + `:- not aggregate(e${encodingCount}, ${agg}).`
					}
				}

				// If there are binning preferences
				if (attr.includes('.bin')) {

					if (r['value'] > 0) {
						// 'moreLikeThis' bin
						newConstraint = newConstraint + `:- not bin(e${encodingCount}, 10).`
					}
				}

			}

			allConstraints.push(newConstraint)
			encodingCount++
		}

	}

	if (allConstraints.length > 0) {
		return allConstraints.join('\n\n')
	}

	return ''
}