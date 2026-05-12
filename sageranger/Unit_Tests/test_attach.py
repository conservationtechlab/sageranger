"""Tests Attach Images

Usage:
    python3 -m UnitTests.test_attach

This function posts an event and takes the
event ID to attach an email. Make sure you are
testing from the sageranger root folder.
"""
from io import BytesIO
from post_event_er import post_event
from attach_image_er import attach_image
from PIL import Image

LABEL = "<animal>"
CAMERA = "<camera name>"
TOKEN = "< bearer token>"
FILE_PATH = "<local_filepath_to_image>"  # use a photo on computer ex. home/user/.....

def main():
    """Tests attach image functions"""
    event_id = post_event(LABEL, CAMERA, TOKEN)
    img = Image.open(FILE_PATH)
    image_bytes = BytesIO()
    img.save(image_bytes, format="JPEG")
    final_image = image_bytes.getvalue()
    response_attach = attach_image(event_id, final_image, TOKEN, LABEL)
    print("Response:", response_attach)


if __name__ == "__main__":
    main()
