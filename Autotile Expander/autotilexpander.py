import PIL
from PIL import Image
from PIL import ImageTk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import sys, os, argparse

class Remex:

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
        autotileSurface = PIL.Image.new("RGB", (32,32))
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
        self._imageAutotile = PIL.Image.open(autotileFilename)
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
        autotileAbs, autotileOrd, i, self._expandedAutotile = 0, 0, 0, PIL.Image.new("RGB", (32*8, 32*6))
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
                    print("Correct, let's continue if you want.")
        elif step == "Input validity":
            try:
                image = PIL.Image.open(self._inputFilename)
            except IOError:
                print("The input autotile \"{0}\" is not a valid PNG image.".format(self._inputFilename))
                raise SystemExit
        elif step == "Input size":
            image = PIL.Image.open(self._inputFilename)
            if image.size != (64, 96):
                print("The input autotile \"{0}\" does not have the right size.\nIt must be 64 * 96 pixels wide. Please refer to tileA2 formatting from RPG Maker VX / VX Ace.".format(self._inputFilename))
                raise SystemExit
        elif step == "Output without extension":
            if self._outputFilename.lower().endswith(".png") is False and self._askConfirmation is True:
                answerIgnoreNoExtension = self._interacter.askString("The output file \"{0}\" does not a a .png extension. Shall I add the extension? (Y/n)".format(self._outputFilename))
                if answerIgnoreNoExtension.lower().split(" ")[0] == "y":
                    self._outputFilename += ".png"
                    print("Correct, I'm adding the extension. The output file is now \"{0}\".".format(self._outputFilename))
                else:
                    print("Correct, I won't do anything about the extension.")
        elif step == "Output already exists":
            if os.path.exists(self._outputFilename) == True and self._askConfirmation is True:
                answerIgnoreExistingOutput = self._interacter.askString("The output file \"{0}\" already exists. Do you want to overwrite it? (y/N)".format(self._outputFilename))
                if answerIgnoreExistingOutput.lower().split(" ")[0] != "y":
                    print("Correct, I'm stopping here.")
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

class AutotileExpanderGUI:
    def __init__(self, autotileExpander):
        self._autotileFilename, self._formerAutotileFilename, self._imageCorrectOnce, self._autotileExpander = "", "", False, autotileExpander
        self._initializeTkinter()
        self._prepareStartWindow()

    def _quit(self, *val):
        self._windowHandler.destroy()

    def _initializeTkinter(self):
        self._windowHandler = Tk()
        self._windowHandler.title("Autotile Expander for VX/VX Ace")
        self._windowHandler.bind('<Escape>', self._quit)
        self._windowHandler.wm_iconbitmap("NuvolaTileIcon.ico")

    def _prepareStartWindow(self):
        self._frame = ttk.Frame(self._windowHandler)
        self._loadButton = ttk.Button(self._frame, text="Open...", command=self._autotileChoice)
        self._loadButtonText = ttk.Label(self._frame, text="Choose an autotile to expand.\nPNG only, 64 per 96 pixels. It must use the TileA2 format from VX / VX Ace.")
        self._autotileWidget = ttk.Label(self._frame, compound="image")
        self._autotileWidgetText = ttk.Label(self._frame)
        self._frame.grid(column=0, row=0)
        self._loadButton.grid(column=1, row=0)
        self._loadButtonText.grid(column=0, row=0, sticky=W)
        self._autotileWidget.grid(column=1, row=1)
        self._autotileWidgetText.grid(column=0, row=1, sticky=W)
        for child in self._frame.winfo_children(): child.grid_configure(padx=30, pady=30)

    def _autotileChoice(self):
        self._formerAutotileFilename = str(self._autotileFilename)
        self._autotileFilename, imageLoading = filedialog.askopenfilename(filetypes=[("Portable Network Graphics", "*.png")]).replace("\\", "/"), False
        autotileCorrect = self._autotileIsCorrect(emptyStringWarning=False)
        if autotileCorrect is False and self._imageCorrectOnce is True: #Incorrect image, mais we've had a correct image once, so we use it again
            self._autotileFilename, imageLoading = str(self._formerAutotileFilename), True
        elif autotileCorrect is True:
            imageLoading = True
        if imageLoading is True:
            self._imageAutotile = PIL.Image.open(self._autotileFilename)
            imageWidget = ImageTk.PhotoImage(self._imageAutotile)
            self._autotileWidget["image"] = imageWidget
            self._autotileWidgetText["text"] = "Autotile to expand:" 
            self._proceedButton = ttk.Button(self._frame, command=self._proceed, text="Expand the autotile")
            self._proceedButton.grid(column=1, row=2)
            for child in self._frame.winfo_children(): child.grid_configure(padx=30, pady=30)
            self._imageCorrectOnce = True
            self._frame.mainloop()

    def _autotileIsCorrect(self, emptyStringWarning=True):
        if self._autotileFilename != "":
            try:
                image = PIL.Image.open(self._autotileFilename)
            except IOError:
                messagebox.showwarning(title="The autotile is not a PNG image", message="The autotile to expand is not a PNG image.", detail="You must choose a PNG file.")
            else:
                if image.size == (64, 96): 
                    return True
                else:
                    messagebox.showwarning(title="The autotile does not have the right size", message="The autotile must be 64 * 96 pixels wide.", detail="Refer to the tileA2 formatting from RPG Maker VX or VX Ace.")
        else:
            if emptyStringWarning:
                messagebox.showwarning(title="No autotile to expand", message="No autotile to expand was found.", detail="You must load an autotile to expand.")
        return False

    def _prepareSaveWindow(self):
        self._frame.grid_forget()
        self._frame = ttk.Frame(self._windowHandler)
        self._frame.grid(column=0, row=0)
        imageWidget = ImageTk.PhotoImage(self._expandedAutotile)
        self._expandedAutotileWidget = ttk.Label(self._frame, compound="image", image=imageWidget)
        self._expandedAutotileWidget.grid(column=0, row=0)
        self._saveButton = ttk.Button(self._frame, text="Save as...", command=self._save)
        self._saveButton.grid(column=0, row=1)
        self._restartButton = ttk.Button(self._frame, text="Expand another autotile", command=self._restart)
        self._restartButton.grid(column=0, row=2)
        for child in self._frame.winfo_children(): child.grid_configure(padx=30, pady=30)
        self._frame.mainloop()

    def _save(self):
        saveFilename = filedialog.asksaveasfilename(filetypes=[("Portable Network Graphics", "*.png")], initialfile="expandedAutotile.png")
        if saveFilename != "":
            if saveFilename.lower().endswith(".png") is False:
                saveFilename += ".png"
            self._expandedAutotile.save(saveFilename.replace("\\", "/"), "PNG")
        self._frame.mainloop()

    def _restart(self):
        self._frame.grid_forget()
        self._autotileFilename, self._formerAutotileFilename, self._imageCorrectOnce = "", "", False
        self._prepareStartWindow()

    def _choixAutotile(self):
        self._ancienNomFichierAutotile = str(self._nomFichierAutotile)
        self._nomFichierAutotile, chargementImage = filedialog.askopenfilename(filetypes=[("Portable Network Graphics", "*.png")]).replace("\\", "/"), False
        autotileCorrect = self._autotileCorrect(messageChaineVide=False)
        if autotileCorrect is False and self._imageCorrecteUneFois is True: #Pas correct, mais on a déjà chargé une image qui était correcte, on la reprend
            self._nomFichierAutotile, chargementImage = str(self._ancienNomFichierAutotile), True
        elif autotileCorrect is True:
            chargementImage = True
        if chargementImage is True:
            self._imageAutotile = Image.open(self._nomFichierAutotile)
            imageWidget = ImageTk.PhotoImage(self._imageAutotile)
            self._widgetAutotile["image"] = imageWidget
            self._texteWidgetAutotile["text"] = "Autotile to expand:" 
            self._boutonTraitement = ttk.Button(self._frame, command=self._traiterAutotileAvecVerif, text="Expand the autotile")
            self._boutonTraitement.grid(column=1, row=2)
            for child in self._frame.winfo_children(): child.grid_configure(padx=30, pady=30)
            self._imageCorrecteUneFois = True
            self._frame.mainloop()

    def _sauvegarde(self):
        nomFichierSauvegarde = filedialog.asksaveasfilename(filetypes=[("Portable Network Graphics", "*.png")], initialfile="expandedAutotile.png")
        if nomFichierSauvegarde != "":
            if nomFichierSauvegarde.lower().endswith(".png") is False:
                nomFichierSauvegarde += ".png"
            self._autotileEtendu.save(nomFichierSauvegarde.replace("\\", "/"), "PNG")
        self._frame.mainloop()

    def _proceed(self):
        if self._autotileIsCorrect():
            self._expandedAutotile = self._autotileExpander.expandAutotile(self._autotileFilename)
            self._prepareSaveWindow()

    def launch(self, verbose):
        self._verbose = verbose
        self._frame.mainloop()

if __name__ == "__main__":
    remex = Remex()
    parser = argparse.ArgumentParser(conflict_handler="resolve")
    parser.add_argument("command", help="The command that the script has to execute. It may be \"expand\", \"maketileset\" or \"makerule\".")
    parser.add_argument("inputFile", help="The autotile to expand. If you don't use this argument, the GUI will start instead of the script. If you use it, it must follow a few rules. It must be a PNG image, 64 * 96 wide. It must use RPG Maker VX or VX Ace's TileA2 formatting.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Starts the program in verbose mode: it prints detailed information on the process.")
    parser.add_argument("-f", "--force", action="store_false", dest="askConfirmation", help="Forces the script to be executed without asking you anything. The script will overwrite the output file without warning you if it already exists.")
    parser.add_argument("-o", "--output", metavar="outputFile", default="expandedAutotile.png", help="The output file (the expanded autotile). By default, it is \"expandedAutotile.png\", located in the directory in which you launch the script. The script will ask you whether it should overwrite the file if it already exists, unless you used the force option.")
    answers = vars(parser.parse_args())
    print(answers)
    outputFile, verbose, askConfirmation, inputFile = answers["output"], answers["verbose"], answers["askConfirmation"], answers["inputFile"]
    if inputFile is not False:
        sys.path.append(os.path.abspath("../"))
        from interacter import *
        remex.launchScript(inputFile, outputFile, askConfirmation, verbose)
    else:
        gui = AutotileExpanderGUI(autotileExpander)
        gui.launch(verbose)
