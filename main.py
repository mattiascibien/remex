import os 
from tkinter import *
from PIL import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
from autotilexpander import *

class Appli:
    def __init__(self):
        self._nomFichierAutotile, self._ancienNomFichierAutotile, self._imageCorrecteUneFois = "", "", False
        self._initialiserTkinter()
        self._preparerFenetreDebut()

    def _quitter(self, *val):
        self._gestionnaireFenetre.destroy()

    def _initialiserTkinter(self):
        self._gestionnaireFenetre = Tk()
        self._gestionnaireFenetre.title("Autotile Expander for VX/VX Ace")
        self._gestionnaireFenetre.bind('<Escape>', self._quitter)
        self._gestionnaireFenetre.wm_iconbitmap("Icone.ico")

    def _preparerFenetreDebut(self):
        self._frame = ttk.Frame(self._gestionnaireFenetre)
        self._boutonCharger = ttk.Button(self._frame, text="Open...", command=self._choixAutotile)
        self._texteBoutonCharger = ttk.Label(self._frame, text="Choose an autotile to expand.\nPNG only, 64 per 96 pixels. It must use the TileA2 format from VX / VX Ace.")
        self._widgetAutotile = ttk.Label(self._frame, compound="image")
        self._texteWidgetAutotile = ttk.Label(self._frame)
        self._frame.grid(column=0, row=0)
        self._boutonCharger.grid(column=1, row=0)
        self._texteBoutonCharger.grid(column=0, row=0, sticky=W)
        self._widgetAutotile.grid(column=1, row=1)
        self._texteWidgetAutotile.grid(column=0, row=1, sticky=W)
        for child in self._frame.winfo_children(): child.grid_configure(padx=30, pady=30)

    def _preparerFenetreSauvegarde(self):
        self._frame.grid_forget()
        self._frame = ttk.Frame(self._gestionnaireFenetre)
        self._frame.grid(column=0, row=0)
        imageWidget = ImageTk.PhotoImage(self._autotileEtendu)
        self._widgetAutotileEtendu = ttk.Label(self._frame, compound="image", image=imageWidget)
        self._widgetAutotileEtendu.grid(column=0, row=0)
        self._boutonSauvegarde = ttk.Button(self._frame, text="Save as...", command=self._sauvegarde)
        self._boutonSauvegarde.grid(column=0, row=1)
        self._boutonRecommencer = ttk.Button(self._frame, text="Expand another autotile", command=self._retourDebut)
        self._boutonSauvegarde.grid(column=0, row=2)
        for child in self._frame.winfo_children(): child.grid_configure(padx=30, pady=30)
        self._frame.mainloop()

    def _retourDebut(self):
        self._frame.grid_forget()
        self._nomFichierAutotile, self._ancienNomFichierAutotile, self._imageCorrecteUneFois = "", "", False
        self._preparerFenetreDebut()

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

    def _autotileCorrect(self, messageChaineVide=True):
        if self._nomFichierAutotile != "":
            if ".png" in self._nomFichierAutotile or ".PNG" in self._nomFichierAutotile:
                image = Image.open(self._nomFichierAutotile)
                if image.size == (64, 96): 
                    return True
                else:
                    messagebox.showwarning(title="The autotile does not have the right size", message="The autotile must be 64 * 96 pixels wide.", detail="Refer to the tileA2 formatting from RPG Maker VX or VX Ace.")
            else:
                messagebox.showwarning(title="The autotile is not a PNG image", message="The autotile to expand is not a PNG image.", detail="You must choose a PNG file.")
        else:
            if messageChaineVide:
                messagebox.showwarning(title="No autotile to expand", message="No autotile to expand was found.", detail="You must load an autotile to expand.")
        return False

    def _initialiserEmplacements(self):
        self._minitiles, self._directionMinitile, self._typeMinitile = dict(NO=dict(), NE=dict(), SO=dict(), SE=dict()), dict(), dict()
        self._typeMinitileSelonGroupe, self._directionMinitilePos = dict(), dict()
        #Liste des types et directions possibles
        self._typeMinitile, self._directionMinitile = ["Normal", "Angle int", "Angle ext", "BordHori", "BordVerti", "Présentation"], ["NO", "NE", "SO", "SE"]
        #Direction selon la position au sein du groupe
        self._directionMinitilePos[0, 0], self._directionMinitilePos[16, 0], self._directionMinitilePos[0, 16], self._directionMinitilePos[16, 16] = "NO", "NE", "SO", "SE"
        #Type des minitiles selon leurs groupes et directions
        self._typeMinitileSelonGroupe[0, 0, "NO"] = "Présentation"
        self._typeMinitileSelonGroupe[0, 0, "NE"] = "Présentation"
        self._typeMinitileSelonGroupe[0, 0, "SO"] = "Présentation"
        self._typeMinitileSelonGroupe[0, 0, "SE"] = "Présentation"
        self._typeMinitileSelonGroupe[32, 0, "NO"] = "Angle int"
        self._typeMinitileSelonGroupe[32, 0, "NE"] = "Angle int"
        self._typeMinitileSelonGroupe[32, 0, "SO"] = "Angle int"
        self._typeMinitileSelonGroupe[32, 0, "SE"] = "Angle int"
        self._typeMinitileSelonGroupe[0, 32, "NO"] = "Angle ext"
        self._typeMinitileSelonGroupe[32, 32, "NE"] = "Angle ext"
        self._typeMinitileSelonGroupe[0, 64, "SO"] = "Angle ext"
        self._typeMinitileSelonGroupe[32, 64, "SE"] = "Angle ext"
        self._typeMinitileSelonGroupe[32, 32, "NO"] = "BordHori"
        self._typeMinitileSelonGroupe[0, 32, "NE"] = "BordHori"
        self._typeMinitileSelonGroupe[32, 64, "SO"] = "BordHori"
        self._typeMinitileSelonGroupe[0, 64, "SE"] = "BordHori"
        self._typeMinitileSelonGroupe[0, 64, "NO"] = "BordVerti"
        self._typeMinitileSelonGroupe[32, 64, "NE"] = "BordVerti"
        self._typeMinitileSelonGroupe[0, 32, "SO"] = "BordVerti"
        self._typeMinitileSelonGroupe[32, 32, "SE"] = "BordVerti"
        self._typeMinitileSelonGroupe[32, 64, "NO"] = "Normal"
        self._typeMinitileSelonGroupe[0, 64, "NE"] = "Normal"
        self._typeMinitileSelonGroupe[0, 32, "SE"] = "Normal"
        self._typeMinitileSelonGroupe[32, 32, "SO"] = "Normal"

    def _constituerAutotile(self, *types):
        surfaceAutotile = Image.new("RGB", (32,32))
        absMinitile, ordMinitile, i = 0, 0, 0
        while ordMinitile < 32:
            absMinitile = 0
            while absMinitile < 32:
                directionMinitile = self._directionMinitilePos[absMinitile, ordMinitile]
                typeMinitile = types[i]
                surfaceMinitile = self._minitiles[directionMinitile][typeMinitile]
                surfaceAutotile.paste(surfaceMinitile, (absMinitile, ordMinitile))
                i += 1
                absMinitile += 16
            ordMinitile += 16
        return surfaceAutotile

    def _traiterAutotileAvecVerif(self):
        if self._autotileCorrect():
            self._autotileEtendu = AutotileExpander.expandAutotile(self._nomFichierAutotile)
            self._preparerFenetreSauvegarde()

    def _traiterAutotile(self):
        self._imageAutotile = Image.open(self._nomFichierAutotile)
        self._initialiserEmplacements()
        #### On trouve les minitiles, puis on les classe par position et type
        absGroupe, ordGroupe = 0, 0
        while ordGroupe < self._imageAutotile.size[1]: #Parcours des groupes de minitiles
            absGroupe = 0
            while absGroupe < self._imageAutotile.size[0]:
                absMinitile, ordMinitile = 0, 0
                while ordMinitile < 32: #Parcours des minitiles
                    absMinitile = 0
                    while absMinitile < 32:
                        directionMinitile = self._directionMinitilePos[absMinitile, ordMinitile]
                        typeMinitile = self._typeMinitileSelonGroupe[absGroupe, ordGroupe, directionMinitile]
                        self._minitiles[directionMinitile][typeMinitile] = self._imageAutotile.crop((absGroupe+absMinitile, ordGroupe+ordMinitile, absGroupe+absMinitile+16, ordGroupe+ordMinitile+16))
                        absMinitile += 16
                    ordMinitile += 16
                absGroupe += 32
            ordGroupe += 32
        ##### On définit les types qui composent les 48 autotiles
        surfacesAutotiles = dict()
        surfacesAutotiles[0] = self._constituerAutotile("Normal", "Normal", "Normal", "Normal")
        surfacesAutotiles[1] = self._constituerAutotile("Angle int", "Normal", "Normal", "Normal")
        surfacesAutotiles[2] = self._constituerAutotile("Normal", "Angle int", "Normal", "Normal")
        surfacesAutotiles[3] = self._constituerAutotile("Angle int", "Angle int", "Normal", "Normal")
        surfacesAutotiles[4] = self._constituerAutotile("Normal", "Normal", "Normal", "Angle int")
        surfacesAutotiles[5] = self._constituerAutotile("Angle int", "Normal", "Normal", "Angle int")
        surfacesAutotiles[6] = self._constituerAutotile("Normal", "Angle int", "Normal", "Angle int")
        surfacesAutotiles[7] = self._constituerAutotile("Angle int", "Angle int", "Normal", "Angle int")
        surfacesAutotiles[8] = self._constituerAutotile("Normal", "Normal", "Angle int", "Normal")
        surfacesAutotiles[9] = self._constituerAutotile("Angle int", "Normal", "Angle int", "Normal")
        surfacesAutotiles[10] = self._constituerAutotile("Normal", "Angle int", "Angle int", "Normal")
        surfacesAutotiles[11] = self._constituerAutotile("Angle int", "Angle int", "Angle int", "Normal")
        surfacesAutotiles[12] = self._constituerAutotile("Normal", "Normal", "Angle int", "Angle int")
        surfacesAutotiles[13] = self._constituerAutotile("Angle int", "Normal", "Angle int", "Angle int")
        surfacesAutotiles[14] = self._constituerAutotile("Normal", "Angle int", "Angle int", "Angle int")
        surfacesAutotiles[15] = self._constituerAutotile("Angle int", "Angle int", "Angle int", "Angle int")
        surfacesAutotiles[16] = self._constituerAutotile("BordVerti", "Normal", "BordVerti", "Normal")
        surfacesAutotiles[17] = self._constituerAutotile("BordVerti", "Angle int", "BordVerti", "Normal")
        surfacesAutotiles[18] = self._constituerAutotile("BordVerti", "Normal", "BordVerti", "Angle int")
        surfacesAutotiles[19] = self._constituerAutotile("BordVerti", "Angle int", "BordVerti", "Angle int")
        surfacesAutotiles[20] = self._constituerAutotile("BordHori", "BordHori", "Normal", "Normal")
        surfacesAutotiles[21] = self._constituerAutotile("BordHori", "BordHori", "Normal", "Angle int")
        surfacesAutotiles[22] = self._constituerAutotile("BordHori", "BordHori", "Angle int", "Normal")
        surfacesAutotiles[23] = self._constituerAutotile("BordHori", "BordHori", "Angle int", "Angle int")
        surfacesAutotiles[24] = self._constituerAutotile("Normal", "BordVerti", "Normal", "BordVerti")
        surfacesAutotiles[25] = self._constituerAutotile("Normal", "BordVerti", "Angle int", "BordVerti")
        surfacesAutotiles[26] = self._constituerAutotile("Angle int", "BordVerti", "Normal", "BordVerti")
        surfacesAutotiles[27] = self._constituerAutotile("Angle int", "BordVerti", "Angle int", "BordVerti")
        surfacesAutotiles[28] = self._constituerAutotile("Normal", "Normal", "BordHori", "BordHori")
        surfacesAutotiles[29] = self._constituerAutotile("Angle int", "Normal", "BordHori", "BordHori")
        surfacesAutotiles[30] = self._constituerAutotile("Normal", "Angle int", "BordHori", "BordHori")
        surfacesAutotiles[31] = self._constituerAutotile("Angle int", "Angle int", "BordHori", "BordHori")
        surfacesAutotiles[32] = self._constituerAutotile("BordVerti", "BordVerti", "BordVerti", "BordVerti")
        surfacesAutotiles[33] = self._constituerAutotile("BordHori", "BordHori", "BordHori", "BordHori")
        surfacesAutotiles[34] = self._constituerAutotile("Angle ext", "BordHori", "BordVerti", "Normal")
        surfacesAutotiles[35] = self._constituerAutotile("Angle ext", "BordHori", "BordVerti", "Angle int")
        surfacesAutotiles[36] = self._constituerAutotile("BordHori", "Angle ext", "Normal", "BordVerti")
        surfacesAutotiles[37] = self._constituerAutotile("BordHori", "Angle ext", "Angle int", "BordVerti")
        surfacesAutotiles[38] = self._constituerAutotile("Normal", "BordVerti", "BordHori", "Angle ext")
        surfacesAutotiles[39] = self._constituerAutotile("Angle int", "BordVerti", "BordHori", "Angle ext")
        surfacesAutotiles[40] = self._constituerAutotile("BordVerti", "Normal", "Angle ext", "BordHori")
        surfacesAutotiles[41] = self._constituerAutotile("BordVerti", "Angle int", "Angle ext", "BordHori")
        surfacesAutotiles[42] = self._constituerAutotile("Présentation", "Présentation", "BordVerti", "BordVerti")
        surfacesAutotiles[43] = self._constituerAutotile("Présentation", "BordHori", "Présentation", "BordHori")
        surfacesAutotiles[44] = self._constituerAutotile("BordVerti", "BordVerti", "Présentation", "Présentation")
        surfacesAutotiles[45] = self._constituerAutotile("BordHori", "Présentation", "BordHori", "Présentation")
        surfacesAutotiles[46] = self._constituerAutotile("Présentation", "Présentation", "Présentation", "Présentation")
        surfacesAutotiles[47] = self._constituerAutotile("Présentation", "Présentation", "Présentation", "Présentation")
        ##### On crée la surface finale
        absAutotile, ordAutotile, i, self._autotileEtendu = 0, 0, 0, Image.new("RGB", (32*8, 32*6))
        while ordAutotile < 32 * 6:
            absAutotile = 0
            while absAutotile < 32 * 8:
                self._autotileEtendu.paste(surfacesAutotiles[i], (absAutotile, ordAutotile))
                i += 1
                absAutotile += 32
            ordAutotile += 32
        self._preparerFenetreSauvegarde()

    def executer(self):
        onArrete, blitSurfaceFinaleFait = False, False
        self._frame.mainloop()

if __name__ == "__main__":
    appli = Appli()
    appli.executer()
