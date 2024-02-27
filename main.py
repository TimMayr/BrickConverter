import configparser
import csv
import os
import shutil
import subprocess
from pathlib import Path

import requests
from colorama import Fore, Style

ldrawPath = ""
outputPath = os.path.join(os.getcwd(), "generated")
rebrickableAPIKey = ""
rebrickableBaseURL = "https://rebrickable.com/api/v3/"


def getPartsForSet(setNumber):
    rebrickableAPIArguments = "?key=" + rebrickableAPIKey + ("&inc_part_details=1&"
                                                             "inc_minifig_parts=1&inc_color_details=0")
    setJson = (requests.get(rebrickableBaseURL + "lego/sets/" + setNumber + "/parts/" + rebrickableAPIArguments).json())
    parts = list()

    if "detail" in setJson:
        print("API key invalid")
        return

    if setJson["count"] == 0:
        print("Unknown Set (Format: {SetNum}-[version})")
        return

    for brick in setJson["results"]:
        if not brick["is_spare"]:
            parts.append(brick)

    if not os.path.exists(os.path.join(outputPath, setNumber)):
        os.makedirs(os.path.join(outputPath, setNumber))

    f = open(os.path.join(outputPath, setNumber, "partlist.txt"), "w")

    printPartList(f, parts)

    f.flush()

    print("Generated Partlist")
    generatedParts = set()
    errorParts = set()

    for path in Path(outputPath).rglob("*.stl"):
        generatedParts.add(str(path.name).split(".")[0])

    generatePartsFromDict(errorParts, generatedParts, parts, setNumber)

    f = open(os.path.join(outputPath, setNumber, "error.txt"), "w")
    for part in errorParts:
        print(part, file=f)

    if len(errorParts) > 0:
        print("Errors have been logged to error.txt")


def generatePartsFromDict(errorParts, generatedParts, parts, setNumber):
    for brick in parts:
        if "LDraw" in brick["part"]["external_ids"]:
            ldrawID = brick["part"]["external_ids"]["LDraw"][0]
            if not generatedParts.__contains__(brick["part"]["part_num"]):
                print("Generating " + brick["part"]["part_num"] + " " + brick["part"]["name"])
                generatePart(brick["part"]["part_num"], ldrawID, setNumber)
                generatedParts.add(ldrawID)
                print("Finished generating " + brick["part"]["part_num"] + " " + brick["part"]["name"])
            else:
                print(brick["part"]["part_num"] + " has already been generated. Copying to new Directory")
                for path in Path(outputPath).rglob(brick["part"]["part_num"] + ".stl"):
                    if not str(path).__contains__(setNumber):
                        shutil.copy(path, os.path.join(outputPath, setNumber))
                        break

        else:
            print(Fore.RED + "No Ldraw file exist for part " + brick["part"]["part_num"])
            print("Try finding an interchangeable part (on Bricklink, Rebrickable, etc) "
                  "and converting it separately")
            print(Style.RESET_ALL, end="")
            errorParts.add(brick["part"]["part_num"])


def printPartList(f, parts):
    for brick in parts:
        print(brick["quantity"], end=" ", file=f)
        print("x", end=" ", file=f)
        print(brick["part"]["part_num"], file=f)
        print("\t", end="", file=f)
        print(brick["part"]["name"], file=f)
        print("\t", end="", file=f)
        print(brick["color"]["name"], file=f)


def removeLdr(name, location):
    if os.path.exists(os.path.join(outputPath, location, name + ".ldr")):
        os.remove(os.path.join(outputPath, location, name + ".ldr"))


def generatePart(name, ldrawName, location):
    generateLdr(name, ldrawName, location)
    generateStl(name, location)
    removeLdr(name, location)


def generateStl(name, location):
    if not os.path.exists(os.path.join(outputPath, location, name + ".stl")):
        subprocess.run(f'"{ldrawPath}" "{os.path.join(outputPath, location, name + ".ldr")}" '
                       f'-ExportFile="{os.path.join(outputPath, location, name + ".stl")}"', shell=True)


def generateLdr(name, ldrawName, location):
    if not os.path.exists(os.path.join(outputPath, location, name + ".ldr")):
        if not os.path.exists(os.path.join(outputPath, location)):
            os.makedirs(os.path.join(outputPath, location))

        f = open(os.path.join(outputPath, location, name + ".ldr"), "w")
        f.write("0 FILE " + ldrawName + " - Main model.ldr")
        f.write("\n")
        f.write("1 0 0 0 0 0 0 1 0 1 0 -1 0 0 " + ldrawName + ".dat")
        f.flush()


def getLDrawPartNumber(name):
    rebrickableAPIArguments = "?key=" + rebrickableAPIKey + ("&inc_part_details=1&"
                                                             "inc_minifig_parts=1&inc_color_details=0")
    partJSON = (requests.get(rebrickableBaseURL + "lego/parts/" + name + "/" + rebrickableAPIArguments).json())
    if "detail" in partJSON:
        exit("Part does not exist. Try finding an interchangeable part (on Bricklink, Rebrickable, etc)")
    return partJSON["external_ids"]["LDraw"][0]


# noinspection PyTypeChecker,PyUnresolvedReferences
def getPartsFromList(partList):
    folderName = os.path.basename(partList)
    folderName = str(folderName).split(".")[0]

    if not os.path.exists(os.path.join(outputPath, folderName)):
        os.makedirs(os.path.join(outputPath, folderName))

    f = open(os.path.join(outputPath, folderName, "partlist.txt"), "w")
    parts = list()

    with open(partList) as partListFile:
        reader = csv.DictReader(partListFile)
        next(reader, None)
        for row in reader:
            parts.append(row)

    parts.pop()
    parts.pop()
    parts.pop()

    for brick in parts:
        brick["quantity"] = brick["Qty"]
        brick["part"] = dict()
        brick["part"]["part_num"] = brick["BLItemNo"]
        brick["part"]["name"] = brick["PartName"]
        brick["part"]["external_ids"] = dict()
        brick["part"]["external_ids"]["LDraw"] = list()
        brick["part"]["external_ids"]["LDraw"].append(brick["LdrawId"])

        brick["color"] = dict()
        brick["color"]["name"] = brick["ColorName"]

    printPartList(f, parts)

    errorParts = set()
    generatedParts = set()
    generatePartsFromDict(errorParts, generatedParts, parts, folderName)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    if not os.path.exists("finder.config"):
        config["General"] = {"ldrawpath": "", "rebrickable_api_key": ""}
        with open('finder.config', 'w') as configfile:
            config.write(configfile)

    config.read("finder.config")
    if not config["General"]["ldrawpath"]:
        currentLdrawPath = input("Enter Path to LDView executable: ")
        config["General"]["ldrawpath"] = currentLdrawPath
    if not config["General"]["rebrickable_api_key"]:
        currentAPIKey = input("Enter your Rebrickable API Key (https://rebrickable.com/api/): ")
        config["General"]["rebrickable_api_key"] = currentAPIKey

    ldrawPath = config["General"]["ldrawpath"]
    rebrickableAPIKey = config["General"]["rebrickable_api_key"]

    with open('finder.config', 'w') as configfile:
        config.write(configfile)

    command = input("Enter command ([S]et, [P]art, Part[L]ist): ")
    if command == "S":
        setNum = input("Enter set number: ")
        getPartsForSet(setNum)
    if command == "P":
        partNum = input("Enter Rebrickable part number: ")
        print("Generating " + partNum)
        generatePart(partNum, getLDrawPartNumber(partNum), "parts")
        print("Finished generating " + partNum)
    if command == "L":
        partList = input("Enter path to Partlist: ")
        getPartsFromList(partList)
