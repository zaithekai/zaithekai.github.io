---
layout: post
title: Headless Linux lab
date: 2026-09-10
description: >-
  Three Ubuntu VMs on a Mac mini with no monitor, created with Multipass and managed over SSH. I built it because my course's browser labs erased my work every 30 minutes.
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

The browser labs in my LPI Linux Essentials course expired after 30 minutes, and everything I'd done went with them. That worked for a single exercise, but I couldn't build on anything. I wanted a lab that kept its state and that I could break on purpose without losing my work.

##### What I built

I run a Mac mini with no monitor as a virtualization host. Multipass creates the Ubuntu VMs, and I manage everything over SSH from my iMac.

1. The host has no display, so all access is over the network.
2. I create and delete VMs with Multipass. Breaking one costs me a rebuild instead of an afternoon.
3. SSH uses keys only. Password login is off, so nobody gets in by guessing a password.

##### What I learned

Most of the coursework was command line: moving around the filesystem, archiving and compressing with tar, and shell scripting. A lab that keeps its state changed how I study. I can leave something half configured and pick it up later. When I break something badly enough that a fix isn't worth the time, I delete the instance and launch a new one.

##### What's next

I earned Linux Essentials in September 2026, and this site now builds on the same machine. Next I'm setting up deployment from GitHub to AWS.
