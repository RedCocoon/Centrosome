######
# This script will merge loot tables.
# It works by selecting a pack as "Mother" and
# merge every other pack into it.
# Non-important things such as comments etc are left out.
######

## Import stuffs
import glob
import json
import os
from datapack_merger import *

directory = "loot_tables"
print("==============Begin loot tables merging==============")

## Init
Packs = getRelevantPacks(directory)

def MergeTables(ChildPath, MotherPath):
    ## Magic goes here
    ChildJson = loadJson(ChildPath)
    MotherJson = loadJson(MotherPath)
    try:
        NewJson = MotherJson
        for i in ChildJson["pools"]:
            if i not in MotherJson["pools"]:
                NewJson["pools"].append(i)
        MergedFile = NewJson
        print("Merged:",ChildPath,"\n With: ",MotherPath)
    except:
        MergedFile = MotherJson
        print("Error with merging files!\n Mother:",MotherPath,"\n Child:",ChildPath,"\nIgnoring...")
    return(MergedFile)

processFiles(Packs, directory, MergeTables, DoOutput=False)

print("==============All loot tables merged==============")

