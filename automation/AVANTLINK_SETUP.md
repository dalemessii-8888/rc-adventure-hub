# Turning on real commission for AvantLink / ShareASale products

Amazon links work automatically once you set `amazon_tag` in
`data/config.yaml` -- nothing else needed. AvantLink and ShareASale need one
extra manual step per product, because their affiliate links are generated
per-product on their own sites (there's no simple formula like Amazon's).

## AvantLink (Horizon Hobby, AMain Hobbies)

1. Apply and get accepted at avantlink.com.
2. Also apply to the specific merchant program (Horizon Hobby and/or AMain
   Hobbies) from inside your AvantLink dashboard -- being an AvantLink
   affiliate doesn't automatically approve you for every merchant on the
   network.
3. Once approved for a merchant, use AvantLink's **Link Generator** /
   **Product Search** tool to find the specific product page and generate
   its tracking link.
4. Paste that link into the matching product's `affiliate_url_override`
   field in `data/products.yaml`. Example:

   ```yaml
   - id: traxxas-spartan
     name: "Traxxas Spartan SR"
     category: boats
     merchant: avantlink
     merchant_name: "AMain Hobbies"
     affiliate_url_override: "https://www.avantlink.com/click.php?...(the real link)..."
     search_query: "Traxxas Spartan SR boat"
     blurb: "..."
   ```

5. Run `python3 build.py` and redeploy (a git push, if hosting is connected).

## ShareASale (Genstattu, Bezgar, etc.)

Same idea: apply at shareasale.com, apply to the specific merchant program,
generate the product-specific link from their tools, and paste it into
`affiliate_url_override` for that product.

## Why this isn't automated

Both networks require you to be individually approved per-merchant, and
generating a correct tracking link requires being logged into your own
approved account -- there's no public API step I can do on your behalf
without your account credentials. This is a ~5 minute task per product once
you're approved, not a recurring one.
