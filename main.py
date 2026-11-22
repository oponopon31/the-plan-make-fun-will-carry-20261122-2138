#!/usr/bin/env python3
"""Entry for make.fun competition the-plan-make-fun-will-carry-20261122-2138.

Writes a single plan text (1-280 Unicode code points) to entry.txt in the
output directory. Pure standard library, deterministic, no network.
"""

import hashlib
import os

PLAN = (
    "Day 1: build a missed-call SMS auto-reply for US dental clinics on "
    "Twilio ($20 credit). Days 2-5: find 200 clinics on Google Maps, email "
    "owners the demo. $149 setup + $49/mo. Close 3 = $447 + $147/mo. "
    "Day 30: ~$590. Edge: a live demo in one painful niche beats generic "
    "pitches."
)


def main() -> None:
    text = PLAN
    count = len(text)
    assert 1 <= count <= 280, f"plan length {count} out of range 1-280"
    assert text.strip(), "plan must not be only whitespace"
    data = text.encode("utf-8")
    data.decode("utf-8")  # validate UTF-8 round-trip

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output" or "."
    if not os.path.isdir(out_dir):
        out_dir = "."
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    digest = hashlib.sha256(data).hexdigest()

    # Post-write verification: re-read the file and confirm the bytes on
    # disk are exactly what was intended before reporting success.
    with open(path, "rb") as f:
        written = f.read()
    assert written == data, "entry.txt bytes differ from intended plan"
    assert hashlib.sha256(written).hexdigest() == digest, "sha256 mismatch"

    print(f"chars: {count}")
    print(f"sha256: {digest}")
    print(f"wrote: {path}")
    print("verified: entry.txt bytes match the plan exactly")


if __name__ == "__main__":
    main()
