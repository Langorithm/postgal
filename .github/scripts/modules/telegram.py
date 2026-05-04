import os
import mimetypes
import requests

# Set TELEGRAM_CHANNEL_ID and/or TELEGRAM_GROUP_ID in secrets.
# Each is optional — whichever is set gets a post.


def post(file_path: str, caption: str) -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    targets = _targets()
    for chat_id in targets:
        _send(token, chat_id, file_path, caption)


def _targets() -> list[str]:
    targets = []
    for key in ("TELEGRAM_CHANNEL_ID", "TELEGRAM_GROUP_ID"):
        val = os.environ.get(key, "").strip()
        if val:
            targets.append(val)
    if not targets:
        raise EnvironmentError("Set TELEGRAM_CHANNEL_ID and/or TELEGRAM_GROUP_ID")
    return targets


def _send(token: str, chat_id: str, file_path: str, caption: str) -> None:
    base = f"https://api.telegram.org/bot{token}"
    mime, _ = mimetypes.guess_type(file_path)
    mime = mime or "application/octet-stream"

    with open(file_path, "rb") as f:
        if mime.startswith("image/"):
            endpoint, field = "sendPhoto", "photo"
        elif mime.startswith("video/"):
            endpoint, field = "sendVideo", "video"
        else:
            endpoint, field = "sendDocument", "document"

        resp = requests.post(
            f"{base}/{endpoint}",
            data={"chat_id": chat_id, "caption": caption[:1024]},
            files={field: f},
            timeout=60,
        )

    resp.raise_for_status()
