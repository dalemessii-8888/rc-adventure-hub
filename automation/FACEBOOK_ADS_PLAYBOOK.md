# Facebook ads + Marketplace placement: ready-to-build plan

Everything below is copy and settings to enter in Meta Ads Manager. I can't
log in to your Meta account, so you create the campaign; this removes the
guesswork. Same rules as the rest of the site: no invented prices or specs,
and ads go to OUR pages, never straight to Amazon.

## First, what "Marketplace" means here
- **Marketplace ad placement (what we want):** a placement inside Meta Ads
  Manager. Your ad can appear among Facebook Marketplace listings. You turn it
  on under Placements > Edit placements > Facebook Marketplace. No separate
  account or product listing needed.
- **Marketplace listings (not for this):** Marketplace is for selling items
  you actually have. Listing affiliate products you don't own breaks its
  rules and will get the account flagged. Don't do it.

## Campaign structure
| Level | Setting |
|---|---|
| Campaign | Objective: **Traffic**, optimized for **Landing page views** (conversions happen on Amazon, so Meta can't see them) |
| Ad set A | "Gifters": adults 28-65 in Canada, interest in gifts / parenting / hobbies |
| Ad set B | "Hobby curious": adults 25-55, interests in RC / remote control / drones / model hobbies |
| Placements | Start with Advantage+ placements; confirm **Facebook Feed**, **Facebook Marketplace**, Instagram Feed, Stories/Reels are on. After ~a week, cut placements with poor landing-page-view cost |
| Schedule | Nov 9 to Dec 14 (adjust after checking Amazon.ca's holiday delivery guidance) |
| Budget | Your call. A small test (say two ad sets at a modest daily amount for a week) before scaling |

**Do not target teens.** The buyer is the adult. Keep minimum age 25 or
higher and don't use "teen" interest targeting; this also keeps you clear of
Meta's rules on advertising to minors.

## Landing pages (one per ad)
| Ad angle | Send to |
|---|---|
| Teen gift | `/gifts/best-rc-cars-for-teens/` |
| What's in the box | `/gifts/rc-gift-buying-guide/` |
| Budget | `/gifts/rc-gifts-by-budget/` |
| Young adults | `/gifts/rc-gifts-for-young-adults/` |
| Quiz | `/gifts/#gift-quiz` |

Add UTM tags to every link, e.g.
`?utm_source=facebook&utm_medium=paid&utm_campaign=gift-2026&utm_content=<ad-name>`

## Ad copy (5 variants)
Meta shows about the first 125 characters of primary text before "See more";
keep the hook there. Headline ~40 characters.

**1. Battery check (hook: gift-day letdown)**
- Primary: Buying an RC car as a gift? Check one thing first: is the battery and charger in the box? Some popular listings don't include them.
- Headline: Check Before You Gift
- Description: What's actually in the box
- Button: Learn More -> rc-gift-buying-guide

**2. Teen gift**
- Primary: A teen RC gift that survives the first week. See which ones are repairable, which aren't, and what's included in the box.
- Headline: Best RC Cars for Teens
- Description: Independent gift guide
- Button: Learn More -> best-rc-cars-for-teens

**3. Hobby vs toy**
- Primary: Toy-grade means replace the car. Hobby-grade means replace the part. Know which one you're gifting.
- Headline: Hobby vs Toy RC Gifts
- Description: Don't gift the wrong one
- Button: Learn More -> rc-gift-buying-guide

**4. Apartment / small space**
- Primary: No yard? A palm-sized RC drift car runs on a desk or coffee table. The easy "try this hobby" gift.
- Headline: RC Gifts for Small Spaces
- Description: No outdoor space needed
- Button: Learn More -> best-rc-cars-for-teens

**5. Quiz**
- Primary: Not sure which RC to get? Answer 3 quick questions and get one clear pick.
- Headline: 3-Question Gift Quiz
- Description: Takes 30 seconds
- Button: Learn More -> /gifts/#gift-quiz

**Marketplace-friendly tip:** Marketplace readers are in shopping mode, so
the "what's in the box" and "small space" angles (1 and 4) tend to fit best.
Test; don't assume.

## Creative specs
- Feed / Marketplace: 1080x1080 (1:1) or 1080x1350 (4:5)
- Stories / Reels: 1080x1920 (9:16), keep text out of the top and bottom ~250px
- Under 20% of the image as text is a good rule of thumb for readability

**Image rules:** don't reuse Amazon's product photos in ads (Associates
terms and Meta both restrict it). Use your own photos of items you own, a
clean graphic (big text: "Is the battery in the box?"), or short phone video.
Never imply an endorsement or that a product ships with something we haven't
confirmed.

## Tracking and compliance
- Create a **separate Amazon Associates tracking ID** for Facebook traffic
  (Associates lets you create several). Read Amazon's current rules on paid
  traffic before spending.
- If you install the Meta pixel, update `content/privacy-policy.md` and
  consider a consent banner (Canada/Quebec privacy law applies to you).
- Keep the affiliate disclosure visible; the gift pages already show it.
- Read Meta's ad policies once; avoid "before/after" claims and anything
  about guaranteed results.

## Measure
After ~3-5 days per ad: cost per landing page view, then Associates clicks
and orders by tracking ID. Pause the weakest ad in each ad set, keep two
winners, and add one new variant at a time.
