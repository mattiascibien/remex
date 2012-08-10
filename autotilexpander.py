from PIL import *
from PIL import Image
import sys, getopt

class AutotileExpander:

    def _initializeLocations():
        AutotileExpander._minitiles, AutotileExpander._minitilePosition, AutotileExpander._minitileType = dict(NO=dict(), NE=dict(), SO=dict(), SE=dict()), dict(), dict()
        AutotileExpander._minitileTypeDependingOnGroup, AutotileExpander._minitilePositionGroup = dict(), dict()
        #Liste des types et directions possibles
        AutotileExpander._minitileType, AutotileExpander._minitilePosition = ["Normal", "Angle int", "Angle ext", "BordHori", "BordVerti", "Présentation"], ["NO", "NE", "SO", "SE"]
        #Direction selon la position au sein du groupe
        AutotileExpander._minitilePositionGroup[0, 0], AutotileExpander._minitilePositionGroup[16, 0], AutotileExpander._minitilePositionGroup[0, 16], AutotileExpander._minitilePositionGroup[16, 16] = "NO", "NE", "SO", "SE"
        #Type des minitiles selon leurs groupes et directions
        AutotileExpander._minitileTypeDependingOnGroup[0, 0, "NO"] = "Présentation"
        AutotileExpander._minitileTypeDependingOnGroup[0, 0, "NE"] = "Présentation"
        AutotileExpander._minitileTypeDependingOnGroup[0, 0, "SO"] = "Présentation"
        AutotileExpander._minitileTypeDependingOnGroup[0, 0, "SE"] = "Présentation"
        AutotileExpander._minitileTypeDependingOnGroup[32, 0, "NO"] = "Angle int"
        AutotileExpander._minitileTypeDependingOnGroup[32, 0, "NE"] = "Angle int"
        AutotileExpander._minitileTypeDependingOnGroup[32, 0, "SO"] = "Angle int"
        AutotileExpander._minitileTypeDependingOnGroup[32, 0, "SE"] = "Angle int"
        AutotileExpander._minitileTypeDependingOnGroup[0, 32, "NO"] = "Angle ext"
        AutotileExpander._minitileTypeDependingOnGroup[32, 32, "NE"] = "Angle ext"
        AutotileExpander._minitileTypeDependingOnGroup[0, 64, "SO"] = "Angle ext"
        AutotileExpander._minitileTypeDependingOnGroup[32, 64, "SE"] = "Angle ext"
        AutotileExpander._minitileTypeDependingOnGroup[32, 32, "NO"] = "BordHori"
        AutotileExpander._minitileTypeDependingOnGroup[0, 32, "NE"] = "BordHori"
        AutotileExpander._minitileTypeDependingOnGroup[32, 64, "SO"] = "BordHori"
        AutotileExpander._minitileTypeDependingOnGroup[0, 64, "SE"] = "BordHori"
        AutotileExpander._minitileTypeDependingOnGroup[0, 64, "NO"] = "BordVerti"
        AutotileExpander._minitileTypeDependingOnGroup[32, 64, "NE"] = "BordVerti"
        AutotileExpander._minitileTypeDependingOnGroup[0, 32, "SO"] = "BordVerti"
        AutotileExpander._minitileTypeDependingOnGroup[32, 32, "SE"] = "BordVerti"
        AutotileExpander._minitileTypeDependingOnGroup[32, 64, "NO"] = "Normal"
        AutotileExpander._minitileTypeDependingOnGroup[0, 64, "NE"] = "Normal"
        AutotileExpander._minitileTypeDependingOnGroup[0, 32, "SE"] = "Normal"
        AutotileExpander._minitileTypeDependingOnGroup[32, 32, "SO"] = "Normal"

    def _makeAutotile(*types):
        autotileSurface = Image.new("RGB", (32,32))
        minitileAbs, minitileOrd, i = 0, 0, 0
        while minitileOrd < 32:
            minitileAbs = 0
            while minitileAbs < 32:
                minitilePosition = AutotileExpander._minitilePositionGroup[minitileAbs, minitileOrd]
                minitileType = types[i]
                minitileSurface = AutotileExpander._minitiles[minitilePosition][minitileType]
                autotileSurface.paste(minitileSurface, (minitileAbs, minitileOrd))
                i += 1
                minitileAbs += 16
            minitileOrd += 16
        return autotileSurface

    def expandAutotile(autotileFilename):
        AutotileExpander._imageAutotile = Image.open(autotileFilename)
        AutotileExpander._initializeLocations()
        #### First we find the minitiles, then we use their types and position to sort them
        groupAbs, groupOrd = 0, 0
        while groupOrd < AutotileExpander._imageAutotile.size[1]: #We run through the groups of minitiles
            groupAbs = 0
            while groupAbs < AutotileExpander._imageAutotile.size[0]:
                minitileAbs, minitileOrd = 0, 0
                while minitileOrd < 32: #We run through the minitiles
                    minitileAbs = 0
                    while minitileAbs < 32:
                        minitilePosition = AutotileExpander._minitilePositionGroup[minitileAbs, minitileOrd]
                        minitileType = AutotileExpander._minitileTypeDependingOnGroup[groupAbs, groupOrd, minitilePosition]
                        AutotileExpander._minitiles[minitilePosition][minitileType] = AutotileExpander._imageAutotile.crop((groupAbs+minitileAbs, groupOrd+minitileOrd, groupAbs+minitileAbs+16, groupOrd+minitileOrd+16))
                        minitileAbs += 16
                    minitileOrd += 16
                groupAbs += 32
            groupOrd += 32
        ##### We define the types composing the 48 autotiles
        autotilesSurfaces = dict()
        autotilesSurfaces[0] = AutotileExpander._makeAutotile("Normal", "Normal", "Normal", "Normal")
        autotilesSurfaces[1] = AutotileExpander._makeAutotile("Angle int", "Normal", "Normal", "Normal")
        autotilesSurfaces[2] = AutotileExpander._makeAutotile("Normal", "Angle int", "Normal", "Normal")
        autotilesSurfaces[3] = AutotileExpander._makeAutotile("Angle int", "Angle int", "Normal", "Normal")
        autotilesSurfaces[4] = AutotileExpander._makeAutotile("Normal", "Normal", "Normal", "Angle int")
        autotilesSurfaces[5] = AutotileExpander._makeAutotile("Angle int", "Normal", "Normal", "Angle int")
        autotilesSurfaces[6] = AutotileExpander._makeAutotile("Normal", "Angle int", "Normal", "Angle int")
        autotilesSurfaces[7] = AutotileExpander._makeAutotile("Angle int", "Angle int", "Normal", "Angle int")
        autotilesSurfaces[8] = AutotileExpander._makeAutotile("Normal", "Normal", "Angle int", "Normal")
        autotilesSurfaces[9] = AutotileExpander._makeAutotile("Angle int", "Normal", "Angle int", "Normal")
        autotilesSurfaces[10] = AutotileExpander._makeAutotile("Normal", "Angle int", "Angle int", "Normal")
        autotilesSurfaces[11] = AutotileExpander._makeAutotile("Angle int", "Angle int", "Angle int", "Normal")
        autotilesSurfaces[12] = AutotileExpander._makeAutotile("Normal", "Normal", "Angle int", "Angle int")
        autotilesSurfaces[13] = AutotileExpander._makeAutotile("Angle int", "Normal", "Angle int", "Angle int")
        autotilesSurfaces[14] = AutotileExpander._makeAutotile("Normal", "Angle int", "Angle int", "Angle int")
        autotilesSurfaces[15] = AutotileExpander._makeAutotile("Angle int", "Angle int", "Angle int", "Angle int")
        autotilesSurfaces[16] = AutotileExpander._makeAutotile("BordVerti", "Normal", "BordVerti", "Normal")
        autotilesSurfaces[17] = AutotileExpander._makeAutotile("BordVerti", "Angle int", "BordVerti", "Normal")
        autotilesSurfaces[18] = AutotileExpander._makeAutotile("BordVerti", "Normal", "BordVerti", "Angle int")
        autotilesSurfaces[19] = AutotileExpander._makeAutotile("BordVerti", "Angle int", "BordVerti", "Angle int")
        autotilesSurfaces[20] = AutotileExpander._makeAutotile("BordHori", "BordHori", "Normal", "Normal")
        autotilesSurfaces[21] = AutotileExpander._makeAutotile("BordHori", "BordHori", "Normal", "Angle int")
        autotilesSurfaces[22] = AutotileExpander._makeAutotile("BordHori", "BordHori", "Angle int", "Normal")
        autotilesSurfaces[23] = AutotileExpander._makeAutotile("BordHori", "BordHori", "Angle int", "Angle int")
        autotilesSurfaces[24] = AutotileExpander._makeAutotile("Normal", "BordVerti", "Normal", "BordVerti")
        autotilesSurfaces[25] = AutotileExpander._makeAutotile("Normal", "BordVerti", "Angle int", "BordVerti")
        autotilesSurfaces[26] = AutotileExpander._makeAutotile("Angle int", "BordVerti", "Normal", "BordVerti")
        autotilesSurfaces[27] = AutotileExpander._makeAutotile("Angle int", "BordVerti", "Angle int", "BordVerti")
        autotilesSurfaces[28] = AutotileExpander._makeAutotile("Normal", "Normal", "BordHori", "BordHori")
        autotilesSurfaces[29] = AutotileExpander._makeAutotile("Angle int", "Normal", "BordHori", "BordHori")
        autotilesSurfaces[30] = AutotileExpander._makeAutotile("Normal", "Angle int", "BordHori", "BordHori")
        autotilesSurfaces[31] = AutotileExpander._makeAutotile("Angle int", "Angle int", "BordHori", "BordHori")
        autotilesSurfaces[32] = AutotileExpander._makeAutotile("BordVerti", "BordVerti", "BordVerti", "BordVerti")
        autotilesSurfaces[33] = AutotileExpander._makeAutotile("BordHori", "BordHori", "BordHori", "BordHori")
        autotilesSurfaces[34] = AutotileExpander._makeAutotile("Angle ext", "BordHori", "BordVerti", "Normal")
        autotilesSurfaces[35] = AutotileExpander._makeAutotile("Angle ext", "BordHori", "BordVerti", "Angle int")
        autotilesSurfaces[36] = AutotileExpander._makeAutotile("BordHori", "Angle ext", "Normal", "BordVerti")
        autotilesSurfaces[37] = AutotileExpander._makeAutotile("BordHori", "Angle ext", "Angle int", "BordVerti")
        autotilesSurfaces[38] = AutotileExpander._makeAutotile("Normal", "BordVerti", "BordHori", "Angle ext")
        autotilesSurfaces[39] = AutotileExpander._makeAutotile("Angle int", "BordVerti", "BordHori", "Angle ext")
        autotilesSurfaces[40] = AutotileExpander._makeAutotile("BordVerti", "Normal", "Angle ext", "BordHori")
        autotilesSurfaces[41] = AutotileExpander._makeAutotile("BordVerti", "Angle int", "Angle ext", "BordHori")
        autotilesSurfaces[42] = AutotileExpander._makeAutotile("Présentation", "Présentation", "BordVerti", "BordVerti")
        autotilesSurfaces[43] = AutotileExpander._makeAutotile("Présentation", "BordHori", "Présentation", "BordHori")
        autotilesSurfaces[44] = AutotileExpander._makeAutotile("BordVerti", "BordVerti", "Présentation", "Présentation")
        autotilesSurfaces[45] = AutotileExpander._makeAutotile("BordHori", "Présentation", "BordHori", "Présentation")
        autotilesSurfaces[46] = AutotileExpander._makeAutotile("Présentation", "Présentation", "Présentation", "Présentation")
        autotilesSurfaces[47] = AutotileExpander._makeAutotile("Présentation", "Présentation", "Présentation", "Présentation")
        ##### We make the final surface
        autotileAbs, autotileOrd, i, AutotileExpander._expandedAutotile = 0, 0, 0, Image.new("RGB", (32*8, 32*6))
        while autotileOrd < 32 * 6:
            autotileAbs = 0
            while autotileAbs < 32 * 8:
                AutotileExpander._expandedAutotile.paste(autotilesSurfaces[i], (autotileAbs, autotileOrd))
                i += 1
                autotileAbs += 32
            autotileOrd += 32
        return AutotileExpander._expandedAutotile

    def launchScript():
        arguments = sys.argv[1:]


if __name__ == "__main__":
    AutotileExpander.launchScript()
