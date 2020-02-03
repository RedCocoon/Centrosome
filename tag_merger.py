######
# This script will merge tags.
# It works by selecting a pack as "Mother" and
# merge every other pack into it.
# Non-important things such as comments etc are left out.
######

## Import stuffs
import glob
import json
import os
from datapack_merger import *

directory = "tags"
print("==============Begin tags merging==============")

## Init
Packs = getRelevantPacks(directory)

def MergeTags(ChildPath, MotherPath):
    ## Magic goes here
    ChildJson = loadJson(ChildPath)
    MotherJson = loadJson(MotherPath)
    NewJson = MotherJson
    try:
        for i in ChildJson["values"]:
            if i not in NewJson:
                NewJson["values"].append(i)
        print("Merged:",ChildPath,"\n With: ",MotherPath)
    except:
        print("Error with merging files! Ignoring...")
    return(NewJson)

processFiles(Packs, directory, MergeTags)

print("==============All tags merged==============")

