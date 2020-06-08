import flatten from 'flat'
import defaultConstraints from './defaults.js'

export default function(vegaSpec) {
	let attributes = flatten(vegaSpec['encoding'])

	let defaults = defaultConstraints['defaultVisConstraints'].concat(defaultConstraints['defaultMarkConstraints'])

	let result = {}

	for (let a of defaults) {
		if (a in attributes && typeof(attributes[a]) == 'string') {
			result[ a + '.' + attributes[a]] = 1
		} else if (a in attributes) {
			result[a] = 1
		} else {
			result[a] = 0
		}
	}

	let mark = vegaSpec['mark']

	result[`mark_${mark}`] = 1

	return result
}