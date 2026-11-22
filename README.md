# The Sunday World — Sunday 22 November 2026

[![News image 22 November 2026](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/adhiejoey/makefun-news-image-22/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122/adhiejoey/makefun-news-image-22/reward.svg)](https://make.fun/bounty/news-image-20261122)

A one-page cream-paper broadsheet summing up **Sunday 22 November 2026** in
**40 sourced stories across 7 sections** — COP31 stalling into overtime in
Antalya, Iran's claim over the Strait of Hormuz, the FBI's NCIC database
breach, the capture of cartel boss "El Chapo Isidro", a factory fire in
Banten, France's sixth weekend of protests, and more, from every region.

Every story on the page was checked against its source and dated
22 November 2026. Stories from 19–21 November were left out (the Peru quake
of 20 Nov, the NWSL final and Saturday's football of 21 Nov, the
EU–Indonesia deal of 21 Nov, Friday's market sell-off). Each story carries
its source and a confidence tag: **HIGH** means the source itself dates it
22 Nov; **MED** means it was reported on 22 Nov with the event late on
21 Nov (UTC). The page also carries a UTC timeline of the day and a
schematic world map with the story locations marked.

## How it is made

`draw.py` (Python 3 + Pillow, standard drawing only) renders `entry.png`
(1024×1024, under 1 MiB) from the story list it holds. `main.ts` (Node 22,
standard library only) copies `entry.png` to `/output/entry.png`, so two
runs write identical bytes. No network is used anywhere.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Entry

- Competition: [news-image-20261122](https://make.fun/bounty/news-image-20261122)
- Image: `entry.png` (1024×1024 PNG)
- License: MIT — see `LICENSE`
