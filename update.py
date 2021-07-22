import os, shutil
import requests
import zipfile


def run_update(force = False):
    if not force:
        if not should_update():
            return

        update = input("There is new Script Version. Do you want to update? [Y/n] ") or "Y"
        if update not in ["y", "Y"]:
            return

    print("Downloading Update")
    url = "https://github.com/agus24/macro_seal_plus/archive/refs/heads/master.zip"
    r = requests.get(url, allow_redirects=True)
    with open("update.zip", 'wb') as file:
        file.write(r.content)


    print("Extracting File.")
    with zipfile.ZipFile("update.zip", 'r') as zip_ref:
        zip_ref.extractall("./update")

    copytree("./update/macro_seal_plus-master", "./")

    print("Copying Config.")
    if not os.path.isfile('./config.py'):
        shutil.copyfile("./config.tmp.py", "./config.py")
    else:
        replace = input("Do you want to replace config file? [Y/n] ") or "Y"
        if replace in ["Y", "y"]:
            shutil.copyfile("./config.py", "./config.old.py")
            shutil.copyfile("./config.tmp.py", "./config.py")

    shutil.rmtree("./update")
    os.remove("update.zip")

    print(f"Updated.")


def should_update():
    if not os.path.isfile('./config.py'):
        run_update(force=True)
        return

    with open("./version.txt", 'r') as file:
        current_version = int(file.readline())

    url = "https://raw.githubusercontent.com/agus24/macro_seal_plus/master/version.txt"
    new_version = int(requests.get(url).json())

    print("Current Version : ", current_version)
    print("Server Version : ", new_version)

    if current_version < new_version:
        return True

    return False


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
