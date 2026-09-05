# Search Console + GA4 Setup, and the $20/week Google Ads Plan

These are the two things I can't do for you (they need your own Google
account and, for Ads, a payment method) -- but everything downstream of
your setup, I *can* wire in and automate.

---

## 1. Google Search Console (free, ~5 minutes)

1. Go to https://search.google.com/search-console and sign in with
   whatever Google account you want to own this (use one you'll keep
   long-term -- this is tied to the property forever unless you add
   other owners).
2. Click **Add property** -> choose **URL prefix** (not "Domain") ->
   enter `https://rcadventurehub.com`.
3. Under verification methods, pick **HTML tag**. Google shows you a
   line like:
   `<meta name="google-site-verification" content="AbC123...xyz" />`
   Copy **only** the long random string inside `content="..."` -- not
   the whole tag.
4. Send me that string (or paste it into `data/config.yaml` under
   `search_console_verification:`) and tell me it's ready. I'll rebuild
   and redeploy the site with that meta tag live, then you click
   **Verify** back in Search Console.
5. Once verified: go to **Sitemaps** in the left nav, and submit
   `sitemap.xml` (the full URL is `https://rcadventurehub.com/sitemap.xml`,
   already live and auto-updated by every build). Google will start
   crawling and, within a few days to a couple weeks, you'll see
   impressions/clicks data in the **Performance** report -- that's your
   real, free signal for which queries are actually finding the site.

## 2. Google Analytics 4 (free, ~5 minutes)

1. Go to https://analytics.google.com and sign in (same account as
   Search Console is simplest, not required).
2. Create an **Account** (e.g. "RC Adventure Hub"), then a **Property**
   of the same name, then add a **Web** data stream with URL
   `https://rcadventurehub.com`.
3. GA4 shows a **Measurement ID** for that stream, formatted like
   `G-XXXXXXXXXX`. Copy it.
4. Send it to me (or paste into `data/config.yaml` under
   `ga4_measurement_id:`) and I'll wire in the tracking snippet and
   redeploy. Give it a day of traffic and you'll see real-time +
   historical visitor data, including which pages people land on and
   which outbound (Amazon/affiliate) links they click.

Once both are live, this closes the loop: Search Console tells you
*what people search* to find you, GA4 tells you *what they do* once
they're there. That combination is what should drive future content
and campaign decisions -- more reliable than guessing.

---

## 3. Google Ads: $20/week starter plan

Budget context: $20/week is roughly **$2.85-$3.00/day**. At that level
the goal isn't "run a real growth campaign" yet -- it's to buy your
first real click-through data cheaply, prove the funnel works
(ad -> guide -> Amazon link -> sale), and learn which keywords are worth
scaling before you spend more. Google Ads averages your daily budget
over a month (some days more, some less, capped at ~2x on any single
day), so don't panic if one day shows $6 spent.

**A note on affiliate sites and Ads policy:** Google allows advertising
affiliate content, but the *landing page* has to offer real, substantial
value beyond just links -- which this site's guides already do (buying
advice, comparisons, honest caveats). Don't run ads straight to a page
that's just a list of affiliate buttons with no editorial content.

### Structure: one campaign, one ad group, to start

Spreading $3/day across cars + planes + boats + guides means each
keyword gets almost no clicks -- not enough data to learn anything.
Start narrow on your single strongest page, prove it converts, then
expand.

**Campaign:** RC Adventure Hub -- Search
- **Type:** Search Network only (uncheck Display Network partner sites)
- **Goal:** Website traffic (no conversion goal yet -- you don't have
  GA4/conversion tracking live yet; revisit once you do)
- **Location:** Canada only, to start (your Amazon links are
  Amazon.ca -- US or global traffic on a `.ca` affiliate tag mostly
  won't convert)
- **Budget:** $3.00 CAD/day
- **Bidding:** Maximize Clicks, with a **max CPC bid limit of $0.60**
  (without a bid cap, Maximize Clicks can burn your whole daily budget
  on 2-3 expensive clicks; the cap keeps volume steady while you learn)
- **Ad extensions:** Add Sitelinks (link to `/planes/...`, `/boats/...`,
  `/guides/...`) and a Callout ("Independent Reviews", "Real Amazon
  Links", "No Sponsored Picks")

**Ad group: RC Cars for Adults**
Landing page: `https://rcadventurehub.com/cars/best-rc-cars-for-adults/`

Keywords -- phrase and exact match only (broad match will burn a tiny
budget on irrelevant traffic like "rc car repair" or "rc car games"):

| Match type | Keyword |
|---|---|
| Exact | `[best rc cars for adults]` |
| Exact | `[rc cars for adults]` |
| Phrase | `"hobby grade rc car"` |
| Phrase | `"rc car buying guide"` |
| Phrase | `"rtr vs kit rc car"` |
| Phrase | `"brushless rc car for adults"` |

**Negative keywords** (add at the campaign level so they apply to every
ad group you add later):
`free, cheap, toy, kids, walmart, canadian tire, rental, repair, parts
only, jobs, wikipedia, definition, meaning, video, games, remote
control car crash`

**Responsive Search Ad -- headlines** (pick 8-10 of these; Google mixes
and matches them):
- Best RC Cars for Adults
- Hobby-Grade RC Buying Guide
- Skip the Toy-Grade Mistakes
- RTR vs Kit: Which to Buy?
- Real Amazon.ca Links, No Fluff
- Independent RC Car Reviews
- Brushless vs Brushed Explained
- Honest Picks, Not Sponsored
- What to Buy (and What to Skip)
- Built for Adult Hobbyists

**Descriptions** (2-4):
- "Independent buying guides for hobby-grade RC cars -- we tell you what's actually worth buying, and what to skip."
- "Compare brushless vs brushed, RTR vs kit. Honest advice with real, current Amazon.ca links."

### First-two-weeks checklist
1. Launch with the settings above, let it run **7-14 days untouched** --
   resist adjusting bids daily; you need enough data first.
2. Check Search Terms report after ~1 week; add anything irrelevant
   as a new negative keyword.
3. Once GA4 is live, set up a **conversion action** for outbound clicks
   to Amazon (GA4 can send this to Ads as a conversion) -- only then
   does it make sense to switch bidding from Maximize Clicks to
   Maximize Conversions.
4. If cars performs well after 2-3 weeks, duplicate the ad group
   structure for planes and boats using the same keyword-mapping
   already documented in `automation/SEO_KEYWORDS.md`, and only then
   consider raising the daily budget.

I can't create the Ads account or enter a payment method for you (that
part has to be you, in your own Google Ads account) -- but once it
exists, I can help review performance data, tighten keyword lists, and
draft new ad copy any time you want.
