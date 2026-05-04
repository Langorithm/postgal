# postgal

Gamedev progress sharing pipeline. Take a screenshot or video, run one script, and it commits to git, posts to all configured socials, and rebuilds a GitHub Pages gallery.

## Local usage

```zsh
./scripts/post.sh ~/Desktop/screenshot.png "Added parallax scrolling"
# or interactively:
./scripts/post.sh ~/Desktop/screenshot.png
```

The script copies the file to `captures/`, updates `captures/index.json`, commits with the caption as the message, and pushes. GitHub Actions handles everything from there.

## How the pipeline works

1. **detect** — finds the newly added file in `captures/` from the commit diff, extracts caption from commit message
2. **convert** *(videos only)* — ffmpeg converts to palette-optimised GIF and animated WebP
3. **publish** — Python engine fans out to all configured platforms in parallel
4. **build-site** — regenerates `site/index.html` gallery and deploys to `gh-pages` branch

## Social modules

| Module | File | Status |
|---|---|---|
| Bluesky | `modules/bluesky.py` | Ready |
| Telegram | `modules/telegram.py` | Ready (channel + group) |
| Tumblr | `modules/tumblr.py` | Ready |
| Reddit | `modules/reddit.py` | Ready |
| Twitter | `modules/twitter.py` | Stub (Puppeteer — pending) |

Platforms with missing secrets are **skipped gracefully**, not failed. Add credentials one at a time.

## GitHub Secrets to configure

| Secret | Platform |
|---|---|
| `BLUESKY_HANDLE` | Bluesky |
| `BLUESKY_APP_PASSWORD` | Bluesky |
| `TELEGRAM_BOT_TOKEN` | Telegram |
| `TELEGRAM_CHANNEL_ID` | Telegram (optional) |
| `TELEGRAM_GROUP_ID` | Telegram (optional) |
| `TUMBLR_CONSUMER_KEY` | Tumblr |
| `TUMBLR_CONSUMER_SECRET` | Tumblr |
| `TUMBLR_OAUTH_TOKEN` | Tumblr |
| `TUMBLR_OAUTH_SECRET` | Tumblr |
| `TUMBLR_BLOG_NAME` | Tumblr |
| `REDDIT_CLIENT_ID` | Reddit |
| `REDDIT_CLIENT_SECRET` | Reddit |
| `REDDIT_USERNAME` | Reddit |
| `REDDIT_PASSWORD` | Reddit |
| `REDDIT_SUBREDDIT` | Reddit |

## Telegram setup

1. Create a bot via [@BotFather](https://t.me/botfather) — get the bot token
2. Add the bot to your group (member) and/or channel (admin)
3. Send a message, then call `https://api.telegram.org/bot{TOKEN}/getUpdates` to find the chat IDs
4. Set `TELEGRAM_GROUP_ID` and/or `TELEGRAM_CHANNEL_ID` in repo secrets

## GitHub Pages

After first push, go to repo **Settings → Pages** and set source to the `gh-pages` branch.
