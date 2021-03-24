
# version 0.1.0


from plexapi.server import PlexServer
from datetime import datetime
import plexapi.exceptions
import csv
import sys
import plexExportCSV_config
import requests

# Your plex credentials
PLEX_URL = plexExportCSV_config.PLEX_URL
PLEX_TOKEN = plexExportCSV_config.PLEX_TOKEN

# ask user for movie vs tv shows -- plex api has different stuff for each
MOVIES_or_TV = ()
while MOVIES_or_TV not in ('movies', 'tv', 'MOVIES', 'TV'):
    MOVIES_or_TV = input('Would you like info on movies or TV shows?\n'
                         '(enter movies or TV): '
                        )

# ask user for list of plex "channels" based on selection above
if MOVIES_or_TV.lower() == 'movies':
    MOVIE_LIBRARIES_TO_EXPORT = input('Which Plex Movie Channel(s) would you like to export.\n'
                                      '(comma separated list): '
                                      )
    MOVIE_LIBRARIES_TO_EXPORT = [MOVIE_LIBRARIES_TO_EXPORT]
elif MOVIES_or_TV.lower() == 'tv':
    TV_SHOWS_TO_EXPORT = input('Which Plex TV Channel(s) would you like to export.\n'
                               '(comma separated list): '
                              )
    TV_SHOWS_TO_EXPORT = [TV_SHOWS_TO_EXPORT]

# Create plex server instance
try:
    print("Connecting to server...")
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    print("Connected")
except plexapi.exceptions.Unauthorized:
    print("Your Plex Token is invalid")
    sys.exit()
except requests.exceptions.ConnectTimeout:
    print(f"The connection timed out, is {PLEX_URL} correct?")
    sys.exit()


# Functions
def property_list_to_string(property_list: list) -> str:
    tidy_list = []
    for item in property_list:
        tidy_list.append(item.tag)
    new_string = ":".join(tidy_list)
    return new_string


def create_movie_object_list(plex_movie_libraries: list) -> list:
    object_list = []
    for library in plex_movie_libraries:
        object_list.extend(plex.library.section(library).all())
    return object_list


def create_movie_dictionary(object_list: list) -> list:
    m_list = []
    for i in range(len(object_list)):
        m_list.append({
            "addedAt": object_list[i].addedAt,
            "Title": object_list[i].title,
           # "Original Title": object_list[i].originalTitle, this will slow the script down 
            "Year": object_list[i].year,
            "Duration(minutes)": round((object_list[i].duration * 0.00001666667)),
            "Rating": object_list[i].rating,
            "Genres": property_list_to_string(object_list[i].genres),
            "Directors": property_list_to_string(object_list[i].directors),
            "Studio": object_list[i].studio,
            "Content Rating": object_list[i].contentRating,
            "Video Resolution": object_list[i].media[0].videoResolution,
            "Video Codec": object_list[i].media[0].videoCodec,
            "Video Profile": object_list[i].media[0].videoProfile,
            "Container": object_list[i].media[0].container,
            "Aspect Ratio": object_list[i].media[0].aspectRatio,
            "Audio Channels": object_list[i].media[0].audioChannels,
            "Audio Codec": object_list[i].media[0].audioCodec,
            "Audio Profile": object_list[i].media[0].audioProfile,
            "Bitrate": object_list[i].media[0].bitrate,
            "Size (GB)": round(object_list[i].media[0].parts[0].size / 1073741824, 2),
            "LocationOnDisk": object_list[i].media[0].parts[0].file
        })
    return m_list

print("\nGetting movie libraries information...")
try:
    movie_objects = create_movie_object_list(MOVIE_LIBRARIES_TO_EXPORT)
except:
    print(f"\nThat Plex movie {MOVIE_LIBRARIES_TO_EXPORT} selection is invalid")
    sys.exit(1)

movie_list = (create_movie_dictionary(movie_objects))
labels = [key for key in movie_list[0]]
print("\nThere are a total of ", len(movie_list), "movies in the selected libraries.")

# Create the labels from they keys of the dictionary of the first movie# Write the dictionary to a csv
print("\nCreating .csv file...")
try:
    with open(f'movies-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}.csv', 'w') as movies_csv:
        writer = csv.DictWriter(movies_csv, fieldnames=labels)
        writer.writeheader()
        for elem in movie_list:
            writer.writerow(elem)
    print('\nYour .csv is ready!')
    sys.exit()
except IOError:
    print("I/O error")
    sys.exit()
