# Gift-season promotion playbook

Off-site work that sends gift buyers to the pages under `/gifts/`.
Everything here is copy/ready-to-paste; none of it runs automatically.
Same honesty rules as `CONTENT_GUIDE.md`: no invented prices or specs, and
always link to OUR pages (not straight to Amazon) from social, ads and email.

## Key dates (2026)
- Now - Nov 15: gift pages live; start Pinterest + short video.
- Nov 15 - Nov 26: push content, small paid tests.
- Black Friday Nov 27 / Cyber Monday Nov 30: biggest spike. Point everything at `/gifts/`; tell readers to check live Amazon.ca deals.
- Dec 1 onward: shipping-deadline messaging. Set `gifts.order_by_note` in `data/config.yaml` ONLY after checking Amazon.ca's published holiday delivery guidance yourself.

## Keyword targets (gift pages)
| Page | Primary | Supporting |
|---|---|---|
| /gifts/best-rc-cars-for-teens/ | best rc car for teenager | rc car gift for teen, hobby grade rc car for teens, rc car for 14 year old |
| /gifts/rc-gifts-for-young-adults/ | rc gifts for young adults | rc car gift for nephew, rc gift for boyfriend, rc boat gift |
| /gifts/rc-gifts-by-budget/ | rc gift ideas by budget | cheap rc gift, rc gift what's in the box |
| /gifts/rc-gift-buying-guide/ | what to know before buying an rc car as a gift | hobby grade vs toy grade rc gift |

## Pinterest (10 pins; link each to the matching gift page)
1. "RC Car Gift for a Teen? Check This Before You Buy" -> teens
2. "Hobby-Grade vs Toy-Grade RC: Which Makes the Better Gift?" -> buying guide
3. "The One RC Truck That Comes With Everything in the Box" -> teens
4. "Gift an RC Car to a Teen Who Lives in an Apartment" -> teens (desk drift car)
5. "RC Boat Gift Ideas for Someone Near a Lake" -> young adults
6. "RC Gifts for Young Adults: By Where They Live" -> young adults
7. "RC Gift Mistakes That Ruin Christmas Morning" -> buying guide
8. "RC Gifts by Budget: Modest, Middle, Splurge" -> by-budget
9. "Does the RC Car Come With a Battery? Check Before You Gift" -> buying guide
10. "Not Sure What RC to Buy? Take the 3-Question Quiz" -> /gifts/#gift-quiz
Pin description template: one line of value + "Gift guide for adults buying for teens and young adults." Disclose affiliate links where the platform requires it.

## Short video scripts (20-30 seconds)
- **Battery check:** "Before you buy an RC car as a gift, check one thing: is the battery and charger in the box? Some popular listings don't include them. Here's how to check..." CTA: gift buying guide.
- **Toy-grade vs hobby-grade:** show a broken part; "toy-grade means replace the car, hobby-grade means replace the part." CTA: teens guide.
- **Apartment gift:** desk drift car demo; "no yard needed." CTA: teens guide.
Keep claims to what's on the guides. Disclose affiliate relationship in the caption.

## Reddit / forums / parent groups
Answer real "what RC should I get for my kid/nephew/partner" threads with the actual reasoning (where will they use it, what's in the box, hobby vs toy). Mention the site only where the rules allow it and disclose that it's yours. Don't paste links into threads that aren't asking. Check each community's self-promotion rules first.

## Paid search (small test; send traffic to OUR pages)
Headlines (30 chars max each):
- "RC Car Gift for Teens"
- "What's in the Box? Check First"
- "RC Gift Guide: Teens & Adults"
- "Hobby vs Toy RC Gifts"
Descriptions (90 chars max):
- "Independent gift guides. See what's included, what breaks, and what they'll actually use."
- "Buying an RC for a teen? Take the 3-question quiz and get one clear pick."
Negative keywords to start: free, kit build, nitro engine parts, repair, manual, used.
Amazon Associates restricts some paid-traffic patterns: read the current Operating Agreement before spending anything.

## Email (when `email_signup.action` is set)
- Send 1-2 emails: "Gift deadline reminder" and "Last-chance gift picks".
- Link to pages on this site, NOT Amazon affiliate links, inside the email.
- Update `content/privacy-policy.md` to say you collect email addresses before turning the form on.

## Measure
Turn on GA4 (`ga4_measurement_id`) and Search Console (`search_console_verification`) in `data/config.yaml`, and watch which gift page gets clicks to Amazon in the Associates report.
