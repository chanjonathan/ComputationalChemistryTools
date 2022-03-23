import os
import sys


def main():
    if len(sys.argv) == 2:
        if sys.argv[1][-4:] == ".sdf" or sys.argv[1] == "-all":
            takeInput(sys.argv[1])
        else:
            print("Enter a valid sdf filename or -all")
    elif len(sys.argv) == 1:
        print("<<<<<<<<<<<<<<<<<<<< Welcome to sdf2com! >>>>>>>>>>>>>>>>>>>>")
        print("\nTo use sdf2com, run it with a filename or -all as an argument")
    else:
        print("Invalid number of arguments")

def takeInput(argument):
    validSuffix = False
    suffixPrompt = "Enter a suffix for output file  eg. '_m062x'\n>>>> "
    while not validSuffix:
        suffix = input(suffixPrompt)
        if suffix != "":
            validSuffix = True
        else:
            suffixPrompt = "Enter a valid suffix\n>>>> "

    jobKeywords = input("Paste job keywords  eg. '# opt=(calcfc,ts,noeigen) freq=noraman 6-31g(d) scf=qc'\n>>>> ").replace("#", "").strip()

    charge = input("Enter charge  eg. '-1'\n>>>> ").strip()

    multiplicity = input("Enter multiplicity  eg. '2'\n>>>> ").strip()

    jobOptions = input("Paste job options with <br> separating new lines  eg. 'B 1 3 F<br><br>C H O P S N 0<br>6-31G(d)'\n>>>> ").replace("<br>", "\n")

    if argument == "-all":
        doAll(suffix, jobKeywords, jobOptions, charge, multiplicity)
    else:
        sdf2com(argument, suffix, jobKeywords, jobOptions, charge, multiplicity)


def doAll(suffix, jobKeywords, jobOptions, charge, multiplicity):
    filenames = os.listdir()

    sdfFileNames = []

    for filename in filenames:
        if filename[-4:] == ".sdf":
            sdfFileNames.append(filename)

    for sdfFileName in sdfFileNames:
        sdf2com(sdfFileName, suffix, jobKeywords, jobOptions, charge, multiplicity)


def sdf2com(sdfFileName, suffix, jobKeywords, jobOptions, charge, multiplicity):
    try:
        frames = sdfReader(sdfFileName)
    except:
        print("Could not read " + sdfFileName)
    else:
        frameNumber = 1
        for frame in frames:
            try:
                title = frame[0]
                rows = frame[1]
                bonds = frame[2]
                comWriter(frameNumber, sdfFileName, suffix, jobKeywords, title, charge, multiplicity, rows, bonds,
                          jobOptions)
            except:
                print("Could not write " + sdfFileName[0:-4] + sdfFileName[-4:].replace(".sdf", "_" + str(
                    frameNumber) + suffix + ".com"))
            finally:
                frameNumber += 1


def sdfReader(sdfFileName):
    sdfFile = open(sdfFileName)
    lines = sdfFile.readlines()

    startIndex = 4

    atomCount = 0
    for line in lines[startIndex:]:
        if len(line.strip().split()) != 10:
            break
        else:
            atomCount += 1
    frames = []
    while startIndex:
        frame = readFrame(lines, startIndex, atomCount)
        frames.append(frame)
        startIndex = findFrame(lines, startIndex + atomCount + atomCount, len(lines))

    return frames


def readFrame(lines, startIndex, atomCount):
    title = lines[startIndex - 4].strip()

    rows = []
    for i in range(startIndex, startIndex + atomCount):
        row = lines[i].strip().split()
        rows.append(row)

    bonds = []
    for i in range(startIndex + atomCount, startIndex + atomCount + atomCount):
        atom1 = lines[i][0:3].strip()
        atom2 = lines[i][3:6].strip()
        bondOrder = lines[i][6:9].strip()
        bond = [atom1, atom2, bondOrder]
        bonds.append(bond)

    frame = [title, rows, bonds]

    return frame


def findFrame(lines, start, end):
    startIndex = False
    for i in range(start, end):
        if lines[i].strip() == "$$$$":
            startIndex = i + 5
            if startIndex >= end:
                startIndex = False
            break
    return startIndex


def comWriter(frameNumber, sdfFileName, suffix, jobKeywords, title, charge, multiplicity, rows, bonds, jobOptions):
    comFile = open(sdfFileName[0:-4] + sdfFileName[-4:].replace(".sdf", "_" + str(frameNumber) + suffix + ".com"), "w")

    comFile.write("%nprocshared=32\n%mem=8000MB\n")
    comFile.write(
        "%chk=" + sdfFileName[0:-4] + sdfFileName[-4:].replace(".sdf", "_" + str(frameNumber) + suffix + ".chk\n"))
    comFile.write("# " + jobKeywords + "\n\n")
    comFile.write(title + "\n")

    comFile.write("\n")
    comFile.write((" " + charge).replace(" -", "-") + " " + multiplicity + "\n")
    for row in rows:
        atomName = row[3]
        xCoord = float(row[0])
        yCoord = float(row[1])
        zCoord = float(row[2])
        comFile.write(" {:3}{:26.8f}{:14.8f}{:14.8f}".format(atomName, xCoord, yCoord, zCoord))
        comFile.write("\n")

    comFile.write("\n")
    for i in range(1, len(rows) + 1):
        bondString = " " + str(i)
        for bond in bonds:
            if str(i) == bond[0]:
                bondString += " " + bond[1] + " " + str(float(bond[2]))
        comFile.write(bondString + "\n")
    if jobOptions != "":
        comFile.write("\n")
        comFile.write(jobOptions + "\n")

    comFile.write("\n")

    comFile.close()

    print("Wrote " + sdfFileName[0:-4] + sdfFileName[-4:].replace(".sdf", "_" + str(frameNumber) + suffix + ".com"))


main()