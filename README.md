# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/asfel307/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/asfel307/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

## The World Today — Thursday, 26 November 2026

A single front-page newspaper infographic summing up the world's news for
Thursday, 26 November 2026. One lead story on the BBC's analysis of leaked
Russian statistics — at least 490,334 Russian soldiers dead in Ukraine —
plus five more stories: Donald Trump proposing new tariffs on 14 trading
partners, China facing the highest capped rate; North Korea expelling
Switzerland's envoy from Pyongyang; 31 killed when a fuel tanker caught
fire on Cairo's ring road; Bangladesh garment workers winning a 36%
minimum-wage rise; and Gukesh and Sindarov level at 1–1 after two draws in
the World Chess Championship, with Game 3 played today.

The image is drawn entirely in code with Pillow: warm cream paper, dark
slate ink, dark-teal and gold accents, a big serif masthead, and a small
pictogram for every story — a memorial candle, a tariff globe, a diplomatic
flag, a tanker fire, a sewing needle, and a chessboard. No photos, no
downloaded assets, no network calls anywhere in the build.

## The six stories

The front page is dated Thursday, 26 November 2026 and was compiled in the
early hours of that day (UTC). Each story was checked against wire
reporting before it was drawn: the BBC's Rosstat leak analysis, the Trump
tariff proposal, the North Korea expulsion, the Cairo tanker fire, the
Bangladesh wage deal and the chess match were all first reported on
25 November 2026 (overnight for 26 November papers in Asia) or, for the
chess match, continue into 26 November with Game 3 played today.

## How it is built

- `render.py` — draws `entry.png` (1024×1024) with Pillow. Run it again
  any time to regenerate the identical image.
- `main.py` — standard library only; runs `render.py` and writes the
  deterministic result into the output directory (`MAKEFUN_OUTPUT_DIR`,
  default `./out`). Deterministic: repeated runs produce byte-identical
  output.
