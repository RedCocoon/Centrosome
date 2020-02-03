######
# This script contains all the common functions.
# It works by selecting a pack as "Mother" and
# merge every other pack into it.
# Non-important things such as comments etc are left out.
######

## Import stuffs
import glob
import json
import os
import sys
from shutil import copyfile

Directory = "temp\\centrosome\\data\\minecraft\\"
tempFolder = "temp\\centrosome\\"

## Get a list of all Datapacks with target
def getRelevantPacks(Target):
    Packs = glob.glob("*\\data\\minecraft\\"+Target,recursive=True)
    return(Packs)

## Copy all the .json files of Mother and return the copied files list
def getMotherPaths(Mother,Target):
    global Directory
    MotherPaths = glob.glob(Mother+"/*.json") + glob.glob(Mother+"/**/*.json",recursive=True)
    TempPaths = []
    for path in MotherPaths:
        tempPath = path.replace(Mother,Directory+Target)
        ensure_dir(tempPath)
        copyfile(path, tempPath)
        TempPaths.append(tempPath)
    return(TempPaths)

## https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-Target
def ensure_dir(file_path):
    Target = os.path.dirname(file_path)
    if not os.path.exists(Target):
        os.makedirs(Target)

def loadJson(Path):
    try:
        with open(Path, "r") as File:
            try:
                Json = json.loads(File.read())
            except:
                print("Error while loading json from the file! Ignoring...")
    except:
        Json = json.loads("{}")
        print("Error: Cannot open files! Ignoring...")
    File.close()
    return(Json)

def writeJson(Path, Json):
    ensure_dir(Path)
    with open(Path, "w+") as file:
        file.write(json.dumps(Json, sort_keys=False, indent=4))
        
## Loop through every pack and merge them.
## Packs: List of packs to do operation of
## Target: The place to do the operations (loot_tables, recipes, etc)
## Process: The operation to run, always take 2 argument. (Process(Child, Mother))
def processFiles(Packs, Target, Process, FileType=".json", DoOutput=True):
    global Directory
    try:
        Mother = Packs[0]
        TempPaths = getMotherPaths(Mother, Target)
    except:
        print("No "+Target+" found.")
    for i in Packs:
        ## Set the current pack as the "Child"
        Child = i
        ## Get a list of all Loot Tables of current Child (.json files)
        ChildPaths = glob.glob(Child+"/*"+FileType) + glob.glob(Child+"/**/*"+FileType,recursive=True)
        ## Compare every Child Path with every Mother Path and check if matched
        if Child != Mother:
            for CurrentChild in ChildPaths:
                merged = False
                
                for CurrentTemp in TempPaths:
                    if CurrentTemp != CurrentChild:
                        ## Generify the path to test if they're the same
                        CurrentChildPath = CurrentChild.replace(Child, Directory+Target)
                        CurrentTempPath = CurrentTemp
                        
                        ## If the paths matched, attemp to merge them
                        if CurrentChildPath == CurrentTempPath and not merged:
                            ## Ignore anything that's not .json
                            if FileType == ".json":
                                FinalJson = Process(CurrentChild, CurrentTemp)
                                ## Write them to a temporary file
                                writeJson(CurrentTempPath,FinalJson)
                            merged = True

                ## If not merged, it means that it doesn't match with any MotherPaths  
                if not merged:
                    ## Add it to MotherPaths so other Childs will attemp to merge with it
                    TempPaths.append(CurrentChild)
                    ## Add it to temp folder anyways
                    CurrentChildPath = CurrentChild.replace(Child, Directory+Target)
                    ensure_dir(CurrentChildPath)
                    copyfile(CurrentChild, CurrentChildPath)
##                    with open(CurrentChildPath, "w+") as newFile:
##                        with open(CurrentChild, "r") as original:
##                            print(original)
##                            newFile.write(original.read())
                    if DoOutput:
                        print("Copied:",CurrentChild)

## SetMode function must be run before FileSelect to set the mode.
def SetMode():
    global mode
    print("Select Mode\n1) Always use \"Mother\"\n2) Always use \"Child\"\n3) Manual select")
    while True:
        select = input("Your Choice [1/2/3]: ")
        if select == "1":
            mode = 1
            break
        elif select == "2":
            mode = 2
            break
        elif select == "3":
            mode = 3
            break
        else:
            print("Invalid Input!")
    
def FileSelect(ChildPath, MotherPath):
    global mode
    ## Magic goes here
    if mode == 1:
        Json = loadJson(MotherPath)
        print("Selected:",MotherPath)
    elif mode == 2:
        Json = loadJson(ChildPath)
        print("Selected:",ChildPath)
    elif mode == 3:
        while True:
            print("Conflict found! 1 = Mother, 2 = Child\n1)",MotherPath,"\n2)",ChildPath)
            select = input("Your Choice [1/2]: ")
            if select == "1":
                Json = loadJson(MotherPath)
                print("Mother selected")
                break
            elif select == "2":
                Json = loadJson(ChildPath)
                print("Child selected")
                break
            else:
                print("Invalid Input!")
    
    return(Json)

def setDir(Path):
    directory = sys.argv[1]
    directory += Path
    return(directory)
    
