from plexapi.server import PlexServer
import plexExportCSV_config

# This script tests if a full video object is called for video, movie, media and part
# If an attribute causes a full part reload it will slow the script down

# Your plex credentials
PLEX_URL = plexExportCSV_config.PLEX_URL
PLEX_TOKEN = plexExportCSV_config.PLEX_TOKEN
plex = PlexServer(PLEX_URL, PLEX_TOKEN)

# video object

video_object_list = [
    "addedAt",
    "art",
    "artBlurHash",
    "fields",
    "guid",
    "key",
    "lastViewedAt",
    "librarySectionID",
    "librarySectionKey",
    "librarySectionTitle",
    "listType",
    "ratingKey",
    "summary",
    "thumb",
    "thumbBlurHash",
    "title",
    "titleSort",
    "type",
    "updatedAt",
    "viewCount"]

movie_object_list = [
    "TAG",
    "TYPE",
    "audienceRating",
    "audienceRatingImage",
    "chapters",
    "chapterSource",
    "collections",
    "contentRating",
    "countries",
    "directors",
    "duration",
    "genres",
    "guids",
    "labels",
    "languageOverride",
    "media",
    "originallyAvailableAt",
    "originalTitle",
    "primaryExtraKey",
    "producers",
    "rating",
    "ratingImage",
    "roles",
    "similar",
    "studio",
    "tagline",
    "useOriginalTitle",
    "userRating",
    "viewOffset",
    "writers",
    "year"
]


def full_object_attributes_video_movie(attr_list, prefix_):
    full_obj_list = []
    for _i in attr_list:
        function_movie = plex.library.section('movies').get('Mercury Rising')
        _test_movie = getattr(function_movie, _i)
        if function_movie.isFullObject() is True:
            full_obj_list.append((prefix_ + "." + _i))
    return full_obj_list


list1 = full_object_attributes_video_movie(video_object_list, "video")
list1.extend(full_object_attributes_video_movie(movie_object_list, "movie"))

for i in list1:
    print(i)
