from argparse import ArgumentParser
from main import *
from PIL import ImageTk
from PIL import Image as ImagePIL
from tkinter import Tk, W, ttk, filedialog, messagebox

class GUI:
    def _reloadFrame(self):
        self._frame.grid_forget()
        self._frame = ttk.Frame(self._windowHandler)
        self._frame.grid(column=0, row=0)

    def _spaceWidgets(self):
        for child in self._frame.winfo_children(): child.grid_configure(padx=10, pady=10)

class ScriptGUI(GUI):
    def __init__(self, frame, windowHandler, noInputFileFound, noInputFileFoundLonger, noInputFileFoundExplanation, proceedText, doItAgainText, outputFileTypeDescription, outputFileExtension, defaultOutputFilename, inputFileTypeDescription, inputFileExtension):
        self._noInputFileFound, self._noInputFileFoundLonger, self._noInputFileFoundExplanation = noInputFileFound, noInputFileFoundLonger, noInputFileFoundExplanation
        self._proceedText, self._doItAgainText = proceedText, doItAgainText
        self._outputFileTypeDescription, self._outputFileExtension, self._defaultOutputFilename = outputFileTypeDescription, outputFileExtension, defaultOutputFilename
        self._inputFileTypeDescription, self._inputFileExtension = inputFileTypeDescription, inputFileExtension
        self._inputFilename, self._formerInputFilename, self._inputCorrectOnce = "", "", False
        self._frame, self._windowHandler = frame, windowHandler

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
            self._proceedButton = ttk.Button(self._frame, command=self._proceed, text=self._proceedText)
            self._proceedButton.grid(column=1, row=2)
            self._showLoadedInput()
            self._spaceWidgets()
            self._inputCorrectOnce = True
            self._frame.mainloop()

    def _inputIsCorrect(self, emptyStringWarning=True):
        if self._inputFilename != "":
            return self._checkInput()
        else:
            print("empty")
            if emptyStringWarning:
                messagebox.showwarning(title=self._noInputFileFound, message=self._noInputFileFoundLonger, detail=self._noInputFileFoundExplanation)
            return False

    def _proceed(self):
        if self._inputIsCorrect():
            self._makeOutput()
            self._prepareSaveWindow()

    def _prepareSaveWindow(self):
        self._reloadFrame()
        self._showOutput()
        self._saveButton = ttk.Button(self._frame, text="Save as...", command=self._saveFileDialog)
        self._saveButton.grid(column=0, row=1)
        self._doItAgainButton = ttk.Button(self._frame, text=self._doItAgainText, command=self._prepareFirstStepWindow)
        self._doItAgainButton.grid(column=0, row=2)
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


class RemexGUI(GUI):
    def __init__(self):
        self._initializeTkinter()
        self._prepareStartWindow()

    def _quit(self, *val):
        self._windowHandler.destroy()

    def _restart(self):
        self._frame.grid_forget()
        self._autotileFilename, self._formerAutotileFilename, self._imageCorrectOnce = "", "", False
        self._prepareStartWindow()

    def launch(self, verbose):
        self._verbose = verbose
        self._frame.mainloop()

    def _initializeTkinter(self):
        self._windowHandler = Tk()
        self._windowHandler.title("Remex")
        self._windowHandler.bind('<Escape>', self._quit)
        self._windowHandler.wm_iconbitmap("NuvolaTileIcon.ico")

    def _prepareStartWindow(self):
        self._frame = ttk.Frame(self._windowHandler)
        self._expanderButton = ttk.Button(self._frame, text="Expand an autotile", command=self._prepareExpanderWindow)
        self._tilesetGeneratorButton = ttk.Button(self._frame, text="Generate a tileset for Tiled editor from an expanded autotile", command=self._prepareTilesetGeneratorWindow)
        self._ruleMakerButton = ttk.Button(self._frame, text="Make an automapping rule for Tiled editor", command=self._prepareRuleMakerWindow)
        self._frame.grid(column=0, row=0)
        self._expanderButton.grid(column=0, row=0)
        self._tilesetGeneratorButton.grid(column=0, row=1)
        self._ruleMakerButton.grid(column=0, row=2)
        self._spaceWidgets()

    def _prepareExpanderWindow(self):
        expanderGUI = ExpanderGUI(self._frame, self._windowHandler, "No autotile to expand", "a", "a", "Expand the autotile!", "Expand another autotile", "Portable Network Graphics", ".png", "expandedAutotile.png", "Portable Network Graphics", ".png")
        expanderGUI._prepareFirstStepWindow()

    def _prepareTilesetGeneratorWindow(self):
        self._reloadFrame()

    def _prepareRuleMakerWindow(self):
        self._reloadFrame()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="Starts the program in verbose mode: it prints detailed information on the process.")
    answers = vars(parser.parse_args())
    gui = RemexGUI()
    gui.launch(answers["verbose"])
