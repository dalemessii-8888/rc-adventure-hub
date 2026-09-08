# Google Ads First Campaign — Copy-Paste Checklist

Follow this in **one sitting**, in your own browser, from "Create your
first campaign" through to payment and launch. I tried to build this
for you from Claude's browser, but Google Ads' draft state turned out
to be tied to the browser session it started in, so it can't be handed
off partway through — this checklist is the reliable way to get it done.

Go to https://ads.google.com and start (or resume) "Create your first
campaign." At each step below, use exactly what's here — Google will
try to default you to things that don't match the plan (Performance
Max instead of Search, Maximize Conversions instead of Clicks, a much
higher recommended budget, auto-generated headlines) — override all of
those.

---

## 1. Choose campaign type

- Pick **Search** (not the default Performance Max — look for a "view
  other campaign types" link if it defaults you elsewhere).
- Campaign name: **RC Adventure Hub -- Search**

## 2. Select keywords

**Final URL:**
```
https://rcadventurehub.com/cars/best-rc-cars-for-adults/
```

**Keywords** (paste all six lines into the keyword box):
```
[best rc cars for adults]
[rc cars for adults]
"hobby grade rc car"
"rc car buying guide"
"rtr vs kit rc car"
"brushless rc car for adults"
```

**Locations:** Canada only (not "All countries and territories")

**Networks** — click the edit (pencil) icon and **uncheck both**:
- [ ] Google Search Partners Network
- [ ] Google Display Network

(Google will offer to "opt back in" — ignore it. You want Search
Network only.)

## 3. Create ads

**Final URL** (it sometimes resets to the site root — re-check it):
```
https://rcadventurehub.com/cars/best-rc-cars-for-adults/
```

**Headlines** (delete the auto-generated ones like "RC Planes" / "RC
Adventure Hub" / "We Tell You What's Different" — paste these 10
instead, one per field, click "+ Headline" to add more slots):
```
Best RC Cars for Adults
Hobby-Grade RC Buying Guide
Skip the Toy-Grade Mistakes
RTR vs Kit: Which to Buy?
Real Amazon.ca Links, No Fluff
Independent RC Car Reviews
Brushless vs Brushed Explained
Honest Picks, Not Sponsored
What to Buy (and What to Skip)
Built for Adult Hobbyists
```

**Descriptions** (delete the auto-generated ones — paste these 2;
they're trimmed to fit Google's 90-character limit):
```
Independent buying guides for hobby-grade RC cars. What's worth buying, what to skip.
```
```
Compare brushless vs brushed, RTR vs kit. Honest advice, real current Amazon.ca links.
```
Leave any extra description/headline slots empty — you don't need
more than these.

## 4. Set bid strategy

- Dropdown: **Clicks** (not the default "Maximize conversions" — you
  don't have conversion tracking live yet)
- Check **"Set a maximum cost per click bid limit"**
- Maximum CPC bid limit: **CA$0.60**

## 5. Set budget

- Select **"Set custom budget"** (not the recommended ~CA$44/day)
- Daily budget: **CA$3.00**
- You'll see a warning that this is lower than other advertisers'
  budgets — that's expected and fine, ignore it. Weekly cost should
  show ~CA$21.00.

## 6. Enter payment details

This part is yours to do — add your own payment method here.

## 7. Before you click "Publish" / "Save and launch"

Add these two things if the wizard gives you the option (otherwise
add them right after launch, from the campaign's own settings page):

**Negative keywords** (campaign level, so they apply to every ad group
you add later):
```
free
cheap
toy
kids
walmart
canadian tire
rental
repair
parts only
jobs
wikipedia
definition
meaning
video
games
remote control car crash
```

**Optional — ad extensions:**
- Sitelinks: link to `/planes/`, `/boats/`, `/guides/`
- Callout: "Independent Reviews", "Real Amazon Links", "No Sponsored
  Picks"

Once all of that matches, review the summary and click launch — that's
the real, recurring-spend action, so it should be your click, not
mine.

---

## First two weeks, after launch

1. Let it run **7-14 days untouched** — resist adjusting bids daily;
   you need enough data first.
2. Check the Search Terms report after ~1 week; add anything
   irrelevant as a new negative keyword.
3. Once GA4 is live, set up a conversion action for outbound clicks to
   Amazon — only then does it make sense to switch bidding from
   Maximize Clicks to Maximize Conversions.
4. If cars performs well after 2-3 weeks, duplicate this ad group
   structure for planes and boats (see `SEO_KEYWORDS.md` for the
   keyword mapping), and only then consider raising the daily budget.

Come back any time and I can help review performance data, tighten
keyword lists, or draft new ad copy.
