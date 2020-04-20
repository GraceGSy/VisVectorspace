import flatten from 'flat'

export default function(vegaSpec) {
	let attributes = flatten(vegaSpec['encoding'])

	let allAttributes = ['x.field','x.type','x.aggregate','x.channel','x.bin','x.maxbins','x.scale',
						 'y.field','y.type','y.aggregate','y.channel','y.bin','y.maxbins','y.scale',
						 'row.field','row.type','row.aggregate','row.channel','row.bin','row.maxbins','row.scale',
						 'column.field','column.type','column.aggregate','column.channel','column.bin','column.maxbins','column.scale',
						 'color.field','color.type','color.aggregate','color.channel','color.bin','color.maxbins','color.scale',
						 'size.field','size.type','size.aggregate','size.channel','size.bin','size.maxbins','size.scale',
						 'shape.field','shape.type','shape.aggregate','shape.channel','shape.bin','shape.maxbins','shape.scale',
						 'text.field','text.type','text.aggregate','text.channel','text.bin','text.maxbins','text.scale',
						 'mark_area','mark_bar','mark_boxplot','mark_circle','mark_errorband','mark_errorbar','mark_line','mark_point',
						 'mark_rect','mark_rule','mark_tick']

	let result = {}

	for (let a of allAttributes) {
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