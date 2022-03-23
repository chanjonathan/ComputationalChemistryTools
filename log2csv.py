import os

def main():
    doAll()


def doAll():
    filenames = os.listdir()

    logFileNames = []

    for filename in filenames:
        if filename.endswith(".log"):
            logFileNames.append(filename)

    logFileNames.sort(key=lambda f: int(''.join(filter(str.isdigit, f)) or -1))

    for logFileName in logFileNames:
        log2csv(logFileName)


def log2csv(logFileName):
    try:
        electronicEnergy, thermalCorrection = logReader(logFileName)
    except:
        print("Could not read " + logFileName)
    else:
        try:
            csvWriter(logFileName, electronicEnergy, thermalCorrection)
            print("Wrote " + logFileName[0:-4] + " into csv")
        except:
            print("Coud not write " + logFileName[:-4] + " into csv")


def logReader(logFileName):
    logFile = open(logFileName)

    electronicEnergy = False
    thermalCorrection = False

    for line in logFile:
        if "Thermal correction to Gibbs Free Energy" in line:
            thermalCorrection = line.strip().split()[6]
        if "SCF Done:" in line:
            electronicEnergy = line.strip().split()[4]

    logFile.close()

    for variable in [electronicEnergy, thermalCorrection]:
        if variable is not False:
            break
    else:
        raise Exception


    return electronicEnergy, thermalCorrection


def csvWriter(logFileName, electronicEnergy, thermalCorrection):
    global startedWriting

    if not startedWriting:
        csvFile = open("energies.csv", "w")
        csvFile.write("File, Electronic Energy, Thermal Correction\n")
        print("Writing to energies.csv")
        csvFile.close()
        startedWriting = True

    if electronicEnergy is False:
        electronicEnergy = ""
    if thermalCorrection is False:
        thermalCorrection = ""

    csvFile = open("energies.csv", "a")
    csvFile.write(logFileName[0:-4] + ", " + electronicEnergy + ", " + thermalCorrection + "\n")

    csvFile.close()


startedWriting = False

main()
