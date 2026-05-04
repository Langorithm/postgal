#!/usr/bin/env python3
"""One-time script to get Tumblr OAuth access token and secret."""
from requests_oauthlib import OAuth1Session

consumer_key    = input("Consumer key:    ").strip()
consumer_secret = input("Consumer secret: ").strip()

oauth = OAuth1Session(consumer_key, client_secret=consumer_secret, callback_uri="https://localhost")
tokens = oauth.fetch_request_token("https://www.tumblr.com/oauth/request_token")

print("\nVisit this URL and authorise the app:")
print(oauth.authorization_url("https://www.tumblr.com/oauth/authorize"))
print("\nAfter approving, the browser will redirect to localhost and fail — that's fine.")
print("Copy the full redirect URL and paste it here.")

redirect_url = input("\nRedirect URL: ").strip()
verifier = redirect_url.split("oauth_verifier=")[-1].split("&")[0].split("#")[0]

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=tokens["oauth_token"],
    resource_owner_secret=tokens["oauth_token_secret"],
    verifier=verifier,
)
access = oauth.fetch_access_token("https://www.tumblr.com/oauth/access_token")

print("\nAdd these to your .env and GitHub Secrets:")
print(f"TUMBLR_CONSUMER_KEY={consumer_key}")
print(f"TUMBLR_CONSUMER_SECRET={consumer_secret}")
print(f"TUMBLR_OAUTH_TOKEN={access['oauth_token']}")
print(f"TUMBLR_OAUTH_SECRET={access['oauth_token_secret']}")
