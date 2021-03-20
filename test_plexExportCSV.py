from unittest import TestCase
from plexExportCSV import genre_string
from plexapi.server import PlexServer
import plexExportCSV_config


class Test(TestCase):
    def setUp(self) -> None:
        """Get a movie from a plex instance"""
        self.plex = PlexServer(plexExportCSV_config.PLEX_URL, token=plexExportCSV_config.PLEX_TOKEN)
        self.movie = self.plex.library.section('movies').get('Mercury Rising')

    def test_genre_string(self):
        """make sure function output is string"""
        gen_string = genre_string(self.movie.genres)
        self.assertEqual(type(gen_string), type(str()))

    def test_seperator_is_colon(self):
        """check seperator is colon"""
        gen_string = genre_string(self.movie.genres)
        self.assertIn(":", gen_string)
