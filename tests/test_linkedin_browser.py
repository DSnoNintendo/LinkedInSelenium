import unittest
from linkedin_selenium import LinkedInBrowser

browser = LinkedInBrowser()
browser.login()

class TestLinkedInBrowser(unittest.TestCase):

    def test_get_profile_picture_no_picture(self):
        """Test getting profile picture from a URL where we don't have access"""
        url = "https://www.linkedin.com/in/brianna-birdwell-30b85435/"
        result = browser.get_profile_picture_from_url(url)
        self.assertIsNone(result, "Expected None for profile without access")

    def test_get_profile_picture_from_url_with_picture(self):
        """Test getting profile picture from a URL where we have access"""
        url = "https://www.linkedin.com/in/christine-boudreau-6750b25/"
        expected_url = "https://media.licdn.com/dms/image/v2/C4E03AQGOZgLtycIRdg/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1517726975275?e=1752710400&v=beta&t=nZo6W9gyIb7j_P11Zy6Z_AvLWeLLSmtHdh7VwLW5S3Q"
        result = browser.get_profile_picture_from_url(url)
        self.assertEqual(result, expected_url, "Profile picture URL doesn't match expected value")

if __name__ == '__main__':
    unittest.main() 