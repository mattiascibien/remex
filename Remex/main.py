import xml.dom.minidom
from PIL import Image as ImagePIL
from PIL import ImageTk
from os import path
from argparse import ArgumentParser
from interacter import *

class Script:
    def __init__(self, inputFileDescription, outputFileExtenion):
        self._inputFileDescription, self._outputFileExtension = inputFileDescription, outputFileExtenion

    def _printVerbose(self, message):
        if self._verbose is True:
            print(message)
            
    def _checkInputValidity(self):
        pass

    def _checkInputSize(self):
        pass
            
    def _checkArguments(self, step):
        if step == "Input exists":
            if path.exists(self._inputFilename) is False:
                print("The input {0} \"{1}\" does not exist.".format(self._inputFileDescription, self._inputFilename))
                raise SystemExit
        elif step == "Input validity":
            self._checkInputValidity()
        elif step == "Input size":
            self._checkInputSize()
        elif step == "Output without extension":
            if self._outputFilename.lower().endswith(self._outputFileExtension) is False and self._askConfirmation is True:
                answerIgnoreNoExtension = self._interacter.askString("The output file \"{0}\" does not have a {1} extension. Shall I add the extension? (Y/n)".format(self._outputFilename, self._outputFileExtension))
                if answerIgnoreNoExtension.lower().split(" ")[0] == "y":
                    self._outputFilename += self._outputFileExtension
                    print("Ok, I'm adding the extension. The output file is now \"{0}\".".format(self._outputFilename))
                else:
                    print("Ok, I won't do anything about the extension.")
        elif step == "Output already exists":
            if path.exists(self._outputFilename) == True and self._askConfirmation is True:
                answerIgnoreExistingOutput = self._interacter.askString("The output file \"{0}\" already exists. Do you want to overwrite it? (y/N)".format(self._outputFilename))
                if answerIgnoreExistingOutput.lower().split(" ")[0] != "y":
                    print("Correct, I'm stopping here.")
                    raise SystemExit
                else:
                    print("Fine, I'll overwrite the existing file.")

    def launchScript(self, inputFilename, outputFilename, askConfirmation, verbose, testSteps=["Input exists", "Input validity", "Input size", "Output without extension", "Output already exists"]):
        self._inputFilename, self._outputFilename, self._askConfirmation, self._verbose = inputFilename.replace("\\", "/"), outputFilename.replace("\\", "/"), askConfirmation, verbose
        self._interacter = Interacter()
        i = True
        while i < len(testSteps):
            self._checkArguments(testSteps[i])
            i += 1

class AutotileExpander(Script):

    def _initializeLocations(self):
        self._minitiles, self._minitilePosition, self._minitileType = dict(NO=dict(), NE=dict(), SO=dict(), SE=dict()), dict(), dict()
        self._minitileTypeDependingOnGroup, self._minitilePositionGroup = dict(), dict()
        #List of the possible types and directions
        self._minitileType, self._minitilePosition = ["Normal", "External angle", "Internal angle", "HorizontalEdge", "VerticalEdge", "Showcase"], ["NO", "NE", "SO", "SE"]
        #Directions depending on the position in the group
        self._minitilePositionGroup[0, 0], self._minitilePositionGroup[16, 0], self._minitilePositionGroup[0, 16], self._minitilePositionGroup[16, 16] = "NO", "NE", "SO", "SE"
        #Types of the minitiles depending on their groups and directions
        self._minitileTypeDependingOnGroup[0, 0, "NO"] = "Showcase"
        self._minitileTypeDependingOnGroup[0, 0, "NE"] = "Showcase"
        self._minitileTypeDependingOnGroup[0, 0, "SO"] = "Showcase"
        self._minitileTypeDependingOnGroup[0, 0, "SE"] = "Showcase"
        self._minitileTypeDependingOnGroup[32, 0, "NO"] = "External angle"
        self._minitileTypeDependingOnGroup[32, 0, "NE"] = "External angle"
        self._minitileTypeDependingOnGroup[32, 0, "SO"] = "External angle"
        self._minitileTypeDependingOnGroup[32, 0, "SE"] = "External angle"
        self._minitileTypeDependingOnGroup[0, 32, "NO"] = "Internal angle"
        self._minitileTypeDependingOnGroup[32, 32, "NE"] = "Internal angle"
        self._minitileTypeDependingOnGroup[0, 64, "SO"] = "Internal angle"
        self._minitileTypeDependingOnGroup[32, 64, "SE"] = "Internal angle"
        self._minitileTypeDependingOnGroup[32, 32, "NO"] = "HorizontalEdge"
        self._minitileTypeDependingOnGroup[0, 32, "NE"] = "HorizontalEdge"
        self._minitileTypeDependingOnGroup[32, 64, "SO"] = "HorizontalEdge"
        self._minitileTypeDependingOnGroup[0, 64, "SE"] = "HorizontalEdge"
        self._minitileTypeDependingOnGroup[0, 64, "NO"] = "VerticalEdge"
        self._minitileTypeDependingOnGroup[32, 64, "NE"] = "VerticalEdge"
        self._minitileTypeDependingOnGroup[0, 32, "SO"] = "VerticalEdge"
        self._minitileTypeDependingOnGroup[32, 32, "SE"] = "VerticalEdge"
        self._minitileTypeDependingOnGroup[32, 64, "NO"] = "Normal"
        self._minitileTypeDependingOnGroup[0, 64, "NE"] = "Normal"
        self._minitileTypeDependingOnGroup[0, 32, "SE"] = "Normal"
        self._minitileTypeDependingOnGroup[32, 32, "SO"] = "Normal"

    def _makeAutotile(self, *types):
        autotileSurface = ImagePIL.new("RGB", (32,32))
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
        self._imageAutotile = ImagePIL.open(autotileFilename)
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
        autotilesSurfaces[1] = self._makeAutotile("External angle", "Normal", "Normal", "Normal")
        autotilesSurfaces[2] = self._makeAutotile("Normal", "External angle", "Normal", "Normal")
        autotilesSurfaces[3] = self._makeAutotile("External angle", "External angle", "Normal", "Normal")
        autotilesSurfaces[4] = self._makeAutotile("Normal", "Normal", "Normal", "External angle")
        autotilesSurfaces[5] = self._makeAutotile("External angle", "Normal", "Normal", "External angle")
        autotilesSurfaces[6] = self._makeAutotile("Normal", "External angle", "Normal", "External angle")
        autotilesSurfaces[7] = self._makeAutotile("External angle", "External angle", "Normal", "External angle")
        autotilesSurfaces[8] = self._makeAutotile("Normal", "Normal", "External angle", "Normal")
        autotilesSurfaces[9] = self._makeAutotile("External angle", "Normal", "External angle", "Normal")
        autotilesSurfaces[10] = self._makeAutotile("Normal", "External angle", "External angle", "Normal")
        autotilesSurfaces[11] = self._makeAutotile("External angle", "External angle", "External angle", "Normal")
        autotilesSurfaces[12] = self._makeAutotile("Normal", "Normal", "External angle", "External angle")
        autotilesSurfaces[13] = self._makeAutotile("External angle", "Normal", "External angle", "External angle")
        autotilesSurfaces[14] = self._makeAutotile("Normal", "External angle", "External angle", "External angle")
        autotilesSurfaces[15] = self._makeAutotile("External angle", "External angle", "External angle", "External angle")
        autotilesSurfaces[16] = self._makeAutotile("VerticalEdge", "Normal", "VerticalEdge", "Normal")
        autotilesSurfaces[17] = self._makeAutotile("VerticalEdge", "External angle", "VerticalEdge", "Normal")
        autotilesSurfaces[18] = self._makeAutotile("VerticalEdge", "Normal", "VerticalEdge", "External angle")
        autotilesSurfaces[19] = self._makeAutotile("VerticalEdge", "External angle", "VerticalEdge", "External angle")
        autotilesSurfaces[20] = self._makeAutotile("HorizontalEdge", "HorizontalEdge", "Normal", "Normal")
        autotilesSurfaces[21] = self._makeAutotile("HorizontalEdge", "HorizontalEdge", "Normal", "External angle")
        autotilesSurfaces[22] = self._makeAutotile("HorizontalEdge", "HorizontalEdge", "External angle", "Normal")
        autotilesSurfaces[23] = self._makeAutotile("HorizontalEdge", "HorizontalEdge", "External angle", "External angle")
        autotilesSurfaces[24] = self._makeAutotile("Normal", "VerticalEdge", "Normal", "VerticalEdge")
        autotilesSurfaces[25] = self._makeAutotile("Normal", "VerticalEdge", "External angle", "VerticalEdge")
        autotilesSurfaces[26] = self._makeAutotile("External angle", "VerticalEdge", "Normal", "VerticalEdge")
        autotilesSurfaces[27] = self._makeAutotile("External angle", "VerticalEdge", "External angle", "VerticalEdge")
        autotilesSurfaces[28] = self._makeAutotile("Normal", "Normal", "HorizontalEdge", "HorizontalEdge")
        autotilesSurfaces[29] = self._makeAutotile("External angle", "Normal", "HorizontalEdge", "HorizontalEdge")
        autotilesSurfaces[30] = self._makeAutotile("Normal", "External angle", "HorizontalEdge", "HorizontalEdge")
        autotilesSurfaces[31] = self._makeAutotile("External angle", "External angle", "HorizontalEdge", "HorizontalEdge")
        autotilesSurfaces[32] = self._makeAutotile("VerticalEdge", "VerticalEdge", "VerticalEdge", "VerticalEdge")
        autotilesSurfaces[33] = self._makeAutotile("HorizontalEdge", "HorizontalEdge", "HorizontalEdge", "HorizontalEdge")
        autotilesSurfaces[34] = self._makeAutotile("Internal angle", "HorizontalEdge", "VerticalEdge", "Normal")
        autotilesSurfaces[35] = self._makeAutotile("Internal angle", "HorizontalEdge", "VerticalEdge", "External angle")
        autotilesSurfaces[36] = self._makeAutotile("HorizontalEdge", "Internal angle", "Normal", "VerticalEdge")
        autotilesSurfaces[37] = self._makeAutotile("HorizontalEdge", "Internal angle", "External angle", "VerticalEdge")
        autotilesSurfaces[38] = self._makeAutotile("Normal", "VerticalEdge", "HorizontalEdge", "Internal angle")
        autotilesSurfaces[39] = self._makeAutotile("External angle", "VerticalEdge", "HorizontalEdge", "Internal angle")
        autotilesSurfaces[40] = self._makeAutotile("VerticalEdge", "Normal", "Internal angle", "HorizontalEdge")
        autotilesSurfaces[41] = self._makeAutotile("VerticalEdge", "External angle", "Internal angle", "HorizontalEdge")
        autotilesSurfaces[42] = self._makeAutotile("Showcase", "Showcase", "VerticalEdge", "VerticalEdge")
        autotilesSurfaces[43] = self._makeAutotile("Showcase", "HorizontalEdge", "Showcase", "HorizontalEdge")
        autotilesSurfaces[44] = self._makeAutotile("VerticalEdge", "VerticalEdge", "Showcase", "Showcase")
        autotilesSurfaces[45] = self._makeAutotile("HorizontalEdge", "Showcase", "HorizontalEdge", "Showcase")
        autotilesSurfaces[46] = self._makeAutotile("Showcase", "Showcase", "Showcase", "Showcase")
        autotilesSurfaces[47] = self._makeAutotile("Showcase", "Showcase", "Showcase", "Showcase")
        ##### We make the final surface by blitting our individual surfaces
        autotileAbs, autotileOrd, i, self._expandedAutotile = 0, 0, 0, ImagePIL.new("RGB", (32*8, 32*6))
        while autotileOrd < 32 * 6:
            autotileAbs = 0
            while autotileAbs < 32 * 8:
                self._expandedAutotile.paste(autotilesSurfaces[i], (autotileAbs, autotileOrd))
                i += 1
                autotileAbs += 32
            autotileOrd += 32
        return self._expandedAutotile
            
    def _checkInputValidity(self):
            try:
                image = ImagePIL.open(self._inputFilename)
            except IOError:
                print("The input autotile \"{0}\" is not a valid PNG image.".format(self._inputFilename))
                raise SystemExit

    def _checkInputSize(self):
            image = ImagePIL.open(self._inputFilename)
            if image.size != (64, 96):
                print("The input autotile \"{0}\" does not have the right size.\nIt must be 64 * 96 pixels wide. Please refer to tileA2 formatting from RPG Maker VX / VX Ace.".format(self._inputFilename))
                raise SystemExit

    def launchScript(self, inputFilename, outputFilename, askConfirmation, verbose, testSteps=["Input exists", "Input validity", "Input size", "Output without extension", "Output already exists"]):
        super().launchScript(inputFilename, outputFilename, askConfirmation, verbose, testSteps=testSteps)
        self.expandAutotile(self._inputFilename)
        self._expandedAutotile.save(self._outputFilename, "PNG")
        self._printVerbose("Successfully created the autotile \"{0}\"!".format(self._outputFilename))

class TilesetGenerator(Script):

    def _checkInputValidity(self):
            try:
                image = ImagePIL.open(self._inputFilename)
            except IOError:
                print("The input expanded autotile \"{0}\" is not a valid PNG image.".format(self._inputFilename))
                raise SystemExit

    def _checkInputSize(self):
            image = ImagePIL.open(self._inputFilename)
            if image.size != (256, 192):
                print("The input expanded autotile \"{0}\" does not have the right size.\nIt must be 256 * 192 pixels wide. Please expand an autotile from RPG Maker VX / VX Ace with this program first.".format(self._inputFilename))
                raise SystemExit

    def makeXML(self, inputFilename, outputFilename="Tileset"):
        self._inputFilename = inputFilename
        mainXML = xml.dom.minidom.getDOMImplementation().createDocument(None, "tileset", None)
        tilesetXML = mainXML.documentElement
        tilesetName = path.basename(outputFilename)
        if tilesetName.lower().endswith(".tsx") is True:
            tilesetName = tilesetName[: len(tilesetName) - 4]
        tilesetXML.setAttribute("name", tilesetName)
        tilesetXML.setAttribute("tilewidth", "32")
        tilesetXML.setAttribute("tileheight", "32")
        imageXML = mainXML.createElement("image")
        imageXML.setAttribute("source", path.abspath(self._inputFilename).replace("\\", "/"))
        imageXML.setAttribute("trans", "ffffff")
        width, height = 256, 192
        imageXML.setAttribute("width", str(width))
        imageXML.setAttribute("height", str(height))
        tilesetXML.appendChild(imageXML)
        return mainXML

    def launchScript(self, inputFilename, outputFilename, askConfirmation, verbose, testSteps=["Input exists", "Input validity", "Input size", "Output without extension", "Output already exists"]):
        super().launchScript(inputFilename, outputFilename, askConfirmation, verbose, testSteps=testSteps)
        xmlData = self.makeXML(inputFilename, outputFilename=outputFilename)
        with open(self._outputFilename, "w") as outputFile:
            xmlData.writexml(outputFile, addindent="  ", newl="\n", encoding="UTF-8")
        xmlData.unlink()

class RuleMaker(Script):

    def launchScript(self, inputFilename, outputFilename, askConfirmation, verbose, testSteps=["Input exists", "Input validity", "Output without extension", "Output already exists"]):
        super().launchScript(inputFilename, outputFilename, askConfirmation, verbose, testSteps=testSteps)
        xmlData = self.makeXML(inputFilename, outputFilename=outputFilename)
        with open(self._outputFilename, "w") as outputFile:
            xmlData.writexml(outputFile, addindent="  ", newl="\n", encoding="UTF-8")
        xmlData.unlink()

if __name__ == "__main__":
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(title="Commands", description="The command to execute", dest="command")
    expandSubCommand = subparsers.add_parser("expand", help="Autotile Expander. Expands an autotile from RPG Maker VX or VX Ace into a grid containing all the possible cases.")
    expandSubCommand.add_argument("-o", "--output", metavar="outputAutotile", dest="outputAutotile", default="expandedAutotile.png", help="The output file (the expanded autotile). By default, it is \"expandedAutotile.png\", located in the directory in which you launch the script. The script will ask you whether it should overwrite the file if it already exists, unless you used the force option.")
    expandSubCommand.add_argument("inputAutotile", help="The autotile to expand. It must follow a few rules. It must be a PNG image, 64 * 96 wide. It must use RPG Maker VX or VX Ace's TileA2 formatting.")
    expandSubCommand.add_argument("-v", "--verbose", action="store_true", help="Starts the program in verbose mode: it prints detailed information on the process.")
    expandSubCommand.add_argument("-f", "--force", action="store_false", dest="askConfirmation", help="Forces the script to be executed without asking you anything. The script will overwrite the output file without warning you if it already exists. Furthermore, it won't ask add an extension to the output file if it lacks.")
    makeTilesetSubCommand = subparsers.add_parser("maketileset", help="Tileset Generator. Generates a tileset for Tiled map editor with an expanded autotile. You can use it directly (but manually) in your maps, or use it with the Rule Maker to make an automatic automapping rule.")
    makeTilesetSubCommand.add_argument("-o", "--output", metavar="outputTileset", dest="outputTileset", default="expandedAutotileTileset.tsx", help="The output file (the tileset). By default, it is \"expandedAutotileTileset.tsx\", located in the directory in which you launch the script. The script will ask you whether it should overwrite the file if it already exists, unless you used the force option.")
    makeTilesetSubCommand.add_argument("inputExpandedAutotile", help="The expanded autotile to make a tileset with. It must be a PNG image, 256 * 192 wide. To get this expanded autotile, use the autotile expander featured with Remex (with the command \"expand\").")
    makeTilesetSubCommand.add_argument("-v", "--verbose", action="store_true", help="Starts the program in verbose mode: it prints detailed information on the process.")
    makeTilesetSubCommand.add_argument("-f", "--force", action="store_false", dest="askConfirmation", help="Forces the script to be executed without asking you anything. The script will overwrite the output file without warning you if it already exists. Furthermore, it won't ask add an extension to the output file if it lacks.")
    makeRuleSubCommand = subparsers.add_parser("makerule", help="Rule Maker. Generates an automapping rule for Tiled map editor using a tileset of an expanded autotile. It enables you to map autotiles automatically, without worrying about the precise case to use.")
    makeRuleSubCommand.add_argument("-v", "--verbose", action="store_true", help="Starts the program in verbose mode: it prints detailed information on the process.")
    makeRuleSubCommand.add_argument("-f", "--force", action="store_false", dest="askConfirmation", help="Forces the script to be executed without asking you anything. The script will overwrite the output file without warning you if it already exists. Furthermore, it won't ask add an extension to the output file if it lacks.")
    answers = vars(parser.parse_args())
    print(answers)
    command, verbose, askConfirmation = answers["command"], answers["verbose"], answers["askConfirmation"]
    if command == "expand":
        autotileExpander, outputAutotile, inputAutotile = AutotileExpander("autotile", ".png"), answers["outputAutotile"], answers["inputAutotile"]
        autotileExpander.launchScript(inputAutotile, outputAutotile, askConfirmation, verbose)
    elif command == "maketileset":
        tilesetGenerator, outputTileset, inputExpandedAutotile = TilesetGenerator("expanded autotile", ".tsx"), answers["outputTileset"], answers["inputExpandedAutotile"]
        tilesetGenerator.launchScript(inputExpandedAutotile, outputTileset, askConfirmation, verbose)
