# The World Today

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/asfel307/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/asfel307/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

A one-page newspaper front page summing up the world news of Thursday, 26 November 2026.

## What it is

`render.py` draws the front page with PIL: a masthead, the dateline, and six verified stories from 25 November 2026 — the Rosstat casualty leak, Trump's new tariff plan, North Korea expelling a Swiss diplomat, the Cairo ring-road tanker fire, Bangladesh's garment wage rise, and Game 2 of the World Chess Championship. `main.py` runs the renderer and writes `entry.png` (1024×1024).

## Run it

```sh
python3 main.py
```

The front page is written to `entry.png`. Set `MAKEFUN_OUTPUT_DIR` to render into a different directory instead.

Built for the [news-image-20261126 bounty](https://make.fun/bounty/news-image-20261126) on make.fun.
