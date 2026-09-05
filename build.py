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
    "guides": ("Guides", "Evergreen buying guides that apply across the whole RC hobby."),
}


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
        return override, f"Check Price at {product.get('merchant_name', 'Retailer')}", False

    merchant = product.get("merchant", "amazon")

    if merchant == "amazon":
        url = build_amazon_url(product["search_query"], config.get("amazon_tag", ""))
        return url, "Check Price on Amazon", False

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
    if article["category"] == "guides":
        items.append({
            "@type": "ListItem", "position": position,
            "name": "Guides", "item": site_url + "/guides/",
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


def render_product_card(product_id, products_by_id, config):
    product = products_by_id.get(product_id)
    if not product:
        return f'<p style="color:red">[Unknown product id: {product_id}]</p>'
    url, label, pending = resolve_product_link(product, config)
    pending_badge = '<span class="pending-badge">link pending</span>' if pending else ""
    image_url = product.get("image_url")
    image_html = (
        f'<img class="product-card-photo" src="{image_url}" alt="{product["name"]}" loading="lazy">'
        if image_url
        else ""
    )
    return f"""
<div class="product-card">
  <div class="product-card-body">
    <h3>{product['name']}</h3>
    <p>{product['blurb']}</p>
  </div>
  {image_html}
  <a class="cta-button" href="{url}" rel="sponsored nofollow noopener" target="_blank">
    {label} {pending_badge}
  </a>
</div>
""".strip()


def process_body(md_text, products_by_id, config):
    """Replace {{product:id}} shortcodes with rendered CTA cards, then
    convert the remaining markdown to HTML."""

    def repl(match):
        # Use a placeholder token so markdown doesn't mangle the raw HTML,
        # then swap it back in after conversion.
        return f"\n\n<!--PRODUCT_CARD:{match.group(1)}-->\n\n"

    with_placeholders = PRODUCT_TAG_RE.sub(repl, md_text)
    html = markdown.markdown(with_placeholders, extensions=["extra", "sane_lists"])

    def swap(match):
        return render_product_card(match.group(1), products_by_id, config)

    html = re.sub(r"<!--PRODUCT_CARD:([a-z0-9-]+)-->", swap, html)
    return html


def load_articles(products_by_id, config):
    default_og_image = config["site"]["url"] + "/static/img/og-default.png"
    articles = []
    for path in sorted(CONTENT_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        assert raw.startswith("---"), f"{path} missing frontmatter"
        _, fm_text, body = raw.split("---", 2)
        meta = yaml.safe_load(fm_text)
        meta["html"] = process_body(body, products_by_id, config)
        meta["url"] = f"/{meta['category']}/{meta['slug']}/" if meta["category"] != "page" else f"/{meta['slug']}/"
        meta["og_image"] = resolve_article_image(meta, products_by_id, default_og_image)
        articles.append(meta)
    articles.sort(key=lambda a: a.get("date", date.min), reverse=True)
    return articles


def main():
    config = load_yaml(DATA_DIR / "config.yaml")
    products = load_yaml(DATA_DIR / "products.yaml")
    products_by_id = {p["id"]: p for p in products}

    articles = load_articles(products_by_id, config)

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
