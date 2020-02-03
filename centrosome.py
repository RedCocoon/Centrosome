######
# Welcome to the main script! Thanks for using Controsome!
# This script contains all the common functions.
# It works by selecting a pack as "Mother" and
# merge every other pack into it.
# Non-important things such as comments etc are left out.
######

import selective_merger
import loot_merger
import tag_merger

import shutil
from datapack_merger import *

print(">>> All merging completed. Copying files. <<<")

## Due to how getRelevantPacks(directory) works,
## by setting the directory to ".." and run processFiles(),
## it will loop through every single file in all the datapacks
## and copy those not already in temp folder

directory = ".."

Packs = getRelevantPacks(directory)

def CopyFiles(ChildPath, MotherPath):
    return(loadJson(MotherPath))

processFiles(Packs, directory, CopyFiles, ".json", False)
processFiles(Packs, directory, CopyFiles, ".mcfunction", False)

print(">>> All merges completed. Generating necessary files. <<<")

## Simple stuffs, just getting all the pack names and put them in pack.mcmeta
Packs = getRelevantPacks("..\\..\\pack.mcmeta")

## Strips the path so only the pack name left
Packs = [directory.replace("\\data\\minecraft\\..\\..\\pack.mcmeta","") for directory in Packs]

Directory = "temp\\centrosome\\"
ensure_dir(Directory)

with open(Directory+"pack.mcmeta", "w+") as file:
    Json = {"pack":{"pack_format":5,"description":Packs}}
    Json.update({"description":"Merged Packs using Cocoon's Datapack Merger."})
    file.write(json.dumps(Json, sort_keys=False, indent=4))

shutil.make_archive("centrosome","zip",Directory)
print(">>>>> Datapacks Merged & Packed <<<<<")

input("Press Enter to Close Terminal.")
exit(0)
