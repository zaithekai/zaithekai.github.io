---
layout: post
title: Headless Linux lab
date: 2026-09-10
description: >-
  A Mac mini running headless as a virtualization host, with Ubuntu instances I provision through Multipass. Administered entirely over SSH, so nothing resets when I close the tab.
tags: [linux, multipass, ssh, homelab]
number: "001"
status: Ongoing
hero_image: /lab-topology.svg
hero_alt: Lab topology diagram
spec:
  host: Mac mini, headless
  vms: Ubuntu via Multipass
  access: SSH, keys only
  instances: 3
---

##### The problem

I'm working through the LPI Linux Essentials material, and the browser labs it ships with expire after 30 minutes. Everything I did was gone when the timer ran out. Fine for a single exercise, useless for anything I wanted to build on. I wanted an environment that stuck around, and one I could break on purpose without losing my work.

##### What I built

A Mac mini running headless as a virtualization host, with Ubuntu instances I provision through Multipass. I administer all of it over SSH from my iMac. No monitor on the host, no desktop on the guests.

1. The host runs with no display attached. I reach it over the network or not at all.
2. I create and destroy Ubuntu VMs through Multipass, so breaking one costs me a rebuild instead of an afternoon.
3. Key-based SSH with password authentication disabled, so a guessable password is not a way into the host.

##### What I learned

Most of the coursework has been command line: finding my way around the filesystem, archiving and compression with tar, shell scripting. Having a machine that keeps its state changed how I study. I can leave something half-configured, come back to it later, and pick up where I stopped. And when I break something badly enough that fixing it isn't worth the time, I delete the instance and launch a new one.

##### What's next

Finishing the shell scripting section, then moving my development work onto this machine and using it as the environment I actually build in, with deployment running from GitHub out to AWS.
