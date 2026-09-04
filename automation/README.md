# Keeping this site growing on autopilot

"Automate it" for a content site really means three separate things, and
they need different amounts of setup:

## 1. Content research & writing -- I can do this on a recurring schedule today
Once the site is live in a GitHub repo, I can set up a recurring scheduled
task (weekly, biweekly, whatever cadence you want) that:

1. Searches the web for what's currently trending, newly released, or
   getting attention in RC cars/planes/boats.
2. Drafts one new article following the same format and voice as the
   existing five (see `CONTENT_GUIDE.md`), adding any new products to
   `data/products.yaml`.
3. Runs `build.py`, commits, and pushes -- which auto-deploys if you've
   connected Cloudflare Pages/Netlify to the repo.
4. Sends you a short message saying what it added.

I'm holding off creating that recurring task until the repo + hosting exist
(see the main README), since there's nowhere for it to push to yet. Once
that's set up, tell me and I'll create it -- it takes one tool call.

## 2. Publishing -- automatic once hosting is connected to the repo
Cloudflare Pages / Netlify both redeploy automatically on every git push, so
once that's connected, step 1's automation *is* the publishing automation --
there's no separate step.

## 3. Social distribution -- semi-automated at best without paid tools
There's no free, no-account way to actually auto-post to social platforms.
Two realistic options, in order of effort:

- **Manual, but drafted for you (free).** As part of the same recurring task,
  I can also draft 2-3 social captions (Pinterest/Instagram/X-style) per new
  article, pointing back to the site, saved to `automation/social_drafts/`.
  You copy/paste and post them -- a few minutes a week, not fully hands-off,
  but zero extra cost or accounts.
- **Actually automated posting.** Needs a scheduler like Buffer or Zapier
  connected to your social accounts (their free tiers are limited but real),
  or direct API access per platform. If you want this, tell me which
  platforms matter most and I'll help you wire it up once accounts exist --
  this is a good use of some of your monthly budget if Pinterest is a
  priority, since Pinterest tends to convert unusually well for buying-guide
  content like this.

## What "research" actually means here, concretely
When the scheduled task fires, I use web search to check things like: newly
released models from the brands already in `products.yaml`, RC hobby news
sites and subreddits for what's getting attention, and whether any existing
article's picks look stale (discontinued, widely reported as changed/worse).
I do not invent specs or prices -- articles stay in the same evidence-based
style as the initial five (see `CONTENT_GUIDE.md`).
