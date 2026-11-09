#!/usr/bin/env python3
"""
Static site builder for RC Adventure Hub.

Reads:
  data/config.yaml     -- site-wide settings + affiliate program IDs
  data/products.yaml    -- the product/link catalog
  content/*.md           -- articles & pages (YAML frontmatter + markdown body)
  templates/*.html       -- Jinja2 templates

Writes a fully static site to dist/, ready to deploy as-is to GitHub Pages,
Netlify, Cloudflare Pages, or any plain static host.

Usage:
    python3 build.py
"""
import html as html_lib
import json
import re
import shutil
import urllib.parse
from datetime import date
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
DATA_DIR = ROOT / "data"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
DIST_DIR = ROOT / "dist"

# Non-affiliate fallback search URLs, used only until a real affiliate
# link is supplied via `affiliate_url_override` in products.yaml.
MERCHANT_SEARCH_TEMPLATES = {
    "AMain Hobbies": "https://www.amainhobbies.com/searchall.aspx?searchtext={q}",
    "Horizon Hobby": "https://www.horizonhobby.com/search?q={q}",
}

CATEGORY_META = {
    "gifts": (
        "RC Gift Guides",
        "Gift guides for adults buying RC cars, boats and planes for teenagers and young adults: what to buy, what's in the box, and what to avoid.",
    ),
    "guides": ("Guides", "Evergreen buying guides that apply across the whole RC hobby."),
}

GRADE_LABELS = {
    "hobby": "Hobby-grade (repairable)",
    "toy": "Toy-grade (not repairable)",
    "desk": "Desk / indoor",
    "hobby-lite": "Beginner-friendly",
}

# Where each product category's full guide lives (used by the gift quiz).
CATEGORY_GUIDE_URLS = {
    "cars": "/cars/best-rc-cars-for-adults/",
    "planes": "/planes/best-beginner-rc-planes-for-adults/",
    "boats": "/boats/best-rc-boats-for-adults/",
}

SHORTCODE_RE = re.compile(
    r"\{\{\s*(quickpicks|shipping-note|email-signup|gift-quiz|battery-safety)\s*\}\}"
)


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_amazon_url(search_query, amazon_tag):
    q = urllib.parse.quote_plus(search_query)
    # amazon.ca, not amazon.com: Amazon Associates tags are marketplace-
    # specific, and this site's tag was issued by Amazon.ca Associates.
    # A .com link with a .ca tag tracks no commission at all.
    return f"https://www.amazon.ca/s?k={q}&tag={urllib.parse.quote_plus(amazon_tag)}"


def resolve_product_link(product, config):
    """Return (url, label, pending) for a product's call-to-action button."""
    override = product.get("affiliate_url_override")
    if override:
        merchant_name = product.get("merchant_name", "Retailer")
        if merchant_name == "Amazon":
            return override, "See Price & Delivery Date at Amazon", False
        return override, f"Check Price at {merchant_name}", False

    merchant = product.get("merchant", "amazon")

    if merchant == "amazon":
        url = build_amazon_url(product["search_query"], config.get("amazon_tag", ""))
        return url, "See Price & Delivery Date at Amazon", False

    # avantlink / shareasale / direct without an override yet -> safe,
    # working, NON-affiliate fallback link so nothing is ever dead.
    # If pending_product_url is set, we've identified the exact real
    # product page (and its photo) even though the link isn't monetized
    # yet -- use that instead of a generic search, so the photo always
    # matches what the link actually points to.
    merchant_name = product.get("merchant_name", "Retailer")
    pending_url = product.get("pending_product_url")
    if pending_url:
        url = pending_url
    else:
        template = MERCHANT_SEARCH_TEMPLATES.get(merchant_name)
        q = urllib.parse.quote_plus(product["search_query"])
        if template:
            url = template.format(q=q)
        else:
            url = f"https://www.google.com/search?q={q}"
    return url, f"Check Price at {merchant_name} (affiliate link pending)", True


PRODUCT_TAG_RE = re.compile(r"\{\{\s*product:([a-z0-9-]+)\s*\}\}")


def resolve_article_image(meta, products_by_id, default_og_image):
    """First mentioned product's real photo if there is one (makes a
    shared guide link show the actual pick instead of a generic banner),
    otherwise the site's default social-share image."""
    for pid in meta.get("products") or []:
        product = products_by_id.get(pid)
        if product and product.get("image_url"):
            return product["image_url"]
    return default_og_image


def build_breadcrumb_schema(site_url, article):
    """BreadcrumbList JSON-LD matching the actual site structure -- cars/
    planes/boats have no hub page (see git history), so only 'guides'
    articles get a middle crumb; everything else is Home > Article."""
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": site_url + "/"}]
    position = 2
    if article["category"] in CATEGORY_META:
        items.append({
            "@type": "ListItem", "position": position,
            "name": CATEGORY_META[article["category"]][0],
            "item": site_url + f"/{article['category']}/",
        })
        position += 1
    items.append({
        "@type": "ListItem", "position": position,
        "name": article["title"], "item": site_url + article["url"],
    })
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def build_article_schema(site, org_logo_url, article):
    date_str = article["date"].isoformat() if hasattr(article.get("date"), "isoformat") else str(article.get("date"))
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article["title"],
        "description": article["meta_description"],
        "image": article["og_image"],
        "datePublished": date_str,
        "dateModified": date_str,
        "author": {"@type": "Organization", "name": site["name"]},
        "publisher": {
            "@type": "Organization",
            "name": site["name"],
            "logo": {"@type": "ImageObject", "url": org_logo_url},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": site["url"] + article["url"]},
    }


def esc(text):
    return html_lib.escape(str(text), quote=True)


def render_product_card(product_id, products_by_id, config, gift_meta=None):
    product = products_by_id.get(product_id)
    if not product:
        return f'<p style="color:red">[Unknown product id: {product_id}]</p>'
    meta = (gift_meta or {}).get(product_id, {})
    url, label, pending = resolve_product_link(product, config)
    pending_badge = '<span class="pending-badge">link pending</span>' if pending else ""
    image_url = product.get("image_url")
    image_html = (
        f'<img class="product-card-photo" src="{image_url}" alt="{product["name"]}" loading="lazy">'
        if image_url
        else ""
    )

    # --- gift-buyer extras (all optional, from data/gift_meta.yaml) ---
    badges = []
    grade = meta.get("grade")
    if grade in GRADE_LABELS:
        badges.append(f'<span class="badge badge-grade">{esc(GRADE_LABELS[grade])}</span>')
    if meta.get("in_box"):
        cls = "badge-ok" if meta.get("in_box_ok") else "badge-warn"
        icon = "&#10003;" if meta.get("in_box_ok") else "&#33;"
        badges.append(f'<span class="badge {cls}"><span aria-hidden="true">{icon}</span> {esc(meta["in_box"])}</span>')
    else:
        badges.append('<span class="badge badge-neutral">Check what\'s in the box on the listing</span>')
    badge_html = f'<div class="badge-row">{"".join(badges)}</div>'

    best_for_html = (
        f'<p class="best-for"><strong>Best for:</strong> {esc(meta["best_for"])}</p>'
        if meta.get("best_for") else ""
    )

    def bullets(items):
        return "".join(f"<li>{esc(i)}</li>" for i in items)

    pros_cons_html = ""
    if meta.get("pros") or meta.get("cons"):
        pros_cons_html = '<div class="pros-cons">'
        if meta.get("pros"):
            pros_cons_html += f'<div class="pros"><h4>Why it works as a gift</h4><ul>{bullets(meta["pros"])}</ul></div>'
        if meta.get("cons"):
            pros_cons_html += f'<div class="cons"><h4>Know before you buy</h4><ul>{bullets(meta["cons"])}</ul></div>'
        pros_cons_html += "</div>"

    return f"""
<div class="product-card" id="pick-{product_id}">
  <div class="product-card-body">
    <h3>{product['name']}</h3>
    {badge_html}
    {best_for_html}
    <p>{product['blurb']}</p>
    {pros_cons_html}
  </div>
  {image_html}
  <a class="cta-button" href="{url}" rel="sponsored nofollow noopener" target="_blank">
    {label} {pending_badge}
  </a>
</div>
""".strip()


# ---------------------------------------------------------------
# Shortcode blocks (gift pages)
# ---------------------------------------------------------------
def render_quickpicks(meta, products_by_id, config, gift_meta):
    picks = meta.get("quick_picks") or []
    if not picks:
        return ""
    rows = []
    for pick in picks:
        product = products_by_id.get(pick["product"])
        if not product:
            rows.append(f'<li style="color:red">[Unknown product id: {esc(pick["product"])}]</li>')
            continue
        url, label, _ = resolve_product_link(product, config)
        pm = (gift_meta or {}).get(pick["product"], {})
        why = pick.get("why") or pm.get("best_for", "")
        rows.append(f"""
<li class="quickpick">
  <span class="quickpick-label">{esc(pick["label"])}</span>
  <span class="quickpick-name"><a href="#pick-{esc(pick["product"])}">{esc(product["name"])}</a></span>
  <span class="quickpick-why">{esc(why)}</span>
  <a class="quickpick-cta" href="{url}" rel="sponsored nofollow noopener" target="_blank">{esc(label)}</a>
</li>""".strip())
    return f"""
<div class="quickpicks">
  <h2>Quick picks: if you only have 30 seconds</h2>
  <ul>{"".join(rows)}</ul>
</div>
""".strip()


def render_shipping_note(config):
    gifts = config.get("gifts") or {}
    text = " ".join(str(gifts.get("shipping_note") or "").split())
    order_by = " ".join(str(gifts.get("order_by_note") or "").split())
    if not text and not order_by:
        return ""
    extra = f" <strong>{esc(order_by)}</strong>" if order_by else ""
    return (
        '<div class="callout callout-ship">'
        f"<strong>Gifting for the holidays?</strong> {esc(text)}{extra}"
        "</div>"
    )


def render_battery_safety():
    return (
        '<div class="callout callout-safety">'
        "<strong>Battery safety, for whoever is gifting.</strong> Most RC vehicles run on "
        "rechargeable batteries. Use the charger made for that battery, charge on a hard, "
        "non-flammable surface away from anything that can burn, never leave a charging "
        "battery unattended, and stop using any battery that is swollen, hot or damaged. "
        "For younger teens, plan to supervise the first few charges."
        "</div>"
    )


def render_email_signup(config):
    cfg = config.get("email_signup") or {}
    action = (cfg.get("action") or "").strip()
    if not action:
        return ""  # not configured -> render nothing
    return f"""
<form class="email-signup" action="{esc(action)}" method="{esc(cfg.get("method", "post"))}" target="_blank">
  <div class="email-signup-text">
    <h3>{esc(cfg.get("headline", "Get the gift-deadline reminder"))}</h3>
    <p>{esc(cfg.get("blurb", ""))}</p>
  </div>
  <label class="visually-hidden" for="gift-email">Email address</label>
  <input id="gift-email" type="email" name="{esc(cfg.get("field_name", "email"))}" placeholder="you@example.com" required>
  <button type="submit" class="btn btn-navy">{esc(cfg.get("button_label", "Sign up"))}</button>
</form>
""".strip()


def build_quiz_data(products_by_id, config, gift_meta):
    """Everything the client-side gift quiz needs, as JSON, so the quiz never
    contains a hard-coded affiliate link or invented claim."""
    data = {}
    for pid, product in products_by_id.items():
        url, label, _ = resolve_product_link(product, config)
        pm = (gift_meta or {}).get(pid, {})
        data[pid] = {
            "name": product["name"],
            "url": url,
            "cta": label,
            "guide": CATEGORY_GUIDE_URLS.get(product.get("category"), "/gifts/"),
            "bestFor": pm.get("best_for", ""),
            "inBox": pm.get("in_box", ""),
            "inBoxOk": bool(pm.get("in_box_ok")),
            "image": product.get("image_url", ""),
        }
    return data


def render_gift_quiz(quiz_data):
    payload = esc(json.dumps(quiz_data, separators=(",", ":")))
    return f"""
<section class="gift-quiz" id="gift-quiz" data-products="{payload}">
  <h2>Not sure what to get? Answer 3 quick questions</h2>
  <p class="quiz-sub">We'll point you to one pick from this site's guides. Nothing is sent anywhere; this runs in your browser.</p>
  <form class="quiz-form">
    <fieldset>
      <legend>1. Where will they use it?</legend>
      <label><input type="radio" name="where" value="indoors" required> Indoors, on a desk or table</label>
      <label><input type="radio" name="where" value="land"> Outside on land (yard, park, driveway)</label>
      <label><input type="radio" name="where" value="water"> On a lake or pond</label>
      <label><input type="radio" name="where" value="air"> In the air (open field)</label>
    </fieldset>
    <fieldset>
      <legend>2. Have they used RC vehicles before?</legend>
      <label><input type="radio" name="exp" value="new" required> Never or barely</label>
      <label><input type="radio" name="exp" value="some"> Yes, they know the basics</label>
    </fieldset>
    <fieldset>
      <legend>3. How are you feeling about budget?</legend>
      <label><input type="radio" name="budget" value="low" required> Keep it modest</label>
      <label><input type="radio" name="budget" value="mid"> Somewhere in the middle</label>
      <label><input type="radio" name="budget" value="high"> Happy to spend more for the right one</label>
    </fieldset>
    <button type="submit" class="btn btn-navy">Show my pick</button>
  </form>
  <div class="quiz-result" aria-live="polite" hidden></div>
</section>
<script src="/static/js/gift-quiz.js" defer></script>
""".strip()


def process_body(md_text, products_by_id, config, gift_meta=None, meta=None, extras=None):
    """Replace {{product:id}} and gift shortcodes with rendered blocks, then
    convert the remaining markdown to HTML."""
    meta = meta or {}
    extras = extras or {}

    def repl(match):
        # Use a placeholder token so markdown doesn't mangle the raw HTML,
        # then swap it back in after conversion.
        return f"\n\n<!--PRODUCT_CARD:{match.group(1)}-->\n\n"

    def repl_shortcode(match):
        return f"\n\n<!--SHORTCODE:{match.group(1)}-->\n\n"

    with_placeholders = PRODUCT_TAG_RE.sub(repl, md_text)
    with_placeholders = SHORTCODE_RE.sub(repl_shortcode, with_placeholders)
    html = markdown.markdown(with_placeholders, extensions=["extra", "sane_lists"])

    def swap(match):
        return render_product_card(match.group(1), products_by_id, config, gift_meta)

    def swap_shortcode(match):
        name = match.group(1)
        if name == "quickpicks":
            return render_quickpicks(meta, products_by_id, config, gift_meta)
        if name == "shipping-note":
            return render_shipping_note(config)
        if name == "email-signup":
            return render_email_signup(config)
        if name == "battery-safety":
            return render_battery_safety()
        if name == "gift-quiz":
            return render_gift_quiz(extras["quiz_data"])
        return ""

    html = re.sub(r"<!--PRODUCT_CARD:([a-z0-9-]+)-->", swap, html)
    html = re.sub(r"<!--SHORTCODE:([a-z-]+)-->", swap_shortcode, html)
    return html


def load_articles(products_by_id, config, gift_meta=None, extras=None):
    default_og_image = config["site"]["url"] + "/static/img/og-default.png"
    articles = []
    for path in sorted(CONTENT_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        assert raw.startswith("---"), f"{path} missing frontmatter"
        _, fm_text, body = raw.split("---", 2)
        meta = yaml.safe_load(fm_text)
        meta["html"] = process_body(body, products_by_id, config, gift_meta, meta, extras)
        meta["url"] = f"/{meta['category']}/{meta['slug']}/" if meta["category"] != "page" else f"/{meta['slug']}/"
        meta["og_image"] = resolve_article_image(meta, products_by_id, default_og_image)
        articles.append(meta)
    articles.sort(key=lambda a: a.get("date", date.min), reverse=True)
    return articles


def main():
    config = load_yaml(DATA_DIR / "config.yaml")
    products = load_yaml(DATA_DIR / "products.yaml")
    products_by_id = {p["id"]: p for p in products}
    gift_meta = load_yaml(DATA_DIR / "gift_meta.yaml") or {}
    unknown = [pid for pid in gift_meta if pid not in products_by_id]
    assert not unknown, f"gift_meta.yaml references unknown product ids: {unknown}"

    quiz_data = build_quiz_data(products_by_id, config, gift_meta)
    extras = {"quiz_data": quiz_data}

    articles = load_articles(products_by_id, config, gift_meta, extras)

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)

    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, DIST_DIR / "static")

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
    )

    site_url = config["site"]["url"]
    org_logo_url = site_url + "/static/img/logo-mark-180.png"
    default_og_image = site_url + "/static/img/og-default.png"
    org_schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": config["site"]["name"],
        "url": site_url + "/",
        "logo": org_logo_url,
    }
    website_schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": config["site"]["name"],
        "url": site_url + "/",
    }

    common = {
        "site": config["site"],
        "year": date.today().year,
        "default_og_image": default_og_image,
        "org_schema": org_schema,
        "website_schema": website_schema,
        "search_console_verification": config.get("search_console_verification") or "",
        "ga4_measurement_id": config.get("ga4_measurement_id") or "",
        "holiday_bar": (config.get("gifts") or {}).get("holiday_bar") or {},
        "category_labels": {c: label for c, (label, _) in CATEGORY_META.items()},
        "shipping_note_html": render_shipping_note(config),
        "email_signup_html": render_email_signup(config),
        "quiz_html": render_gift_quiz(quiz_data),
    }

    # Home page
    real_articles = [a for a in articles if a["category"] != "page"]
    home_tpl = env.get_template("home.html")
    (DIST_DIR / "index.html").write_text(
        home_tpl.render(**common, articles=real_articles, canonical_path="/"),
        encoding="utf-8",
    )

    # Category hub pages
    cat_tpl = env.get_template("category.html")
    for cat, (label, desc) in CATEGORY_META.items():
        cat_articles = [a for a in real_articles if a["category"] == cat]
        out_dir = DIST_DIR / cat
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(
            cat_tpl.render(
                **common,
                articles=cat_articles,
                category_key=cat,
                category_label=label,
                category_description=desc,
                canonical_path=f"/{cat}/",
            ),
            encoding="utf-8",
        )

    # Individual article & standalone pages
    art_tpl = env.get_template("article.html")
    for a in articles:
        out_path = DIST_DIR / a["url"].strip("/") / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        extra = {}
        if a["category"] != "page":
            extra["breadcrumb_schema"] = build_breadcrumb_schema(site_url, a)
            extra["article_schema"] = build_article_schema(config["site"], org_logo_url, a)
        out_path.write_text(
            art_tpl.render(**common, article=a, canonical_path=a["url"], **extra),
            encoding="utf-8",
        )

    # sitemap.xml (includes <lastmod> so crawlers can see what's fresh)
    today_str = date.today().isoformat()
    dated_urls = [("/", today_str)] + [(f"/{c}/", today_str) for c in CATEGORY_META]
    for a in articles:
        d = a.get("date")
        dated_urls.append((a["url"], d.isoformat() if hasattr(d, "isoformat") else today_str))
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, lastmod in dated_urls:
        sitemap.append(f"  <url><loc>{site_url}{u}</loc><lastmod>{lastmod}</lastmod></url>")
    sitemap.append("</urlset>")
    (DIST_DIR / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")

    # robots.txt
    (DIST_DIR / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {config['site']['url']}/sitemap.xml\n",
        encoding="utf-8",
    )

    print(f"Built {len(articles)} pages -> {DIST_DIR}")


if __name__ == "__main__":
    main()
