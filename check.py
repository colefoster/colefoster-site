"""Check the built page: share tags, share image size, and (with --links) that every link answers 200.

Run: python3 build.py && python3 check.py --links
"""
import re
import struct
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
REQUIRED = ["og:title", "og:description", "og:image", "og:url", "twitter:card", "twitter:image"]
UA = "Mozilla/5.0 (compatible; link-check)"  # generic on purpose


def main():
    html = (ROOT / "site" / "index.html").read_text()
    meta = dict(re.findall(r'<meta (?:property|name)="([^"]+)" content="([^"]*)"', html))
    missing = [k for k in REQUIRED if not meta.get(k)]
    assert not missing, f"missing tags: {missing}"
    assert meta["twitter:card"] == "summary_large_image"
    png = (ROOT / "site" / meta["og:image"].rsplit("/", 1)[1]).read_bytes()
    size = struct.unpack(">II", png[16:24])
    assert size == (1200, 630), f"share image is {size}"
    print("tags ok, image 1200x630")

    if "--links" in sys.argv:
        links = sorted(set(re.findall(r'(?:href|src)="(https?://[^"]+)"', html)))
        bad = []
        for url in links:
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
            try:
                code = urllib.request.urlopen(req, timeout=15).status
            except urllib.error.HTTPError as e:
                code = e.code
            print(code, url)
            if code != 200:
                bad.append(url)
        assert not bad, f"broken links: {bad}"


if __name__ == "__main__":
    main()
