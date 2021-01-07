import csv

allGenres = {'Drama': 133400,
'Short': 12665,
'Documentary': 42250,
'Action': 32333,
'Horror': 2461,
'Adventure': 20090,
'Comedy': 113303,
'Crime': 21476,
'Biography': 5247,
'Animation': 21464,
'Adult': 16061,
'News': 21731,
'Family': 23035,
'Mystery': 1312,
'Talk-Show': 21008,
'Fantasy': 1500,
'Thriller': 2069,
'Western': 169,
'Music': 17671,
'Sci-Fi': 1130,
'Game-Show': 18509,
'History': 1256,
'War': 178,
'Romance': 4205,
'Musical': 1702,
'Sport': 7081,
'Reality-TV': 4722}

other = ['Horror', 'Biography', 'Mystery', 'Fantasy', 'Thriller', 'Western', 'Sci-Fi', 'History', 'War', 'Romance', 'Musical', 'Sport', 'Reality-TV']

# with open("title.basics.tsv") as fileMeta:
# 	readMeta = csv.reader(fileMeta, delimiter="\t", quotechar='"')

# 	# Skip headers
# 	next(readMeta, None)

# 	moviesData = ["tconst,title,type,start year,runtime (min),average rating,num votes"]

# 	genresDict = {}

# 	for row in readMeta:

# 		try:
# 			[tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres] = row
# 			if (int(startYear) >= 1990) and (int(startYear) < 2000) and (genres != "\\N"):
# 				genreMain = genres.split(",")[0]
# 				if genreMain in other:
# 					genreMain = 'Other'

# 				if genreMain not in genresDict:
# 					genresDict[genreMain] = 0

# 				genresDict[genreMain] += 1


# 		except Exception as e:
# 			continue

# 	print(genresDict)

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

	print(principalsCount['tt0000001'])



