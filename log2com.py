import os
import sys


def main():
    if len(sys.argv) == 2:
        if sys.argv[1][-4:] == ".log" or sys.argv[1] == "-all":
            takeInput(sys.argv[1])
        else:
            print("Enter a valid log filename or -all")
    elif len(sys.argv) == 1:
        print("<<<<<<<<<<<<<<<<<<<< Welcome to log2com! >>>>>>>>>>>>>>>>>>>>")
        print("\nTo use log2com, run it with a filename or -all as an argument")
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
            suffixPrompt = "Enter a suffix so we do not overwrite something\n>>>> "

    jobKeywords = input("Paste job keywords  eg. '# opt=(calcfc,ts,noeigen) freq=noraman 6-31g(d) scf=qc'\n>>>> ").replace("# ", "").strip()

    jobOptions = input("Paste job options with <br> separating new lines  eg. 'B 1 3 F<br><br>C H O P S N 0<br>6-31G(d)'\n>>>> ").replace("<br>", "\n")

    if argument == "-all":
        doAll(suffix, jobKeywords, jobOptions)
    else:
        log2com(argument, suffix, jobKeywords, jobOptions)

def doAll(suffix, jobKeywords, jobOptions):
    filenames = os.listdir()

    logFileNames = []

    for filename in filenames:
        if filename[-4:] == ".log":
            logFileNames.append(filename)

    for logFileName in logFileNames:
        log2com(logFileName, suffix, jobKeywords, jobOptions)


def log2com(logFileName, suffix, jobKeywords, jobOptions):
    try:
        charge, multiplicity, rows = logReader(logFileName)
    except:
        print("Could not read " + logFileName)
    else:
        try:
            comWriter(logFileName, suffix, jobKeywords, charge, multiplicity, rows, jobOptions)
        except:
            print("Coud not write " + logFileName[0:-4] + logFileName[-4:].replace(".log", suffix + ".com"))


def logReader(logFileName):
    logFile = open(logFileName)
    lines = logFile.readlines()

    currentIndex = 0

    for line in lines:
        if line.strip() == "Standard orientation:":
            coordTitleIndex = currentIndex
        if line.strip() == "Symbolic Z-matrix:":
            stoichIndex = currentIndex + 1
        currentIndex += 1

    stoichLine = lines[stoichIndex].strip().split()

    charge = stoichLine[2]
    multiplicity = stoichLine[5]

    coordIndex = coordTitleIndex + 5
    rows = []

    for line in lines[coordIndex:]:
        if "--" in line:
            break
        else:
            row = line.strip().split()
            rows.append(row)

    logFile.close()

    return charge, multiplicity, rows


def comWriter(logFileName, suffix, jobKeywords, charge, multiplicity, rows, jobOptions):
    elementDict = {'1': 'H', '2': 'He', '3': 'Li', '4': 'Be', '5': 'B', '6': 'C', '7': 'N', '8': 'O', '9': 'F',
                   '10': 'Ne', '11': 'Na', '12': 'Mg', '13': 'Al', '14': 'Si', '15': 'P', '16': 'S', '17': 'Cl',
                   '18': 'Ar', '19': 'K', '20': 'Ca', '21': 'Sc', '22': 'Ti', '23': 'V', '24': 'Cr', '25': 'Mn',
                   '26': 'Fe', '27': 'Co', '28': 'Ni', '29': 'Cu', '30': 'Zn', '31': 'Ga', '32': 'Ge', '33': 'As',
                   '34': 'Se', '35': 'Br', '36': 'Kr', '37': 'Rb', '38': 'Sr', '39': 'Y', '40': 'Zr', '41': 'Nb',
                   '42': 'Mo', '43': 'Tc', '44': 'Ru', '45': 'Rh', '46': 'Pd', '47': 'Ag', '48': 'Cd', '49': 'In',
                   '50': 'Sn', '51': 'Sb', '52': 'Te', '53': 'I', '54': 'Xe', '55': 'Cs', '56': 'Ba', '57': 'La',
                   '58': 'Ce', '59': 'Pr', '60': 'Nd', '61': 'Pm', '62': 'Sm', '63': 'Eu', '64': 'Gd', '65': 'Tb',
                   '66': 'Dy', '67': 'Ho', '68': 'Er', '69': 'Tm', '70': 'Yb', '71': 'Lu', '72': 'Hf', '73': 'Ta',
                   '74': 'W', '75': 'Re', '76': 'Os', '77': 'Ir', '78': 'Pt', '79': 'Au', '80': 'Hg', '81': 'Tl',
                   '82': 'Pb', '83': 'Bi', '84': 'Po', '85': 'At', '86': 'Rn', '87': 'Fr', '88': 'Ra', '89': 'Ac',
                   '90': 'Th', '91': 'Pa', '92': 'U', '93': 'Np', '94': 'Pu', '95': 'Am', '96': 'Cm', '97': 'Bk',
                   '98': 'Cf', '99': 'Es', '100': 'Fm', '101': 'Md', '102': 'No', '103': 'Lr', '104': 'Rf', '105': 'Db',
                   '106': 'Sg', '107': 'Bh', '108': 'Hs', '109': 'Mt', '110': 'Ds', '111': 'Rg', '112': 'Cp',
                   '113': 'Uut', '114': 'Uuq', '115': 'Uup', '116': 'Uuh', '117': 'Uus', '118': 'Uuo'}

    comFile = open(logFileName[0:-4] + logFileName[-4:].replace(".log", suffix + ".com"), "w")

    comFile.write("%nprocshared=32\n%mem=8000MB\n")
    comFile.write("%chk=" + logFileName[0:-4] + logFileName[-4:].replace(".log", suffix + ".chk\n"))
    comFile.write("# " + jobKeywords + "\n")
    comFile.write("\nTitle Card Required\n")

    comFile.write("\n")
    comFile.write(charge + " " + multiplicity + "\n")
    for row in rows:
        atomName = elementDict[row[1]]
        xCoord = float(row[3])
        yCoord = float(row[4])
        zCoord = float(row[5])
        comFile.write(" {:3}{:26.8f}{:14.8f}{:14.8f}".format(atomName, xCoord, yCoord, zCoord))
        comFile.write("\n")

    if jobOptions != "":
        comFile.write("\n")
        comFile.write(jobOptions + "\n")

    comFile.write("\n")

    comFile.close()

    print("Wrote " + logFileName[0:-4] + logFileName[-4:].replace(".log", suffix + ".com"))


main()
