from argparse import ArgumentParser
from main import *
from PIL import ImageTk
from PIL import Image as ImagePIL
from tkinter import Tk, W, S, E, N, ttk, filedialog, messagebox, Text, INSERT, VERTICAL, HORIZONTAL, IntVar, StringVar
from os import path
from sys import argv

class GUI:
    def _reloadFrame(self):
        self._frame.grid_forget()
        self._frame = ttk.Frame(self._windowHandler)
        self._frame.grid(column=0, row=0)

    def _spaceWidgets(self):
        for child in self._frame.winfo_children(): child.grid_configure(padx=10, pady=10)

    def _restart(self):
        self._reloadFrame()
        self._prepareStartWindow()

class ScriptGUI(GUI):
    def __init__(self, frame, windowHandler, noInputFileFound, noInputFileFoundLonger, noInputFileFoundExplanation, proceedText, doItAgainText, outputFileTypeDescription, outputFileExtension, defaultOutputFilename, inputFileTypeDescription, inputFileExtension, prepareStartWindow):
        self._noInputFileFound, self._noInputFileFoundLonger, self._noInputFileFoundExplanation = noInputFileFound, noInputFileFoundLonger, noInputFileFoundExplanation
        self._proceedText, self._doItAgainText = proceedText, doItAgainText
        self._outputFileTypeDescription, self._outputFileExtension, self._defaultOutputFilename = outputFileTypeDescription, outputFileExtension, defaultOutputFilename
        self._inputFileTypeDescription, self._inputFileExtension = inputFileTypeDescription, inputFileExtension
        self._inputFilename, self._formerInputFilename, self._inputCorrectOnce = "", "", False
        self._frame, self._windowHandler, self._prepareStartWindow = frame, windowHandler, prepareStartWindow

    def _prepareFirstStepModules(self):
        pass

    def _showLoadedInput(self):
        pass

    def _checkInput(self):
        pass

    def _makeOutput(self):
        pass

    def _showOutput(self):
        pass

    def _saveData(self):
        pass

    def _prepareFirstStepWindow(self):
        self._reloadFrame()
        self._prepareFirstStepModules()
        self._backToMainMenu = ttk.Button(self._frame, text="Back to main menu", command=self._restart)
        self._backToMainMenu.grid(column=0, row=self._frame.grid_size()[1], sticky=(W,S))
        self._spaceWidgets()

    def _inputChoice(self):
        self._formerInputFilename = str(self._inputFilename)
        self._inputFilename, inputLoading = filedialog.askopenfilename(filetypes=[(self._inputFileTypeDescription, "*" + self._inputFileExtension)]).replace("\\", "/"), False
        inputCorrect = self._inputIsCorrect(emptyStringWarning=False)
        if inputCorrect is False and self._inputCorrectOnce is True: #Incorrect input, mais we've had a correct input once, so we use it again
            self._inputFilename, inputLoading = str(self._formerInputFilename), True
        elif inputCorrect is True:
            inputLoading = True
        if inputLoading is True:
            self._showLoadedInput()
            self._proceedButton = ttk.Button(self._frame, command=self._proceed, text=self._proceedText)
            lastRow = self._frame.grid_size()[1]
            self._proceedButton.grid(column=1, row=lastRow)
            self._backToMainMenu.grid(column=0, row=lastRow, sticky=(W,S))
            self._spaceWidgets()
            self._inputCorrectOnce = True
            self._frame.mainloop()

    def _inputIsCorrect(self, emptyStringWarning=True):
        if self._inputFilename != "" and path.exists(self._inputFilename) is True:
            return self._checkInput()
        else:
            if emptyStringWarning:
                messagebox.showwarning(title=self._noInputFileFound, message=self._noInputFileFoundLonger, detail=self._noInputFileFoundExplanation.format(self._inputFilename))
            return False

    def _proceed(self):
        if self._inputIsCorrect():
            self._makeOutput()
            self._prepareSaveWindow()

    def _prepareSaveWindow(self):
        self._reloadFrame()
        self._showOutput()
        self._saveButton = ttk.Button(self._frame, text="Save as...", command=self._saveFileDialog)
        self._saveButton.grid(column=0, row=self._frame.grid_size()[1])
        self._doItAgainButton = ttk.Button(self._frame, text=self._doItAgainText, command=self._prepareFirstStepWindow)
        self._doItAgainButton.grid(column=0, row=self._frame.grid_size()[1])
        self._backToMainMenu = ttk.Button(self._frame, text="Back to main menu", command=self._restart)
        self._backToMainMenu.grid(column=0, row=self._frame.grid_size()[1], sticky=(W,S))
        self._spaceWidgets()
        self._frame.mainloop()

    def _saveFileDialog(self):
        self._saveFilename = filedialog.asksaveasfilename(filetypes=[(self._outputFileTypeDescription, "*" + self._outputFileExtension)], initialfile=self._defaultOutputFilename)
        if self._saveFilename != "":
            if self._saveFilename.lower().endswith(self._outputFileExtension) is False:
                self._saveFilename += self._outputFileExtension
            self._saveData()
        self._frame.mainloop()

class ExpanderGUI(ScriptGUI):

    def _prepareFirstStepModules(self):
        self._loadButton = ttk.Button(self._frame, text="Open...", command=self._inputChoice)
        self._loadButtonText = ttk.Label(self._frame, text="Choose an autotile to expand.\nPNG only, 64 per 96 pixels. It must use the TileA2 format from VX / VX Ace.")
        self._autotileWidget = ttk.Label(self._frame, compound="image")
        self._autotileWidgetText = ttk.Label(self._frame)
        self._loadButton.grid(column=1, row=0)
        self._loadButtonText.grid(column=0, row=0, sticky=W)
        self._autotileWidget.grid(column=1, row=1)
        self._autotileWidgetText.grid(column=0, row=1, sticky=W)

    def _checkInput(self):
        try:
            image = ImagePIL.open(self._inputFilename)
        except IOError:
            messagebox.showwarning(title="The autotile is not a PNG image", message="The autotile to expand is not a PNG image.", detail="You must choose a PNG file.")
        else:
            if image.size == (64, 96): 
                return True
            else:
                messagebox.showwarning(title="The autotile does not have the right size", message="The autotile must be 64 * 96 pixels wide.", detail="Refer to the tileA2 formatting from RPG Maker VX or VX Ace.")

    def _showLoadedInput(self):
        self._imageAutotile = ImagePIL.open(self._inputFilename)
        self._imageWidget = ImageTk.PhotoImage(self._imageAutotile)
        self._autotileWidget["image"] = self._imageWidget
        self._autotileWidgetText["text"] = "Autotile to expand:"  

    def _makeOutput(self):
        autotileExpander = AutotileExpander("autotile", ".png")
        self._expandedAutotile = autotileExpander.expandAutotile(self._inputFilename)

    def _showOutput(self):
        self._imageWidget = ImageTk.PhotoImage(self._expandedAutotile)
        self._expandedAutotileWidget = ttk.Label(self._frame, compound="image", image=self._imageWidget)
        self._expandedAutotileWidget.grid(column=0, row=0)

    def _saveData(self):
        self._expandedAutotile.save(self._saveFilename.replace("\\", "/"), "PNG")

class TilesetGeneratorGUI(ScriptGUI):

    def _prepareFirstStepModules(self):
        self._loadButton = ttk.Button(self._frame, text="Open...", command=self._inputChoice)
        self._loadButtonText = ttk.Label(self._frame, text="Choose an expanded autotile to make a tileset with.\nPNG only, 256 per 192 pixels. You can expand an autotile from RPG Maker VX / VX Ace with this software (Main menu > Expand an autotile).")
        self._autotileWidget = ttk.Label(self._frame, compound="image")
        self._autotileWidgetText = ttk.Label(self._frame)
        self._loadButton.grid(column=1, row=0)
        self._loadButtonText.grid(column=0, row=0, sticky=W)
        self._autotileWidget.grid(column=1, row=1)
        self._autotileWidgetText.grid(column=0, row=1, sticky=W)

    def _checkInput(self):
        try:
            image = ImagePIL.open(self._inputFilename)
        except IOError:
            messagebox.showwarning(title="The autotile is not a PNG image", message="The autotile to expand is not a PNG image.", detail="You must choose a PNG file.")
        else:
            if image.size == (256, 192): 
                return True
            else:
                messagebox.showwarning(title="The autotile does not have the right size", message="The expanded autotile must be 256 * 192 pixels wide.", detail="You can expand an autotile from RPG Maker VX / VX Ace with this software (Main menu > Expand an autotile).")

    def _showLoadedInput(self):
        self._imageAutotile = ImagePIL.open(self._inputFilename)
        self._imageWidget = ImageTk.PhotoImage(self._imageAutotile)
        self._autotileWidget["image"] = self._imageWidget
        self._autotileWidgetText["text"] = "Expanded autotile to make a tileset with:"  

    def _makeOutput(self):
        tilesetGenerator = TilesetGenerator("expanded autotile", ".tsx")
        self._tileset = tilesetGenerator.makeXML(self._inputFilename)

    def _showOutput(self):
        self._expandedAutotileWidget = Text(self._frame, wrap="none")
        self._expandedAutotileWidget.insert(INSERT, self._tileset.toprettyxml(indent="  ", newl="\n", encoding="UTF-8") )
        self._expandedAutotileScrollbarX = ttk.Scrollbar(self._frame, orient=HORIZONTAL, command=self._expandedAutotileWidget.xview)
        self._expandedAutotileWidget["xscrollcommand"] = self._expandedAutotileScrollbarX.set
        self._expandedAutotileWidget.grid(column=0, row=0)
        self._expandedAutotileScrollbarX.grid(column=0, row=1, sticky=(W,E))

    def _saveData(self):
        with open(self._saveFilename, "w") as outputFile:
            self._tileset.writexml(outputFile, addindent="  ", newl="\n", encoding="UTF-8")
        self._tileset.unlink()

class RuleMakerGUI(ScriptGUI):
    
    def _prepareFirstStepModules(self):
        self._loadButton = ttk.Button(self._frame, text="Open...", command=self._inputChoice)
        self._loadButtonText = ttk.Label(self._frame, text="Choose an Tileset for Tiled to make an automapping rule with.\nIt must be a .tsx file referring to an expanded autotile. You can make a tileset with this software (Main menu > Generate a tileset).")
        self._loadButton.grid(column=1, row=0)
        self._loadButtonText.grid(column=0, row=0, sticky=W)

    def _checkInput(self):
        try:
            tilesetConfig = xml.dom.minidom.parse(self._inputFilename)
            tilesetXML = tilesetConfig.documentElement
        except Exception as error:
            print("An error was encountered while loading the tileset {0}. Details:\n{1}".format(self._inputFilename,error))
            messagebox.showwarning(title="The tileset is invalid", message="An error was encountered while loading the tileset.", detail="{0}".format(error))
        else:
            return True

    def _showLoadedInput(self):
        self._tilesetWidget = ttk.Label(self._frame, text=self._inputFilename)
        self._tilesetWidgetText = ttk.Label(self._frame, text="Tileset to use:")
        self._mapLayerVar = StringVar()
        self._mapLayerVar.set("Tile Layer 1")
        self._mapLayerEntry = ttk.Entry(self._frame, textvariable=self._mapLayerVar)
        self._mapLayerEntryText = ttk.Label(self._frame, text="Map layer to consider:\nIt is the tile layer on which the automapping will apply.\nYou can only choose a layer per rule, so you need to make another rule if you want another layer to be considered too.")
        self._version08 = StringVar()
        self._version08.set("False")
        self._versionRadiobuttonText = ttk.Label(self._frame, text="Which version of Tiled do you use?")
        self._version09Radiobutton = ttk.Radiobutton(self._frame, text="Tiled 0.9", variable=self._version08, value="False")
        self._version08Radiobutton = ttk.Radiobutton(self._frame, text="Tiled 0.8", variable=self._version08, value="True")
        self._tilesetWidget.grid(column=1, row=1)
        self._tilesetWidgetText.grid(column=0, row=1, sticky=W)
        self._mapLayerEntry.grid(column=1, row=2, sticky=(W,E))
        self._mapLayerEntryText.grid(column=0, row=2, sticky=W)
        self._versionRadiobuttonText.grid(column=0, row=3, sticky=W)
        self._version09Radiobutton.grid(column=0, row=4, sticky=W)
        self._version08Radiobutton.grid(column=1, row=4, sticky=W)

    def _makeOutput(self):
        self._ruleMaker = RuleMaker("automapping rule", ".tmx")
        self._ruleMaker.setRegionsLocation(path.abspath(path.dirname(argv[0])).replace("\\", "/"))
        version08 = False
        if self._version08.get() == "True":
            version08 = True
        self._ruleMaker.initializeEverything(inputFilename=self._inputFilename, mapLayer=self._mapLayerVar.get(), version08=version08)
        self._rule = self._ruleMaker.makeRule()

    def _showOutput(self):
        self._ruleWidget = Text(self._frame, wrap="none")
        self._ruleWidget.insert(INSERT, self._rule.toprettyxml(indent="  ", newl="\n", encoding="UTF-8") )
        self._ruleScrollbarX = ttk.Scrollbar(self._frame, orient=HORIZONTAL, command=self._ruleWidget.xview)
        self._ruleWidget["xscrollcommand"] = self._ruleScrollbarX.set
        self._ruleScrollbarY = ttk.Scrollbar(self._frame, orient=VERTICAL, command=self._ruleWidget.yview)
        self._ruleWidget["yscrollcommand"] = self._ruleScrollbarY.set
        self._ruleWidget.grid(column=0, row=0)
        self._ruleScrollbarX.grid(column=0, row=1, sticky=(W,E))
        self._ruleScrollbarY.grid(column=1, row=0, sticky=(N,S))

    def _copyRegionsImage(self):
        i, tilesetsXML = 0, self._rule.documentElement.getElementsByTagName("tileset")
        while i < len(tilesetsXML):
            if tilesetsXML[i].getAttribute("name") == "Automapping Regions":
                imageXML = tilesetsXML[i].getElementsByTagName("image")[0]
                newLocation = path.abspath(path.dirname(self._saveFilename)).replace("\\", "/")
                imageXML.setAttribute("source", newLocation + "/automappingRegions.png")
            i += 1
        originalRegionsFile = path.abspath(path.dirname(argv[0])).replace("\\", "/") + "/automappingRegions.png"
        self._ruleMaker.copyRegionsImage(originalRegionsFile, newLocation)

    def _saveData(self):
        with open(self._saveFilename, "w") as outputFile:
            self._copyRegionsImage()
            self._rule.writexml(outputFile, addindent="  ", newl="\n", encoding="UTF-8")
        self._rule.unlink()
        self._ruleMaker.unlinkOtherData()

class RemexGUI(GUI):
    def __init__(self):
        self._initializeTkinter()
        self._prepareStartWindow()

    def _quit(self, *val):
        self._windowHandler.destroy()


    def launch(self, verbose):
        self._verbose = verbose
        self._frame.mainloop()

    def _initializeTkinter(self):
        self._windowHandler = Tk()
        self._windowHandler.title("Remex")
        self._windowHandler.bind('<Escape>', self._quit)
        self._windowHandler.wm_iconbitmap("NuvolaTileIcon.ico")
        self._frame = ttk.Frame(self._windowHandler)

    def _prepareStartWindow(self):
        self._expanderButton = ttk.Button(self._frame, text="Expand an autotile", command=self._prepareExpanderWindow)
        self._tilesetGeneratorButton = ttk.Button(self._frame, text="Generate a tileset for Tiled editor from an expanded autotile", command=self._prepareTilesetGeneratorWindow)
        self._ruleMakerButton = ttk.Button(self._frame, text="Make an automapping rule for Tiled editor", command=self._prepareRuleMakerWindow)
        self._frame.grid(column=0, row=0)
        self._expanderButton.grid(column=0, row=0)
        self._tilesetGeneratorButton.grid(column=0, row=1)
        self._ruleMakerButton.grid(column=0, row=2)
        self._spaceWidgets()

    def _prepareExpanderWindow(self):
        expanderGUI = ExpanderGUI(self._frame, self._windowHandler, "No autotile to expand", "No autotile to expand was found.", "Please make sure that the file \"{0}\" exists.", "Expand the autotile!", "Expand another autotile", "Portable Network Graphics", ".png", "expandedAutotile.png", "Portable Network Graphics", ".png", self._prepareStartWindow)
        expanderGUI._prepareFirstStepWindow()

    def _prepareTilesetGeneratorWindow(self):
        tilesetGeneratorGUI = TilesetGeneratorGUI(self._frame, self._windowHandler, "No expanded autotile", "No expanded autotile to make a tileset with was found.", "Please make sure that the file \"{0}\" exists.", "Make a tileset!", "Make another tileset", "Tileset for Tiled", ".tsx", "expandedAutotileTileset.tsx", "Portable Network Graphics", ".png", self._prepareStartWindow)
        tilesetGeneratorGUI._prepareFirstStepWindow()

    def _prepareRuleMakerWindow(self):
        ruleMakerGUI = RuleMakerGUI(self._frame, self._windowHandler, "No tileset", "No tileset to make an automapping rule was found.", "Please make sure that the file \"{0}\" exists.", "Make an automapping rule!", "Make another automapping rule", "Automapping rule", ".tmx", "automappingRule.tmx", "Tileset for Tiled", ".tsx", self._prepareStartWindow)
        ruleMakerGUI._prepareFirstStepWindow()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="Starts the program in verbose mode: it prints detailed information on the process.")
    answers = vars(parser.parse_args())
    gui = RemexGUI()
    gui.launch(answers["verbose"])
