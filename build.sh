#!/bin/sh

# incremental builds are FAST
# rm -rf build
# rm -rf dist

# rm *.spec
# original command that generates spec. We can't do this because we can't add datas
# through the cmdline yet (the in-dev version of PyInstaller has it, though).
# pyinstaller main.py --onefile

pyinstaller main.spec
