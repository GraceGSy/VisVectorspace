import defaultConstraints from './defaults.js'

export default function(constraints) {
	if (!constraints) {return ''}

	let defaults = defaultConstraints['defaultMarkConstraints']
	
	let allConstraints = []

	for (let c of constraints) {

		let attr = c['attr']

		if (attr.startsWith('mark')) {
			let markType = attr.slice(5)

			let value = c['value']

			if (value > 0) {
				allConstraints.push(`mark(${markType}).`)
			}
		}
	}

	if (allConstraints.length > 0) {
		return allConstraints.join('\n\n')
	}

	return ''
}