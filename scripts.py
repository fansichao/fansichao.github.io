import os




cmds = [
    "hexo clean",
    "hexo g",
    "hexo d",
]

for cmd in cmds:
    os.system(cmd)
