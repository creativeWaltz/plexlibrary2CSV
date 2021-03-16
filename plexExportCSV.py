#import modules and dependencies
from plexapi.server import PlexServer
from plexapi.media import Media
import csv


#Your plex credentials
PLEX_URL = 'http://192.168.0.2:32400'
PLEX_TOKEN = 'mL5Y3ttWity3xv5gTJCR'
MOVIE_LIBRARIES = ['Test','4K HDR']

#Create plex server instance
plex = PlexServer(PLEX_URL, PLEX_TOKEN)

#Get list of movies in MOVIE_LIBRARIES
movies = []
movies = plex.library.section('Test').all()

movie_list = []



#print("\n\n", movies)
for movie in movies:
		#print(movie)
		movie_list.append({"Title" : movie.title,
						   "Type" : movie.type,
						   "LastViewed" : movie.lastViewedAt
						   })



#print(movie_list[0])

for i in range(len(movie_list)):
	for media_item in movies[i].media:
		movie_list[i].update({"Bitrate":media_item.bitrate})


print(movie_list)
