import unittest
from tag_counter.process_url import url_name, url_format, count_tags


class TestUrl(unittest.TestCase):
    def test_url_name(self):
        """Test url_name function"""
        self.assertEqual(url_name('http://www.epam.com'), 'epam.com')

    def test_url_format(self):
        """Test url_format function"""
        self.assertEqual(url_format('epam.com'), 'http://epam.com')

    def test_count_tags(self):
        """Test count_tags function"""
        self.assertEqual(count_tags(url_format('test.com'))['html'], 1)


if __name__ == "__main__":
    unittest.main()

