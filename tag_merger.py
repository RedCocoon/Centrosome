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
from pathlib import Path
import pathlib
from shutil import copyfile
from datapack_merger import *

directory = "tags"
tempFolder = "temp\\centrosome\\"
print("==============Begin tags merging==============")

## Get a list of all Datapacks with target
def getRelavantTags(Target):
    Packs = glob.glob("*\\data\\*\\"+Target,recursive=True)
    i=1
    while i >= len(Packs):
        currentPack = Packs[i]
        actualName = currentPack.replace("*\\data\\","")
        actualName = actualName.replace("\\"+Target,"")
        Packs[i] = currentPack.replace("\\data\\*\\",actualName)
        i += 1
    return(Packs)

## Copy all the .json files and if matches, attemp to merge them.
def getMotherTags(Mother,Target):
    global Directory
    global tempFolder
    MotherPaths = glob.glob(Mother+"/*.json") + glob.glob(Mother+"/**/*.json",recursive=True)
    TempPaths = []
    for path in MotherPaths:
        p = pathlib.Path(path)
        p = pathlib.Path(*p.parts[1:])
        tempPath = tempFolder+str(p)
        if Path(tempPath).is_file():
            merged = MergeTags(path, tempPath)
            writeJson(tempPath, merged)
        else:
            ensure_dir(tempPath)
            copyfile(path, tempPath)
            TempPaths.append(tempPath)
    return(TempPaths)

## Init
Packs = getRelavantTags(directory)

def MergeTags(ChildPath, MotherPath):
    ## Magic goes here
    ChildJson = loadJson(ChildPath)
    MotherJson = loadJson(MotherPath)
    NewJson = MotherJson
    try:
        for i in ChildJson["values"]:
            if i not in NewJson["values"]:
                NewJson["values"].append(i)
        print("Merged:",ChildPath,"\n With: ",MotherPath)
    except:
        print("Error with merging files! Ignoring...")
    return(NewJson)

MotherTags = getMotherTags(Packs[0],directory)
for currentPack in Packs:
    currentTags = getMotherTags(currentPack,directory)

print("==============All tags merged==============")

