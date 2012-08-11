from PIL import *
from PIL import Image
import sys, getopt, os

class AutotileExpander:

    def printHelp(self):
        pass

    def _initializeLocations(self):
        self._minitiles, self._minitilePosition, self._minitileType = dict(NO=dict(), NE=dict(), SO=dict(), SE=dict()), dict(), dict()
        self._minitileTypeDependingOnGroup, self._minitilePositionGroup = dict(), dict()
        #Liste des types et directions possibles
        self._minitileType, self._minitilePosition = ["Normal", "Angle int", "Angle ext", "BordHori", "BordVerti", "Présentation"], ["NO", "NE", "SO", "SE"]
        #Direction selon la position au sein du groupe
        self._minitilePositionGroup[0, 0], self._minitilePositionGroup[16, 0], self._minitilePositionGroup[0, 16], self._minitilePositionGroup[16, 16] = "NO", "NE", "SO", "SE"
        #Type des minitiles selon leurs groupes et directions
        self._minitileTypeDependingOnGroup[0, 0, "NO"] = "Présentation"
        self._minitileTypeDependingOnGroup[0, 0, "NE"] = "Présentation"
        self._minitileTypeDependingOnGroup[0, 0, "SO"] = "Présentation"
        self._minitileTypeDependingOnGroup[0, 0, "SE"] = "Présentation"
        self._minitileTypeDependingOnGroup[32, 0, "NO"] = "Angle int"
        self._minitileTypeDependingOnGroup[32, 0, "NE"] = "Angle int"
        self._minitileTypeDependingOnGroup[32, 0, "SO"] = "Angle int"
        self._minitileTypeDependingOnGroup[32, 0, "SE"] = "Angle int"
        self._minitileTypeDependingOnGroup[0, 32, "NO"] = "Angle ext"
        self._minitileTypeDependingOnGroup[32, 32, "NE"] = "Angle ext"
        self._minitileTypeDependingOnGroup[0, 64, "SO"] = "Angle ext"
        self._minitileTypeDependingOnGroup[32, 64, "SE"] = "Angle ext"
        self._minitileTypeDependingOnGroup[32, 32, "NO"] = "BordHori"
        self._minitileTypeDependingOnGroup[0, 32, "NE"] = "BordHori"
        self._minitileTypeDependingOnGroup[32, 64, "SO"] = "BordHori"
        self._minitileTypeDependingOnGroup[0, 64, "SE"] = "BordHori"
        self._minitileTypeDependingOnGroup[0, 64, "NO"] = "BordVerti"
        self._minitileTypeDependingOnGroup[32, 64, "NE"] = "BordVerti"
        self._minitileTypeDependingOnGroup[0, 32, "SO"] = "BordVerti"
        self._minitileTypeDependingOnGroup[32, 32, "SE"] = "BordVerti"
        self._minitileTypeDependingOnGroup[32, 64, "NO"] = "Normal"
        self._minitileTypeDependingOnGroup[0, 64, "NE"] = "Normal"
        self._minitileTypeDependingOnGroup[0, 32, "SE"] = "Normal"
        self._minitileTypeDependingOnGroup[32, 32, "SO"] = "Normal"

    def _makeAutotile(self, *types):
        autotileSurface = Image.new("RGB", (32,32))
        minitileAbs, minitileOrd, i = 0, 0, 0
        while minitileOrd < 32:
            minitileAbs = 0
            while minitileAbs < 32:
                minitilePosition = self._minitilePositionGroup[minitileAbs, minitileOrd]
                minitileType = types[i]
                minitileSurface = self._minitiles[minitilePosition][minitileType]
                autotileSurface.paste(minitileSurface, (minitileAbs, minitileOrd))
                i += 1
                minitileAbs += 16
            minitileOrd += 16
        return autotileSurface

    def expandAutotile(self, autotileFilename):
        self._imageAutotile = Image.open(autotileFilename)
        self._initializeLocations()
        #### First we find the minitiles, then we use their types and position to sort them
        groupAbs, groupOrd = 0, 0
        while groupOrd < self._imageAutotile.size[1]: #We run through the groups of minitiles
            groupAbs = 0
            while groupAbs < self._imageAutotile.size[0]:
                minitileAbs, minitileOrd = 0, 0
                while minitileOrd < 32: #We run through the minitiles
                    minitileAbs = 0
                    while minitileAbs < 32:
                        minitilePosition = self._minitilePositionGroup[minitileAbs, minitileOrd]
                        minitileType = self._minitileTypeDependingOnGroup[groupAbs, groupOrd, minitilePosition]
                        self._minitiles[minitilePosition][minitileType] = self._imageAutotile.crop((groupAbs+minitileAbs, groupOrd+minitileOrd, groupAbs+minitileAbs+16, groupOrd+minitileOrd+16))
                        minitileAbs += 16
                    minitileOrd += 16
                groupAbs += 32
            groupOrd += 32
        ##### We define the types composing the 48 autotiles
        autotilesSurfaces = dict()
        autotilesSurfaces[0] = self._makeAutotile("Normal", "Normal", "Normal", "Normal")
        autotilesSurfaces[1] = self._makeAutotile("Angle int", "Normal", "Normal", "Normal")
        autotilesSurfaces[2] = self._makeAutotile("Normal", "Angle int", "Normal", "Normal")
        autotilesSurfaces[3] = self._makeAutotile("Angle int", "Angle int", "Normal", "Normal")
        autotilesSurfaces[4] = self._makeAutotile("Normal", "Normal", "Normal", "Angle int")
        autotilesSurfaces[5] = self._makeAutotile("Angle int", "Normal", "Normal", "Angle int")
        autotilesSurfaces[6] = self._makeAutotile("Normal", "Angle int", "Normal", "Angle int")
        autotilesSurfaces[7] = self._makeAutotile("Angle int", "Angle int", "Normal", "Angle int")
        autotilesSurfaces[8] = self._makeAutotile("Normal", "Normal", "Angle int", "Normal")
        autotilesSurfaces[9] = self._makeAutotile("Angle int", "Normal", "Angle int", "Normal")
        autotilesSurfaces[10] = self._makeAutotile("Normal", "Angle int", "Angle int", "Normal")
        autotilesSurfaces[11] = self._makeAutotile("Angle int", "Angle int", "Angle int", "Normal")
        autotilesSurfaces[12] = self._makeAutotile("Normal", "Normal", "Angle int", "Angle int")
        autotilesSurfaces[13] = self._makeAutotile("Angle int", "Normal", "Angle int", "Angle int")
        autotilesSurfaces[14] = self._makeAutotile("Normal", "Angle int", "Angle int", "Angle int")
        autotilesSurfaces[15] = self._makeAutotile("Angle int", "Angle int", "Angle int", "Angle int")
        autotilesSurfaces[16] = self._makeAutotile("BordVerti", "Normal", "BordVerti", "Normal")
        autotilesSurfaces[17] = self._makeAutotile("BordVerti", "Angle int", "BordVerti", "Normal")
        autotilesSurfaces[18] = self._makeAutotile("BordVerti", "Normal", "BordVerti", "Angle int")
        autotilesSurfaces[19] = self._makeAutotile("BordVerti", "Angle int", "BordVerti", "Angle int")
        autotilesSurfaces[20] = self._makeAutotile("BordHori", "BordHori", "Normal", "Normal")
        autotilesSurfaces[21] = self._makeAutotile("BordHori", "BordHori", "Normal", "Angle int")
        autotilesSurfaces[22] = self._makeAutotile("BordHori", "BordHori", "Angle int", "Normal")
        autotilesSurfaces[23] = self._makeAutotile("BordHori", "BordHori", "Angle int", "Angle int")
        autotilesSurfaces[24] = self._makeAutotile("Normal", "BordVerti", "Normal", "BordVerti")
        autotilesSurfaces[25] = self._makeAutotile("Normal", "BordVerti", "Angle int", "BordVerti")
        autotilesSurfaces[26] = self._makeAutotile("Angle int", "BordVerti", "Normal", "BordVerti")
        autotilesSurfaces[27] = self._makeAutotile("Angle int", "BordVerti", "Angle int", "BordVerti")
        autotilesSurfaces[28] = self._makeAutotile("Normal", "Normal", "BordHori", "BordHori")
        autotilesSurfaces[29] = self._makeAutotile("Angle int", "Normal", "BordHori", "BordHori")
        autotilesSurfaces[30] = self._makeAutotile("Normal", "Angle int", "BordHori", "BordHori")
        autotilesSurfaces[31] = self._makeAutotile("Angle int", "Angle int", "BordHori", "BordHori")
        autotilesSurfaces[32] = self._makeAutotile("BordVerti", "BordVerti", "BordVerti", "BordVerti")
        autotilesSurfaces[33] = self._makeAutotile("BordHori", "BordHori", "BordHori", "BordHori")
        autotilesSurfaces[34] = self._makeAutotile("Angle ext", "BordHori", "BordVerti", "Normal")
        autotilesSurfaces[35] = self._makeAutotile("Angle ext", "BordHori", "BordVerti", "Angle int")
        autotilesSurfaces[36] = self._makeAutotile("BordHori", "Angle ext", "Normal", "BordVerti")
        autotilesSurfaces[37] = self._makeAutotile("BordHori", "Angle ext", "Angle int", "BordVerti")
        autotilesSurfaces[38] = self._makeAutotile("Normal", "BordVerti", "BordHori", "Angle ext")
        autotilesSurfaces[39] = self._makeAutotile("Angle int", "BordVerti", "BordHori", "Angle ext")
        autotilesSurfaces[40] = self._makeAutotile("BordVerti", "Normal", "Angle ext", "BordHori")
        autotilesSurfaces[41] = self._makeAutotile("BordVerti", "Angle int", "Angle ext", "BordHori")
        autotilesSurfaces[42] = self._makeAutotile("Présentation", "Présentation", "BordVerti", "BordVerti")
        autotilesSurfaces[43] = self._makeAutotile("Présentation", "BordHori", "Présentation", "BordHori")
        autotilesSurfaces[44] = self._makeAutotile("BordVerti", "BordVerti", "Présentation", "Présentation")
        autotilesSurfaces[45] = self._makeAutotile("BordHori", "Présentation", "BordHori", "Présentation")
        autotilesSurfaces[46] = self._makeAutotile("Présentation", "Présentation", "Présentation", "Présentation")
        autotilesSurfaces[47] = self._makeAutotile("Présentation", "Présentation", "Présentation", "Présentation")
        ##### We make the final surface
        autotileAbs, autotileOrd, i, self._expandedAutotile = 0, 0, 0, Image.new("RGB", (32*8, 32*6))
        while autotileOrd < 32 * 6:
            autotileAbs = 0
            while autotileAbs < 32 * 8:
                self._expandedAutotile.paste(autotilesSurfaces[i], (autotileAbs, autotileOrd))
                i += 1
                autotileAbs += 32
            autotileOrd += 32
        return self._expandedAutotile

    def _printVerbose(self, message):
        if self._verbose is True:
            print(message)
            
    def _checkArguments(self, step):
        if step == "Input exists":
            if os.path.exists(self._inputFilename) is False:
                print("The input autotile \"{0}\" does not exist.".format(self._inputFilename))
                raise SystemExit
        elif step == "Input type":
            if ".png" not in self._inputFilename.lower() and self._askConfirmation is True:
                answerIgnoreType = self._interacter.askString("The input autotile does not seem to be a PNG image. Continue? (y/N)")
                if answerIgnoreType.lower().split(" ")[0] != "y":
                    print("Fine, just choose a PNG next time.")
                    raise SystemExit
                else:
                    print("Ok, let's continue if you want.")
        elif step == "Input validity":
            try:
                image = Image.open(self._inputFilename)
            except IOError:
                print("The input autotile \"{0}\" is not a valid PNG image.".format(self._inputFilename))
                raise SystemExit
        elif step == "Input size":
            image = Image.open(self._inputFilename)
            if image.size != (64, 96):
                print("The input autotile \"{0}\" does not have the right size.\nIt must be 64 * 96 pixels wide. Please refer to tileA2 formatting from RPG Maker VX / VX Ace.".format(self._inputFilename))
                raise SystemExit
        elif step == "Output without extension":
            if self._outputFilename.lower().endswith(".png") is False and self._askConfirmation is True:
                answerIgnoreNoExtension = self._interacter.askString("The output file \"{0}\" does not a a .png extension. Shall I add the extension? (Y/n)".format(self._outputFilename))
                if answerIgnoreNoExtension.lower().split(" ")[0] == "y":
                    self._outputFilename += ".png"
                    print("Ok, I'm adding the extension. The output file is now \"{0}\".".format(self._outputFilename))
                else:
                    print("Ok, I won't do anything about the extension.")
        elif step == "Output already exists":
            if os.path.exists(self._outputFilename) == True and self._askConfirmation is True:
                answerIgnoreExistingOutput = self._interacter.askString("The output file \"{0}\" already exists. Do you want to overwrite it? (y/N)".format(self._outputFilename))
                if answerIgnoreExistingOutput.lower().split(" ")[0] != "y":
                    print("Ok, I'm stopping here.")
                    raise SystemExit
                else:
                    print("Fine, I'll overwrite the existing file.")

    def launchScript(self, inputFilename, outputFilename, askConfirmation, verbose, testSteps=["Input exists", "Input type", "Input validity", "Input size", "Output without extension", "Output already exists"]):
        self._inputFilename, self._outputFilename, self._askConfirmation, self._verbose = inputFilename.replace("\\", "/"), outputFilename.replace("\\", "/"), askConfirmation, verbose
        self._interacter = Interacter()
        i = True
        while i < len(testSteps):
            self._checkArguments(testSteps[i])
            i += 1
        self.expandAutotile(self._inputFilename)
        self._expandedAutotile.save(self._outputFilename, "PNG")
        self._printVerbose("Successfully created the autotile \"{0}\"!".format(self._outputFilename))

if __name__ == "__main__":
    autotileExpander = AutotileExpander()
    shortOptions, longOptions = "o:fhv", ["output=", "help", "verbose", "force"]
    try:
        optionsUsed, argumentsUsed = getopt.getopt(sys.argv[1:], shortOptions, longOptions)
    except getopt.GetoptError as error:
        print(error)
        autotileExpander.printHelp()
        raise SystemExit
    outputFile, verbose, askConfirmation = "expandedAutotile.png", False, True
    for option, value in optionsUsed:
        if option in ("-h", "--help"):
            autotileExpander.printHelp()
            raise SystemExit
        elif option in ("-v", "--verbose"):
            verbose = True
        elif option in ("-f", "--force"):
            askConfirmation = False
        elif option in ("-o", "--output"):
            outputFile = value
    if len(argumentsUsed) == 1:
        inputFile = argumentsUsed[0]
        sys.path.append(os.path.abspath("../"))
        from interacter import *
        autotileExpander.launchScript(inputFile, outputFile, askConfirmation, verbose)
    else:
        if len(argumentsUsed) > 1:
            print(argumentsUsed, verbose, sys.argv[1:])
            print("Error: Too many input autotiles. There must only be one (one argument).")
        elif len(argumentsUsed) < 1:
            print("Error: No input autotile specified.")
        autotileExpander.printHelp()
        raise SystemExit
