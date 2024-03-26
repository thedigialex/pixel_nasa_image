import requests
from PIL import Image
from io import BytesIO
import os

def fetch_nasa_image(api_key):
    """Fetch an image URL from NASA's APOD API."""
    url = 'https://api.nasa.gov/planetary/apod'
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    data = response.json()
    image_url = data.get('url')
    media_type = data.get('media_type')
    
    if media_type != 'image':
        raise ValueError('The APOD for today is not an image.')
    
    return image_url


def pixelate_image(image_url, pixel_size=9):
    """Pixelate the image from the given URL and return both original and pixelated images."""
    response = requests.get(image_url)
    original_image = Image.open(BytesIO(response.content))
    pixelated_image = original_image.resize(
        (original_image.width // pixel_size, original_image.height // pixel_size),
        Image.NEAREST
    )
    pixelated_image = pixelated_image.resize(
        (pixelated_image.width * pixel_size, pixelated_image.height * pixel_size),
        Image.NEAREST
    )
    return original_image, pixelated_image

def save_image(image, path):
    """Save the image to the specified path."""
    image.save(path)

# Main program
if __name__ == "__main__":
    NASA_API_KEY = 'YOUR_NASA_API_KEY_HERE'
    image_url = fetch_nasa_image(NASA_API_KEY)
    original_image, pixelated_image = pixelate_image(image_url)
    
    # Save original image
    original_save_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'nasa_original_image.png')
    save_image(original_image, original_save_path)
    
    # Save pixelated image
    pixelated_save_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'nasa_pixelated_image.png')
    save_image(pixelated_image, pixelated_save_path)
    
    print(f'Original image saved to {original_save_path}')
    print(f'Pixelated image saved to {pixelated_save_path}')
