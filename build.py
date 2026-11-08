"""Build site/index.html from projects.yaml. Run: python3 build.py"""
from html import escape as _escape
from pathlib import Path

import yaml

ROOT = Path(__file__).parent


def escape(s):
    return _escape(s, quote=False).replace('"', "&quot;")


HEAD = """<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{intro}">
<meta property="og:image" content="{image}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{image_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{intro}">
<meta name="twitter:image" content="{image}">
<meta name="twitter:image:alt" content="{image_alt}">
<style>
  :root {{ color-scheme: light dark; }}
  body {{ max-width: 40rem; margin: 2rem auto; padding: 0 1rem; font: 16px/1.5 system-ui, sans-serif; background: #fff; color: #222; }}
  a {{ color: #0645ad; }}
  li {{ margin-bottom: .6rem; }}
  @media (prefers-color-scheme: dark) {{
    body {{ background: #111; color: #ddd; }}
    a {{ color: #8ab4f8; }}
  }}
</style>
<script defer src="https://stats.bringfour.com/b4.js" data-website-id="8675ff73-4918-4e22-b3a8-3c2635d23539"></script>
"""


def project(p):
    links = [f'<a href="{escape(p[k])}">{k}</a>' for k in ("site", "repo") if p.get(k)]
    return (f"  <li><b>{escape(p['name'])}</b> — {escape(p['blurb'])}\n"
            f"    {' · '.join(links)}</li>")


def visible_sections(data):
    for section in data["sections"]:
        shown = [p for p in section["projects"] if not p.get("hidden")]
        if shown:
            yield section["title"], shown


def build(data):
    groups = [title for title, _ in visible_sections(data)]
    image_alt = f"{data['title']}: projects in {', '.join(groups[:-1])} and {groups[-1]}."
    out = [HEAD.format(title=escape(data["title"]), description=escape(data["description"]),
                       intro=escape(data["intro"]), url=escape(data["url"]),
                       image=escape(data["url"] + data["image"]), image_alt=escape(image_alt)),
           f"<h1>{escape(data['title'])}</h1>",
           f"<p>{escape(data['intro'])} <a href=\"{escape(data['github'])}\">GitHub</a></p>"]
    for title, shown in visible_sections(data):
        out += ["", f"<h2>{escape(title)}</h2>", "<ul>", *map(project, shown), "</ul>"]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    data = yaml.safe_load((ROOT / "projects.yaml").read_text())
    (ROOT / "site" / "index.html").write_text(build(data))
