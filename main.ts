// The Sunday World — news-image-20261122 entry (Node 22, standard library only).
// The entry image sits beside this file as entry.png; the program copies it to
// /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png when set, for local runs).
// The image itself is drawn by draw.py (Python + PIL) from 40 sourced stories
// of Sunday 22 November 2026; this file only moves the finished bytes, so two
// runs always write identical output.

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), target);
// Fail loudly if the copy somehow landed empty, instead of passing a 0-byte image.
if (statSync(target).size === 0) {
  throw new Error("entry.png copied as 0 bytes");
}
