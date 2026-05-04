import os
import mimetypes
import praw


def post(file_path: str, caption: str) -> None:
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        user_agent="postgal/1.0",
    )

    subreddit = reddit.subreddit(os.environ["REDDIT_SUBREDDIT"])
    mime, _ = mimetypes.guess_type(file_path)
    mime = mime or "image/jpeg"

    if mime.startswith("image/"):
        subreddit.submit_image(title=caption[:300], image_path=file_path)
    elif mime.startswith("video/"):
        subreddit.submit_video(
            title=caption[:300],
            video_path=file_path,
            without_websockets=True,
        )
    else:
        subreddit.submit(title=caption[:300], selftext="")
