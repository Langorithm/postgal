#!/usr/bin/env python3
"""
Social posting engine.
Usage: python publish.py <file_path> <caption>
Each module is attempted independently; a failure in one doesn't block others.
"""
import importlib
import os
import sys
import traceback

# Modules to attempt, in order. Add "twitter" here once implemented.
MODULES = ["bluesky", "telegram", "tumblr", "reddit"]

# Env vars that must all be present for a module to run.
# If any are missing the module is skipped (not failed).
REQUIRED_ENV: dict[str, list[str]] = {
    "bluesky": ["BLUESKY_HANDLE", "BLUESKY_APP_PASSWORD"],
    "telegram": ["TELEGRAM_BOT_TOKEN"],          # needs at least the token; targets checked inside module
    "tumblr": [
        "TUMBLR_CONSUMER_KEY", "TUMBLR_CONSUMER_SECRET",
        "TUMBLR_OAUTH_TOKEN", "TUMBLR_OAUTH_SECRET", "TUMBLR_BLOG_NAME",
    ],
    "reddit": [
        "REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET",
        "REDDIT_USERNAME", "REDDIT_PASSWORD", "REDDIT_SUBREDDIT",
    ],
    "twitter": [],
}


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: publish.py <file_path> <caption>")
        sys.exit(1)

    file_path, caption = sys.argv[1], sys.argv[2]

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    results: dict[str, str] = {}

    for name in MODULES:
        missing = [k for k in REQUIRED_ENV.get(name, []) if not os.environ.get(k)]
        if missing:
            results[name] = f"skipped (missing: {', '.join(missing)})"
            continue

        try:
            mod = importlib.import_module(f"modules.{name}")
            mod.post(file_path, caption)
            results[name] = "ok"
        except NotImplementedError as e:
            results[name] = f"skipped ({e})"
        except Exception as e:
            results[name] = f"FAILED: {e}"
            traceback.print_exc()

    print("\n─── Publish summary ───")
    failed = []
    for platform, status in results.items():
        if status == "ok":
            icon = "✓"
        elif status.startswith("skipped"):
            icon = "–"
        else:
            icon = "✗"
            failed.append(platform)
        print(f"  {icon} {platform}: {status}")

    if failed:
        print(f"\nFailed platforms: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
