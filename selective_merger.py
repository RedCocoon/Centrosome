######
# Things that can't really be merged will get processed here.
# Includes: Recipes, Advancements, Predicates, Functions and Structures.
# It works by selecting a pack as "Mother" and
# merge every other pack into it.
# Non-important things such as comments etc are left out.
######

## Import stuffs
import glob
import json
import os
import msvcrt
from datapack_merger import *

print("==============Begin selective merging==============")

SetMode()

def SelectiveMerger(directory):
    print("==============Begin "+directory+" merging==============")
    Packs = getRelevantPacks(directory)
    processFiles(Packs, directory, FileSelect)
    print("==============Finished "+directory+" merging==============")

SelectiveMerger("recipes")
SelectiveMerger("advancements")
SelectiveMerger("predicates")
SelectiveMerger("functions")
SelectiveMerger("structures")

print("==============All selective merging completed==============")

