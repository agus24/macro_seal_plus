import os, shutil
import requests
import zipfile


def run_update():
    print("Downloading Update..")
    url = "https://github.com/agus24/macro_seal_plus/archive/refs/heads/master.zip"
    r = requests.get(url, allow_redirects=True)
    with open("update.zip", 'wb') as file:
        file.write(r.content)

    with zipfile.ZipFile("update.zip", 'r') as zip_ref:
        zip_ref.extractall("./update")

    copytree("./update/macro_seal_plus-master", "./")
    shutil.rmtree("./update")
    os.remove("update.zip")
    print(f"Updated.")


def copytree(src, dst, symlinks=False, ignore=None):
    print(f"Updating..")
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.exists(d):
            if os.path.isdir(d):
                shutil.rmtree(d)
            else:
                os.remove(d)

        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
