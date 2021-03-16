#import modules and dependencies
from plexapi.server import PlexServer
from plexapi.media import Media
import csv

print("""
  _____  _           ______                       _    _____  _______      __
 |  __ \| |         |  ____|                     | |  / ____|/ ____\ \    / /
 | |__) | | _____  _| |__  __  ___ __   ___  _ __| |_| |    | (___  \ \  / / 
 |  ___/| |/ _ \ \/ |  __| \ \/ | '_ \ / _ \| '__| __| |     \___ \  \ \/ /  
 | |    | |  __/>  <| |____ >  <| |_) | (_) | |  | |_| |____ ____) |  \  /   
 |_|    |_|\___/_/\_|______/_/\_| .__/ \___/|_|   \__|\_____|_____/    \/    
                                | |                                          
                                |_|                                          
""")

#Your plex credentials
PLEX_URL = 'http://192.168.0.2:32400'
PLEX_TOKEN = 'mL5Y3ttWity3xv5gTJCR'
MOVIE_LIBRARIES = ['Test','Test2']

#Create plex server instance
plex = PlexServer(PLEX_URL, PLEX_TOKEN)
print("\nConnecting to your server...")

#Get list of movies in MOVIE_LIBRARIES
#ovies = []
movies = [plex.library.section(library).all() for library in MOVIE_LIBRARIES]
movie_list = []


for library_list in movies:
	for movie in library_list:
		movie_list.append({
			"addedAt": movie.addedAt,
			"Title": movie.title,
			"Year": movie.year,
			"Duration(minutes)":round((movie.duration*0.00001666667)),
			"Type": movie.type,
			"Rating": movie.rating,
			"LastViewed" : movie.lastViewedAt,
			"Genres": movie.genres,
			"Studio": movie.studio,
			"Content Rating": movie.contentRating
						   })

print("\nGenerating movie list from selected libraries...")
print("\nThere are a total of ",len(movie_list), "movies in the selected libraries" )


full_list = []
for plexlib in movies:
	for film in plexlib:
		full_list.append(film.media)

for i in range(len(movie_list)):
	for media in full_list[i]:
		movie_list[i].update({
			"Video Resolution": media.videoResolution,
			"Video Codec": media.videoCodec,
			"Video Framerate": media.videoFrameRate,
			"Video Profile": media.videoProfile,
			"Container": media.container,
			"Apsect Ratio": media.aspectRatio,
			"Height": media.height,
			"Width": media.width,
			"Audio Channels": media.audioChannels,
			"Audio Codec": media.audioCodec,
			"Audio Profile": media.audioProfile,
			})



labels = [key for key in movie_list[0]]

#Write the dictionary to a csv
try:
    with open('movies.csv', 'w') as movies_csv:
        writer = csv.DictWriter(movies_csv, fieldnames=labels)
        writer.writeheader()
        for elem in movie_list:
            writer.writerow(elem)
except IOError:
    print("I/O error")
