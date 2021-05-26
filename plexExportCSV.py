from plexapi.server import PlexServer
from datetime import datetime
import plexapi.exceptions
import plexapi.library
import csv
import sys
import plexExportCSV_config
import requests


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

def create_tv_dictionary(object_list: list) -> list:
    tv_list = []
    for i in range(len(object_list)):
        tv_list.append({
            "addedAt": object_list[i].addedAt,
            "Title": object_list[i].title,
            "Year": object_list[i].year,
        })
    return tv_list


def display_movie_libraries():
    library = plex.library.sections()
    library_list = []
    for i in library:
        if isinstance(i, plexapi.library.MovieSection):
            library_list.append(i.title)
    print("The following Movie libraries are available for export: \n", library_list)


def display_tv_libraries():
    library = plex.library.sections()
    library_list = []
    for i in library:
        if isinstance(i, plexapi.library.ShowSection):
            library_list.append(i.title)
    print("The following TV libraries are available for export: \n", library_list)


# Your plex credentials
PLEX_URL = plexExportCSV_config.PLEX_URL
PLEX_TOKEN = plexExportCSV_config.PLEX_TOKEN

# Create plex server instance
print(
    """           __          ___ __                         ___  ____________    __
    ____  / /__  _  __/ (_) /_  _________ ________  _|__ \/ ____/ ___/ |  / /
   / __ \/ / _ \| |/_/ / / __ \/ ___/ __ `/ ___/ / / /_/ / /    \__ \| | / / 
  / /_/ / /  __/>  </ / / /_/ / /  / /_/ / /  / /_/ / __/ /___ ___/ /| |/ /  
 / .___/_/\___/_/|_/_/_/_.___/_/   \__,_/_/   \__, /____|____//____/ |___/   
/_/                                          /____/                          

"""
)
try:
    print("Connecting to server...")
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    print("Connected!")
except plexapi.exceptions.Unauthorized:
    print("Your Plex Token is invalid")
    sys.exit()
except requests.exceptions.ConnectTimeout:
    print(f"The connection timed out, is {PLEX_URL} correct?")
    sys.exit()

# ask user for movie vs tv shows -- plex api has different stuff for each
movies_or_tv = ()
while movies_or_tv not in ('movies', 'tv'):
    movies_or_tv = input('Would you like to export movie or tv information?\n'
                         '(enter movies or tv): '
                         )

# ask user for list of plex "channels" based on selection above
if movies_or_tv.lower() == 'movies':
    display_movie_libraries()
    libraries_to_export = input('Which Plex Movie Channel(s) would you like to export.\n'
                                '(comma separated list): '
                                )
    libraries_to_export = libraries_to_export.split(',')
    movie_libraries_to_export = [i.strip() for i in libraries_to_export]

    try:
        movie_objects = create_movie_object_list(movie_libraries_to_export)
    except NameError:
        print(f"\nThat Plex movie {movie_libraries_to_export} selection is invalid")
        sys.exit(1)
    except plexapi.exceptions.NotFound:
        print(f"\nThe library {movie_libraries_to_export} is invalid")
        sys.exit(1)

    movie_list = (create_movie_dictionary(movie_objects))
    labels = [key for key in movie_list[0]]
    print("\nThere are a total of ", len(movie_list), "movies in the selected libraries.")

    # Create the labels from they keys of the dictionary of the first movie# Write the dictionary to a csv
    print("\nCreating .csv file...")
    try:
        with open(f'movies-{datetime.now().strftime("%Y-%m-%d-%H.%M.%S")}.csv', 'w') as movies_csv:
            writer = csv.DictWriter(movies_csv, fieldnames=labels)
            writer.writeheader()
            for elem in movie_list:
                writer.writerow(elem)
        print('\nYour .csv is ready!')
        sys.exit()
    except IOError:
        print("I/O error")
        sys.exit()


elif movies_or_tv.lower() == 'tv':
    display_tv_libraries()
    libraries_to_export = input('Which TV libraries would you like to export?\n'
                                '(comma separated list): '
                                )
    libraries_to_export = libraries_to_export.split(',')
    tv_libraries_to_export = [i.strip() for i in libraries_to_export]

    try:
        tv_objects = create_movie_object_list(tv_libraries_to_export)
    except NameError:
        print(f"\nThat Plex movie {tv_libraries_to_export} selection is invalid")
        sys.exit(1)
    except plexapi.exceptions.NotFound:
        print(f"\nThe library {tv_libraries_to_export} is invalid")
        sys.exit(1)

    tv_list = (create_tv_dictionary(tv_objects))
    labels = [key for key in tv_list[0]]
    print("\nThere are a total of ", len(tv_list), "shows in the selected libraries.")

    print("\nCreating .csv file...")
    try:
        with open(f'tv-{datetime.now().strftime("%Y-%m-%d-%H.%M.%S")}.csv', 'w') as tv_csv:
            writer = csv.DictWriter(tv_csv, fieldnames=labels)
            writer.writeheader()
            for elem in tv_list:
                writer.writerow(elem)
        print('\nYour .csv is ready!')
        sys.exit()
    except IOError:
        print("I/O error")
        sys.exit()




