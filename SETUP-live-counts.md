# Turning on live follower counts

The dashboard already refreshes daily on its own. To make the **Instagram** and
**Facebook** follower numbers *live* (and flip Facebook from "can't see the numbers"
to a real count), we need one Meta access token. This is a ~10-minute, one-time setup
Dani does once; after that the counts pull automatically every morning.

## What you get
- **Instagram** — live follower + post count (official Meta API, free, reliable).
- **Facebook** — live Page follower count (no more "login-gated").
- **TikTok** — *not* covered here; TikTok has no official follower API. It stays on a
  counter-site read (optional, best-effort).

## One-time setup (Dani)
1. Go to **developers.facebook.com** and log in with the account that manages the
   Tapestry Acres Facebook Page.
2. **My Apps → Create App → "Business"**. Name it anything (e.g. "Tapestry Insights").
3. In the app, add the **Instagram** product and the **Facebook Login** product.
4. Open **Graph API Explorer** (Tools menu). Pick your new app, then **Generate Access
   Token** and grant these permissions:
   `pages_read_engagement`, `pages_show_list`, `instagram_basic`.
5. That gives a short-lived token. Convert it to a **long-lived Page token** (lasts ~60
   days, auto-refreshable) — the Explorer's "long-lived token" option, or the token tool.
6. Send Steve three values (he'll paste them into the private secrets file — never put
   them in this repo):
   - the **Page access token**
   - the **Instagram business user ID** (Graph Explorer: `me/accounts` → your Page →
     `instagram_business_account`)
   - the **Facebook Page ID** (`me/accounts` shows it)

## What Steve does with them
Adds to `.llm-system/orchestrator/secrets.local.env`:
```
META_PAGE_TOKEN=<the long-lived page token>
META_IG_USER_ID=<instagram business user id>
META_FB_PAGE_ID=<facebook page id>
```
Nothing else changes — the existing daily task (`update_social_dashboard.py`) detects
the token and starts pulling live IG + FB counts the next morning. No token = it just
keeps the cadence clock current, exactly as it does today.

## Token upkeep
Long-lived Page tokens last ~60 days. When it expires, IG/FB counts quietly stop
updating (the clock keeps running). Regenerate via steps 4–5 and re-paste. A proper
system token that never expires is possible later if this becomes routine.
