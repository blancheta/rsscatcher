from django.test import TestCase
from base.helpers import slugify


class SlugifyHelperTests(TestCase):

    def test_can_slugify_a_string(self):

        """
        Can slugify the incoming string and return it
        """

        actual = "sony 400mm f/2 8 oss voor systeemcamera's komt in september uit voor 12 000 euro"
        expected = "sony-400mm-f-2-8-oss-voor-systeemcameras-komt-in-september-uit-voor-12-000-euro"

        slug = slugify(actual)
        self.assertEqual(slug, expected)
