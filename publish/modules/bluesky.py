import os
import mimetypes
from atproto import Client


def post(file_path: str, caption: str) -> None:
    client = Client()
    client.login(os.environ["BLUESKY_HANDLE"], os.environ["BLUESKY_APP_PASSWORD"])

    mime, _ = mimetypes.guess_type(file_path)
    mime = mime or "image/jpeg"

    with open(file_path, "rb") as f:
        data = f.read()

    if mime.startswith("image/"):
        client.send_image(
            text=caption[:300],
            image=data,
            image_alt=caption[:1000],
        )
    else:
        # Video support on Bluesky is limited; post as text-only
        client.send_post(text=caption[:300])
