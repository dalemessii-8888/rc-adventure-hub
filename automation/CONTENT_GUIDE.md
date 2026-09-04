# Content guide (for me, future-me, or anyone else writing for this site)

Keep new articles consistent with the first five. Specifically:

- **Opinionated, not a listicle.** Every recommendation says *why*, and
  explicitly says what we'd skip and why. No "10 Best X" filler with no real
  point of view.
- **No invented numbers.** Don't state a specific price, top speed, or
  runtime unless it's genuinely well-established/verified -- prices and specs
  go stale fast and a wrong number erodes trust fast. When in doubt, say
  "check current pricing" rather than quoting a figure.
- **Only recommend real, established products.** Prefer brands and product
  lines with a real track record and real parts/support ecosystems (Traxxas,
  ARRMA, Redcat, HobbyZone/E-flite, Pro Boat, etc., or their genuine
  successors). Don't recommend something because it's easy to find an
  affiliate link for it.
- **Every product mentioned gets an entry in `data/products.yaml`** and is
  referenced in the article body with `{{product:its-id}}` -- never a raw
  hyperlink to a retailer. This keeps every affiliate destination editable
  from one file.
- **Practical, specific advice over generic filler.** The "one thing nobody
  tells beginners" / "before you take X to open water" style sections in the
  existing articles perform better and read as more trustworthy than generic
  wrap-up paragraphs. New articles should include something like this.
- **Internal links.** Link to the two evergreen guides
  (`/guides/rc-hobby-101-beginners-guide/` and `/guides/nitro-vs-electric/`)
  where relevant, and have them link back to new articles as they're added.
- **Frontmatter fields required:** `title`, `slug`, `category`
  (`cars`/`planes`/`boats`/`guides`), `meta_description` (under ~155
  characters), `date`, `products` (list of product ids used).
