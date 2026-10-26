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


def build(data):
    out = [HEAD.format(title=escape(data["title"]), description=escape(data["description"])),
           f"<h1>{escape(data['title'])}</h1>",
           f"<p>{escape(data['intro'])} <a href=\"{escape(data['github'])}\">GitHub</a></p>"]
    for section in data["sections"]:
        shown = [p for p in section["projects"] if not p.get("hidden")]
        if not shown:
            continue
        out += ["", f"<h2>{escape(section['title'])}</h2>", "<ul>", *map(project, shown), "</ul>"]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    data = yaml.safe_load((ROOT / "projects.yaml").read_text())
    (ROOT / "site" / "index.html").write_text(build(data))
