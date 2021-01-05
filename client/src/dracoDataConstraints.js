// This is a heuristic function and may not always work
// May need to be improved at a later date
function getType(uniqueValues) {
	let result = 'number'

	for (let v of uniqueValues) {

		// Does Draco support ordinal/temporal?
		// Needs verification
		if (isNaN(parseFloat(v)) && v != "NaN") {
			result = 'string'
		} else {
			continue
		}
	}

	console.log(result)

	return result
}

function schemaToConstraint(a, attributeSchema) {
	let attributeType = getType(Object.keys(attributeSchema['unique']))

	console.log("attribute schema", attributeSchema)

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

	console.log(allConstraints)

	return allConstraints.join('\n\n')
}