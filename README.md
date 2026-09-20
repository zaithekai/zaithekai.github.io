# abdulzainos.com

A Jekyll site published with GitHub Pages at <https://www.abdulzainos.com>.

## Layout of the repo

```
_config.yml              site settings and the two collections
_layouts/default.html    header, nav, footer, theme toggle, <head>, scripts
_layouts/post.html       adds the title, date and body; inherits default
index.html               the home page
notes.html               the /notes/ index
projects.html            the /projects/ index, as image cards
contact.html             the /contact/ page
_working_notes/*.md      posts that appear at /notes/<filename>/
_project_notes/*.md      posts that appear at /projects/<filename>/
assets/style.css         all CSS
site.js                  theme toggle, scroll reveal, certification pills
lab-topology.svg         diagrams and images live at the repo root
badges/                  credential images
tools/                   build scripts, excluded from the published site
```

## Adding a post

Create a Markdown file in the collection folder. The filename becomes the URL,
so keep it lowercase with hyphens and **no date prefix** — the date belongs in
the front matter.

| Collection       | Put the file in   | It publishes at                    |
| ---------------- | ----------------- | ---------------------------------- |
| Working notes    | `_working_notes/` | `/notes/<filename>/`               |
| Project write-up | `_project_notes/` | `/projects/<filename>/`            |

`_working_notes/multipass-networking.md` becomes
`https://www.abdulzainos.com/notes/multipass-networking/`.

## Front matter

Every post starts with a block fenced by `---`:

```yaml
---
layout: post
title: Multipass networking, the part that confused me
date: 2026-09-19
description: >-
  One or two sentences. Shown under the title on the post, in the listing on
  the index page, and as the page description and Open Graph description.
tags: [multipass, networking]
---
```

| Field         | Required | What it does                                                       |
| ------------- | -------- | ------------------------------------------------------------------ |
| `layout`      | yes      | Always `post`.                                                     |
| `title`       | yes      | Page heading, `<title>`, listing entry, Open Graph title.          |
| `date`        | yes      | `YYYY-MM-DD`. Sorts the index pages, newest first.                 |
| `description` | yes      | Standfirst under the title, listing blurb, meta and OG description.|
| `tags`        | no       | A list. Shown in the post header and as `article:tag`.             |

`layout`, `nav` and the back-link label are already set per collection in
`_config.yml`, so `layout: post` is the only one you could technically leave
out. Keep writing it — it makes the file readable on its own.

### Working-note extras

| Field          | What it does                                            |
| -------------- | ------------------------------------------------------- |
| `reading_time` | Free text, e.g. `5 min read`. Shown beside the date.     |

### Project-write-up extras

A post in `_project_notes/` switches to the wide two-column project layout as
soon as it has a `spec:` block:

```yaml
number: "001"                    # the accent-coloured index in the header
status: Ongoing                  # shown beside the year
hero_image: /lab-topology.svg    # banner above the body
hero_alt: Lab topology diagram
spec:                            # renders as the sticky Specification panel
  host: Mac mini, headless
  vms: Ubuntu via Multipass
  access: SSH, keys only
  instances: 3
```

Leave `spec:` out and the post renders in the single-column note layout instead.

## Writing the body

Standard Markdown. Everything is styled in the **article body** section of
`assets/style.css`:

- `##` through `####` for headings. `#####` renders as a mono accent label,
  the style the project pages use for *The problem*, *What I built* and so on.
  Don't use `#` — the post title is already the page's `<h1>`.
- Bulleted and numbered lists. In a project write-up, a numbered list becomes
  the bordered step rows with `01` `02` `03` down the side.
- `> ` for a blockquote, which gets the accent left rule.
- Backticks for inline code, triple backticks with a language for a block.
- `![alt](/image.svg)` for an image. Put image files at the repo root or in a
  folder beside it and reference them with a leading slash.

A fenced block scrolls sideways instead of wrapping if you tag it, which is
what you want for output tables, diffs and ASCII art, where a wrapped line
changes the meaning:

````markdown
```
lab-01    Running    192.168.64.2    Ubuntu 24.04 LTS
```
{:.scroll}
````

## Previewing locally

macOS ships Ruby 2.6, which is too old for Jekyll. Install Ruby 3.4 once —
**not** plain `brew install ruby`, which now gives you 4.x. `github-pages`
depends on `commonmarker`, which refuses to install on Ruby 4, and the older
`github-pages` releases bundler falls back to depend on `liquid` 4.0.3, which
calls `String#tainted?` — removed in Ruby 3.2. Only 3.x satisfies both ends.

```sh
brew install ruby@3.4
echo 'export PATH="/opt/homebrew/opt/ruby@3.4/bin:$PATH"' >> ~/.zshrc
exec zsh
ruby -v          # expect 3.4.x
```

Then, from the repo:

```sh
bundle install                   # once, and after any Gemfile change
bundle exec jekyll serve --livereload
```

Open <http://127.0.0.1:4000>. Pages rebuild as you save. Front matter errors
show up in the terminal, so watch it while you write.

### Previewing from another machine

The lab host runs headless, so there is no browser on it. Bind the server to
every interface instead of just loopback:

```sh
bundle exec jekyll serve --host 0.0.0.0 --livereload
```

Then browse to `http://<host-lan-ip>:4000` from a laptop on the same network —
`ipconfig getifaddr en0` on the host prints the address. LiveReload still works,
because the injected script follows whatever hostname the page was loaded from.

If the two machines are not on the same network, tunnel over SSH instead and
keep the server on loopback:

```sh
ssh -L 4000:localhost:4000 user@host    # then open http://localhost:4000
```

To check what GitHub will actually publish:

```sh
bundle exec jekyll build
```

The output lands in `_site/`, which is gitignored.

## Deploying

Push to `main`. GitHub Pages builds the site itself — do not commit `_site/`.
`CNAME` holds the custom domain and must stay at the repo root. There is no
`.nojekyll` file; adding one back would turn the Jekyll build off.
