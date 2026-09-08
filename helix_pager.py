#!/usr/bin/env python3
import sys, re, subprocess, tempfile, os

raw = sys.stdin.read()

# 1. Strip OSC sequences (like OSC 133 prompt markers: \x1b]133;...\x07)
clean = re.sub(r"\x1b\][^\x07\x1b]*(\x07|\x1b\\)", "", raw)

# 2. Strip standard CSI escape sequences (\x1b[...)
clean = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", clean)

# 3. Strip remaining single escape control characters and carriage returns
clean = re.sub(r"\x1b[@-Z\\-_]", "", clean)
clean = clean.replace("\r\n", "\n").replace("\r", "")

with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as f:
    f.write(clean)
    tmp_path = f.name

try:
    subprocess.run(["hx", "+999999", tmp_path])
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
