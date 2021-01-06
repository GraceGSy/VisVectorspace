# Original data from imdb https://www.imdb.com/interfaces/

import csv

with open("title.akas.tsv") as titles:
	readTitles = csv.reader(titles, delimiter="\t", quotechar='"')

	# Skip headers
	next(readTitles, None)

	titles = {}

	for row in readTitles:
		[titleId, ordering, title, region, language, types, attributes, isOriginalTitle] = row
		
		# we use the US title for each movie 
		# if movie does not have a US title, exclude for now
		if region == "US":
			titles[titleId] = title

print("titles done...")

with open("title.ratings.tsv") as fileRatings:
	readRatings = csv.reader(fileRatings, delimiter="\t", quotechar='"')

	# Skip headers
	next(readRatings, None)

	ratings = {}

	for row in readRatings:
		[tconst, averageRating, numVotes] = row
		ratings[tconst] = {"averageRating": averageRating, "numVotes": numVotes}

print("ratings done...")

with open("title.basics.tsv") as fileMeta:
	readMeta = csv.reader(fileMeta, delimiter="\t", quotechar='"')

	# Skip headers
	next(readMeta, None)

	moviesData = ["tconst,title,type,start year,runtime (min),average rating,num votes"]

	for row in readMeta:

		try:
			[tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres] = row

		except Exception as e:
			continue

		# if (runtimeMinutes != "\\N") and (int(runtimeMinutes) > 1000):
		# 	print(tconst, originalTitle)

		# Exclude titles without runtime, start year and ratings
		# Also exclude titles with runtime > 1000
		# Limit to shows from the 1990s (so >= 1990 <2000)
		if (runtimeMinutes != "\\N") and (int(runtimeMinutes) < 1000) and (startYear != "\\N") and (int(startYear) >= 1990) and (int(startYear) < 2000) and (tconst in titles) and (tconst in ratings):
			newRow = [tconst, titles[tconst].replace(",", ""), titleType, startYear, runtimeMinutes, ratings[tconst]["averageRating"], ratings[tconst]["numVotes"]]

			moviesData.append(",".join(newRow))

print(len(moviesData))

with open("movies.csv", "w") as writefile:
	writefile.write("\n".join(moviesData))