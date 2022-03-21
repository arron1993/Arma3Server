import os
import re
import subprocess
import urllib.request

import keys

WORKSHOP = "steamapps/workshop/content/107410/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"  # noqa: E501
DL_ATTEMPT_LIMIT = 10

def download_mod(id):
    timed_out = False
    attempts = 0
    while attempts < DL_ATTEMPT_LIMIT and timed_out:
        print(id, attempts, timed_out)
        steamcmd = ["/steamcmd/steamcmd.sh"]
        steamcmd.extend(["+force_install_dir", "/arma3"])
        steamcmd.extend(["+login", os.environ["STEAM_USER"], os.environ["STEAM_PASSWORD"]])
        steamcmd.extend(["+workshop_download_item", "107410", id, "validate"])
        steamcmd.extend(["+quit"])
        proc = subprocess.run(steamcmd, stdout=subprocess.PIPE)
        if 'Timeout downloading item' in proc.stdout.decode():
            print(proc.stdout.decode())
            timed_out = True
            attempts += 1



def preset(mod_file):
    if mod_file.startswith("http"):
        req = urllib.request.Request(
            mod_file,
            headers={"User-Agent": USER_AGENT},
        )
        remote = urllib.request.urlopen(req)
        with open("preset.html", "wb") as f:
            f.write(remote.read())
        mod_file = "preset.html"
    mods = []
    with open(mod_file) as f:
        html = f.read()
        regex = r"filedetails\/\?id=(\d+)\""
        matches = re.finditer(regex, html, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            download_mod(match.group(1))
            moddir = WORKSHOP + match.group(1)
            mods.append(moddir)
            keys.copy(moddir)
    return mods


if __name__ == '__main__':
    preset(os.environ.get("MODS_PRESET"))
