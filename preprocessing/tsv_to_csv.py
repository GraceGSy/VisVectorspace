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

with open("title.principals.tsv") as fileMeta:
	readMeta = csv.reader(fileMeta, delimiter="\t", quotechar='"')

	# Skip headers
	next(readMeta, None)

	principalsCount = {}

	for row in readMeta:

		try:
			[tconst, ordering, nconst, category, job, characters] = row
			if tconst not in principalsCount:
				principalsCount[tconst] = 0

			principalsCount[tconst] += 1


		except Exception as e:
			continue

print("principals done...")

other = ['Horror', 'Biography', 'Mystery', 'Fantasy', 'Thriller', 'Western', 'Sci-Fi', 'History', 'War', 'Romance', 'Musical', 'Sport', 'Reality-TV']

with open("title.basics.tsv") as fileMeta:
	readMeta = csv.reader(fileMeta, delimiter="\t", quotechar='"')

	# Skip headers
	next(readMeta, None)

	moviesData = ["tconst,title,type,year,minutes,rating,votes,principals,genre"]

	for row in readMeta:

		try:
			[tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres] = row

			# Exclude titles with no genres
			if genres == "\\N":
				continue

			genreMain = genres.split(",")[0]
			if genreMain in other:
				genreMain = 'Other'

		except Exception as e:
			continue

		# if (runtimeMinutes != "\\N") and (int(runtimeMinutes) > 1000):
		# 	print(tconst, originalTitle)

		# Exclude titles without runtime, start year, ratings and principals count
		# Also exclude titles with runtime > 1000 and genre == Adult
		# Limit to titles from the 1990s (so >= 1990 <2000)
		if (runtimeMinutes != "\\N") and \
			(int(runtimeMinutes) < 1000) and \
			(startYear != "\\N") and \
			(int(startYear) >= 1990) and \
			(int(startYear) < 2000) and \
			(tconst in titles) and \
			(tconst in ratings) and \
			(tconst in principalsCount) and \
			genreMain != "Adult":
			newRow = [tconst, titles[tconst].replace(",", ""), titleType, startYear, runtimeMinutes, ratings[tconst]["averageRating"], ratings[tconst]["numVotes"], str(principalsCount[tconst]), genreMain]

			moviesData.append(",".join(newRow))

print(len(moviesData))

with open("movies.csv", "w") as writefile:
	writefile.write("\n".join(moviesData))