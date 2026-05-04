# postgal

A minimal pipeline for sharing gamedev progress. Run one command — it commits your screenshot or video, posts to all configured social platforms, and your gallery updates automatically.

## How it works

1. You run `post.sh` with a file and caption
2. The file is copied to `captures/`, committed, and pushed
3. GitHub Actions picks up the push and fans out to all configured platforms
4. Your GitHub Pages gallery updates automatically

## Requirements

- Git
- Python 3.10+
- A GitHub repo with Pages enabled (set source to **main branch, root folder**)

## Setup

### 1. Fork or clone this repo

```sh
git clone https://github.com/yourname/postgal.git
cd postgal
```

### 2. Enable GitHub Pages

Go to **Settings → Pages** and set:
- Source: **Deploy from a branch**
- Branch: `main`, folder: `/ (root)`

Your gallery will be live at `https://yourname.github.io/postgal`.

### 3. Add social platform credentials

Go to **Settings → Secrets and variables → Actions** and add secrets for whichever platforms you want. Platforms with missing secrets are skipped — you don't need to configure all of them.

#### Bluesky
| Secret | Value |
|---|---|
| `BLUESKY_HANDLE` | Your handle, e.g. `yourname.bsky.social` |
| `BLUESKY_APP_PASSWORD` | Generate one at Settings → App Passwords |

#### Telegram
| Secret | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Create a bot via [@BotFather](https://t.me/botfather) |
| `TELEGRAM_CHANNEL_ID` | Channel to post to (optional) |
| `TELEGRAM_GROUP_ID` | Group to post to (optional) |

To find chat IDs: add the bot to your channel/group, send a message, then open `https://api.telegram.org/bot{TOKEN}/getUpdates` and look for `chat.id`.

#### Tumblr
| Secret | Value |
|---|---|
| `TUMBLR_CONSUMER_KEY` | From your Tumblr app |
| `TUMBLR_CONSUMER_SECRET` | From your Tumblr app |
| `TUMBLR_OAUTH_TOKEN` | OAuth token |
| `TUMBLR_OAUTH_SECRET` | OAuth secret |
| `TUMBLR_BLOG_NAME` | Your blog name, e.g. `yourname` |

Register an app at [tumblr.com/oauth/apps](https://www.tumblr.com/oauth/apps).

#### Reddit
| Secret | Value |
|---|---|
| `REDDIT_CLIENT_ID` | From your Reddit app |
| `REDDIT_CLIENT_SECRET` | From your Reddit app |
| `REDDIT_USERNAME` | Your Reddit username |
| `REDDIT_PASSWORD` | Your Reddit password |
| `REDDIT_SUBREDDIT` | Subreddit to post to, e.g. `gamedev` |

Register an app (script type) at [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps).

## Posting

```sh
./post.sh ~/Desktop/screenshot.png "Added parallax scrolling"
```

Omit the caption to be prompted interactively:

```sh
./post.sh ~/Desktop/screenshot.png
```

Supported formats: PNG, JPG, GIF, WebP, MP4, MOV, WebM. Videos are automatically converted to an optimised GIF and animated WebP before posting.

## Local testing

To test the publishing pipeline locally before relying on GitHub Actions, create a `.env` file at the repo root:

```sh
# .env  (gitignored)
BLUESKY_HANDLE=yourname.bsky.social
BLUESKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
# etc.
```

Install dependencies and run directly:

```sh
pip install -r publish/requirements.txt
python publish/publish.py captures/yourfile.png "Your caption"
```

To preview the gallery locally:

```sh
python3 -m http.server
# open http://localhost:8000
```

## Project layout

```
post.sh           — local entry point
index.html        — gallery (static, no build step)
captures/         — your screenshots and videos
  index.json      — metadata index (managed by post.sh)
publish/          — social posting engine (runs on GitHub Actions)
  publish.py
  modules/        — one file per platform
  requirements.txt
.github/
  workflows/
    publish.yml   — CI pipeline
```
