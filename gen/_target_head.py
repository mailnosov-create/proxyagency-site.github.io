import os, re, shutil, glob

ROOT = "/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad"
OUT = ROOT + "/tilda-target"
osrc = open(ROOT + "/gen/build_opti.py", encoding="utf-8").read()

# reuse setup (BASE, FONTS, header, wrap, CHECK) and CSS from the OPTI build
pre = osrc[:osrc.index("