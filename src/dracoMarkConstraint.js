export default function(constraints) {
	let allConstraints = []

	for (let c of constraints) {

		let attr = c['attr']

		if (attr.startsWith('mark')) {
			let markType = attr.slice(5)

			let value = c['value']

			if (value > 0) {
				allConstraints.push(`mark(${markType}).`)
			} else {
				allConstraints.push(`not mark(${markType}).`)
			}
		}
	}

	return allConstraints.join('\n\n')
}