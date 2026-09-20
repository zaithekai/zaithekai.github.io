---
layout: post
title: How I built this website
date: 2026-09-20
description: >-
  How I moved my portfolio from a single exported HTML page to a Jekyll site
  with two post collections, built and previewed on a headless Mac mini.
tags: [jekyll, github-pages, ruby, claude-code, homelab]
number: "002"
status: Complete
hero_image: /jekyll-logo.png
hero_alt: Jekyll logo
spec:
  generator: Jekyll
  hosting: GitHub Pages
  edge: Cloudflare
  host: Mac mini, headless
  ruby: "3.4"
  database: None
---

##### The problem

The first version of this site was a single HTML page exported from Claude Design. It looked right on GitHub Pages, but there was nowhere to put a post. Adding one meant editing one large file by hand.

My Work and Notes sections also weren't written into the HTML. JavaScript generated them after the page loaded, so anything that doesn't run scripts, including some search crawlers and link previewers, saw little more than the nav.

##### How the site is served

Nothing runs on a server. A request makes three stops:

1. DNS sends abdulzainos.com to Cloudflare, and the bare domain redirects to www.
2. Cloudflare handles HTTPS, caches pages, and hides my email from scrapers.
3. GitHub Pages hands over the files as they are.

No database, no login, nothing to patch.

##### Why Jekyll

I wanted posts as Markdown files in folders, versioned in Git. A static site generator turns those files into HTML at build time.

I looked at Next.js, Hugo, Astro, and Eleventy. Next.js is built for applications, which this isn't. The other three would work, but GitHub Pages only builds Jekyll on its own. The rest need a GitHub Actions workflow. This site isn't mission critical, so I chose the option where pushing is deploying.

##### How I designed it

I designed the first version of this site in Claude Design. I asked for something industrial, minimal, and modern, with a precise feel where every element looks intentional. I added light and dark modes to make it easier on the eyes.

I wanted the homepage to focus on three things:

- A hero that says what I do and where I'm headed
- My current projects, a short bio, credentials, and experience
- My education and how it's progressing

The education section matters most to me, and I haven't seen it on other personal sites. Every course in my degree is listed as completed, in progress, or remaining, so an employer can see exactly where I am and what's next. Typing that out by hand would have been tedious. Instead, I used AI to build the catalog from a PDF of my coursework, then gave it the list of completed classes from my student portal.

##### Two kinds of posts

Working notes are where I recount experiences and lessons learned.

Project write-ups are sessions of work with an end goal and a clear beginning and end. They record the process and everything the project involved. This post is one.

##### What changed

Claude Code did the conversion. I had it read the existing files and report back before changing anything. That's how I found out JavaScript was generating my content.

- Moved the inline CSS into its own stylesheet unchanged, then added styles for articles
- Rewrote the JavaScript-generated sections as plain HTML, so all content is in the page source
- Set up two collections: `/notes/` and `/projects/`
- Added front matter for title, date, description, and tags, which also drives link previews

Each post is a Markdown file, and the filename becomes the URL:

```
_working_notes/multipass-networking.md  →  /notes/multipass-networking/
```
{:.scroll}

##### How I set up my dev environment

The build lives on a Mac mini with no monitor. I SSH in from my iMac. The project has its own folder in my projects directory, and Claude Code only has permission to work inside it.

macOS ships Ruby 2.6, too old for Jekyll. Claude Code tried the current Ruby, 4.0.6, which also failed: `github-pages` depends on `commonmarker`, which won't install on Ruby 4, and the older releases Bundler falls back to break on anything past Ruby 3.2. Ruby 3.4 satisfied both.

```
brew install ruby@3.4
echo 'export PATH="/opt/homebrew/opt/ruby@3.4/bin:$PATH"' >> ~/.zshrc
exec zsh
bundle install
```
{:.scroll}

Gems install into `vendor/bundle`, which is gitignored along with the built `_site/` folder.

##### How I preview on a headless machine

Jekyll's server only listens on its own machine by default. Binding it to every interface makes it reachable from my network:

```
bundle exec jekyll serve --host 0.0.0.0 --livereload
```
{:.scroll}

Then I open `http://<mac-mini-ip>:4000` on my iMac or laptop, and pages refresh as I save. An SSH tunnel also works and keeps the server private:

```
ssh -L 4000:localhost:4000 user@my-server.local
```
{:.scroll}

Claude Code also ran headless Chrome to render pages and catch visual problems. The Mac mini has no screen, and neither did the browser testing the site.

##### Workflow

Claude Code commits to a branch and opens a pull request. I review the diff on GitHub, and merging to main publishes the site. The Revert button on a merged pull request undoes it in one step.

##### Locking it down

A static site has little attack surface, so the risk moves to the accounts around it.

- Two-factor authentication on GitHub, Cloudflare, and the domain registrar
- Custom domain verified in GitHub Pages, so no one else can claim it
- Cloudflare SSL set to Full (strict)
- No real IPs, hostnames, or config files in posts, since the repo history is public
