import unittest
from linkedin_selenium import LinkedInBrowser
import base64
import io
from PIL import Image
import imghdr

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
        result = browser.get_profile_picture_from_url(url)
        self.assertIsNotNone(result, "Expected a profile picture URL")

        # Convert the image URL result to base64
        import requests
        response = requests.get(result)
        response.raise_for_status()
        image_data = response.content
        result = base64.b64encode(image_data).decode('utf-8')

        self.assertTrue(is_valid_base64_image(result), "Expected a valid base64 image")

def is_valid_base64_image(base64_string):
    """
    Validate if a base64 string contains valid image data
    
    Args:
        base64_string (str): Base64 encoded string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Remove data URL prefix if present (e.g., "data:image/png;base64,")
        if 'base64,' in base64_string:
            base64_string = base64_string.split('base64,')[1]
        
        # Decode base64 string
        image_data = base64.b64decode(base64_string)
        
        # Method 1: Check file signature (magic bytes)
        image_format = imghdr.what(None, h=image_data)
        if image_format:
            return True
        
        # Method 2: Try to open with PIL/Pillow
        try:
            image = Image.open(io.BytesIO(image_data))
            image.verify()  # Verify it's a valid image
            return True, image.format.lower(), None
        except Exception as pil_error:
            print(f"PIL validation failed: {str(pil_error)}")
            return False
            
    except Exception as e:
        return False


if __name__ == '__main__':
    unittest.main() 