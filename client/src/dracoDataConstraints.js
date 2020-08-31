// This is a heuristic function and may not always work
// May need to be improved at a later date
function getType(uniqueValues) {
	let result = 'number'

	for (let v of uniqueValues) {

		// Does Draco support ordinal/temporal?
		// Needs verification
		if (isNaN(parseFloat(v))) {
			result = 'string'
		} else {
			continue
		}
	}

	return result
}

function schemaToConstraint(a, attributeSchema) {
	let attributeType = getType(Object.keys(attributeSchema['unique']))

	let constraintTemplate = `fieldtype(${a},${attributeType}). cardinality(${a},${attributeSchema['distinct']}).`

	return constraintTemplate
}

export default function(schema) {
	let allConstraints = []

	let attributes = Object.keys(schema['stats'])

	for (let a of attributes) {
		let attributeSchema = schema['stats'][a]

		let attributeConstraint = schemaToConstraint(a, attributeSchema)

		allConstraints.push(attributeConstraint)
	}

	return allConstraints.join('\n\n')
}