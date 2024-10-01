import argparse
import os
import tomllib

# TODO NOW test with all by first adding more names in
# python3 integrateFlatpak.py flatpaktoxdg --flatpaks FreeTube

# TODO add more truenames?


parser = argparse.ArgumentParser(description ="This script integrates flatpaks to your system by linking program data directories in flatpaks to your normal XDG locations.")
parser.add_argument("mode", 
                    choices=["flatpaktoxdg", "xdgtoflatpak"], 
                    default="flatpaktoxdg",  
                    help="Flatpak To System: move flatpak files to XDG dir then symlink. System to Flatpak: Delete flatpak files then symlink XDG dir.")
parser.add_argument("--noconfig", dest="NOCONFIG", action="store_true", help="Do not alter config dirs.")
parser.add_argument("--nodata", dest="NODATA", action="store_true", help="Do not alter data dirs.")
parser.add_argument("--nocache", dest="NOCACHE", action="store_true", help="Do not alter cache dirs.")
parser.add_argument("--flatpaks", dest="FLATPAKLIST", action="append", help="Limit to certain flatpaks instead of all installed.")
args = parser.parse_args()





flatpaksDir = os.path.expanduser("~/.var/app/")
configsDir = os.environ.get("XDG_CONFIG_HOME")
cachesDir = os.environ.get("XDG_CACHE_HOME")
datasDir = os.environ.get("XDG_DATA_HOME")

bashStr = "#!/usr/bin/sh\n"

with open("truenames.toml", "rb+") as file:
    config = tomllib.load(file)

flatpakPaths = [f.path for f in os.scandir(flatpaksDir) if f.is_dir]

if(args.mode == "flatpaktoxdg"):
    for flatpakPath in flatpakPaths:
        flatpakLocName = flatpakPath.removeprefix(flatpaksDir)

        if flatpakLocName in config["skip"]:
            continue

        # Check if flatpak's true name is known
        if flatpakLocName not in config["run"]:
            print(f"Error! '${flatpakLocName}' not found in config file. Please look in its' config file and its true name to the true names toml.")
            continue
        
        flatpakTrueName = config["run"][flatpakLocName]

        # Check if user wants this flatpak to be altered. Default: yes
        if args.FLATPAKLIST is not None:
            if flatpakLocName not in args.FLATPAKLIST and flatpakTrueName not in args.FLATPAKLIST:
                print(f"Skipping {flatpakLocName} ...")
                continue

        #Steps for commands
        #1. mv files to dest
        #2. create link
        #3. create permissions


        #CONFIG
        if (not args.NOCONFIG and os.path.exists(f"{flatpaksDir}{flatpakLocName}/config/{flatpakTrueName}/")):
            bashStr += f"###### {flatpakTrueName} - Config #####\n"
            bashStr += f"mkdir {configsDir}/{flatpakTrueName}\n"
            bashStr += f"mv {flatpaksDir}{flatpakLocName}/config/{flatpakTrueName}/* {configsDir}/{flatpakTrueName}\n"
            bashStr += f"ln -s {configsDir}/{flatpakTrueName} {flatpaksDir}{flatpakLocName}/config/\n"
            bashStr += f"flatpak override {flatpakLocName} --user --filesystem={configsDir}/{flatpakTrueName}\n"
        #CACHE
        if (not args.NOCACHE and os.path.exists(f"{flatpaksDir}{flatpakLocName}/cache/{flatpakTrueName}/")):
            bashStr += f"###### {flatpakTrueName} - Cache #####\n"
            bashStr += f"mkdir {cachesDir}/{flatpakTrueName}\n"
            bashStr += f"mv {flatpaksDir}{flatpakLocName}/cache/{flatpakTrueName}/* {cachesDir}/{flatpakTrueName}\n"
            bashStr += f"ln -s {cachesDir}/{flatpakTrueName} {flatpaksDir}{flatpakLocName}/cache/\n"
            bashStr += f"flatpak override {flatpakLocName} --user --filesystem={cachesDir}/{flatpakTrueName}\n"
        #DATA
        if (not args.NODATA and os.path.exists(f"{flatpaksDir}{flatpakLocName}/data/{flatpakTrueName}/")):
            bashStr += f"###### {flatpakTrueName} - Data #####\n"
            bashStr += f"mkdir {datasDir}/{flatpakTrueName}\n"
            bashStr += f"mv {flatpaksDir}{flatpakLocName}/data/{flatpakTrueName}/* {datasDir}/{flatpakTrueName}\n"
            bashStr += f"ln -s {datasDir}/{flatpakTrueName} {flatpaksDir}{flatpakLocName}/data/\n"
            bashStr += f"flatpak override {flatpakLocName} --user --filesystem={datasDir}/{flatpakTrueName}\n"

    with open("flatpak-to-xdg", "w+") as file:
        file.write(bashStr)
#System To Flatpak
else:
    for flatpakPath in flatpakPaths:
        flatpakLocName = flatpakPath.removeprefix(flatpaksDir)

        if flatpakLocName in config["skip"]:
            continue

        # Check if flatpak's true name is known
        if flatpakLocName not in config:
            print(f"Error! '${flatpakLocName}' not found in config file. Please look in its' config file and its true name to the true names toml.")
            continue

        flatpakTrueName = config["run"][flatpakLocName]

        # Check if user wants this flatpak to be altered. Default: yes
        if args.FLATPAKLIST is not None:
            if flatpakLocName not in args.FLATPAKLIST and flatpakTrueName not in args.FLATPAKLIST:
                print(f"Skipping {flatpakLocName} ...")
                continue

        #Steps for commands
        #1. delete flatpak files
        #2. create link
        #3. create permissions


        #CONFIG
        if (not args.NOCONFIG and os.path.exists(f"{configsDir}/{flatpakTrueName}/")):
            bashStr += f"###### {flatpakTrueName} - Config #####\n"
            bashStr += f"rmdir ~/.var/app/{flatpakLocName}/config/{flatpakTrueName}/\n"
            bashStr += f"ln -s {configsDir}/{flatpakTrueName} ~/.var/app/{flatpakLocName}/config/\n"
            bashStr += f"flatpak override {flatpakLocName} --user --filesystem={configsDir}/{flatpakTrueName}\n"
        #CACHE
        if (not args.NOCACHE and os.path.exists(f"{cachesDir}{flatpakTrueName}/")):
            bashStr += f"###### {flatpakTrueName} - Cache #####\n"
            bashStr += f"rmdir ~/.var/app/{flatpakLocName}/cache/{flatpakTrueName}/\n"
            bashStr += f"ln -s {cachesDir}/{flatpakTrueName} ~/.var/app/{flatpakLocName}/cache/\n"
            bashStr += f"flatpak override {flatpakLocName} --user --filesystem={cachesDir}/{flatpakTrueName}\n"
        #DATA
        if (not args.NODATA and os.path.exists(f"{datasDir}{flatpakTrueName}/")):
            bashStr += f"###### {flatpakTrueName} - Data #####\n"
            bashStr += f"rmdir ~/.var/app/{flatpakLocName}/data/{flatpakTrueName}/\n"
            bashStr += f"ln -s {datasDir}/{flatpakTrueName} ~/.var/app/{flatpakLocName}/data/\n"
            bashStr += f"flatpak override {flatpakLocName} --user --filesystem={datasDir}/{flatpakTrueName}\n"

    with open("xdg-to-flatpak", "w+") as file:
        file.write(bashStr)


print("Integration task complete.")
