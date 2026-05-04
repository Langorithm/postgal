import os
import mimetypes
import requests
from requests_oauthlib import OAuth1


def post(file_path: str, caption: str) -> None:
    blog = os.environ["TUMBLR_BLOG_NAME"]
    auth = OAuth1(
        os.environ["TUMBLR_CONSUMER_KEY"],
        os.environ["TUMBLR_CONSUMER_SECRET"],
        os.environ["TUMBLR_OAUTH_TOKEN"],
        os.environ["TUMBLR_OAUTH_SECRET"],
    )

    mime, _ = mimetypes.guess_type(file_path)
    mime = mime or "image/jpeg"
    url = f"https://api.tumblr.com/v2/blog/{blog}/post"

    with open(file_path, "rb") as f:
        if mime.startswith("image/"):
            resp = requests.post(
                url,
                auth=auth,
                data={"type": "photo", "caption": caption},
                files={"data[0]": (os.path.basename(file_path), f, mime)},
                timeout=60,
            )
        elif mime.startswith("video/"):
            resp = requests.post(
                url,
                auth=auth,
                data={"type": "video", "caption": caption},
                files={"data": (os.path.basename(file_path), f, mime)},
                timeout=120,
            )
        else:
            resp = requests.post(
                url,
                auth=auth,
                json={"type": "text", "title": caption[:250], "body": caption},
                timeout=30,
            )

    resp.raise_for_status()
