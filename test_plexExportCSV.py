from unittest import TestCase
from plexExportCSV import property_list_to_string
from plexapi.server import PlexServer
import plexExportCSV_config


class TestPropertyListToStringFunction(TestCase):
    def setUp(self) -> None:
        """Get a movie from a plex instance"""
        self.plex = PlexServer(plexExportCSV_config.PLEX_URL, token=plexExportCSV_config.PLEX_TOKEN)
        self.movie = self.plex.library.section('movies').get('Mercury Rising')

    def test_function_output_is_string(self):
        """make sure function output is string"""
        gen_string = property_list_to_string(self.movie.genres)
        self.assertEqual(type(gen_string), type(str()))

    def test_separator_is_colon(self):
        """check separator is colon"""
        gen_string = property_list_to_string(self.movie.genres)
        self.assertIn(":", gen_string)

    def test_correct_number_separators_genres(self):
        """check correct number of : in genre string"""
        count_genres = 0
        for _genre in self.movie.genres:
            count_genres += 1
        gen_string = property_list_to_string(self.movie.genres)
        count_colons = gen_string.count(":")
        self.assertEqual(count_colons, count_genres-1)

    def test_correct_number_separators_directors(self):
        """check correct number of : in director string """
        count_directors = 0
        for _director in self.movie.directors:
            count_directors += 1
        gen_string = property_list_to_string(self.movie.directors)
        count_colons = gen_string.count(":")
        self.assertEqual(count_colons, count_directors-1)

    def test_all_genre_items_in_string(self):
        """check each genre in genres list is in the string"""
        gen_string = property_list_to_string(self.movie.genres)
        for genre in self.movie.genres:
            self.assertIn(genre.tag, gen_string)

    def test_all_directors_in_string(self):
        """check each director in list is in output string"""
        gen_string = property_list_to_string(self.movie.directors)
        for director in self.movie.directors:
            self.assertIn(director.tag, gen_string)
