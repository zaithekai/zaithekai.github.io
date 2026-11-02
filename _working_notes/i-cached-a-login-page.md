---
layout: post
title: "I cached a login page: what troubleshooting taught me before AI could help"
date: 2026-09-10
description: >-
  I turned on caching at three layers of a WordPress stack without knowing what each one stored. A dashboard started showing one user's information to other users. This is how I tracked it down and fixed it.
tags: [caching, wordpress, troubleshooting]
reading_time: 5 min read
---

A client escalated a problem on a site I built. Their dashboard was caching logged-in pages, so one user's information was showing up for other users.

I was one to two years into running a one-person web agency.

## What I had built

I had been taught that caching makes a site faster, and that's all it meant to me. So I turned it on everywhere I found a toggle: Hummingbird at the plugin layer, server caching on Cloudways, and Cloudflare on top. None of the three were coordinated. Every blog I read treated caching like a vitamin. More is better, take it daily.

Those blogs stayed high level. Anything detailed enough to be useful, I didn't have the patience to sit down and understand.

## What a cache does

A cache saves whatever was rendered for a URL and serves that saved copy to everyone who asks for it until the timer runs out. On a marketing page, that's what you want. On a page that changes depending on who's logged in, the first visitor's version goes to everyone after them.

Cloudflare adds another variable, because each edge location keeps its own copy. The plugin and the server were also caching the same requests on their own timers. Which copy you got came down to timing.

## Googling the symptom

I could write HTML and CSS, but I didn't know PHP or JavaScript yet. So I did what I knew how to do and googled it.

My search was literally "my caching has logged user information on a dashboard, and other people can see it."

That sent me down a lot of rabbit holes. The search described the symptom accurately, but a symptom mostly finds other people who are just as lost. It doesn't find the fix.

## The words I didn't have

The words I needed were cache exclusion. I didn't know the term existed. With it, the search takes thirty seconds. Without it, you can lose a day. Or three.

That was the hard part of troubleshooting back then. A good search took the right terminology, and getting the terminology meant you already had some idea what was wrong.

The research also showed me how much there is to caching. Developers spend real time configuring it, and I had been switching it on without a plan.

## Fixing every layer

This part took the longest. An exclusion in one place meant nothing if the next layer still had its own copy, so I worked through them one at a time.

Cloudflare was the first cause, so I added a rule to bypass the cache for those pages. Varnish on the server was next, and I set a rule not to cache anything under the login directories. I also sent no-cache headers on those pages and excluded them in the plugin.

The plugin had me paste rules into `.htaccess`, which Apache reads before PHP loads. A request could be served from a cached file on disk without WordPress ever running, so that was one more place the exclusion had to be right.

I worried those pages would load slowly without caching, and I was wrong. A login page is a form, and a dashboard is mostly text. Both are dynamic, so a cache has little to save there. As long as images and scripts are handled well, those pages were never the bottleneck.

## What I'd do differently now

I'd exclude by cookie instead of by path. WordPress sets a `wordpress_logged_in_*` cookie once someone logs in. If every layer bypasses the cache when that cookie is present, every logged-in page is covered, including pages added later. Path exclusion only protects the paths you remembered to write down.

There's also a middle option I didn't know about then: fragment caching, or ESI. You cache the page and leave a hole for the part that changes per user. It makes sense on a high-traffic product page or a news site, where a small header strip is the only thing that differs between visitors. For a login page and a dashboard it would have been overkill, so excluding the whole page was the right call.

Now I decide whether a page is dynamic before I turn on any caching. I check what each layer is applying instead of trusting the defaults. When I exclude something, I verify it at every layer.

## What changed, and what didn't

AI can take you from that symptom description to "cache exclusion" in one turn, and it can ask for more context when you're vague.

It still can't tell you when you're finished. You have to describe the symptom accurately, and you have to know that fixing one layer means nothing if the layer above it is still serving a stale copy.

That part is still on you.
