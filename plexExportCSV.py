#import modules and dependencies
from plexapi.server import PlexServer
from plexapi.media import Media
import csv
import sys

#Import your custom config/auth file:
import plexExportCSV_config


#Your plex credentials
PLEX_URL = plexExportCSV_config.PLEX_URL
PLEX_TOKEN = plexExportCSV_config.PLEX_TOKEN

MOVIE_LIBRARIES = ['movies'] #Add your movie libraries here, same as they are called in plex

#Create plex server instance
plex = PlexServer(PLEX_URL, PLEX_TOKEN)
print("\nConnecting to your server...")
print("\nGenerating movie list from selected libraries,please wait...")


#Get list of movies in MOVIE_LIBRARIES
#ovies = []
movies = [plex.library.section(library).all() for library in MOVIE_LIBRARIES] #use plexapi to get a list of all movies in libraries
movie_list = []


#Create the initial list of dictionaries using the Movie object from plexapi
for library_list in movies:
	for movie in library_list:
		movie_list.append({
			"addedAt": movie.addedAt,
			"Title": movie.title,
			"Year": movie.year,
			"Duration(minutes)":round((movie.duration*0.00001666667)),
			"Rating": movie.rating,
			"Genres": movie.genres,
			"Studio": movie.studio,
			"Content Rating": movie.contentRating
						   })


#Add the extra information from the media object from each movie, update dictionary with new attributes
media_object_list = []
for plexlib in movies:
	for film in plexlib:
		media_object_list.append(film.media)

for i in range(len(movie_list)):
	for media in media_object_list[i]:
		movie_list[i].update({
			"Video Resolution": media.videoResolution,
			"Video Codec": media.videoCodec,
			"Video Profile": media.videoProfile,
			"Container": media.container,
			"Apsect Ratio": media.aspectRatio,
			"Audio Channels": media.audioChannels,
			"Audio Codec": media.audioCodec
			})

#Add the location and of the movies from the mediapart object from mediapart object, add to dictionary

for i in range(len(movie_list)):
	for media in media_object_list[i]:
		for parts in media.parts:
			movie_list[i].update({
				"Size (GB)" : round(parts.size/1073741824,2),
				"LocationOnDisk": parts.file
				})
		
				

#Create the labels from they keys of the dictionary of the first movie
labels = [key for key in movie_list[0]]

print("\nThere are a total of ",len(movie_list), "movies in the selected libraries" )

#Write the dictionary to a csv
try:
    with open('movies.csv', 'w') as movies_csv:
        writer = csv.DictWriter(movies_csv, fieldnames=labels)
        writer.writeheader()
        for elem in movie_list:
            writer.writerow(elem)
    print("Your CSV is ready!...")
except IOError:
    print("I/O error")
