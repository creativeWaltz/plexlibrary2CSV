# import modules and dependencies
from plexapi.server import PlexServer
# from plexapi.media import Media
import csv
from datetime import datetime

# Import your custom config/auth file:
import plexExportCSV_config

# Your plex credentials
PLEX_URL = plexExportCSV_config.PLEX_URL
PLEX_TOKEN = plexExportCSV_config.PLEX_TOKEN

# should show a list of existing folders for user to select from:
MOVIE_LIBRARIES_TO_EXPORT = ['movies']

# Create plex server instance
plex = PlexServer(PLEX_URL, PLEX_TOKEN)
print("\nConnecting to your server...")
print("\nGenerating movie list from selected libraries,please wait...")


# Function to create movie object list from selected movie libraries


def create_movie_object_list(plex_movie_libraries):
    object_list = []
    for library in plex_movie_libraries:
        object_list.extend(plex.library.section(library).all())
    return object_list


def create_movie_dictionary(object_list):
    movielist = []
    for i in range(len(object_list)):
        movielist.append({
            "addedAt": object_list[i].addedAt,
            "Title": object_list[i].title.title(),
            "Year": object_list[i].year,
            "Duration(minutes)": round((object_list[i].duration * 0.00001666667)),
            "Rating": object_list[i].rating,
            "Genres": object_list[i].genres,
            "Studio": object_list[i].studio,
            "Content Rating": object_list[i].contentRating,
            "Video Resolution": object_list[i].media[0].videoResolution,
            "Video Codec": object_list[i].media[0].videoCodec,
            "Video Profile": object_list[i].media[0].videoProfile,
            "Container": object_list[i].media[0].container,
            "Aspect Ratio": object_list[i].media[0].aspectRatio,
            "Audio Channels": object_list[i].media[0].audioChannels,
            "Audio Codec": object_list[i].media[0].audioCodec,
            "Size (GB)": round(object_list[i].media[0].parts[0].size / 1073741824, 2),
            "LocationOnDisk": object_list[i].media[0].parts[0].file
        })
    return movielist


movie_objects = create_movie_object_list(MOVIE_LIBRARIES_TO_EXPORT)
movie_list = (create_movie_dictionary(movie_objects))

# Create the labels from they keys of the dictionary of the first movie
labels = [key for key in movie_list[0]]

print("\nThere are a total of ", len(movie_list), "movies in the selected libraries")

# Write the dictionary to a csv
try:
    with open(f'movies-{datetime.now()}.csv', 'w') as movies_csv:
        writer = csv.DictWriter(movies_csv, fieldnames=labels)
        writer.writeheader()
        for elem in movie_list:
            writer.writerow(elem)
    print('Your CSV is ready!...')
except IOError:
    print("I/O error")
