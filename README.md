# colefoster-site

One page listing my projects. The content lives in `projects.yaml`; `build.py` turns it into `site/index.html`.

- **Edit:** change `projects.yaml` and push to main. The Pages workflow builds the page and deploys it to Cloudflare Pages.
- **Preview locally:** `python3 build.py`, then open `site/index.html`. Needs PyYAML.
- **Park a project:** set `hidden: true` on it.
