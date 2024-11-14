from PIL import Image, ExifTags
import os

# Source and destination directories
source_folder = 'origen'
destination_folder = 'destino'
logo_path = 'logo.png'

# Load the logo image
logo = Image.open(logo_path).convert("RGBA")

# Ensure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)

def apply_exif_rotation(image):
    # Check if image has EXIF data
    try:
        exif = image._getexif()
        if exif is not None:
            # Get orientation tag key for rotation
            orientation_key = [k for k, v in ExifTags.TAGS.items() if v == 'Orientation'][0]
            orientation = exif.get(orientation_key)
            # Apply rotation based on orientation value
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError, TypeError):
        # Handle cases where EXIF data is missing or invalid
        pass
    return image

# Loop through all files in the source folder
for filename in os.listdir(source_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # Open the image
        image_path = os.path.join(source_folder, filename)
        image = Image.open(image_path)

        # Apply EXIF rotation
        image = apply_exif_rotation(image).convert("RGBA")

        # Calculate position for the logo (10px from bottom-right corner)
        image_width, image_height = image.size
        logo_width, logo_height = logo.size
        position = (image_width - logo_width - 10, image_height - logo_height - 10)

        # Paste the logo onto the image
        image.paste(logo, position, logo)

        # Save the image to the destination folder
        output_path = os.path.join(destination_folder, filename)
        image.convert("RGB").save(output_path)

print("Logo added to all images.")
